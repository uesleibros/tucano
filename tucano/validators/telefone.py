"""Validador de Telefone brasileiro (fixo e celular)."""

import random
from typing import List, Literal
from ..core.base import BaseValidator
from ..core.exceptions import InvalidTelefone


TipoTelefone = Literal["fixo", "celular"]


class TelefoneValidator(BaseValidator[str]):
	"""Validador de telefone brasileiro com suporte a fixo e celular.
	
	O telefone brasileiro pode ser:
	- Fixo: 10 dígitos (XX) XXXX-XXXX
	- Celular: 11 dígitos (XX) 9XXXX-XXXX
	
	Onde XX é o DDD (código de área) válido do Brasil.
	
	Attributes:
		DDDS_VALIDOS: Lista de DDDs válidos no Brasil.
		
	Examples:
		>>> from tucano import telefone
		>>> telefone.validate("(11) 98765-4321")
		True
		>>> telefone.format("11987654321")
		"(11) 98765-4321"
		>>> telefone.get_tipo("11987654321")
		"celular"
		>>> telefone.is_celular("(11) 98765-4321")
		True
	"""
	
	DDDS_VALIDOS: List[str] = [
		"11", "12", "13", "14", "15", "16", "17", "18", "19",  # São Paulo
		"21", "22", "24",  # Rio de Janeiro
		"27", "28",  # Espírito Santo
		"31", "32", "33", "34", "35", "37", "38",  # Minas Gerais
		"41", "42", "43", "44", "45", "46",  # Paraná
		"47", "48", "49",  # Santa Catarina
		"51", "53", "54", "55",  # Rio Grande do Sul
		"61",  # Distrito Federal
		"62", "64",  # Goiás
		"63",  # Tocantins
		"65", "66",  # Mato Grosso
		"67",  # Mato Grosso do Sul
		"68",  # Acre
		"69",  # Rondônia
		"71", "73", "74", "75", "77",  # Bahia
		"79",  # Sergipe
		"81", "87",  # Pernambuco
		"82",  # Alagoas
		"83",  # Paraíba
		"84",  # Rio Grande do Norte
		"85", "88",  # Ceará
		"86", "89",  # Piauí
		"91", "93", "94",  # Pará
		"92", "97",  # Amazonas
		"95",  # Roraima
		"96",  # Amapá
		"98", "99",  # Maranhão
	]
	
	def validate(self, value: str, raise_error: bool = False) -> bool:
		"""Valida um número de telefone brasileiro.
		
		Verifica se o telefone fornecido é válido de acordo com as regras:
		- Deve ter 10 dígitos (fixo) ou 11 dígitos (celular)
		- DDD deve ser válido
		- Celular deve começar com 9
		- Fixo não pode começar com 9
		
		Args:
			value: Telefone a ser validado (aceita com ou sem formatação).
			raise_error: Se True, levanta InvalidTelefone ao invés de retornar False.
						
		Returns:
			True se o telefone é válido, False caso contrário.
			
		Raises:
			InvalidTelefone: Se raise_error=True e o telefone for inválido.
			
		Examples:
			>>> telefone.validate("(11) 98765-4321")
			True
			>>> telefone.validate("11987654321")
			True
			>>> telefone.validate("(11) 3456-7890")
			True
			>>> telefone.validate("1134567890")
			True
			>>> telefone.validate("(00) 98765-4321", raise_error=True)
			Traceback (most recent call last):
			...
			InvalidTelefone: DDD inválido: 00
		"""
		try:
			cleaned = self.clean(value)
			
			if len(cleaned) not in [10, 11]:
				raise InvalidTelefone(
					f"Telefone deve ter 10 (fixo) ou 11 (celular) dígitos, "
					f"recebido: {len(cleaned)}"
				)
			
			ddd = cleaned[:2]
			if ddd not in self.DDDS_VALIDOS:
				raise InvalidTelefone(f"DDD inválido: {ddd}")
			
			if len(cleaned) == 11:
				if cleaned[2] != "9":
					raise InvalidTelefone(
						"Celular deve começar com 9 após o DDD"
					)
			elif len(cleaned) == 10:
				if cleaned[2] == "9":
					raise InvalidTelefone(
						"Telefone fixo não pode começar com 9"
					)
			
			return True
			
		except InvalidTelefone:
			if raise_error:
				raise
			return False
	
	def format(self, value: str) -> str:
		"""Formata um telefone no padrão brasileiro.
		
		- Fixo: (XX) XXXX-XXXX
		- Celular: (XX) 9XXXX-XXXX
		
		Args:
			value: Telefone a ser formatado (com ou sem formatação prévia).
			
		Returns:
			Telefone formatado com parênteses, espaço e hífen.
			
		Raises:
			InvalidTelefone: Se o telefone não tiver 10 ou 11 dígitos.
			
		Examples:
			>>> telefone.format("11987654321")
			"(11) 98765-4321"
			>>> telefone.format("1134567890")
			"(11) 3456-7890"
			>>> telefone.format("(11) 98765-4321")
			"(11) 98765-4321"
		"""
		cleaned = self.clean(value)
		
		if len(cleaned) not in [10, 11]:
			raise InvalidTelefone(
				f"Telefone deve ter 10 ou 11 dígitos para formatação"
			)
		
		ddd = cleaned[:2]
		
		if len(cleaned) == 11:
			numero = cleaned[2:]
			return f"({ddd}) {numero[:5]}-{numero[5:]}"
		else:
			numero = cleaned[2:]
			return f"({ddd}) {numero[:4]}-{numero[4:]}"
	
	def clean(self, value: str) -> str:
		"""Remove toda formatação do telefone, mantendo apenas dígitos.
		
		Args:
			value: Telefone formatado ou não formatado.
			
		Returns:
			Telefone contendo apenas dígitos.
			
		Examples:
			>>> telefone.clean("(11) 98765-4321")
			"11987654321"
			>>> telefone.clean("11987654321")
			"11987654321"
		"""
		return self._only_digits(value)
	
	def generate(
		self, 
		tipo: TipoTelefone = "celular",
		ddd: str = "11",
		formatted: bool = True
	) -> str:
		"""Gera um número de telefone válido aleatório.
		
		Args:
			tipo: Tipo de telefone ("fixo" ou "celular").
			ddd: DDD desejado (padrão: "11" - São Paulo).
			formatted: Se True, retorna formatado.
					  
		Returns:
			Telefone válido gerado aleatoriamente.
			
		Raises:
			InvalidTelefone: Se o DDD for inválido ou tipo não for "fixo" ou "celular".
			
		Examples:
			>>> tel = telefone.generate(tipo="celular", ddd="11")
			>>> telefone.validate(tel)
			True
			>>> tel = telefone.generate(tipo="fixo", ddd="21")
			>>> telefone.is_fixo(tel)
			True
		"""
		if ddd not in self.DDDS_VALIDOS:
			raise InvalidTelefone(f"DDD inválido: {ddd}")
		
		if tipo not in ["fixo", "celular"]:
			raise InvalidTelefone(f"Tipo deve ser 'fixo' ou 'celular', recebido: {tipo}")
		
		if tipo == "celular":
			primeiro_digito = "9"
			qtd_digitos = 8
		else:
			primeiro_digito = str(random.randint(2, 5))
			qtd_digitos = 7
		
		numero = primeiro_digito + "".join(
			str(random.randint(0, 9)) for _ in range(qtd_digitos)
		)
		
		telefone_completo = ddd + numero
		
		return self.format(telefone_completo) if formatted else telefone_completo
	
	def get_tipo(self, value: str) -> TipoTelefone:
		"""Identifica o tipo de telefone (fixo ou celular).
		
		Args:
			value: Telefone a ser identificado (com ou sem formatação).
			
		Returns:
			"celular" se for celular, "fixo" se for fixo.
			
		Raises:
			InvalidTelefone: Se o telefone for inválido.
			
		Examples:
			>>> telefone.get_tipo("(11) 98765-4321")
			"celular"
			>>> telefone.get_tipo("(11) 3456-7890")
			"fixo"
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidTelefone(f"Telefone inválido: {value}")
		
		return "celular" if len(cleaned) == 11 else "fixo"
	
	def get_ddd(self, value: str) -> str:
		"""Retorna o DDD do telefone.
		
		Args:
			value: Telefone a ser analisado (com ou sem formatação).
			
		Returns:
			DDD do telefone (2 dígitos).
			
		Raises:
			InvalidTelefone: Se o telefone for inválido.
			
		Examples:
			>>> telefone.get_ddd("(11) 98765-4321")
			"11"
			>>> telefone.get_ddd("21987654321")
			"21"
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidTelefone(f"Telefone inválido: {value}")
		
		return cleaned[:2]
	
	def is_celular(self, value: str) -> bool:
		"""Verifica se o telefone é celular.
		
		Args:
			value: Telefone a ser verificado (com ou sem formatação).
			
		Returns:
			True se for celular, False se for fixo.
			
		Raises:
			InvalidTelefone: Se o telefone for inválido.
			
		Examples:
			>>> telefone.is_celular("(11) 98765-4321")
			True
			>>> telefone.is_celular("(11) 3456-7890")
			False
		"""
		return self.get_tipo(value) == "celular"
	
	def is_fixo(self, value: str) -> bool:
		"""Verifica se o telefone é fixo.
		
		Args:
			value: Telefone a ser verificado (com ou sem formatação).
			
		Returns:
			True se for fixo, False se for celular.
			
		Raises:
			InvalidTelefone: Se o telefone for inválido.
			
		Examples:
			>>> telefone.is_fixo("(11) 3456-7890")
			True
			>>> telefone.is_fixo("(11) 98765-4321")
			False
		"""
		return self.get_tipo(value) == "fixo"
	
	def get_estado_por_ddd(self, ddd: str) -> str:
		"""Retorna a sigla do estado baseado no DDD.
		
		Args:
			ddd: DDD a ser consultado (2 dígitos).
			
		Returns:
			Sigla do estado (UF).
			
		Raises:
			InvalidTelefone: Se o DDD for inválido.
			
		Examples:
			>>> telefone.get_estado_por_ddd("11")
			"SP"
			>>> telefone.get_estado_por_ddd("21")
			"RJ"
			>>> telefone.get_estado_por_ddd("85")
			"CE"
		"""
		mapa_ddd_uf = {
			"11": "SP", "12": "SP", "13": "SP", "14": "SP", "15": "SP",
			"16": "SP", "17": "SP", "18": "SP", "19": "SP",
			"21": "RJ", "22": "RJ", "24": "RJ",
			"27": "ES", "28": "ES",
			"31": "MG", "32": "MG", "33": "MG", "34": "MG", "35": "MG",
			"37": "MG", "38": "MG",
			"41": "PR", "42": "PR", "43": "PR", "44": "PR", "45": "PR", "46": "PR",
			"47": "SC", "48": "SC", "49": "SC",
			"51": "RS", "53": "RS", "54": "RS", "55": "RS",
			"61": "DF",
			"62": "GO", "64": "GO",
			"63": "TO",
			"65": "MT", "66": "MT",
			"67": "MS",
			"68": "AC",
			"69": "RO",
			"71": "BA", "73": "BA", "74": "BA", "75": "BA", "77": "BA",
			"79": "SE",
			"81": "PE", "87": "PE",
			"82": "AL",
			"83": "PB",
			"84": "RN",
			"85": "CE", "88": "CE",
			"86": "PI", "89": "PI",
			"91": "PA", "93": "PA", "94": "PA",
			"92": "AM", "97": "AM",
			"95": "RR",
			"96": "AP",
			"98": "MA", "99": "MA",
		}
		
		if ddd not in mapa_ddd_uf:
			raise InvalidTelefone(f"DDD inválido: {ddd}")
		
		return mapa_ddd_uf[ddd]


telefone: TelefoneValidator = TelefoneValidator()