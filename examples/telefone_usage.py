"""Exemplos de uso do validador de Telefone."""

from tucano import telefone


def exemplo_validacao() -> None:
    """Demonstra validação de telefone."""
    print("=" * 60)
    print("VALIDAÇÃO DE TELEFONE")
    print("=" * 60)
    
    test_telefones = [
        "(11) 98765-4321",
        "11987654321",
        "(11) 3456-7890",
        "1134567890",
        "(00) 98765-4321",
    ]
    
    for tel in test_telefones:
        is_valid = telefone.validate(tel)
        status = "✓ VÁLIDO" if is_valid else "✗ INVÁLIDO"
        print(f"{tel:20} -> {status}")


def exemplo_formatacao() -> None:
    """Demonstra formatação de telefone."""
    print("\n" + "=" * 60)
    print("FORMATAÇÃO DE TELEFONE")
    print("=" * 60)
    
    telefones = [
        "11987654321",
        "1134567890",
    ]
    
    for tel in telefones:
        formatted = telefone.format(tel)
        tipo = telefone.get_tipo(tel)
        print(f"{tel} -> {formatted} ({tipo})")


def exemplo_identificacao() -> None:
    """Demonstra identificação de tipo e DDD."""
    print("\n" + "=" * 60)
    print("IDENTIFICAÇÃO DE TIPO E DDD")
    print("=" * 60)
    
    telefones = [
        "(11) 98765-4321",
        "(21) 3456-7890",
        "(85) 98888-7777",
    ]
    
    for tel in telefones:
        tipo = telefone.get_tipo(tel)
        ddd = telefone.get_ddd(tel)
        estado = telefone.get_estado_por_ddd(ddd)
        is_cel = "SIM" if telefone.is_celular(tel) else "NÃO"
        
        print(f"\nTelefone: {tel}")
        print(f"  Tipo: {tipo}")
        print(f"  DDD: {ddd}")
        print(f"  Estado: {estado}")
        print(f"  É celular: {is_cel}")


def exemplo_geracao() -> None:
    """Demonstra geração de telefone."""
    print("\n" + "=" * 60)
    print("GERAÇÃO DE TELEFONE")
    print("=" * 60)
    
    print("\nCelulares:")
    for i in range(3):
        tel = telefone.generate(tipo="celular", ddd="11")
        print(f"{i + 1}. {tel}")
    
    print("\nFixos:")
    for i in range(3):
        tel = telefone.generate(tipo="fixo", ddd="21")
        print(f"{i + 1}. {tel}")
    
    print("\nDiferentes estados:")
    ddds = [("11", "SP"), ("21", "RJ"), ("85", "CE"), ("47", "SC")]
    for ddd, uf in ddds:
        tel = telefone.generate(tipo="celular", ddd=ddd)
        print(f"{uf}: {tel}")


def main() -> None:
    """Executa todos os exemplos."""
    exemplo_validacao()
    exemplo_formatacao()
    exemplo_identificacao()
    exemplo_geracao()


if __name__ == "__main__":
    main()