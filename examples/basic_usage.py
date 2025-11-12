"""Exemplos básicos de uso do Tucano."""

from tucano import cpf


def main() -> None:
	"""Demonstra o uso básico do validador de CPF."""
	
	print("=" * 50)
	print("VALIDAÇÃO DE CPF")
	print("=" * 50)
	
	test_cpfs = [
		"123.456.789-09",
		"000.000.000-00",
		"12345678909",
		"111.111.111-11",
	]
	
	for test_cpf in test_cpfs:
		is_valid = cpf.validate(test_cpf)
		status = "✓ VÁLIDO" if is_valid else "✗ INVÁLIDO"
		print(f"{test_cpf:20} -> {status}")
	
	print("\n" + "=" * 50)
	print("FORMATAÇÃO DE CPF")
	print("=" * 50)
	
	unformatted = "12345678909"
	formatted = cpf.format(unformatted)
	print(f"{unformatted} -> {formatted}")
	
	print("\n" + "=" * 50)
	print("LIMPEZA DE CPF")
	print("=" * 50)
	
	formatted_cpf = "123.456.789-09"
	cleaned = cpf.clean(formatted_cpf)
	print(f"{formatted_cpf} -> {cleaned}")
	
	print("\n" + "=" * 50)
	print("GERAÇÃO DE CPF")
	print("=" * 50)
	
	print("\nCPFs válidos gerados:")
	for i in range(5):
		generated = cpf.generate()
		print(f"{i + 1}. {generated}")
	
	print("\n" + "=" * 50)
	print("CÁLCULO DE DÍGITOS VERIFICADORES")
	print("=" * 50)
	
	base = "123456789"
	check_digits = cpf.get_check_digits(base)
	print(f"Base: {base}")
	print(f"Dígitos verificadores: {check_digits}")
	print(f"CPF completo: {base}{check_digits}")


if __name__ == "__main__":
	main()