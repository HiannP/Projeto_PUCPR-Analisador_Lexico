# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo

import sys

class Gerar_Assembly:

    def __init__(self):
        self.codigo = ""
        self.historico = []
        self.memoria = {}


    def lerArquivo(self, arquivo: str):
        linhas = []

        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        linhas.append(linha)

        except FileNotFoundError:
            print(f"ERROR: não abriu o: {arquivo}")
            return []

        return linhas


    def tokenizar(self, linha: str):
        linha = linha.replace("(", " ( ").replace(")", " ) ")
        return linha.split()



    def gerarAssembly(self, tokens: list):
        self.codigo += "\n -Nova Expressao- \n"

        stack = []

        for token in tokens:


            if self._is_number(token):
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += "    PUSH {R0}\n"
                stack.append("NUM")



            elif self._is_identifier(token):
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += "    PUSH {R0}\n"
                stack.append("VAR")



            elif token in ('+', '-', '*', '/', '//', '%', '^'):
                self.codigo += "    POP {R1}\n"
                self.codigo += "    POP {R0}\n"

                if token == '+':
                    self.codigo += "    ADD R0, R0, R1\n"
                elif token == '-':
                    self.codigo += "    SUB R0, R0, R1\n"
                elif token == '*':
                    self.codigo += "    MUL R0, R0, R1\n"
                elif token == '/':
                    self.codigo += "    SDIV R0, R0, R1\n"
                elif token == '//':
                    self.codigo += "    SDIV R0, R0, R1\n"
                elif token == '%':
                    self.codigo += "    SDIV R2, R0, R1\n"
                    self.codigo += "    MUL R2, R2, R1\n"
                    self.codigo += "    SUB R0, R0, R2\n"
                elif token == '^':
                    self.codigo += "    @ POW (simulado)\n"

                self.codigo += "    PUSH {R0}\n"



            elif token == "MEM":
                if len(stack) == 1:
                    self.codigo += "    @ LOAD\n"
                    self.codigo += "    LDR R0, =mem_var\n"
                    self.codigo += "    PUSH {R0}\n"
                else:
                    self.codigo += "    @ STORE\n"
                    self.codigo += "    POP {R0}\n"
                    self.codigo += "    STR R0, =mem_var\n"



            elif token == "RES":
                self.codigo += "    @ RES\n"
                self.codigo += "    LDR R0, =resultado\n"
                self.codigo += "    PUSH {R0}\n"



            elif token in ("(", ")"):
                continue

            else:
                print(f"Token desconhecido: {token}")

        self.codigo += "    POP {R0}\n"
        self.codigo += "    STR R0, =resultado\n"

        self.historico.append("resultado")

        return self.codigo


    def _is_number(self, token: str):
        try:
            float(token)
            return True
        except:
            return False

    def _is_identifier(self, token: str):
        return token.isalpha() and token.isupper()



def executarArquivo():
    gerador = Gerar_Assembly()
    linhas = gerador.lerArquivo("teste_lexico2.txt")

    if not linhas:
        return

    for linha in linhas:
        tokens = gerador.tokenizar(linha)
        gerador.gerarAssembly(tokens)

    print("-Assembly Final- ")
    print(gerador.codigo)

if __name__ == "__main__":
    executarArquivo()