"""Validador de CNPJ (Cadastro Nacional da Pessoa Jurídica)."""

import random
from typing import List
from ..core.base import BaseValidator
from ..core.exceptions import InvalidCNPJ


class CNPJValidator(BaseValidator[str]):
	"""Validador de CNPJ com suporte a validação, formatação e geração.
	
	O CNPJ (Cadastro Nacional da Pessoa Jurídica) é um documento brasileiro
	composto por 14 dígitos numéricos, sendo os dois últimos dígitos verificadores
	calculados a partir dos 12 primeiros.
	
	Formato padrão: XX.XXX.XXX/XXXX-XX
	
	Estrutura:
	- Primeiros 8 dígitos: número base da empresa
	- 4 dígitos seguintes: filial (0001 = matriz)
	- 2 últimos dígitos: dígitos verificadores
	
	Attributes:
		BLACKLIST: Lista de CNPJs inválidos conhecidos (sequências de dígitos iguais).
		PESO_PRIMEIRO: Sequência de pesos para calcular o primeiro dígito verificador.
		PESO_SEGUNDO: Sequência de pesos para calcular o segundo dígito verificador.
		
	Examples:
		>>> from tucano import cnpj
		>>> cnpj.validate("11.222.333/0001-81")
		True
		>>> cnpj.format("11222333000181")
		"11.222.333/0001-81"
		>>> cnpj.generate()
		"11.222.333/0001-81"
		>>> cnpj.is_matriz("11.222.333/0001-81")
		True
	"""
	
	BLACKLIST: List[str] = [
		"00000000000000",
		"11111111111111",
		"22222222222222",
		"33333333333333",
		"44444444444444",
		"55555555555555",
		"66666666666666",
		"77777777777777",
		"88888888888888",
		"99999999999999",
	]
	
	PESO_PRIMEIRO: List[int] = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
	PESO_SEGUNDO: List[int] = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
	
	def validate(self, value: str, raise_error: bool = False) -> bool:
		"""Valida um CNPJ brasileiro.
		
		Verifica se o CNPJ fornecido é válido de acordo com as regras:
		- Deve ter exatamente 14 dígitos
		- Não pode ser uma sequência de dígitos iguais
		- Dígitos verificadores devem estar corretos
		
		Args:
			value: CNPJ a ser validado (aceita com ou sem formatação).
			raise_error: Se True, levanta InvalidCNPJ ao invés de retornar False.
						
		Returns:
			True se o CNPJ é válido, False caso contrário.
			
		Raises:
			InvalidCNPJ: Se raise_error=True e o CNPJ for inválido.
			
		Examples:
			>>> cnpj.validate("11.222.333/0001-81")
			True
			>>> cnpj.validate("11222333000181")
			True
			>>> cnpj.validate("00.000.000/0000-00")
			False
			>>> cnpj.validate("11.111.111/1111-11", raise_error=True)
			Traceback (most recent call last):
			...
			InvalidCNPJ: CNPJ inválido: sequência de dígitos iguais
		"""
		try:
			cleaned = self.clean(value)
			
			if len(cleaned) != 14:
				raise InvalidCNPJ(f"CNPJ deve ter 14 dígitos, recebido: {len(cleaned)}")
			
			if cleaned in self.BLACKLIST:
				raise InvalidCNPJ("CNPJ inválido: sequência de dígitos iguais")
			
			if not self._validate_check_digits(cleaned):
				raise InvalidCNPJ("CNPJ inválido: dígitos verificadores incorretos")
			
			return True
			
		except InvalidCNPJ:
			if raise_error:
				raise
			return False
	
	def _validate_check_digits(self, cnpj: str) -> bool:
		"""Valida os dígitos verificadores do CNPJ.
		
		Calcula os dois dígitos verificadores usando o algoritmo oficial
		e compara com os dígitos fornecidos.
		
		Args:
			cnpj: CNPJ com 14 dígitos numéricos (sem formatação).
			
		Returns:
			True se os dígitos verificadores estão corretos, False caso contrário.
		"""
		first_digit = self._calculate_first_digit(cnpj[:12])
		if int(cnpj[12]) != first_digit:
			return False
		
		second_digit = self._calculate_second_digit(cnpj[:13])
		return int(cnpj[13]) == second_digit
	
	def _calculate_first_digit(self, cnpj_base: str) -> int:
		"""Calcula o primeiro dígito verificador do CNPJ.
		
		Args:
			cnpj_base: Primeiros 12 dígitos do CNPJ.
			
		Returns:
			Primeiro dígito verificador (0-9).
		"""
		total = sum(int(cnpj_base[i]) * self.PESO_PRIMEIRO[i] for i in range(12))
		remainder = total % 11
		return 0 if remainder < 2 else 11 - remainder
	
	def _calculate_second_digit(self, cnpj_base: str) -> int:
		"""Calcula o segundo dígito verificador do CNPJ.
		
		Args:
			cnpj_base: Primeiros 13 dígitos do CNPJ (incluindo primeiro verificador).
			
		Returns:
			Segundo dígito verificador (0-9).
		"""
		total = sum(int(cnpj_base[i]) * self.PESO_SEGUNDO[i] for i in range(13))
		remainder = total % 11
		return 0 if remainder < 2 else 11 - remainder
	
	def format(self, value: str) -> str:
		"""Formata um CNPJ no padrão brasileiro XX.XXX.XXX/XXXX-XX.
		
		Args:
			value: CNPJ a ser formatado (com ou sem formatação prévia).
			
		Returns:
			CNPJ formatado com pontos, barra e hífen.
			
		Raises:
			InvalidCNPJ: Se o CNPJ não tiver exatamente 14 dígitos.
			
		Examples:
			>>> cnpj.format("11222333000181")
			"11.222.333/0001-81"
			>>> cnpj.format("11.222.333/0001-81")
			"11.222.333/0001-81"
		"""
		cleaned = self.clean(value)
		
		if len(cleaned) != 14:
			raise InvalidCNPJ(f"CNPJ deve ter 14 dígitos para formatação")
		
		return f"{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:8]}/{cleaned[8:12]}-{cleaned[12:]}"
	
	def clean(self, value: str) -> str:
		"""Remove toda formatação do CNPJ, mantendo apenas dígitos.
		
		Args:
			value: CNPJ formatado ou não formatado.
			
		Returns:
			CNPJ contendo apenas os 14 dígitos numéricos.
			
		Examples:
			>>> cnpj.clean("11.222.333/0001-81")
			"11222333000181"
			>>> cnpj.clean("11222333000181")
			"11222333000181"
		"""
		return self._only_digits(value)
	
	def generate(self, formatted: bool = True, filial: int = 1) -> str:
		"""Gera um CNPJ válido aleatório.
		
		Cria um CNPJ completamente aleatório com dígitos verificadores corretos.
		Útil para testes e geração de dados fictícios.
		
		Args:
			formatted: Se True, retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX).
					  Se False, retorna apenas os 14 dígitos.
			filial: Número da filial (1-9999). 1 = matriz (0001).
				   
		Returns:
			CNPJ válido gerado aleatoriamente.
			
		Raises:
			InvalidCNPJ: Se filial estiver fora do range 1-9999.
			
		Examples:
			>>> cnpj_gerado = cnpj.generate()
			>>> cnpj.validate(cnpj_gerado)
			True
			>>> cnpj_sem_formato = cnpj.generate(formatted=False)
			>>> len(cnpj_sem_formato)
			14
			>>> cnpj_filial = cnpj.generate(filial=2)
			>>> "0002" in cnpj_filial
			True
		"""
		if not 1 <= filial <= 9999:
			raise InvalidCNPJ("Número de filial deve estar entre 1 e 9999")
		
		base_digits = [random.randint(0, 9) for _ in range(8)]
		filial_str = f"{filial:04d}"
		
		cnpj_base = "".join(map(str, base_digits)) + filial_str
		
		first_digit = self._calculate_first_digit(cnpj_base)
		cnpj_base += str(first_digit)
		
		second_digit = self._calculate_second_digit(cnpj_base)
		cnpj_complete = cnpj_base + str(second_digit)
		
		return self.format(cnpj_complete) if formatted else cnpj_complete
	
	def get_check_digits(self, cnpj_base: str) -> str:
		"""Calcula e retorna os dígitos verificadores para uma base de CNPJ.
		
		Args:
			cnpj_base: Primeiros 12 dígitos do CNPJ (com ou sem formatação).
			
		Returns:
			String com os 2 dígitos verificadores.
			
		Raises:
			InvalidCNPJ: Se a base não tiver pelo menos 12 dígitos.
			
		Examples:
			>>> cnpj.get_check_digits("112223330001")
			"81"
			>>> cnpj.get_check_digits("11.222.333/0001")
			"81"
		"""
		cleaned = self.clean(cnpj_base)
		
		if len(cleaned) < 12:
			raise InvalidCNPJ("Base do CNPJ deve ter pelo menos 12 dígitos")
		
		base = cleaned[:12]
		first = self._calculate_first_digit(base)
		second = self._calculate_second_digit(base + str(first))
		
		return f"{first}{second}"
	
	def is_matriz(self, value: str) -> bool:
		"""Verifica se o CNPJ é de uma matriz (filial 0001).
		
		Args:
			value: CNPJ a ser verificado (com ou sem formatação).
			
		Returns:
			True se for matriz, False se for filial.
			
		Raises:
			InvalidCNPJ: Se o CNPJ for inválido.
			
		Examples:
			>>> cnpj.is_matriz("11.222.333/0001-81")
			True
			>>> cnpj.is_matriz("11.222.333/0002-62")
			False
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidCNPJ(f"CNPJ inválido: {value}")
		
		return cleaned[8:12] == "0001"
	
	def is_filial(self, value: str) -> bool:
		"""Verifica se o CNPJ é de uma filial (filial diferente de 0001).
		
		Args:
			value: CNPJ a ser verificado (com ou sem formatação).
			
		Returns:
			True se for filial, False se for matriz.
			
		Raises:
			InvalidCNPJ: Se o CNPJ for inválido.
			
		Examples:
			>>> cnpj.is_filial("11.222.333/0001-81")
			False
			>>> cnpj.is_filial("11.222.333/0002-62")
			True
		"""
		return not self.is_matriz(value)
	
	def get_numero_filial(self, value: str) -> int:
		"""Retorna o número da filial do CNPJ.
		
		Args:
			value: CNPJ a ser analisado (com ou sem formatação).
			
		Returns:
			Número da filial (1 = matriz, 2+ = filiais).
			
		Raises:
			InvalidCNPJ: Se o CNPJ for inválido.
			
		Examples:
			>>> cnpj.get_numero_filial("11.222.333/0001-81")
			1
			>>> cnpj.get_numero_filial("11.222.333/0002-62")
			2
			>>> cnpj.get_numero_filial("11.222.333/0010-14")
			10
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidCNPJ(f"CNPJ inválido: {value}")
		
		return int(cleaned[8:12])
	
	def get_base(self, value: str) -> str:
		"""Retorna o número base do CNPJ (primeiros 8 dígitos).
		
		O número base identifica a empresa, independente da filial.
		
		Args:
			value: CNPJ a ser analisado (com ou sem formatação).
			
		Returns:
			Número base do CNPJ (8 dígitos).
			
		Raises:
			InvalidCNPJ: Se o CNPJ for inválido.
			
		Examples:
			>>> cnpj.get_base("11.222.333/0001-81")
			"11222333"
			>>> cnpj.get_base("11.222.333/0002-62")
			"11222333"
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidCNPJ(f"CNPJ inválido: {value}")
		
		return cleaned[:8]


cnpj: CNPJValidator = CNPJValidator()