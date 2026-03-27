"""
test_aluno4.py

Este arquivo contém os testes automatizados da parte do Aluno 4.

Objetivo:
Validar se os principais módulos do projeto estão funcionando corretamente
após a integração final.

O que é testado:
1. Se uma expressão simples é analisada e interpretada corretamente;
2. Se o comando MEM consegue armazenar valores/estruturas em memória;
3. Se o comando MEM consegue recuperar valores/estruturas já armazenados;
4. Se o comando RES consegue acessar resultados anteriores do histórico;
5. Se a leitura de arquivo funciona corretamente;
6. Se a geração de código Assembly retorna uma saída válida.

Como funciona:
- Cada função iniciada com "test_" representa um teste automatizado.
- O pytest executa essas funções e verifica se os resultados esperados acontecem.
- Se uma condição "assert" falhar, o teste será marcado como erro.

Execução:
    python -m pytest test_aluno4.py
"""

import os
import tempfile

# Importa a função responsável pela análise léxica das expressões
from parseExpressao import parseExpressao

# Importa a classe que interpreta os tokens da expressão em notação RPN
from InterpretadorRPN import InterpretadorRPN

# Importa a classe responsável por ler arquivo e gerar Assembly
from gerarAssembly import Gerar_Assembly


def test_parse_e_execucao_simples():
    """
    Testa uma expressão simples de soma.

    Fluxo:
    1. Gera os tokens da expressão "(3.0 2.0 +)"
    2. Interpreta os tokens
    3. Verifica se o resultado retornado é uma tupla
    4. Verifica se a operação identificada foi ADD
    """
    tokens = []

    # Gera os tokens da expressão
    parseExpressao("(3.0 2.0 +)", tokens)

    # Interpreta os tokens gerados
    interpretador = InterpretadorRPN()
    resultado = interpretador.executarExpressao(tokens)

    # Verifica se o resultado é uma estrutura intermediária válida
    assert isinstance(resultado, tuple)

    # Verifica se a operação reconhecida é uma soma
    assert resultado[0] == "ADD"


def test_mem_store():
    """
    Testa o armazenamento em memória com MEM.

    Fluxo:
    1. Gera os tokens da expressão "(X 5.0 MEM)"
    2. Interpreta a expressão
    3. Verifica se a estrutura retornada indica armazenamento (STORE)
    4. Verifica se a variável usada foi X
    """
    tokens = []

    # Gera os tokens da expressão com armazenamento em memória
    parseExpressao("(X 5.0 MEM)", tokens)

    # Interpreta os tokens
    interpretador = InterpretadorRPN()
    resultado = interpretador.executarExpressao(tokens)

    # Verifica se o resultado corresponde a uma operação de armazenamento
    assert resultado[0] == "STORE"

    # Verifica se o identificador usado foi X
    assert resultado[1] == "X"


def test_mem_load():
    """
    Testa a leitura de memória com MEM.

    Fluxo:
    1. Primeiro armazena algo em memória com "(X 5.0 MEM)"
    2. Depois tenta recuperar com "(X MEM)"
    3. Verifica se a estrutura retornada é LOAD
    4. Verifica se a memória acessada foi X
    """
    interpretador = InterpretadorRPN()

    # Armazena um valor/estrutura em memória
    tokens_store = []
    parseExpressao("(X 5.0 MEM)", tokens_store)
    interpretador.executarExpressao(tokens_store)

    # Recupera da memória o conteúdo salvo anteriormente
    tokens_load = []
    parseExpressao("(X MEM)", tokens_load)
    resultado = interpretador.executarExpressao(tokens_load)

    # Verifica se a operação retornada corresponde a leitura de memória
    assert resultado[0] == "LOAD"

    # Verifica se o identificador acessado foi X
    assert resultado[1] == "X"


def test_res_historico():
    """
    Testa o acesso ao histórico com RES.

    Fluxo:
    1. Executa uma expressão inicial para alimentar o histórico
    2. Executa "(0 RES)"
    3. Verifica se o resultado retornado é do tipo RES
    """
    interpretador = InterpretadorRPN()

    # Executa uma expressão inicial para gerar histórico
    tokens1 = []
    parseExpressao("(3.0 2.0 +)", tokens1)
    interpretador.executarExpressao(tokens1)

    # Solicita recuperação de resultado anterior pelo histórico
    tokens2 = []
    parseExpressao("(0 RES)", tokens2)
    resultado = interpretador.executarExpressao(tokens2)

    # Verifica se a estrutura retornada corresponde ao uso de RES
    assert resultado[0] == "RES"


def test_ler_arquivo():
    """
    Testa a leitura de arquivo pela classe Gerar_Assembly.

    Fluxo:
    1. Cria um arquivo temporário com duas expressões
    2. Lê esse arquivo com lerArquivo()
    3. Verifica se duas linhas válidas foram carregadas
    4. Remove o arquivo ao final
    """
    conteudo = "(3.0 2.0 +)\n(4.0 2.0 /)\n"

    # Cria um arquivo temporário para simular um arquivo de entrada real
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        f.write(conteudo)
        nome = f.name

    try:
        # Lê o arquivo temporário usando a classe do projeto
        gerador = Gerar_Assembly()
        linhas = gerador.lerArquivo(nome)

        # Verifica se as duas linhas foram lidas corretamente
        assert len(linhas) == 2
    finally:
        # Remove o arquivo temporário após o teste
        os.remove(nome)


def test_gerar_assembly():
    """
    Testa se a geração de Assembly retorna uma saída válida.

    Fluxo:
    1. Gera tokens de uma expressão simples
    2. Chama gerarAssembly()
    3. Verifica se o retorno é uma string
    4. Verifica se a string não está vazia
    """
    tokens = []

    # Gera os tokens da expressão
    parseExpressao("(3.0 2.0 +)", tokens)

    # Gera o código Assembly correspondente
    gerador = Gerar_Assembly()
    codigo = gerador.gerarAssembly(tokens)

    # Verifica se o retorno é texto
    assert isinstance(codigo, str)

    # Verifica se foi gerado algum conteúdo
    assert len(codigo) > 0