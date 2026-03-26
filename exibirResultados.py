# Aluno 4 - Nome: Enzo Curcio Stival

def _formatar_ir(item):
    if not isinstance(item, tuple):
        return str(item)

    op = item[0]

    if op == "CONST":
        return f"{item[1]:.1f}"

    if op == "VAR":
        return f"VAR({item[1]})"

    if op == "LOAD":
        return f"LOAD({item[1]})"

    if op == "STORE":
        return f"STORE({item[1]}, {_formatar_ir(item[2])})"

    if op == "RES":
        return f"RES({item[1]})"

    if len(item) == 3:
        return f"{op}({_formatar_ir(item[1])}, {_formatar_ir(item[2])})"

    return str(item)


def exibirResultados(resultados):
    print("\n" + "=" * 60)
    print("RESULTADOS DO PROCESSAMENTO")
    print("=" * 60)

    if not resultados:
        print("Nenhum resultado para exibir.")
        print("=" * 60)
        return

    for i, resultado in enumerate(resultados, start=1):
        if isinstance(resultado, float):
            texto = f"{resultado:.1f}"
        else:
            texto = _formatar_ir(resultado)

        print(f"Linha {i:02d}: {texto}")

    print("=" * 60)