# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo

class gerarAssembly:
    def __init__(self):
        self.codigoAssembly = ""

    
    def read_arquivo(self, arquivo):

        """
        Le as linhas do arquivo e retorna uma lista de linhas
        """

        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            return [linha.strip() for linha in linhas if linha.strip()]  #Ignora as linhas vazias
        
        except FileNotFoundError:
            print(f"ERRO: O arquivo '{arquivo}' não foi encontrado")
            return []
        
        except Exception as e:
            print(f"ERRO desconhecido ao ler o arquivo: {e}")
            return []
    
    def gerarAssembly(self, tokens):

        """
        Gera o assembly a partir de uma lista de tokens
        """

        for token in tokens:
            if token.isdigit(): 
                self.codigoAssembly += f"LOAD R0, #{token}\n"  #Carrega o numero em R0

            elif token in ['+', '-', '*', '/']:  # Se o token for operador
                self.codigoAssembly += f"{token.upper()} R1, R0\n"  #Ex simplificado

            else:
                print(f"ERRO: Token invalido {token}")
 
        return self.codigoAssembly
 
#Testando read_arquivo e gerarAssembly
if __name__ == "__main__":
    gerador = gerarAssembly()
    linhas = gerador.read_arquivo('teste_lexico.txt') 
    print("Linhas do arquivo:")
    for linha in linhas:
        tokens = linha.replace('(', '').replace(')', '').split()  #simplificado
        assembly = gerador.gerarAssembly(tokens)
        print(f"Assembly gerado para a linha: '{linha}':\n{assembly}\n")