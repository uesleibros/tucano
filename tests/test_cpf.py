"""Testes para o validador de CPF."""

import pytest
from tucano import cpf
from tucano.core.exceptions import InvalidCPF


class TestCPFValidation:
	"""Testes de validação de CPF."""
	
	def test_validate_valid_cpf_formatted(self) -> None:
		"""Testa validação de CPF válido formatado."""
		assert cpf.validate("123.456.789-09") is True
	
	def test_validate_valid_cpf_unformatted(self) -> None:
		"""Testa validação de CPF válido sem formatação."""
		assert cpf.validate("12345678909") is True
	
	def test_validate_invalid_cpf_wrong_digits(self) -> None:
		"""Testa validação de CPF com dígitos verificadores incorretos."""
		assert cpf.validate("123.456.789-00") is False
	
	def test_validate_cpf_all_zeros(self) -> None:
		"""Testa validação de CPF com todos os dígitos zero."""
		assert cpf.validate("000.000.000-00") is False
		assert cpf.validate("00000000000") is False
	
	def test_validate_cpf_repeated_digits(self) -> None:
		"""Testa validação de CPF com sequência de dígitos iguais."""
		for digit in range(10):
			cpf_repeated = str(digit) * 11
			assert cpf.validate(cpf_repeated) is False
	
	def test_validate_cpf_wrong_length_short(self) -> None:
		"""Testa validação de CPF com menos de 11 dígitos."""
		assert cpf.validate("123.456.789") is False
		assert cpf.validate("12345678") is False
	
	def test_validate_cpf_wrong_length_long(self) -> None:
		"""Testa validação de CPF com mais de 11 dígitos."""
		assert cpf.validate("123.456.789-099") is False
		assert cpf.validate("123456789099") is False
	
	def test_validate_with_raise_error_valid(self) -> None:
		"""Testa validação com raise_error para CPF válido."""
		assert cpf.validate("123.456.789-09", raise_error=True) is True
	
	def test_validate_with_raise_error_invalid(self) -> None:
		"""Testa validação com raise_error para CPF inválido."""
		with pytest.raises(InvalidCPF, match="sequência de dígitos iguais"):
			cpf.validate("111.111.111-11", raise_error=True)
	
	def test_validate_with_raise_error_wrong_length(self) -> None:
		"""Testa validação com raise_error para CPF com tamanho incorreto."""
		with pytest.raises(InvalidCPF, match="deve ter 11 dígitos"):
			cpf.validate("123.456.789", raise_error=True)
	
	def test_validate_with_raise_error_wrong_check_digits(self) -> None:
		"""Testa validação com raise_error para dígitos verificadores incorretos."""
		with pytest.raises(InvalidCPF, match="dígitos verificadores incorretos"):
			cpf.validate("123.456.789-00", raise_error=True)


class TestCPFFormat:
	"""Testes de formatação de CPF."""
	
	def test_format_unformatted_cpf(self) -> None:
		"""Testa formatação de CPF sem formatação."""
		assert cpf.format("12345678909") == "123.456.789-09"
	
	def test_format_already_formatted_cpf(self) -> None:
		"""Testa formatação de CPF já formatado (idempotência)."""
		formatted = "123.456.789-09"
		assert cpf.format(formatted) == formatted
	
	def test_format_partially_formatted_cpf(self) -> None:
		"""Testa formatação de CPF parcialmente formatado."""
		assert cpf.format("123456789-09") == "123.456.789-09"
		assert cpf.format("123.456.78909") == "123.456.789-09"
	
	def test_format_cpf_wrong_length(self) -> None:
		"""Testa formatação de CPF com tamanho incorreto."""
		with pytest.raises(InvalidCPF, match="deve ter 11 dígitos"):
			cpf.format("123456789")
		
		with pytest.raises(InvalidCPF, match="deve ter 11 dígitos"):
			cpf.format("123456789012")


class TestCPFClean:
	"""Testes de limpeza de CPF."""
	
	def test_clean_formatted_cpf(self) -> None:
		"""Testa limpeza de CPF formatado."""
		assert cpf.clean("123.456.789-09") == "12345678909"
	
	def test_clean_unformatted_cpf(self) -> None:
		"""Testa limpeza de CPF sem formatação (idempotência)."""
		assert cpf.clean("12345678909") == "12345678909"
	
	def test_clean_cpf_with_spaces(self) -> None:
		"""Testa limpeza de CPF com espaços."""
		assert cpf.clean("123 456 789 09") == "12345678909"
		assert cpf.clean(" 123.456.789-09 ") == "12345678909"
	
	def test_clean_cpf_with_letters(self) -> None:
		"""Testa limpeza de CPF com letras (remove tudo exceto dígitos)."""
		assert cpf.clean("CPF: 123.456.789-09") == "12345678909"


class TestCPFGenerate:
	"""Testes de geração de CPF."""
	
	def test_generate_formatted_cpf(self) -> None:
		"""Testa geração de CPF formatado."""
		generated = cpf.generate(formatted=True)
		assert len(generated) == 14
		assert cpf.validate(generated) is True
		assert "." in generated
		assert "-" in generated
	
	def test_generate_unformatted_cpf(self) -> None:
		"""Testa geração de CPF sem formatação."""
		generated = cpf.generate(formatted=False)
		assert len(generated) == 11
		assert generated.isdigit()
		assert cpf.validate(generated) is True
	
	def test_generate_multiple_unique_cpfs(self) -> None:
		"""Testa que múltiplos CPFs gerados são únicos."""
		cpfs = {cpf.generate(formatted=False) for _ in range(100)}
		assert len(cpfs) > 95
	
	def test_generate_cpf_not_in_blacklist(self) -> None:
		"""Testa que CPFs gerados não estão na blacklist."""
		for _ in range(50):
			generated = cpf.generate(formatted=False)
			assert generated not in cpf.BLACKLIST


class TestCPFGetCheckDigits:
	"""Testes de cálculo de dígitos verificadores."""
	
	def test_get_check_digits_from_base(self) -> None:
		"""Testa cálculo de dígitos verificadores a partir de base."""
		assert cpf.get_check_digits("123456789") == "09"
	
	def test_get_check_digits_from_formatted_base(self) -> None:
		"""Testa cálculo de dígitos a partir de base formatada."""
		assert cpf.get_check_digits("123.456.789") == "09"
	
	def test_get_check_digits_base_too_short(self) -> None:
		"""Testa erro ao calcular dígitos com base muito curta."""
		with pytest.raises(InvalidCPF, match="deve ter pelo menos 9 dígitos"):
			cpf.get_check_digits("12345678")
	
	def test_get_check_digits_truncates_extra(self) -> None:
		"""Testa que dígitos extras na base são ignorados."""
		assert cpf.get_check_digits("12345678900") == "09"


class TestCPFEdgeCases:
	"""Testes de casos extremos."""
	
	def test_validate_empty_string(self) -> None:
		"""Testa validação de string vazia."""
		assert cpf.validate("") is False
	
	def test_validate_only_special_chars(self) -> None:
		"""Testa validação de string com apenas caracteres especiais."""
		assert cpf.validate("...---") is False
	
	def test_format_cpf_with_only_numbers(self) -> None:
		"""Testa que formatação só aceita exatamente 11 dígitos."""
		valid_cpf = "12345678909"
		formatted = cpf.format(valid_cpf)
		assert formatted.replace(".", "").replace("-", "") == valid_cpf