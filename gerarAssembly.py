# Aluno 3 - Henrique de O. Godoy
# Funcao gerarAssembly e Leitura de Arquivo

import sys

'''
Classe principal para gerar o codigo assembly ARM a partir de arquivo texto
Usa a logica de maquina de pilha para gerenciar as operacoes
'''

class Gerar_Assembly:
    def __init__(self):
        self.codigo = ""
        self.historico = []
        self.memoria = {}

    #Le o arquivo txt, ignora linhas vazias e trata caso o arquivo nao exista
    def lerArquivo(self, arquivo: str) -> list:
        linhas = []
        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        linhas.append(linha)
        except FileNotFoundError:
            print(f"ERROR: nao foi possivel abrir o arquivo: {arquivo}")
            return []
        return linhas

    #Isola os parenteses com espacos e quebra a linha em uma lista de strings (tokens)
    def tokenizar(self, linha: str) -> list:
        linha = linha.replace("(", " ( ").replace(")", " ) ")
        return linha.split()

    '''
    Metodo core que converte os tokens em instrucoes assembly
    Empilha (PUSH) valores e desempilha (POP) para fazer as contas nos registradores
    '''

    def gerarAssembly(self, tokens: list) -> str:
        self.codigo += "\n - Expressao - \n"
        stack = []

        for token in tokens:
            #Se for numero ou variavel, carrega no R0 e joga na pilha
            if self._is_number(token):
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += "    PUSH {R0}\n"
                stack.append("NUM")

            elif self._is_identifier(token):
                self.codigo += f"    LDR R0, ={token}\n"
                self.codigo += "    PUSH {R0}\n"
                stack.append("VAR")

            #Operadores precisam de dois valores previamente empilhados (operandos)
            elif token in ('+', '-', '*', '/', '//', '%', '^'):
                if len(stack) < 2:
                    raise IndexError(f"Operandos insuficientes para '{token}'")
                
                #Tira da pilha para R1 (segundo operando) e R0 (primeiro operando)
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

                #Salva o resultado da operacao de volta na pilha
                self.codigo += "    PUSH {R0}\n"

            #Trata as operacoes de memoria avaliando o estado atual da pilha de operandos
            elif token == "MEM":
                if len(stack) == 1: 
                    self.codigo += "    @ LOAD\n"
                    self.codigo += "    LDR R0, =mem_var\n"
                    self.codigo += "    PUSH {R0}\n"
                elif len(stack) == 2: 
                    self.codigo += "    @ STORE\n"
                    self.codigo += "    POP {R0}\n"
                    self.codigo += "    STR R0, =mem_var\n"
                else:
                    print("MEM invalido")

            elif token == "RES":
                self.codigo += "    @ RES\n"
                self.codigo += "    LDR R0, =resultado\n"
                self.codigo += "    PUSH {R0}\n"

            elif token in ("(", ")"):
                continue  

            else:
                print(f"Token desconhecido: {token}")

        #Desempilha o valor final que sobrou e salva na variavel resultado principal
        self.codigo += "    POP {R0}\n"
        self.codigo += "    STR R0, =resultado\n"
        self.historico.append("resultado")
        return self.codigo

    #Helpers para checar a tipagem do token que estamos iterando
    def _is_number(self, token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _is_identifier(self, token: str) -> bool:
        #Considera variaveis validas apenas strings de letras maiusculas
        return token.isalpha() and token.isupper()

#Fluxo principal: cria instancia, le o txt de teste e gera o asm linha por linha
def executar_arquivo():
    gerador = Gerar_Assembly()
    linhas = gerador.lerArquivo("teste_lexico2.txt")

    if not linhas:
        return

    for linha in linhas:
        tokens = gerador.tokenizar(linha)
        gerador.gerarAssembly(tokens)

    print("- Assembly Final - ")
    print(gerador.codigo)

if __name__ == "__main__":
    executar_arquivo()