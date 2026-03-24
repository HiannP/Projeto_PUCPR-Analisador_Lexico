# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo

class gerarAssembly:
    def __init__(self):
        self.codigoAssembly = ""

    def read_arquivo(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            return [linha.strip() for linha in linhas if linha.strip()]
        
        except FileNotFoundError:
            print(f"ERRO: '{arquivo}' não encontrado")
            return []
        
        except Exception as e:
            print(f"ERRO desconhecido ao ler o arquivo: {e}")
            return []
    
    def gerarAssembly(self, tokens):

        for token in tokens:
            #SUporta numeros decimais e carrega o numero em R0
            if token.replace('.', '', 1).isdigit():
                self.codigoAssembly += f"LOAD R0, #{token}\n"

            elif token in ['+', '-', '*', '/']:
                #Tem que ter pelo menos 2 operandos
                self.codigoAssembly += f"{token.upper()} R1, R0\n"

            elif token == "MEM":
                self.codigoAssembly += "LOAD R1, MEM\n"  #Carrega da memoria

            elif token == "RES":
                self.codigoAssembly += "LOAD R1, RES\n"  #Carrega do RES

            else:
                print(f"ERRO: Token invalido {token}")
        return self.codigoAssembly

# Testando read_arquivo e gerarAssembly
if __name__ == "__main__":
    gerador = gerarAssembly()
    linhas = gerador.read_arquivo('teste_lexico.txt') 
    print("Linhas do arquivo:")
    for linha in linhas:
        tokens = linha.replace('(', '').replace(')', '').split()
        assembly = gerador.gerarAssembly(tokens)
        print(f"Assembly gerado da linha: '{linha}':\n{assembly}\n")
