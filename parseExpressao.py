import os
import sys

def parseExpressao(linha: str, _tokens_: list):
    """
    Analisa uma linha de expressão RPN e extrai tokens usando um AFD.
    """
    _tokens_.clear() # Limpa resquícios de execuções anteriores
    
    # Dicionário mutável para controlar o estado da leitura
    contexto = {"p_atual": 0, "lexema": ""} # Armazena a posição atual e o lexema em construção
    tamanho = len(linha) # Armazena o tamanho da linha para evitar chamadas repetidas

    # Definição dos estados dos Autômatos Finitos Determinísticos (AFDs)

    def estado_inicial(): # Estado inicial do AFD, responsável por identificar o tipo de token a ser processado
        if contexto["p_atual"] >= tamanho: # Verifica se chegou ao final da linha
            return None

        c = linha[contexto["p_atual"]] # Lê o caractere atual

        if c.isspace(): # Ignora espaços em branco
            contexto["p_atual"] += 1 
            return estado_inicial 
        elif c in ['(', ')']:
            return estado_parenteses
        elif c in ['+', '-', '*', '%', '^']:
            return estado_operador
        elif c == '/':
            return estado_divisao
        elif c.isalpha() and c.isupper():
            contexto["lexema"] = c
            contexto["p_atual"] += 1
            return estado_identificador
        elif c.isdigit():
            contexto["lexema"] = c
            contexto["p_atual"] += 1
            return estado_num_inteiro
        else: # Caractere não reconhecido
            raise ValueError(f"Léxico: Caractere não reconhecido '{c}' na posição {contexto['p_atual']}")
        
    
    # Estados de Símbolos Simples (Um Caractere)

    def estado_parenteses(): # Processa parênteses
        _tokens_.append(linha[contexto["p_atual"]]) 
        contexto["p_atual"] += 1
        return estado_inicial

    def estado_operador(): # Processa operadores aritméticos simples
        _tokens_.append(linha[contexto["p_atual"]])
        contexto["p_atual"] += 1
        return estado_inicial
    
    
    # Estados de Símbolos Complexos (Multiplos Caracteres)
    
    def estado_divisao():
        contexto["p_atual"] += 1 
        
        # Olha o próximo caractere para decidir se é / (Divisão real) ou // (Divisão inteira)
        if contexto["p_atual"] >= tamanho:
            _tokens_.append('/') # Se não houver mais caracteres, é uma divisão real simples
            return None
            
        c = linha[contexto["p_atual"]]
        if c == '/':
            _tokens_.append('//') # Divisão inteira
            contexto["p_atual"] += 1  # Consome o segundo '/'
            return estado_inicial
        else:
            _tokens_.append('/')  # Divisão real
            return estado_inicial # Retorna sem consumir, pois o caractere pertence ao próximo token   

    def estado_identificador():
        if contexto["p_atual"] >= tamanho:
            _tokens_.append(contexto["lexema"])
            return None
            
        c = linha[contexto["p_atual"]]
        if c.isalpha() and c.isupper(): # Permite apenas letras maiúsculas para identificadores
            contexto["lexema"] += c
            contexto["p_atual"] += 1
            return estado_identificador
        elif c.isspace() or c in '()': # Identificador termina com espaço ou parêntese
            _tokens_.append(contexto["lexema"])
            return estado_inicial
        else:
            raise ValueError(f"Léxico: Identificador inválido na posição {contexto['p_atual']}. Apenas letras maiúsculas permitidas.")
        
    def estado_num_inteiro():
        if contexto["p_atual"] >= tamanho:
            _tokens_.append(contexto["lexema"])
            return None
            
        c = linha[contexto["p_atual"]]
        if c.isdigit(): # Continua formando o número inteiro
            contexto["lexema"] += c
            contexto["p_atual"] += 1
            return estado_num_inteiro
        elif c == '.': # Se encontrar um ponto, transita para o estado de número decimal
            contexto["lexema"] += c
            contexto["p_atual"] += 1
            return estado_num_decimal
        elif c.isspace() or c in '()+-*/%^': # O número inteiro termina quando encontra um espaço ou um operador
            _tokens_.append(contexto["lexema"])
            return estado_inicial
        else:
            raise ValueError(f"Léxico: Número malformado na posição {contexto['p_atual']}. Encontrado '{c}'.")

    def estado_num_decimal():
        if contexto["p_atual"] >= tamanho:
            _tokens_.append(contexto["lexema"])
            return None
            
        c = linha[contexto["p_atual"]]
        if c.isdigit(): # Continua formando o número decimal
            contexto["lexema"] += c
            contexto["p_atual"] += 1
            return estado_num_decimal
        elif c.isspace() or c in '()+-*/%^': # O número decimal termina quando encontra um espaço ou um operador
            if contexto["lexema"].endswith('.'): # Verifica se o número decimal termina com um ponto, o que é inválido
                 raise ValueError(f"Léxico: Número decimal malformado (termina com ponto) na posição {contexto['p_atual']}")
            _tokens_.append(contexto["lexema"])
            return estado_inicial
        elif c == '.': # Se encontrar outro ponto, é um número decimal inválido
             raise ValueError(f"Léxico: Múltiplos pontos decimais encontrados na posição {contexto['p_atual']}")
        else:
            raise ValueError(f"Léxico: Número decimal malformado na posição {contexto['p_atual']}. Encontrado '{c}'.")

    # Inicia o AFD no estado inicial
    estado_atual = estado_inicial
    while estado_atual is not None:
        estado_atual = estado_atual() # Chama o estado atual e atualiza para o próximo estado retornado

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

# Aluno 2
class InterpretadorRPN:
    def __init__(self):
        # Gerenciamento de variáveis (V MEM) e (MEM)
        self.memorias = {}
        # Histórico de resultados para o comando (N RES)
        self.historico_resultados = []

    def executarExpressao(self, tokens: list):
        """
        Implementação da infraestrutura de pilha e operadores aritméticos.
        Garante a precisão de 64 bits (IEEE 754) nativa do float em Python.
        """
        pilha = []

        # Ignora parênteses, pois a execução RPN é baseada puramente na ordem da pilha
        tokens_uteis = [t for t in tokens if t not in ('(', ')')]

        for idx, token in enumerate(tokens_uteis):
            # 1. Operadores Aritméticos Fundamentais
            if token in ('+', '-', '*', '/', '//', '%', '^'):
                if len(pilha) < 2:
                    raise IndexError(f"Erro: Operandos insuficientes para '{token}'.")

                b = pilha.pop()  # Segundo operando
                a = pilha.pop()  # Primeiro operando

                if token == '+':
                    pilha.append(a + b)
                elif token == '-':
                    pilha.append(a - b)
                elif token == '*':
                    pilha.append(a * b)
                elif token == '/':
                    if b == 0: raise ZeroDivisionError("Divisão real por zero.")
                    pilha.append(a / b)
                elif token == '//':
                    if b == 0: raise ZeroDivisionError("Divisão inteira por zero.")
                    pilha.append(float(int(a) // int(b)))
                elif token == '%':
                    if b == 0: raise ZeroDivisionError("Resto de divisão por zero.")
                    pilha.append(float(int(a) % int(b)))
                elif token == '^':
                    pilha.append(a ** b)

            # 2. Comando de Histórico (RES) - Lógica de busca inicial
            elif token == "RES":
                if len(pilha) < 1:
                    raise IndexError("Erro: Pilha vazia para comando RES.")

                n = int(pilha.pop())
                # Verifica se o índice N existe no histórico (0 é o último, 1 o penúltimo...)
                if 0 <= n < len(self.historico_resultados):
                    valor_res = self.historico_resultados[-(n + 1)]
                    pilha.append(valor_res)
                else:
                    raise IndexError(
                        f"Erro: Histórico RES {n} não disponível (Tamanho: {len(self.historico_resultados)}).")

            # 3. Comando de Memória (MEM)
            elif token == "MEM":
                if len(pilha) < 1:
                    raise IndexError("Erro: Pilha vazia para comando MEM.")

                    # O valor a ser guardado é o topo atual da pilha
                valor = pilha[-1]

                # O identificador 'V' é o token imediatamente anterior ao 'MEM'
                # Note: O interpretador já terá empilhado o valor de V (ou 0.0) no passo anterior.
                # Precisamos recuperar o nome da variável na lista de tokens.
                nome_variavel = tokens_uteis[idx - 1]

                if nome_variavel.replace('.', '', 1).isdigit():
                    raise ValueError(f"Erro: '{nome_variavel}' não é um identificador válido para MEM.")

                self.memorias[nome_variavel] = valor
                # O comando MEM mantém geralmente o valor na pilha para uso posterior na expressão

            # 4. Operandos e Variáveis
            else:
                try:
                    # Conversão para 64-bit float
                    pilha.append(float(token))
                except ValueError:
                    # Se não for número, trata como variável (identificador)
                    # Se a variável não existir, inicia com 0.0 conforme convenção comum
                    valor_var = self.memorias.get(token, 0.0)
                    pilha.append(valor_var)

        # Define o resultado final e atualiza o histórico
        resultado_final = pilha[0] if pilha else 0.0
        self.historico_resultados.append(resultado_final)
        return resultado_final

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parseExpressao.py <nome_arquivo>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    processar_arquivo_teste(nome_arquivo)
