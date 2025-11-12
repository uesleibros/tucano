"""Testes para o validador de Telefone."""

import pytest
from tucano import telefone
from tucano.core.exceptions import InvalidTelefone


class TestTelefoneValidation:
	"""Testes de validação de telefone."""
	
	def test_validate_celular_formatted(self) -> None:
		"""Testa validação de celular formatado."""
		assert telefone.validate("(11) 98765-4321") is True
	
	def test_validate_celular_unformatted(self) -> None:
		"""Testa validação de celular sem formatação."""
		assert telefone.validate("11987654321") is True
	
	def test_validate_fixo_formatted(self) -> None:
		"""Testa validação de fixo formatado."""
		assert telefone.validate("(11) 3456-7890") is True
	
	def test_validate_fixo_unformatted(self) -> None:
		"""Testa validação de fixo sem formatação."""
		assert telefone.validate("1134567890") is True
	
	def test_validate_ddd_invalid(self) -> None:
		"""Testa validação de telefone com DDD inválido."""
		assert telefone.validate("(00) 98765-4321") is False
		assert telefone.validate("(01) 3456-7890") is False
		assert telefone.validate("(90) 3456-7890") is False
	
	def test_validate_celular_without_9(self) -> None:
		"""Testa validação de celular sem 9 inicial."""
		assert telefone.validate("11887654321") is False
		assert telefone.validate("11787654321") is False
	
	def test_validate_fixo_with_9(self) -> None:
		"""Testa validação de fixo começando com 9 (inválido)."""
		assert telefone.validate("1198765432") is False
		assert telefone.validate("(11) 9876-5432") is False
	
	def test_validate_wrong_length_short(self) -> None:
		"""Testa validação de telefone com menos dígitos."""
		assert telefone.validate("119876543") is False
		assert telefone.validate("11876543") is False
	
	def test_validate_wrong_length_long(self) -> None:
		"""Testa validação de telefone com mais dígitos."""
		assert telefone.validate("119876543210") is False
		assert telefone.validate("11987654321098") is False
	
	def test_validate_with_raise_error_valid(self) -> None:
		"""Testa validação com raise_error para telefone válido."""
		assert telefone.validate("(11) 98765-4321", raise_error=True) is True
	
	def test_validate_with_raise_error_invalid_ddd(self) -> None:
		"""Testa validação com raise_error para DDD inválido."""
		with pytest.raises(InvalidTelefone, match="DDD inválido"):
			telefone.validate("(00) 98765-4321", raise_error=True)
	
	def test_validate_with_raise_error_wrong_length(self) -> None:
		"""Testa validação com raise_error para tamanho incorreto."""
		with pytest.raises(InvalidTelefone, match="deve ter 10"):
			telefone.validate("119876543", raise_error=True)
	
	def test_validate_with_raise_error_celular_without_9(self) -> None:
		"""Testa validação com raise_error para celular sem 9."""
		with pytest.raises(InvalidTelefone, match="deve começar com 9"):
			telefone.validate("11887654321", raise_error=True)
	
	def test_validate_with_raise_error_fixo_with_9(self) -> None:
		"""Testa validação com raise_error para fixo começando com 9."""
		with pytest.raises(InvalidTelefone, match="não pode começar com 9"):
			telefone.validate("1198765432", raise_error=True)


class TestTelefoneFormat:
	"""Testes de formatação de telefone."""
	
	def test_format_celular_unformatted(self) -> None:
		"""Testa formatação de celular sem formatação."""
		assert telefone.format("11987654321") == "(11) 98765-4321"
	
	def test_format_fixo_unformatted(self) -> None:
		"""Testa formatação de fixo sem formatação."""
		assert telefone.format("1134567890") == "(11) 3456-7890"
	
	def test_format_already_formatted_celular(self) -> None:
		"""Testa formatação de celular já formatado (idempotência)."""
		formatted = "(11) 98765-4321"
		assert telefone.format(formatted) == formatted
	
	def test_format_already_formatted_fixo(self) -> None:
		"""Testa formatação de fixo já formatado (idempotência)."""
		formatted = "(11) 3456-7890"
		assert telefone.format(formatted) == formatted
	
	def test_format_wrong_length(self) -> None:
		"""Testa formatação de telefone com tamanho incorreto."""
		with pytest.raises(InvalidTelefone, match="deve ter 10 ou 11 dígitos"):
			telefone.format("119876543")


class TestTelefoneClean:
	"""Testes de limpeza de telefone."""
	
	def test_clean_formatted_celular(self) -> None:
		"""Testa limpeza de celular formatado."""
		assert telefone.clean("(11) 98765-4321") == "11987654321"
	
	def test_clean_formatted_fixo(self) -> None:
		"""Testa limpeza de fixo formatado."""
		assert telefone.clean("(11) 3456-7890") == "1134567890"
	
	def test_clean_unformatted(self) -> None:
		"""Testa limpeza de telefone sem formatação (idempotência)."""
		assert telefone.clean("11987654321") == "11987654321"
	
	def test_clean_with_spaces(self) -> None:
		"""Testa limpeza de telefone com espaços."""
		assert telefone.clean("11 98765 4321") == "11987654321"
	
	def test_clean_with_extra_chars(self) -> None:
		"""Testa limpeza de telefone com caracteres extras."""
		assert telefone.clean("Tel: (11) 98765-4321") == "11987654321"


class TestTelefoneGenerate:
	"""Testes de geração de telefone."""
	
	def test_generate_celular(self) -> None:
		"""Testa geração de celular."""
		generated = telefone.generate(tipo="celular", ddd="11")
		assert telefone.validate(generated) is True
		assert telefone.is_celular(generated) is True
	
	def test_generate_fixo(self) -> None:
		"""Testa geração de fixo."""
		generated = telefone.generate(tipo="fixo", ddd="11")
		assert telefone.validate(generated) is True
		assert telefone.is_fixo(generated) is True
	
	def test_generate_formatted(self) -> None:
		"""Testa geração de telefone formatado."""
		generated = telefone.generate(formatted=True)
		assert "(" in generated
		assert ")" in generated
		assert "-" in generated
	
	def test_generate_unformatted(self) -> None:
		"""Testa geração de telefone sem formatação."""
		generated = telefone.generate(formatted=False)
		assert generated.isdigit()
	
	def test_generate_different_ddds(self) -> None:
		"""Testa geração com diferentes DDDs."""
		ddds = ["11", "21", "85", "47"]
		for ddd in ddds:
			generated = telefone.generate(ddd=ddd)
			assert telefone.get_ddd(generated) == ddd
	
	def test_generate_invalid_ddd(self) -> None:
		"""Testa erro ao gerar com DDD inválido."""
		with pytest.raises(InvalidTelefone, match="DDD inválido"):
			telefone.generate(ddd="00")
	
	def test_generate_invalid_tipo(self) -> None:
		"""Testa erro ao gerar com tipo inválido."""
		with pytest.raises(InvalidTelefone, match="Tipo deve ser"):
			telefone.generate(tipo="invalido")  # type: ignore


class TestTelefoneGetTipo:
	"""Testes de identificação de tipo."""
	
	def test_get_tipo_celular(self) -> None:
		"""Testa identificação de celular."""
		assert telefone.get_tipo("(11) 98765-4321") == "celular"
		assert telefone.get_tipo("11987654321") == "celular"
	
	def test_get_tipo_fixo(self) -> None:
		"""Testa identificação de fixo."""
		assert telefone.get_tipo("(11) 3456-7890") == "fixo"
		assert telefone.get_tipo("1134567890") == "fixo"
	
	def test_get_tipo_invalid(self) -> None:
		"""Testa erro ao identificar tipo de telefone inválido."""
		with pytest.raises(InvalidTelefone):
			telefone.get_tipo("119876543")


class TestTelefoneGetDDD:
	"""Testes de obtenção de DDD."""
	
	def test_get_ddd_celular(self) -> None:
		"""Testa obtenção de DDD de celular."""
		assert telefone.get_ddd("(11) 98765-4321") == "11"
		assert telefone.get_ddd("21987654321") == "21"
	
	def test_get_ddd_fixo(self) -> None:
		"""Testa obtenção de DDD de fixo."""
		assert telefone.get_ddd("(11) 3456-7890") == "11"
		assert telefone.get_ddd("8534567890") == "85"
	
	def test_get_ddd_invalid(self) -> None:
		"""Testa erro ao obter DDD de telefone inválido."""
		with pytest.raises(InvalidTelefone):
			telefone.get_ddd("119876543")


class TestTelefoneIsCelular:
	"""Testes de verificação se é celular."""
	
	def test_is_celular_true(self) -> None:
		"""Testa verificação positiva de celular."""
		assert telefone.is_celular("(11) 98765-4321") is True
		assert telefone.is_celular("11987654321") is True
	
	def test_is_celular_false(self) -> None:
		"""Testa verificação negativa de celular (é fixo)."""
		assert telefone.is_celular("(11) 3456-7890") is False
		assert telefone.is_celular("1134567890") is False


class TestTelefoneIsFixo:
	"""Testes de verificação se é fixo."""
	
	def test_is_fixo_true(self) -> None:
		"""Testa verificação positiva de fixo."""
		assert telefone.is_fixo("(11) 3456-7890") is True
		assert telefone.is_fixo("1134567890") is True
	
	def test_is_fixo_false(self) -> None:
		"""Testa verificação negativa de fixo (é celular)."""
		assert telefone.is_fixo("(11) 98765-4321") is False
		assert telefone.is_fixo("11987654321") is False


class TestTelefoneGetEstadoPorDDD:
	"""Testes de obtenção de estado por DDD."""
	
	def test_get_estado_sp(self) -> None:
		"""Testa obtenção de estado para DDDs de São Paulo."""
		assert telefone.get_estado_por_ddd("11") == "SP"
		assert telefone.get_estado_por_ddd("19") == "SP"
	
	def test_get_estado_rj(self) -> None:
		"""Testa obtenção de estado para DDDs do Rio de Janeiro."""
		assert telefone.get_estado_por_ddd("21") == "RJ"
		assert telefone.get_estado_por_ddd("22") == "RJ"
	
	def test_get_estado_ce(self) -> None:
		"""Testa obtenção de estado para DDDs do Ceará."""
		assert telefone.get_estado_por_ddd("85") == "CE"
		assert telefone.get_estado_por_ddd("88") == "CE"
	
	def test_get_estado_invalid_ddd(self) -> None:
		"""Testa erro ao obter estado de DDD inválido."""
		with pytest.raises(InvalidTelefone, match="DDD inválido"):
			telefone.get_estado_por_ddd("00")


class TestTelefoneEdgeCases:
	"""Testes de casos extremos."""
	
	def test_validate_empty_string(self) -> None:
		"""Testa validação de string vazia."""
		assert telefone.validate("") is False
	
	def test_validate_only_special_chars(self) -> None:
		"""Testa validação de string com apenas caracteres especiais."""
		assert telefone.validate("()- ") is False
	
	def test_format_preserves_digits(self) -> None:
		"""Testa que formatação preserva todos os dígitos."""
		original = "11987654321"
		formatted = telefone.format(original)
		cleaned = telefone.clean(formatted)
		assert cleaned == original