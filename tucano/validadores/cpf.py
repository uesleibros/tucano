"""Validador de CPF (Cadastro de Pessoa Física)."""

import random
from typing import List
from ..core.base import BaseValidator
from ..core.exceptions import InvalidCPF


class CPFValidator(BaseValidator[str]):
	"""Validador de CPF com suporte a validação, formatação e geração.
	
	O CPF (Cadastro de Pessoa Física) é um documento brasileiro composto por
	11 dígitos numéricos, sendo os dois últimos dígitos verificadores calculados
	a partir dos 9 primeiros.
	
	Formato padrão: XXX.XXX.XXX-XX
	
	Attributes:
		BLACKLIST: Lista de CPFs inválidos conhecidos (sequências de dígitos iguais).
		
	Examples:
		>>> from tucano import cpf
		>>> cpf.validate("123.456.789-09")
		True
		>>> cpf.format("12345678909")
		"123.456.789-09"
		>>> cpf.generate()
		"123.456.789-09"
	"""
	
	BLACKLIST: List[str] = [
		"00000000000",
		"11111111111",
		"22222222222",
		"33333333333",
		"44444444444",
		"55555555555",
		"66666666666",
		"77777777777",
		"88888888888",
		"99999999999",
	]
	
	def validate(self, value: str, raise_error: bool = False) -> bool:
		"""Valida um CPF brasileiro.
		
		Verifica se o CPF fornecido é válido de acordo com as regras:
		- Deve ter exatamente 11 dígitos
		- Não pode ser uma sequência de dígitos iguais
		- Dígitos verificadores devem estar corretos
		
		Args:
			value: CPF a ser validado (aceita com ou sem formatação).
			raise_error: Se True, levanta InvalidCPF ao invés de retornar False.
						
		Returns:
			True se o CPF é válido, False caso contrário.
			
		Raises:
			InvalidCPF: Se raise_error=True e o CPF for inválido.
			
		Examples:
			>>> cpf.validate("123.456.789-09")
			True
			>>> cpf.validate("12345678909")
			True
			>>> cpf.validate("000.000.000-00")
			False
			>>> cpf.validate("111.111.111-11", raise_error=True)
			Traceback (most recent call last):
			...
			InvalidCPF: CPF inválido: sequência de dígitos iguais
		"""
		try:
			cleaned = self.clean(value)
			
			if len(cleaned) != 11:
				raise InvalidCPF(f"CPF deve ter 11 dígitos, recebido: {len(cleaned)}")
			
			if cleaned in self.BLACKLIST:
				raise InvalidCPF("CPF inválido: sequência de dígitos iguais")
			
			if not self._validate_check_digits(cleaned):
				raise InvalidCPF("CPF inválido: dígitos verificadores incorretos")
			
			return True
			
		except InvalidCPF:
			if raise_error:
				raise
			return False
	
	def _validate_check_digits(self, cpf: str) -> bool:
		"""Valida os dígitos verificadores do CPF.
		
		Calcula os dois dígitos verificadores usando o algoritmo oficial
		e compara com os dígitos fornecidos.
		
		Args:
			cpf: CPF com 11 dígitos numéricos (sem formatação).
			
		Returns:
			True se os dígitos verificadores estão corretos, False caso contrário.
		"""
		first_digit = self._calculate_first_digit(cpf[:9])
		if int(cpf[9]) != first_digit:
			return False
		
		second_digit = self._calculate_second_digit(cpf[:10])
		return int(cpf[10]) == second_digit
	
	def _calculate_first_digit(self, cpf_base: str) -> int:
		"""Calcula o primeiro dígito verificador do CPF.
		
		Args:
			cpf_base: Primeiros 9 dígitos do CPF.
			
		Returns:
			Primeiro dígito verificador (0-9).
		"""
		total = sum(int(cpf_base[i]) * (10 - i) for i in range(9))
		remainder = total % 11
		return 0 if remainder < 2 else 11 - remainder
	
	def _calculate_second_digit(self, cpf_base: str) -> int:
		"""Calcula o segundo dígito verificador do CPF.
		
		Args:
			cpf_base: Primeiros 10 dígitos do CPF (incluindo primeiro verificador).
			
		Returns:
			Segundo dígito verificador (0-9).
		"""
		total = sum(int(cpf_base[i]) * (11 - i) for i in range(10))
		remainder = total % 11
		return 0 if remainder < 2 else 11 - remainder
	
	def format(self, value: str) -> str:
		"""Formata um CPF no padrão brasileiro XXX.XXX.XXX-XX.
		
		Args:
			value: CPF a ser formatado (com ou sem formatação prévia).
			
		Returns:
			CPF formatado com pontos e hífen.
			
		Raises:
			InvalidCPF: Se o CPF não tiver exatamente 11 dígitos.
			
		Examples:
			>>> cpf.format("12345678909")
			"123.456.789-09"
			>>> cpf.format("123.456.789-09")
			"123.456.789-09"
		"""
		cleaned = self.clean(value)
		
		if len(cleaned) != 11:
			raise InvalidCPF(f"CPF deve ter 11 dígitos para formatação")
		
		return f"{cleaned[:3]}.{cleaned[3:6]}.{cleaned[6:9]}-{cleaned[9:]}"
	
	def clean(self, value: str) -> str:
		"""Remove toda formatação do CPF, mantendo apenas dígitos.
		
		Args:
			value: CPF formatado ou não formatado.
			
		Returns:
			CPF contendo apenas os 11 dígitos numéricos.
			
		Examples:
			>>> cpf.clean("123.456.789-09")
			"12345678909"
			>>> cpf.clean("12345678909")
			"12345678909"
		"""
		return self._only_digits(value)
	
	def generate(self, formatted: bool = True) -> str:
		"""Gera um CPF válido aleatório.
		
		Cria um CPF completamente aleatório com dígitos verificadores corretos.
		Útil para testes e geração de dados fictícios.
		
		Args:
			formatted: Se True, retorna o CPF formatado (XXX.XXX.XXX-XX).
					  Se False, retorna apenas os 11 dígitos.
					  
		Returns:
			CPF válido gerado aleatoriamente.
			
		Examples:
			>>> cpf_gerado = cpf.generate()
			>>> cpf.validate(cpf_gerado)
			True
			>>> cpf_sem_formato = cpf.generate(formatted=False)
			>>> len(cpf_sem_formato)
			11
		"""
		base_digits = [random.randint(0, 9) for _ in range(9)]
		base_str = "".join(map(str, base_digits))
		
		first_digit = self._calculate_first_digit(base_str)
		base_str += str(first_digit)
		
		second_digit = self._calculate_second_digit(base_str)
		cpf_complete = base_str + str(second_digit)
		
		return self.format(cpf_complete) if formatted else cpf_complete
	
	def get_check_digits(self, cpf_base: str) -> str:
		"""Calcula e retorna os dígitos verificadores para uma base de CPF.
		
		Args:
			cpf_base: Primeiros 9 dígitos do CPF (com ou sem formatação).
			
		Returns:
			String com os 2 dígitos verificadores.
			
		Raises:
			InvalidCPF: Se a base não tiver pelo menos 9 dígitos.
			
		Examples:
			>>> cpf.get_check_digits("123456789")
			"09"
			>>> cpf.get_check_digits("123.456.789")
			"09"
		"""
		cleaned = self.clean(cpf_base)
		
		if len(cleaned) < 9:
			raise InvalidCPF("Base do CPF deve ter pelo menos 9 dígitos")
		
		base = cleaned[:9]
		first = self._calculate_first_digit(base)
		second = self._calculate_second_digit(base + str(first))
		
		return f"{first}{second}"


cpf: CPFValidator = CPFValidator()