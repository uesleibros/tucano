"""Exemplos de uso do validador de CNPJ."""

from tucano import cnpj


def exemplo_validacao() -> None:
	"""Demonstra validação de CNPJ."""
	print("=" * 60)
	print("VALIDAÇÃO DE CNPJ")
	print("=" * 60)
	
	test_cnpjs = [
		"11.222.333/0001-81",
		"11222333000181",
		"00.000.000/0000-00",
		"11.111.111/1111-11",
	]
	
	for test_cnpj in test_cnpjs:
		is_valid = cnpj.validate(test_cnpj)
		status = "✓ VÁLIDO" if is_valid else "✗ INVÁLIDO"
		print(f"{test_cnpj:25} -> {status}")


def exemplo_formatacao() -> None:
	"""Demonstra formatação de CNPJ."""
	print("\n" + "=" * 60)
	print("FORMATAÇÃO DE CNPJ")
	print("=" * 60)
	
	unformatted = "11222333000181"
	formatted = cnpj.format(unformatted)
	print(f"{unformatted} -> {formatted}")


def exemplo_geracao() -> None:
	"""Demonstra geração de CNPJ."""
	print("\n" + "=" * 60)
	print("GERAÇÃO DE CNPJ")
	print("=" * 60)
	
	print("\nCNPJs válidos gerados:")
	
	print("\nMatriz:")
	for i in range(3):
		generated = cnpj.generate(filial=1)
		print(f"{i + 1}. {generated}")
	
	print("\nFiliais:")
	for i in range(3):
		generated = cnpj.generate(filial=i + 2)
		numero = cnpj.get_numero_filial(generated)
		print(f"{i + 1}. {generated} (Filial {numero})")


def exemplo_matriz_filial() -> None:
	"""Demonstra identificação de matriz e filial."""
	print("\n" + "=" * 60)
	print("IDENTIFICAÇÃO DE MATRIZ E FILIAL")
	print("=" * 60)
	
	test_cnpjs = [
		cnpj.generate(filial=1),
		cnpj.generate(filial=2),
		cnpj.generate(filial=10),
	]
	
	for test_cnpj in test_cnpjs:
		numero_filial = cnpj.get_numero_filial(test_cnpj)
		tipo = "MATRIZ" if cnpj.is_matriz(test_cnpj) else "FILIAL"
		base = cnpj.get_base(test_cnpj)
		
		print(f"\nCNPJ: {test_cnpj}")
		print(f"  Tipo: {tipo}")
		print(f"  Número da filial: {numero_filial}")
		print(f"  Base da empresa: {base}")


def exemplo_digitos_verificadores() -> None:
	"""Demonstra cálculo de dígitos verificadores."""
	print("\n" + "=" * 60)
	print("CÁLCULO DE DÍGITOS VERIFICADORES")
	print("=" * 60)
	
	bases = [
		"112223330001",
		"112223330002",
		"112223330010",
	]
	
	for base in bases:
		check_digits = cnpj.get_check_digits(base)
		cnpj_completo = base + check_digits
		formatted = cnpj.format(cnpj_completo)
		
		print(f"\nBase: {base}")
		print(f"Dígitos verificadores: {check_digits}")
		print(f"CNPJ completo: {formatted}")


def main() -> None:
	"""Executa todos os exemplos."""
	exemplo_validacao()
	exemplo_formatacao()
	exemplo_geracao()
	exemplo_matriz_filial()
	exemplo_digitos_verificadores()


if __name__ == "__main__":
	main()