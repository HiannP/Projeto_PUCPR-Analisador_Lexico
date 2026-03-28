from InterpretadorRPN import InterpretadorRPN

def testar_interpretador():
    print("\n=== INICIANDO TESTES DO INTERPRETADOR RPN ===")

    interp = InterpretadorRPN()

    testes = [
        # =========================
        # OPERAÇÕES BÁSICAS
        # =========================
        (["(", "3", "2", "+", ")"], "soma simples"),
        (["(", "5", "3", "-", ")"], "subtração"),
        (["(", "4", "2", "*", ")"], "multiplicação"),
        (["(", "8", "2", "/", ")"], "divisão"),
        (["(", "7", "2", "//", ")"], "divisão inteira"),
        (["(", "7", "2", "%", ")"], "módulo"),
        (["(", "2", "3", "^", ")"], "potência"),

        # =========================
        # ANINHAMENTO
        # =========================
        (["(", "3", "(", "2", "4", "*", ")", "+", ")"], "aninhado simples"),
        (["(", "(", "1", "2", "+", ")", "(", "3", "4", "*", ")", "/", ")"], "aninhado complexo"),

        # =========================
        # MEMÓRIA
        # =========================
        (["(", "10", "X", "MEM", ")"], "store em memória"),
        (["(", "X", "MEM", ")"], "load de memória"),

        # =========================
        # RES
        # =========================
        (["(", "0", "RES", ")"], "resultado anterior"),

        # =========================
        # ERROS
        # =========================
        (["(", "+", ")"], "erro operador sem operandos"),
        (["(", "X", "RES", ")"], "erro RES inválido"),
    ]

    for tokens, descricao in testes:
        try:
            resultado = interp.executarExpressao(tokens)
            print(f"[OK] {descricao}: {resultado}")
        except Exception as e:
            print(f"[ERRO ESPERADO?] {descricao}: {e}")

    print("=== FIM DOS TESTES ===\n")