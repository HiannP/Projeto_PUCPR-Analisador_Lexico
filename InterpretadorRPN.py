# Aluno 2 - Marcos P. Ruppel
# Função executarExpressao e Gerenciamento de Memória (VERSÃO CORRIGIDA)

class InterpretadorRPN:
    def __init__(self):
        self.memorias = {}
        self.historico_resultados = []

    def executarExpressao(self, tokens: list):
        estrutura = self._parse_parenteses(tokens)

        resultado_ir = self._executar_subexpressao(estrutura)

        self.historico_resultados.append(resultado_ir)

        return resultado_ir

    def _executar_subexpressao(self, expr):
        pilha = []

        for token in expr:

            # =========================
            # SUBEXPRESSÃO
            # =========================
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

                pilha.append(("OP", token, a, b))

            # =========================
            # RES
            # =========================
            elif token == "RES":
                if len(pilha) < 1:
                    raise ValueError("RES requer um operando")

                n = pilha.pop()

                if not isinstance(n, tuple) or n[0] != "CONST_INT":
                    raise ValueError("RES requer número inteiro constante")

                indice = int(n[1])

                if indice < 0 or indice >= len(self.historico_resultados):
                    raise IndexError("RES fora do histórico")

                # CORREÇÃO: pegar N linhas anteriores corretamente
                valor_ir = self.historico_resultados[-(indice + 1)]

                pilha.append(valor_ir)

            # =========================
            # MEM
            # =========================
            elif token == "MEM":

                # LOAD → (VAR MEM)
                if len(pilha) == 1:
                    var = pilha.pop()

                    if not isinstance(var, tuple) or var[0] != "VAR":
                        raise ValueError("MEM leitura requer identificador válido")

                    nome = var[1]

                    if nome in self.memorias:
                        pilha.append(self.memorias[nome])
                    else:
                        pilha.append(("LOAD", nome))

                # STORE → (VAL VAR MEM)
                elif len(pilha) == 2:
                    valor = pilha.pop()
                    var = pilha.pop()

                    if not isinstance(var, tuple) or var[0] != "VAR":
                        raise ValueError("MEM escrita requer identificador válido")

                    nome = var[1]

                    ir = ("STORE", nome, valor)

                    # guarda simbolicamente
                    self.memorias[nome] = ("LOAD", nome)

                    pilha.append(ir)

                else:
                    raise ValueError("Uso inválido de MEM")

            # =========================
            # NÚMEROS
            # =========================
            elif self._is_number(token):
                if '.' in token:
                    pilha.append(("CONST_FLOAT", float(token)))
                else:
                    pilha.append(("CONST_INT", int(token)))

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
    # PARÊNTESES (mantido como está)
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

        return current

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
        # CORREÇÃO: evitar conflito com keywords
        if token in ("RES", "MEM"):
            return False
        return token.isalnum() and token[0].isalpha()