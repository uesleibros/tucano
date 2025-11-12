"""Exemplos de uso do validador de CEP."""

import asyncio
from tucano import cep


def exemplo_validacao() -> None:
	"""Demonstra validação de CEP."""
	print("=" * 60)
	print("VALIDAÇÃO DE CEP")
	print("=" * 60)
	
	test_ceps = [
		"01310-100",
		"01310100",
		"00000-000",
		"12345",
	]
	
	for test_cep in test_ceps:
		is_valid = cep.validate(test_cep)
		status = "✓ VÁLIDO" if is_valid else "✗ INVÁLIDO"
		print(f"{test_cep:20} -> {status}")


def exemplo_formatacao() -> None:
	"""Demonstra formatação de CEP."""
	print("\n" + "=" * 60)
	print("FORMATAÇÃO DE CEP")
	print("=" * 60)
	
	unformatted = "01310100"
	formatted = cep.format(unformatted)
	print(f"{unformatted} -> {formatted}")


def exemplo_consulta() -> None:
	"""Demonstra consulta de CEP."""
	print("\n" + "=" * 60)
	print("CONSULTA DE CEP (SÍNCRONA)")
	print("=" * 60)
	
	try:
		endereco = cep.consultar("01310-100")
		
		print(f"\nCEP: {endereco['cep']}")
		print(f"Logradouro: {endereco['logradouro']}")
		print(f"Bairro: {endereco['bairro']}")
		print(f"Cidade: {endereco['localidade']}")
		print(f"UF: {endereco['uf']}")
		print(f"DDD: {endereco['ddd']}")
		
	except Exception as e:
		print(f"Erro ao consultar CEP: {e}")


async def exemplo_consulta_async() -> None:
	"""Demonstra consulta assíncrona de CEP."""
	print("\n" + "=" * 60)
	print("CONSULTA DE CEP (ASSÍNCRONA)")
	print("=" * 60)
	
	try:
		endereco = await cep.consultar_async("20040-020")
		
		print(f"\nCEP: {endereco['cep']}")
		print(f"Logradouro: {endereco['logradouro']}")
		print(f"Bairro: {endereco['bairro']}")
		print(f"Cidade: {endereco['localidade']}")
		print(f"UF: {endereco['uf']}")
		
	except Exception as e:
		print(f"Erro ao consultar CEP: {e}")


async def exemplo_multiplas_consultas() -> None:
	"""Demonstra múltiplas consultas assíncronas."""
	print("\n" + "=" * 60)
	print("MÚLTIPLAS CONSULTAS ASSÍNCRONAS")
	print("=" * 60)
	
	ceps = ["01310-100", "20040-020", "30130-100"]
	
	tasks = [cep.consultar_async(c) for c in ceps]
	resultados = await asyncio.gather(*tasks, return_exceptions=True)
	
	for cep_consultado, resultado in zip(ceps, resultados):
		if isinstance(resultado, Exception):
			print(f"\n{cep_consultado}: ERRO - {resultado}")
		else:
			print(f"\n{cep_consultado}: {resultado['localidade']}/{resultado['uf']}")


def main() -> None:
	"""Executa todos os exemplos."""
	exemplo_validacao()
	exemplo_formatacao()
	exemplo_consulta()
	
	asyncio.run(exemplo_consulta_async())
	asyncio.run(exemplo_multiplas_consultas())


if __name__ == "__main__":
	main()