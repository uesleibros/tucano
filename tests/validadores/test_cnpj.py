"""Testes para o validador de CNPJ."""

import pytest
from tucano.validadores import cnpj
from tucano.core.exceptions import InvalidCNPJ

class TestCNPJValidation:
	"""Testes de validação de CNPJ."""
	
	def test_validate_valid_cnpj_formatted(self) -> None:
		"""Testa validação de CNPJ válido formatado."""
		assert cnpj.validate("11.222.333/0001-81") is True
	
	def test_validate_valid_cnpj_unformatted(self) -> None:
		"""Testa validação de CNPJ válido sem formatação."""
		assert cnpj.validate("11222333000181") is True
	
	def test_validate_invalid_cnpj_wrong_digits(self) -> None:
		"""Testa validação de CNPJ com dígitos verificadores incorretos."""
		assert cnpj.validate("11.222.333/0001-00") is False
	
	def test_validate_cnpj_all_zeros(self) -> None:
		"""Testa validação de CNPJ com todos os dígitos zero."""
		assert cnpj.validate("00.000.000/0000-00") is False
		assert cnpj.validate("00000000000000") is False
	
	def test_validate_cnpj_repeated_digits(self) -> None:
		"""Testa validação de CNPJ com sequência de dígitos iguais."""
		for digit in range(10):
			cnpj_repeated = str(digit) * 14
			assert cnpj.validate(cnpj_repeated) is False
	
	def test_validate_cnpj_wrong_length_short(self) -> None:
		"""Testa validação de CNPJ com menos de 14 dígitos."""
		assert cnpj.validate("11.222.333/0001") is False
		assert cnpj.validate("1122233300018") is False
	
	def test_validate_cnpj_wrong_length_long(self) -> None:
		"""Testa validação de CNPJ com mais de 14 dígitos."""
		assert cnpj.validate("11.222.333/0001-811") is False
		assert cnpj.validate("112223330001811") is False
	
	def test_validate_with_raise_error_valid(self) -> None:
		"""Testa validação com raise_error para CNPJ válido."""
		assert cnpj.validate("11.222.333/0001-81", raise_error=True) is True
	
	def test_validate_with_raise_error_invalid(self) -> None:
		"""Testa validação com raise_error para CNPJ inválido."""
		with pytest.raises(InvalidCNPJ, match="sequência de dígitos iguais"):
			cnpj.validate("11.111.111/1111-11", raise_error=True)
	
	def test_validate_with_raise_error_wrong_length(self) -> None:
		"""Testa validação com raise_error para CNPJ com tamanho incorreto."""
		with pytest.raises(InvalidCNPJ, match="deve ter 14 dígitos"):
			cnpj.validate("11.222.333/0001", raise_error=True)
	
	def test_validate_with_raise_error_wrong_check_digits(self) -> None:
		"""Testa validação com raise_error para dígitos verificadores incorretos."""
		with pytest.raises(InvalidCNPJ, match="dígitos verificadores incorretos"):
			cnpj.validate("11.222.333/0001-00", raise_error=True)


class TestCNPJFormat:
	"""Testes de formatação de CNPJ."""
	
	def test_format_unformatted_cnpj(self) -> None:
		"""Testa formatação de CNPJ sem formatação."""
		assert cnpj.format("11222333000181") == "11.222.333/0001-81"
	
	def test_format_already_formatted_cnpj(self) -> None:
		"""Testa formatação de CNPJ já formatado (idempotência)."""
		formatted = "11.222.333/0001-81"
		assert cnpj.format(formatted) == formatted
	
	def test_format_partially_formatted_cnpj(self) -> None:
		"""Testa formatação de CNPJ parcialmente formatado."""
		assert cnpj.format("11222333/0001-81") == "11.222.333/0001-81"
		assert cnpj.format("11.222.333000181") == "11.222.333/0001-81"
	
	def test_format_cnpj_wrong_length(self) -> None:
		"""Testa formatação de CNPJ com tamanho incorreto."""
		with pytest.raises(InvalidCNPJ, match="deve ter 14 dígitos"):
			cnpj.format("1122233300018")
		
		with pytest.raises(InvalidCNPJ, match="deve ter 14 dígitos"):
			cnpj.format("112223330001811")


class TestCNPJClean:
	"""Testes de limpeza de CNPJ."""
	
	def test_clean_formatted_cnpj(self) -> None:
		"""Testa limpeza de CNPJ formatado."""
		assert cnpj.clean("11.222.333/0001-81") == "11222333000181"
	
	def test_clean_unformatted_cnpj(self) -> None:
		"""Testa limpeza de CNPJ sem formatação (idempotência)."""
		assert cnpj.clean("11222333000181") == "11222333000181"
	
	def test_clean_cnpj_with_spaces(self) -> None:
		"""Testa limpeza de CNPJ com espaços."""
		assert cnpj.clean("11 222 333 0001 81") == "11222333000181"
		assert cnpj.clean(" 11.222.333/0001-81 ") == "11222333000181"
	
	def test_clean_cnpj_with_letters(self) -> None:
		"""Testa limpeza de CNPJ com letras (remove tudo exceto dígitos)."""
		assert cnpj.clean("CNPJ: 11.222.333/0001-81") == "11222333000181"


class TestCNPJGenerate:
	"""Testes de geração de CNPJ."""
	
	def test_generate_formatted_cnpj(self) -> None:
		"""Testa geração de CNPJ formatado."""
		generated = cnpj.generate(formatted=True)
		assert len(generated) == 18
		assert cnpj.validate(generated) is True
		assert "." in generated
		assert "/" in generated
		assert "-" in generated
	
	def test_generate_unformatted_cnpj(self) -> None:
		"""Testa geração de CNPJ sem formatação."""
		generated = cnpj.generate(formatted=False)
		assert len(generated) == 14
		assert generated.isdigit()
		assert cnpj.validate(generated) is True
	
	def test_generate_cnpj_matriz(self) -> None:
		"""Testa geração de CNPJ matriz (filial 1)."""
		generated = cnpj.generate(filial=1)
		assert "0001" in generated
		assert cnpj.is_matriz(generated) is True
	
	def test_generate_cnpj_filial(self) -> None:
		"""Testa geração de CNPJ filial."""
		generated = cnpj.generate(filial=2)
		assert "0002" in generated
		assert cnpj.is_filial(generated) is True
	
	def test_generate_cnpj_filial_custom(self) -> None:
		"""Testa geração de CNPJ com número de filial customizado."""
		generated = cnpj.generate(filial=123)
		assert "0123" in generated
	
	def test_generate_cnpj_filial_invalid_low(self) -> None:
		"""Testa erro ao gerar CNPJ com filial menor que 1."""
		with pytest.raises(InvalidCNPJ, match="deve estar entre 1 e 9999"):
			cnpj.generate(filial=0)
	
	def test_generate_cnpj_filial_invalid_high(self) -> None:
		"""Testa erro ao gerar CNPJ com filial maior que 9999."""
		with pytest.raises(InvalidCNPJ, match="deve estar entre 1 e 9999"):
			cnpj.generate(filial=10000)
	
	def test_generate_multiple_unique_cnpjs(self) -> None:
		"""Testa que múltiplos CNPJs gerados são únicos."""
		cnpjs = {cnpj.generate(formatted=False) for _ in range(100)}
		assert len(cnpjs) > 95
	
	def test_generate_cnpj_not_in_blacklist(self) -> None:
		"""Testa que CNPJs gerados não estão na blacklist."""
		for _ in range(50):
			generated = cnpj.generate(formatted=False)
			assert generated not in cnpj.BLACKLIST


class TestCNPJGetCheckDigits:
	"""Testes de cálculo de dígitos verificadores."""
	
	def test_get_check_digits_from_base(self) -> None:
		"""Testa cálculo de dígitos verificadores a partir de base."""
		assert cnpj.get_check_digits("112223330001") == "81"
	
	def test_get_check_digits_from_formatted_base(self) -> None:
		"""Testa cálculo de dígitos a partir de base formatada."""
		assert cnpj.get_check_digits("11.222.333/0001") == "81"
	
	def test_get_check_digits_base_too_short(self) -> None:
		"""Testa erro ao calcular dígitos com base muito curta."""
		with pytest.raises(InvalidCNPJ, match="deve ter pelo menos 12 dígitos"):
			cnpj.get_check_digits("11222333000")
	
	def test_get_check_digits_truncates_extra(self) -> None:
		"""Testa que dígitos extras na base são ignorados."""
		assert cnpj.get_check_digits("11222333000100") == "81"


class TestCNPJMatrizFilial:
	"""Testes de identificação de matriz e filial."""
	
	def test_is_matriz_true(self) -> None:
		"""Testa identificação de CNPJ matriz."""
		assert cnpj.is_matriz("11.222.333/0001-81") is True
	
	def test_is_matriz_false(self) -> None:
		"""Testa que filial não é identificada como matriz."""
		generated_filial = cnpj.generate(filial=2)
		assert cnpj.is_matriz(generated_filial) is False
	
	def test_is_filial_true(self) -> None:
		"""Testa identificação de CNPJ filial."""
		generated_filial = cnpj.generate(filial=2)
		assert cnpj.is_filial(generated_filial) is True
	
	def test_is_filial_false(self) -> None:
		"""Testa que matriz não é identificada como filial."""
		assert cnpj.is_filial("11.222.333/0001-81") is False
	
	def test_is_matriz_invalid_cnpj(self) -> None:
		"""Testa erro ao verificar matriz com CNPJ inválido."""
		with pytest.raises(InvalidCNPJ):
			cnpj.is_matriz("11.111.111/1111-11")
	
	def test_is_filial_invalid_cnpj(self) -> None:
		"""Testa erro ao verificar filial com CNPJ inválido."""
		with pytest.raises(InvalidCNPJ):
			cnpj.is_filial("11.111.111/1111-11")


class TestCNPJNumeroFilial:
	"""Testes de obtenção de número de filial."""
	
	def test_get_numero_filial_matriz(self) -> None:
		"""Testa obtenção de número de filial para matriz."""
		assert cnpj.get_numero_filial("11.222.333/0001-81") == 1
	
	def test_get_numero_filial_segunda(self) -> None:
		"""Testa obtenção de número de segunda filial."""
		generated = cnpj.generate(filial=2)
		assert cnpj.get_numero_filial(generated) == 2
	
	def test_get_numero_filial_custom(self) -> None:
		"""Testa obtenção de número de filial customizado."""
		generated = cnpj.generate(filial=123)
		assert cnpj.get_numero_filial(generated) == 123
	
	def test_get_numero_filial_invalid_cnpj(self) -> None:
		"""Testa erro ao obter número de filial de CNPJ inválido."""
		with pytest.raises(InvalidCNPJ):
			cnpj.get_numero_filial("11.111.111/1111-11")


class TestCNPJBase:
	"""Testes de obtenção de número base."""
	
	def test_get_base_matriz(self) -> None:
		"""Testa obtenção de número base de matriz."""
		assert cnpj.get_base("11.222.333/0001-81") == "11222333"
	
	def test_get_base_filial(self) -> None:
		"""Testa obtenção de número base de filial."""
		generated = cnpj.generate(filial=2)
		base = cnpj.get_base(generated)
		assert len(base) == 8
		assert base.isdigit()
	
	def test_get_base_same_for_different_filials(self) -> None:
		"""Testa que base é igual para diferentes filiais da mesma empresa."""
		base_num = "11222333"
		cnpj1 = base_num + "0001" + cnpj.get_check_digits(base_num + "0001")
		cnpj2 = base_num + "0002" + cnpj.get_check_digits(base_num + "0002")
		
		assert cnpj.get_base(cnpj1) == cnpj.get_base(cnpj2)
		assert cnpj.get_base(cnpj1) == base_num
	
	def test_get_base_invalid_cnpj(self) -> None:
		"""Testa erro ao obter base de CNPJ inválido."""
		with pytest.raises(InvalidCNPJ):
			cnpj.get_base("11.111.111/1111-11")


class TestCNPJEdgeCases:
	"""Testes de casos extremos."""
	
	def test_validate_empty_string(self) -> None:
		"""Testa validação de string vazia."""
		assert cnpj.validate("") is False
	
	def test_validate_only_special_chars(self) -> None:
		"""Testa validação de string com apenas caracteres especiais."""
		assert cnpj.validate(".../---") is False
	
	def test_format_cnpj_with_only_numbers(self) -> None:
		"""Testa que formatação só aceita exatamente 14 dígitos."""
		valid_cnpj = "11222333000181"
		formatted = cnpj.format(valid_cnpj)
		cleaned = formatted.replace(".", "").replace("/", "").replace("-", "")
		assert cleaned == valid_cnpj