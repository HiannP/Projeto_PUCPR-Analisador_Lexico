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
        tokens = self._tratar_parenteses(tokens)
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

                if not (isinstance(n, tuple) and n[0] == "CONST"):
                    raise ValueError("RES requer número constante")

                indice = int(n[1])

                if indice >= len(self.historico_resultados):
                    raise IndexError("RES fora do histórico")

                referencia = self.historico_resultados[-(indice + 1)]

                pilha.append(("RES", indice, referencia))

            # =========================
            # COMANDO MEM (STORE)
            # =========================
            elif token == "MEM":
                if len(pilha) < 2:
                    raise IndexError("Erro: MEM requer variável e valor")

                valor = pilha.pop()
                var = pilha.pop()

                if not (isinstance(var, tuple) and var[0] == "VAR"):
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
            elif self._is_identifier(token):
                pilha.append(("VAR", token))

            else:
                raise ValueError(f"Token inválido: {token}")

        if len(pilha) != 1:
            raise ValueError("Expressão inválida: sobrou mais de um elemento na pilha")

        resultado_ir = pilha[0]

        # Guarda IR no histórico
        self.historico_resultados.append(resultado_ir)

        return resultado_ir

    # =========================
    # TRATAMENTO DE PARÊNTESES
    # =========================
    def _tratar_parenteses(self, tokens):
        """
        Remove parênteses e valida estrutura.
        Como RPN já define ordem, os parênteses
        são usados apenas para validação estrutural.
        """

        pilha = []

        for token in tokens:
            if token == "(":
                pilha.append(token)

            elif token == ")":
                if not pilha:
                    raise ValueError("Parênteses desbalanceados")
                pilha.pop()

        if pilha:
            raise ValueError("Parênteses desbalanceados")

        # Remove parênteses
        return [t for t in tokens if t not in ("(", ")")]

    # =========================
    # UTILITÁRIOS
    # =========================
    def _is_number(self, token: str):
        try:
            float(token)
            return True
        except:
            return False

    def _is_identifier(self, token: str):
        return token.isalpha() and token.isupper()