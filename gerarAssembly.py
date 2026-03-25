# Aluno 3 - Henrique de O. Godoy
# Função gerarAssembly e Leitura de Arquivo

import sys

def lerArquivo(arquivo):

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        return [linha.strip() for linha in linhas if linha.strip()]
        
    except FileNotFoundError:
        print(f"ERROR: '{arquivo}' não foi encontrado.")
        return []
    
    except Exception as e:
        print(f"ERROR: Erro ao ler: {e}")
        return []


def gerarAssembly(tokens):

    codigo_assembly = ""
    op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'SDIV'}

    for token in tokens:
        if token.replace('.', '', 1).lstrip('-').isdigit():
            codigo_assembly += f"MOV R0, #{token}\n"
            codigo_assembly += f"PUSH {{R0}}\n"

        elif token in op_map:
            codigo_assembly += f"POP {{R1}}\n"
            codigo_assembly += f"POP {{R0}}\n"
            codigo_assembly += f"{op_map[token]} R2, R0, R1\n"
            codigo_assembly += f"PUSH {{R2}}\n"

        elif token == "MEM":
            codigo_assembly += f"LDR R0, =memoria\nPUSH {{R0}}\n"

        elif token == "RES":
            codigo_assembly += f"LDR R0, =resultado\nPUSH {{R0}}\n"

        else:
            print(f"ERROR: '{token}' invalido")

    return codigo_assembly


def parse_expressao(linha):

    #!
    return linha.replace('(', '').replace(')', '').split() 


def teste():

    arquivo_teste = "teste_expressao.txt" 

    print(f"Testando arquivo: {arquivo_teste}")
    linhas = lerArquivo(arquivo_teste)

    for linha in linhas:
        tokens = parse_expressao(linha)
        assembly = gerarAssembly(tokens)
        print(f"Assembly pra linha: '{linha}':")
        print(assembly)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("0")
        sys.exit(1)

    arquivo = sys.argv[1]
    linhas = lerArquivo(arquivo)

    teste()
