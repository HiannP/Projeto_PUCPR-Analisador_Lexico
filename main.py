import os
import sys

# Importa a função que faz a análise léxica e monta os tokens da expressão
from parseExpressao import parseExpressao

# Importa a classe que interpreta os tokens em RPN e gera a estrutura intermediária da expressão
from InterpretadorRPN import InterpretadorRPN

# Importa a classe responsável por ler o arquivo e gerar o código Assembly
from gerarAssembly import Gerar_Assembly

# Importa a função que exibe os resultados finais no terminal
from exibirResultados import exibirResultados


def processar_arquivo(nome_arquivo):
    """
    Faz o fluxo principal do programa:
    1. Lê as linhas do arquivo de entrada
    2. Faz a análise léxica de cada linha
    3. Interpreta os tokens
    4. Gera o Assembly correspondente
    5. Exibe os resultados ao final
    """

    # Instancia o gerador de Assembly
    gerador = Gerar_Assembly()

    # Instancia o interpretador RPN
    interpretador = InterpretadorRPN()

    # Lê o conteúdo do arquivo de entrada
    # Cada linha representa uma expressão a ser processada
    linhas = gerador.lerArquivo(nome_arquivo)

    # Se não houver linhas válidas, encerra a execução
    if not linhas:
        print("Nenhuma linha válida encontrada no arquivo.")
        return 1

    # Lista para armazenar os resultados processados de cada linha
    resultados = []

    # Percorre cada linha do arquivo, junto com seu número
    for numero_linha, linha in enumerate(linhas, start=1):
        # Lista que receberá os tokens gerados pela análise léxica
        tokens = []

        try:
            # Faz a análise léxica da expressão da linha
            # O resultado é salvo dentro da lista tokens
            parseExpressao(linha, tokens)

            # Interpreta os tokens e gera a estrutura intermediária da expressão
            resultado_ir = interpretador.executarExpressao(tokens)

            # Salva esse resultado para exibição posterior
            resultados.append(resultado_ir)

            # Gera o trecho Assembly correspondente aos tokens dessa linha
            gerador.gerarAssembly(tokens)

            # Exibe no terminal que a linha foi processada com sucesso
            print(f"[OK] Linha {numero_linha}: {linha}")

        except Exception as e:
            # Se houver erro em qualquer etapa da linha, mostra o erro
            print(f"[ERRO] Linha {numero_linha}: {linha}")
            print(f"Motivo: {e}")

            # Também salva o erro na lista de resultados
            resultados.append(f"ERRO: {e}")

    # Ao final do processamento de todas as linhas, exibe os resultados no terminal
    exibirResultados(resultados)

    # Retorna 0 indicando execução bem-sucedida
    return 0


def main():
    """
    Função principal do programa.
    Valida o uso correto via terminal e chama o processamento do arquivo.
    """

    # Verifica se o usuário passou exatamente 1 argumento além do nome do script
    # Exemplo esperado:
    # python main.py teste_lexico.txt
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_teste.txt>")
        sys.exit(1)

    # Pega o nome do arquivo informado no terminal
    nome_arquivo = sys.argv[1]

    # Verifica se o arquivo realmente existe
    if not os.path.exists(nome_arquivo):
        print(f"Erro: arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)

    # Chama a função que processa o arquivo inteiro
    codigo = processar_arquivo(nome_arquivo)

    # Encerra o programa com o código retornado
    sys.exit(codigo)


# Garante que o programa só será executado diretamente
# e não quando esse arquivo for apenas importado em outro módulo
if __name__ == "__main__":
    main()