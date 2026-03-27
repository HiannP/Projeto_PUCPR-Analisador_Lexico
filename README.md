# Projeto_PUCPR-Analisador_Lexico

## Informações do Projeto

**Instituição:** PUCPR - Pontifícia Universidade Católica do Paraná  
**Curso:** Bacharelado em Ciência da Computação  
**Disciplina:** Construindo Interpretadores  
**Professor:** Frank Coelho de Alcântara  

**Projeto:** Fase 1 - Analisador Léxico e Gerador de Assembly para ARMv7  

**Grupo no Canvas:** Grupo 18

## Integrantes do Grupo

- Enzo Curcio Stival — GitHub: `enzocstival`
- Henrique Godoy — GitHub: `Henrique-G15`
- Hiann W. Padilha — GitHub: `HiannP`
- Marcos Paulo Ruppel — GitHub: `MarcosRuppel`

## Visão Geral

Este projeto implementa um analisador léxico para expressões aritméticas escritas em notação polonesa reversa (RPN), além do processamento dos tokens e da geração de código Assembly compatível com o simulador **Cpulator ARMv7 DEC1-SOC (v16.1)**.

O sistema recebe um arquivo de texto com uma expressão por linha, realiza a análise léxica, interpreta os tokens gerados, exibe o resultado do processamento e produz o código Assembly correspondente à última execução realizada.

## Objetivo da Atividade

O objetivo desta fase do trabalho é desenvolver, em grupo, um programa capaz de:

- ler arquivos de texto contendo expressões em RPN;
- realizar análise léxica com base em autômatos finitos determinísticos;
- validar tokens e estruturas inválidas;
- interpretar expressões e comandos especiais da linguagem;
- gerar código Assembly ARMv7 funcional;
- executar o programa por linha de comando;
- manter o projeto documentado e versionado em um repositório público no GitHub.

## Requisitos da Linguagem

A linguagem implementada trabalha com:

### Operações aritméticas
- soma: `+`
- subtração: `-`
- multiplicação: `*`
- divisão real: `/`
- divisão inteira: `//`
- módulo: `%`
- potência: `^`

### Comandos especiais
- `(N RES)` — retorna o resultado da expressão de **N linhas anteriores**
- `(V MEM)` — armazena um valor em uma memória
- `(MEM)` — retorna o valor armazenado em uma memória; se não houver valor, retorna `0.0`

## Estrutura do Projeto

- `parseExpressao.py` — análise léxica das expressões
- `InterpretadorRPN.py` — interpretação dos tokens e tratamento de memória/histórico
- `gerarAssembly.py` — geração do código Assembly ARMv7
- `exibirResultados.py` — exibição formatada dos resultados
- `main.py` — integração geral do sistema e execução via linha de comando
- `test_aluno4.py` — testes automatizados da integração
- `teste_lexico.txt` — arquivo de teste 1
- `teste_lexico2.txt` — arquivo de teste 2
- `teste_lexico3.txt` — arquivo de teste 3
- `tokens_ultima_execucao.txt` — tokens gerados na última execução
- `ultimo_assembly_gerado.s` — código Assembly gerado na última execução

## Organização por Responsabilidade

### Aluno 1
Responsável pela função `parseExpressao` e pelo analisador léxico baseado em autômato finito.

### Aluno 2
Responsável pela função `executarExpressao` e pela interpretação dos tokens em RPN.

### Aluno 3
Responsável pela leitura do arquivo e pela geração do código Assembly.

### Aluno 4
Responsável pela função `exibirResultados`, pela interface do usuário via `main.py`, pela integração dos módulos e pelos testes finais do programa completo.

## Requisitos para Execução

Para executar o projeto, é necessário ter instalado:

- Python 3.10 ou superior
- `pytest` para os testes automatizados

## Como Executar

O programa deve ser executado **via linha de comando**, informando o arquivo de teste como argumento. O projeto **não utiliza menu interativo**.

### Exemplo básico

```bash
python main.py teste_lexico.txt