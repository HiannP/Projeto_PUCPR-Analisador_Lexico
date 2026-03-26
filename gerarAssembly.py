# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo — VERSÃO FINAL CORRIGIDA

class Gerar_Assembly:
    def __init__(self):
        self.codigo = ""
        self.historico = []
        self.memoria = {}
        self.data_section = set()
        self.float_constants = {}
        self.float_counter = 0
        self.stack = []

    # ─────────────────────────────────────────────
    # Leitura do arquivo
    # ─────────────────────────────────────────────
    def lerArquivo(self, arquivo: str) -> list:
        linhas = []
        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        linhas.append(linha)
        except FileNotFoundError:
            print(f"ERROR: Nao foi possivel abrir: {arquivo}")
            return []
        return linhas

    # ─────────────────────────────────────────────
    # Tokenização e parse de parenteses
    # ─────────────────────────────────────────────
    def tokenizar(self, linha: str) -> list:
        linha = linha.replace("(", " ( ").replace(")", " ) ")
        return linha.split()

    def parse_parenteses(self, tokens):
        stack = []
        current = []

        for token in tokens:
            if token == "(":
                stack.append(current)
                new_list = []
                current.append(new_list)
                current = new_list

            elif token == ")":
                if not stack:
                    raise ValueError("Parenteses desbalanceados")
                current = stack.pop()

            else:
                current.append(token)

        if stack:
            raise ValueError("Parenteses desbalanceados")
        return current[0] if len(current) == 1 else current

    # ─────────────────────────────────────────────
    # Helpers de tipagem
    # ─────────────────────────────────────────────
    def _is_number(self, token: str) -> bool:

        try:
            float(token)
            return True
        except ValueError:
            return False

    def _is_float(self, token: str) -> bool:
        return self._is_number(token) and '.' in token

    def _is_integer(self, token: str) -> bool:
        return self._is_number(token) and '.' not in token

    def _is_identifier(self, token: str) -> bool:
        return token.isalpha() and token.isupper()

    def _operandos_sao_float(self, a, b) -> bool:
        float_types = {"CONST_FLOAT", "RESULT_FLOAT", "VAR_FLOAT"}
        return a[0] in float_types or b[0] in float_types

    # ─────────────────────────────────────────────
    # Gera label unica para constante float na .data
    # ─────────────────────────────────────────────
    def _get_float_label(self, token: str) -> str:

        if token not in self.float_constants:
            label = f"__fc_{token.replace('.', '_').replace('-', 'neg')}"
            self.float_constants[token] = label

        return self.float_constants[token]

    # ─────────────────────────────────────────────
    # Geraçao do Assembly principal
    # ─────────────────────────────────────────────
    def gerarAssembly(self, tokens: list) -> str:

        estrutura = self.parse_parenteses(tokens)
        self.codigo += "\n Expressao \n"
        self.stack = []

        self._executar(estrutura)

        if len(self.stack) != 1:
            raise ValueError(
                f"Expressao RPN inválida. Pilha com {len(self.stack)} elemento(s): {self.stack}"
            )

        label_atual = f"resultado_{len(self.historico)}"
        topo = self.stack[-1]
        is_float_result = topo[0] in ("CONST_FLOAT", "RESULT_FLOAT", "VAR_FLOAT")

        if is_float_result:
            #LDR R1 + VSTR em vez de VLDR direto
            self.codigo += f"    VPOP {{S0}}\n"
            self.codigo += f"    LDR R1, ={label_atual}\n"
            self.codigo += f"    VSTR S0, [R1]\n"

        else:
            self.codigo += f"    POP {{R0}}\n"
            self.codigo += f"    LDR R1, ={label_atual}\n"
            self.codigo += f"    STR R0, [R1]\n"

        self.historico.append((label_atual, "float" if is_float_result else "int"))
        self.data_section.add((label_atual, "float" if is_float_result else "int"))

        return self.codigo

    # ─────────────────────────────────────────────
    # Execução recursiva dos tokens
    # ─────────────────────────────────────────────
    def _executar(self, expr):
        for token in expr:

            if isinstance(token, list):
                self._executar(token)

            #Constante FLOAT
            elif self._is_float(token):
                #VLDR não suporta "=label" (literal pool)
                #LDR R0 com o endereço, depois VLDR S0, [R0]
                label = self._get_float_label(token)
                self.codigo += f"    LDR R0, ={label}\n"
                self.codigo += f"    VLDR S0, [R0]\n"
                self.codigo += f"    VPUSH {{S0}}\n"
                self.stack.append(("CONST_FLOAT", token))

            #Constante INT
            elif self._is_integer(token):
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += f"    PUSH {{R0}}\n"
                self.stack.append(("CONST_INT", token))

            #Variaveis
            elif self._is_identifier(token) and token not in ("MEM", "RES"):
                self.data_section.add((token, "int"))
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += f"    LDR R0, [R0]\n"
                self.codigo += f"    PUSH {{R0}}\n"
                self.stack.append(("VAR", token))

            #Operadores
            elif token in ('+', '-', '*', '/', '//', '%', '^'):
                if len(self.stack) < 2:
                    raise IndexError(
                        f"Operandos insuficientes para '{token}'. Pilha: {self.stack}"
                    )

                b = self.stack.pop()
                a = self.stack.pop()
                use_float = self._operandos_sao_float(a, b)

                if use_float:
                    self._converter_float_se_necessario(a, b)

                    if token == '+':
                        self.codigo += f"    VADD.F32 S0, S1, S0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '-':
                        self.codigo += f"    VSUB.F32 S0, S1, S0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '*':
                        self.codigo += f"    VMUL.F32 S0, S1, S0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '/':
                        self.codigo += f"    VDIV.F32 S0, S1, S0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '//':
                        self.codigo += f"    VDIV.F32 S0, S1, S0\n"
                        self.codigo += f"    VCVT.S32.F32 S0, S0\n"
                        self.codigo += f"    VCVT.F32.S32 S0, S0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '%':
                        self.codigo += f"    @ MOD float: S1 mod S0\n"
                        self.codigo += f"    VDIV.F32 S2, S1, S0\n"
                        self.codigo += f"    VCVT.S32.F32 S2, S2\n"
                        self.codigo += f"    VCVT.F32.S32 S2, S2\n"
                        self.codigo += f"    VMUL.F32 S2, S2, S0\n"
                        self.codigo += f"    VSUB.F32 S0, S1, S2\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                    elif token == '^':

                        #Powf devolve o resultado no R0
                        #tem q usar VCVT pra converter o tipo, VMOV so copia bit cru
                        #S1(base) e S0(exp) ja vem carregados da func de conversao
                        self.codigo += f"    @ POW float: powf(S1, S0)\n"
                        self.codigo += f"    VMOV R0, S1\n"
                        self.codigo += f"    VMOV R1, S0\n"
                        self.codigo += f"    BL powf\n"
                        self.codigo += f"    VMOV S0, R0\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))

                else:
                    #Oeracoes INTEGER
                    self.codigo += f"    POP {{R1}}\n"
                    self.codigo += f"    POP {{R0}}\n"

                    if token == '+':
                        self.codigo += f"    ADD R0, R0, R1\n"

                    elif token == '-':
                        self.codigo += f"    SUB R0, R0, R1\n"

                    elif token == '*':
                        self.codigo += f"    MUL R0, R0, R1\n"

                    elif token in ('/', '//'):
                        self.codigo += f"    SDIV R0, R0, R1\n"

                    elif token == '%':
                        self.codigo += f"    SDIV R2, R0, R1\n"
                        self.codigo += f"    MUL R2, R2, R1\n"
                        self.codigo += f"    SUB R0, R0, R2\n"

                    elif token == '^':
                        idx = len(self.historico)
                        lbl_loop  = f"__pow_loop_{idx}"
                        lbl_done  = f"__pow_done_{idx}"

                        self.codigo += f"    @ POW int: R0 = R0 ^ R1 (loop inline)\n"
                        self.codigo += f"    MOV R2, #1\n"
                        self.codigo += f"    MOV R3, R1\n"
                        self.codigo += f"    CMP R3, #0\n"
                        self.codigo += f"    BEQ {lbl_done}\n"
                        self.codigo += f"{lbl_loop}:\n"
                        self.codigo += f"    MUL R2, R2, R0\n"
                        self.codigo += f"    SUBS R3, R3, #1\n"
                        self.codigo += f"    BNE {lbl_loop}\n"
                        self.codigo += f"{lbl_done}:\n"
                        self.codigo += f"    MOV R0, R2\n"

                    self.codigo += f"    PUSH {{R0}}\n"
                    self.stack.append(("RESULT_INT", "R0"))

            #MEM
            elif token == "MEM":
                if len(self.stack) >= 2:
                    valor = self.stack.pop()
                    var   = self.stack.pop()

                    if var[0] not in ("VAR",):
                        raise ValueError("MEM escrita requer primeiro operando como identificador")

                    nome = var[1]
                    self.data_section.add((nome, "int"))
                    is_float_val = valor[0] in ("CONST_FLOAT", "RESULT_FLOAT")

                    self.codigo += f"    @ STORE {nome}\n"
                    if is_float_val:
                        self.codigo += f"    VPOP {{S0}}\n"
                        self.codigo += f"    LDR R1, ={nome}\n"
                        self.codigo += f"    VSTR S0, [R1]\n"
                        self.codigo += f"    VPUSH {{S0}}\n"
                        self.stack.append(("RESULT_FLOAT", "S0"))
                    else:
                        self.codigo += f"    POP {{R0}}\n"
                        self.codigo += f"    LDR R1, ={nome}\n"
                        self.codigo += f"    STR R0, [R1]\n"
                        self.codigo += f"    PUSH {{R0}}\n"
                        self.stack.append(("RESULT_INT", "R0"))

                    self.memoria[nome] = valor

                elif len(self.stack) == 1:
                    var = self.stack.pop()
                    if var[0] != "VAR":
                        raise ValueError("MEM leitura requer identificador")
                    nome = var[1]
                    self.codigo += f"    @ LOAD {nome}\n"
                    self.codigo += f"    LDR R0, ={nome}\n"
                    self.codigo += f"    LDR R0, [R0]\n"
                    self.codigo += f"    PUSH {{R0}}\n"
                    self.stack.append(("RESULT_INT", "R0"))

                else:
                    raise ValueError("MEM requer pelo menos 1 operando na pilha")

            #RES
            elif token == "RES":
                if len(self.stack) < 1:
                    raise ValueError("RES requer índice na pilha")

                indice_token = self.stack.pop()
                if indice_token[0] != "CONST_INT":
                    raise ValueError(f"RES requer número constante inteiro, recebeu: {indice_token}")

                indice = int(float(indice_token[1]))
                if indice >= len(self.historico):
                    raise IndexError(
                        f"RES fora do histórico: índice {indice}, histórico tem {len(self.historico)}"
                    )

                label, tipo = self.historico[indice]
                self.codigo += f"    @ RES {indice} ({tipo})\n"
                self.codigo += f"    LDR R0, ={label}\n"

                if tipo == "float":
                    self.codigo += f"    VLDR S0, [R0]\n"
                    self.codigo += f"    VPUSH {{S0}}\n"
                    self.stack.append(("RESULT_FLOAT", label))
                else:
                    self.codigo += f"    LDR R0, [R0]\n"
                    self.codigo += f"    PUSH {{R0}}\n"
                    self.stack.append(("RESULT_INT", label))

            else:
                raise ValueError(f"Token desconhecido: '{token}'")

    # ─────────────────────────────────────────────
    # Helper: converte operandos para float (S1=a, S0=b)
    # ─────────────────────────────────────────────
    def _converter_float_se_necessario(self, a, b):
        float_types = {"CONST_FLOAT", "RESULT_FLOAT", "VAR_FLOAT"}

        if b[0] in float_types:
            self.codigo += f"    VPOP {{S0}}\n"
        else:
            self.codigo += f"    POP {{R0}}\n"
            self.codigo += f"    VMOV S0, R0\n"
            self.codigo += f"    VCVT.F32.S32 S0, S0\n"

        if a[0] in float_types:
            self.codigo += f"    VPOP {{S1}}\n"
        else:
            self.codigo += f"    POP {{R0}}\n"
            self.codigo += f"    VMOV S1, R0\n"
            self.codigo += f"    VCVT.F32.S32 S1, S1\n"

    # ─────────────────────────────────────────────
    # Gera a seção .data
    # ─────────────────────────────────────────────
    def gerar_data_section(self) -> str:
        ds = ".data\n"

        for token, label in self.float_constants.items():
            ds += f"    {label}: .float {token}\n"

        for item in self.data_section:
            nome, tipo = item if isinstance(item, tuple) else (item, "int")
            if tipo == "float":
                ds += f"    {nome}: .float 0.0\n"
            else:
                ds += f"    {nome}: .word 0\n"

        return ds


# ─────────────────────────────────────────────────────────────────────────────
# Fluxo principal
# ─────────────────────────────────────────────────────────────────────────────
def executar_arquivo():
    
    gerador = Gerar_Assembly()
    linhas  = gerador.lerArquivo("teste_lexico2.txt")

    if not linhas:
        return

    for i, linha in enumerate(linhas):
        try:
            tokens = gerador.tokenizar(linha)
            gerador.gerarAssembly(tokens)
        except (ValueError, IndexError) as e:
            print(f"[ERRO] Linha {i+1}: {linha}")
            print(f"       → {e}")

    print(gerador.gerar_data_section())
    print(".text")
    print(gerador.codigo)


if __name__ == "__main__":
    executar_arquivo()
