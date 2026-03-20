import os

def parseExpressao(linha: str, _tokens_: list):
    """
    Analisa uma linha de expressão RPN e extrai tokens usando um AFD.
    """
    _tokens_.clear() # Limpa resquícios de execuções anteriores
    
    # Dicionário mutável para controlar o estado da leitura
    contexto = {"pos": 0, "lexema": ""} # Armazena a posição atual e o lexema em construção
    tamanho = len(linha) # Armazena o tamanho da linha para evitar chamadas repetidas

    # Definição dos estados dos Autômatos Finitos Determinísticos (AFDs)

    def estado_inicial(): # Estado inicial do AFD, responsável por identificar o tipo de token a ser processado
        if contexto["pos"] >= tamanho: # Verifica se chegou ao final da linha
            return None
        
        c = linha[contexto["pos"]] # Lê o caractere atual

        if c.isspace(): # Ignora espaços em branco
            contexto["pos"] += 1
            return estado_inicial
        elif c == '(':
            return estado_parentese_abre
        elif c == ')':
            return estado_parentese_fecha
        elif c == '+':
            return estado_adicao
        elif c == '-':
            return estado_subtracao
        elif c == '*':
            return estado_multiplicacao
        elif c == '%':
            return estado_resto
        elif c == '^':
            return estado_potenciacao
        else: # Caractere não reconhecido
            raise ValueError(f"Léxico: Caractere não reconhecido '{c}' na posição {contexto['pos']}")
        
    
    # Estados de Símbolos Simples (Um Caractere)

    def estado_parentese_abre(): # Adiciona o parêntese de abertura à lista de tokens
        _tokens_.append('(')
        contexto["pos"] += 1
        return estado_inicial

    def estado_parentese_fecha(): # Adiciona o parêntese de fechamento à lista de tokens
        _tokens_.append(')')
        contexto["pos"] += 1
        return estado_inicial

    def estado_adicao(): # Adiciona o operador de adição à lista de tokens
        _tokens_.append('+')
        contexto["pos"] += 1
        return estado_inicial

    def estado_subtracao(): # Adiciona o operador de subtração à lista de tokens
        _tokens_.append('-')
        contexto["pos"] += 1
        return estado_inicial

    def estado_multiplicacao(): # Adiciona o operador de multiplicação à lista de tokens
        _tokens_.append('*')
        contexto["pos"] += 1
        return estado_inicial

    def estado_resto(): # Adiciona o operador de resto à lista de tokens
        _tokens_.append('%')
        contexto["pos"] += 1
        return estado_inicial

    def estado_potenciacao(): # Adiciona o operador de potenciação à lista de tokens
        _tokens_.append('^')
        contexto["pos"] += 1
        return estado_inicial
    

    # Inicia o AFD no estado inicial
    estado_atual = estado_inicial
    while estado_atual is not None: # Continua processando enquanto houver estados a serem avaliados
        estado_atual = estado_atual()

    saldo = 0 # Variável para verificar o balanceamento de parênteses
    for t in _tokens_:
        if t == '(': saldo += 1
        elif t == ')': saldo -= 1
    
    if saldo < 0:
        raise ValueError("Sintático/Léxico: Parênteses desbalanceados (fechamento inesperado).")
    
    if saldo > 0:
        raise ValueError("Sintático/Léxico: Parênteses desbalanceados (abertura sem fechamento).")
    

# !!! Funções de Teste !!!

def processar_arquivo_teste(nome_arquivo):
    # Descobre o caminho exato onde este script .py está salvo
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Cria o caminho completo para o arquivo de teste
    caminho_completo = os.path.join(diretorio_atual, nome_arquivo)
    
    print(f"\nProcurando o arquivo em: {caminho_completo}\n")
    
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        for numero_linha, linha in enumerate(linhas, start=1):
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue # Pula linhas vazias
                
            tokens = []
            print(f"Linha {numero_linha}: {linha_limpa}")
            try:
                parseExpressao(linha_limpa, tokens)
                print(f"Tokens Gerados: {tokens}\n")
            except ValueError as e:
                print(f"Erro: {e}\n")
                
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado no caminho especificado.")

if __name__ == "__main__":
    # O arquivo .txt deve estar na mesma pasta que este script .py
    processar_arquivo_teste("teste_lexico_1.txt")
