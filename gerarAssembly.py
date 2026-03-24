# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo

class gerarAssembly:
    def __init__(self):
        pass

    
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
 
# Testando read_arquivo
if __name__ == "__main__":
    gerador = gerarAssembly()
    linhas = gerador.read_arquivo('teste_lexico.txt') 
    print("Linhas do arquivo:")
    for linha in linhas:
        print(linha)