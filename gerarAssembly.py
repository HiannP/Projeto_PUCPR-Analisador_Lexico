# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo — VERSÃO FINAL CORRIGIDA

class GerarAssembly:
    def __init__(self):
        self.codigo = ""
        self.historico = []
        self.memoria = {}
        self.data_section = []
        self.float_constants = {}
        self.stack = []
        self.var_types = {}
        self.label_counter = 0
        self.data_labels_set = set()

    # =========================
    # LEITURA DE ARQUIVO
    # =========================
    def lerArquivo(self, nome_arquivo):
        linhas = []

        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()

                    # Ignora linhas vazias
                    if not linha:
                        continue

                    linhas.append(linha)

        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo: {e}")

        return linhas

    # =========================
    # GERAÇÃO PRINCIPAL
    # =========================
    def gerarAssembly(self, ir):
        self.codigo += "\n    @ Expressao\n"
        self.stack = []

        self._executar(ir)

        if len(self.stack) != 1:
            raise ValueError("Expressão inválida no Assembly")

        label = f"resultado_{len(self.historico)}"
        topo = self.stack.pop()

        if topo[0] == "FLOAT":
            self.codigo += "    VPOP {D0}\n"
            tipo = "float"
        else:
            self.codigo += "    POP {R0}\n"
            tipo = "int"

        # Salvar resultado
        self.codigo += f"    LDR R1, ={label}\n"

        if tipo == "float":
            self.codigo += "    VSTR D0, [R1]\n"
        else:
            self.codigo += "    STR R0, [R1]\n"

        # Display (CPULATOR)
        self.codigo += "    LDR R2, =0xFF200020\n"
        if tipo == "float":
            self.codigo += "    VMOV R0, S0\n"
        self.codigo += "    STR R0, [R2]\n"

        self.historico.append((label, tipo))

        if label not in self.data_labels_set:
            self.data_section.append((label, tipo))
            self.data_labels_set.add(label)

        return self.codigo

    # =========================
    # EXECUTOR
    # =========================
    def _executar(self, node):

        # 🔥 SUPORTE A LISTA (compatível com Aluno 2)
        if isinstance(node, list):
            for sub in node:
                self._executar(sub)
            return

        if not isinstance(node, tuple):
            raise ValueError("Formato inválido de IR")

        tipo = node[0]

        # =========================
        # CONSTANTES
        # =========================
        if tipo == "CONST_INT":
            self.codigo += f"    LDR R0, ={node[1]}\n"
            self.codigo += "    PUSH {R0}\n"
            self.stack.append(("INT", None))

        elif tipo == "CONST_FLOAT":
            label = self._get_float_label(node[1])
            self.codigo += f"    LDR R0, ={label}\n"
            self.codigo += "    VLDR D0, [R0]\n"
            self.codigo += "    VPUSH {D0}\n"
            self.stack.append(("FLOAT", None))

        # =========================
        # VAR → vira LOAD automaticamente
        # =========================
        elif tipo == "VAR":
            self._executar(("LOAD", node[1]))

        elif tipo == "LOAD":
            nome = node[1]
            tipo_var = self.var_types.get(nome, "int")

            self.codigo += f"    LDR R0, ={nome}\n"

            if tipo_var == "float":
                self.codigo += "    VLDR D0, [R0]\n"
                self.codigo += "    VPUSH {D0}\n"
                self.stack.append(("FLOAT", None))
            else:
                self.codigo += "    LDR R0, [R0]\n"
                self.codigo += "    PUSH {R0}\n"
                self.stack.append(("INT", None))

        # =========================
        # STORE
        # =========================
        elif tipo == "STORE":
            nome = node[1]
            valor = node[2]

            self._executar(valor)
            topo = self.stack.pop()

            if topo[0] == "FLOAT":
                self.var_types[nome] = "float"

                if nome not in self.data_labels_set:
                    self.data_section.append((nome, "float"))
                    self.data_labels_set.add(nome)

                self.codigo += "    VPOP {D0}\n"
                self.codigo += f"    LDR R1, ={nome}\n"
                self.codigo += "    VSTR D0, [R1]\n"
                self.codigo += "    VPUSH {D0}\n"
                self.stack.append(("FLOAT", None))

            else:
                self.var_types[nome] = "int"

                if nome not in self.data_labels_set:
                    self.data_section.append((nome, "int"))
                    self.data_labels_set.add(nome)

                self.codigo += "    POP {R0}\n"
                self.codigo += f"    LDR R1, ={nome}\n"
                self.codigo += "    STR R0, [R1]\n"
                self.codigo += "    PUSH {R0}\n"
                self.stack.append(("INT", None))

        # =========================
        # OPERAÇÕES
        # =========================
        elif tipo == "OP":
            op, a, b = node[1], node[2], node[3]

            self._executar(a)
            self._executar(b)

            b_tipo = self.stack.pop()
            a_tipo = self.stack.pop()

            # FLOAT
            if "FLOAT" in (a_tipo[0], b_tipo[0]):
                self._to_float(a_tipo, b_tipo)

                if op == '+':
                    self.codigo += "    VADD.F64 D0, D1, D0\n"
                elif op == '-':
                    self.codigo += "    VSUB.F64 D0, D1, D0\n"
                elif op == '*':
                    self.codigo += "    VMUL.F64 D0, D1, D0\n"
                elif op == '/':
                    self.codigo += "    VDIV.F64 D0, D1, D0\n"
                elif op == '^':
                    self._pow_float()

                self.codigo += "    VPUSH {D0}\n"
                self.stack.append(("FLOAT", None))

            # INT
            else:
                self.codigo += "    POP {R1}\n"
                self.codigo += "    POP {R0}\n"

                if op == '+':
                    self.codigo += "    ADD R0, R0, R1\n"
                elif op == '-':
                    self.codigo += "    SUB R0, R0, R1\n"
                elif op == '*':
                    self.codigo += "    MUL R0, R0, R1\n"
                elif op == '//':
                    self.codigo += "    SDIV R0, R0, R1\n"
                elif op == '%':
                    self.codigo += "    SDIV R2, R0, R1\n"
                    self.codigo += "    MUL R2, R2, R1\n"
                    self.codigo += "    SUB R0, R0, R2\n"
                elif op == '^':
                    self._pow_int()

                self.codigo += "    PUSH {R0}\n"
                self.stack.append(("INT", None))

    # =========================
    # HELPERS
    # =========================
    def _to_float(self, a_tipo, b_tipo):
        # b (topo da stack)
        if b_tipo[0] == "FLOAT":
            self.codigo += "    VPOP {D0}\n"
        else:
            self.codigo += "    POP {R0}\n"
            self.codigo += "    VMOV S0, R0\n"
            self.codigo += "    VCVT.F64.S32 D0, S0\n"

        # a (segundo da stack)
        if a_tipo[0] == "FLOAT":
            self.codigo += "    VPOP {D1}\n"
        else:
            self.codigo += "    POP {R0}\n"
            self.codigo += "    VMOV S1, R0\n"
            self.codigo += "    VCVT.F64.S32 D1, S1\n"

    def _pow_int(self):
        self.label_counter += 1
        lid = self.label_counter

        self.codigo += "    MOV R2, #1\n"
        self.codigo += f"loop_pow_{lid}:\n"
        self.codigo += "    CMP R1, #0\n"
        self.codigo += f"    BEQ end_pow_{lid}\n"
        self.codigo += "    MUL R2, R2, R0\n"
        self.codigo += "    SUB R1, R1, #1\n"
        self.codigo += f"    B loop_pow_{lid}\n"
        self.codigo += f"end_pow_{lid}:\n"
        self.codigo += "    MOV R0, R2\n"

    def _pow_float(self):
        self.label_counter += 1
        lid = self.label_counter

        self.codigo += "    VCVT.S32.F64 S0, D0\n"
        self.codigo += "    VMOV R1, S0\n"

        self.codigo += "    VMOV.F64 D2, #1.0\n"

        self.codigo += f"pow_loop_{lid}:\n"
        self.codigo += "    CMP R1, #0\n"
        self.codigo += f"    BEQ end_pow_{lid}\n"
        self.codigo += "    VMUL.F64 D2, D2, D1\n"
        self.codigo += "    SUB R1, R1, #1\n"
        self.codigo += f"    B pow_loop_{lid}\n"

        self.codigo += f"end_pow_{lid}:\n"
        self.codigo += "    VMOV.F64 D0, D2\n"

    def _get_float_label(self, val):
        key = str(val)
        if key not in self.float_constants:
            label = f"f_{key.replace('.', '_').replace('-', 'neg')}"
            self.float_constants[key] = label
        return self.float_constants[key]

    def gerar_data_section(self):
        ds = ".data\n"

        for val, label in self.float_constants.items():
            ds += f"    {label}: .double {val}\n"

        for nome, tipo in self.data_section:
            if tipo == "float":
                ds += f"    {nome}: .double 0.0\n"
            else:
                ds += f"    {nome}: .word 0\n"

        return ds

    def gerar_codigo_final(self):
        return self.gerar_data_section() + "\n.text\n.global _start\n_start:\n" + self.codigo