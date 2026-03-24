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
        estrutura = self._parse_parenteses(tokens)

        resultado_ir = self._executar_subexpressao(estrutura)

        self.historico_resultados.append(resultado_ir)

        return resultado_ir

    def _executar_subexpressao(self, expr):
        """
        Implementa o tratamento de parênteses aninhados através de um executor recursivo.
        """
        pilha = []

        for token in expr:

            # Subexpressão
            if isinstance(token, list):
                pilha.append(self._executar_subexpressao(token))

            # =========================
            # OPERADORES
            # =========================
            elif token in ('+', '-', '*', '/', '//', '%', '^'):
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
            # RES
            # =========================
            elif token == "RES":
                n = pilha.pop()

                if not (isinstance(n, tuple) and n[0] == "CONST"):
                    raise ValueError("RES requer número constante")

                indice = int(n[1])

                if indice >= len(self.historico_resultados):
                    raise IndexError("RES fora do histórico")

                pilha.append(("RES", indice))

            # =========================
            # MEM (corrigido)
            # =========================
            elif token == "MEM":

                # LOAD → (X MEM)
                if len(pilha) == 1:
                    var = pilha.pop()

                    if var[0] != "VAR":
                        raise ValueError("MEM leitura requer identificador")

                    pilha.append(("LOAD", var[1]))

                # STORE → (V X MEM)
                elif len(pilha) == 2:
                    valor = pilha.pop()
                    var = pilha.pop()

                    if var[0] != "VAR":
                        raise ValueError("MEM escrita requer identificador")

                    nome = var[1]
                    ir = ("STORE", nome, valor)

                    self.memorias[nome] = valor
                    pilha.append(ir)

                else:
                    raise ValueError("Uso inválido de MEM")

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
            raise ValueError("Expressão inválida")

        return pilha[0]

    # =========================
    # TRATAMENTO DE PARÊNTESES
    # =========================
    def _parse_parenteses(self, tokens):
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
                    raise ValueError("Parênteses desbalanceados")
                current = stack.pop()

            else:
                current.append(token)

        if stack:
            raise ValueError("Parênteses desbalanceados")

        # retorna a raiz (pode estar dentro de lista)
        return current[0] if len(current) == 1 else current

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