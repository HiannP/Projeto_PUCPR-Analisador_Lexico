# Aluno 2 - Marcos P. Ruppel
# Função executarExpressao e Gerenciamento de Memória

class InterpretadorRPN:
    def __init__(self):
        # Gerenciamento de variáveis (V MEM) e (MEM)
        self.memorias = {}
        # Histórico de resultados para o comando (N RES)
        self.historico_resultados = []

    def executarExpressao(self, tokens: list):
        """
        Gera a Representação Intermediária (IR) da expressão para o Assembly.
        Delega a lógica de parênteses para manter o controle de sub-expressões aninhadas.
        """
        pilha = []

        for token in tokens:

            # =========================
            # OPERADORES
            # =========================
            if token in ('+', '-', '*', '/', '//', '%', '^'):
                if len(pilha) < 2:
                    raise IndexError(f"Operandos insuficientes para '{token}'")

                b = pilha.pop()
                a = pilha.pop()

                op_map = {
                    '+': "ADD",
                    '-': "SUB",
                    '*': "MUL",
                    '/': "DIV",
                    '//': "DIV_INT",
                    '%': "MOD",
                    '^': "POW"
                }

                pilha.append((op_map[token], a, b))

            # =========================
            # COMANDO RES
            # =========================
            elif token == "RES":
                if len(pilha) < 1:
                    raise IndexError("Erro: Pilha vazia para RES")

                n = pilha.pop()

                if not isinstance(n, (int, float)):
                    raise ValueError("RES requer índice numérico")

                pilha.append(("RES", int(n)))

            # =========================
            # COMANDO MEM
            # =========================
            elif token == "MEM":
                if len(pilha) < 2:
                    raise IndexError("Erro: MEM requer variável e valor")

                valor = pilha.pop()
                var = pilha.pop()

                if not isinstance(var, tuple) or var[0] != "VAR":
                    raise ValueError("MEM requer identificador válido")

                nome = var[1]

                ir = ("STORE", nome, valor)
                self.memorias[nome] = ir

                pilha.append(ir)

            # =========================
            # NÚMEROS
            # =========================
            elif self._is_number(token):
                pilha.append(("CONST", float(token)))

            # =========================
            # IDENTIFICADORES
            # =========================
            else:
                pilha.append(("LOAD", token))

        if len(pilha) != 1:
            raise ValueError("Expressão inválida: sobrou mais de um elemento na pilha")

        resultado_ir = pilha[0]

        # Guarda IR no histórico
        self.historico_resultados.append(resultado_ir)

        return resultado_ir

    def _is_number(self, token: str):
        try:
            float(token)
            return True
        except:
            return False