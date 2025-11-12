"""Classe base abstrata para todos os validadores do Tucano."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseValidator(ABC, Generic[T]):
	"""Classe base abstrata para implementação de validadores.
	
	Esta classe define a interface que todos os validadores devem implementar.
	Fornece métodos abstratos para validação, formatação, limpeza e geração
	de dados, além de métodos utilitários comuns.
	
	Type Parameters:
		T: Tipo do valor retornado pelos métodos do validador.
		
	Examples:
		>>> class MeuValidator(BaseValidator[str]):
		...     def validate(self, value: str, raise_error: bool = False) -> bool:
		...         return len(value) > 0
		...     
		...     def format(self, value: str) -> str:
		...         return value.upper()
		...     
		...     def clean(self, value: str) -> str:
		...         return value.strip()
	"""
	
	@abstractmethod
	def validate(self, value: str, raise_error: bool = False) -> bool:
		"""Valida o valor fornecido.
		
		Args:
			value: Valor a ser validado.
			raise_error: Se True, levanta exceção em caso de validação falhar.
						Se False, retorna False silenciosamente.
						
		Returns:
			True se o valor é válido, False caso contrário.
			
		Raises:
			ValidationError: Se raise_error=True e a validação falhar.
		"""
		pass
	
	@abstractmethod
	def format(self, value: str) -> str:
		"""Formata o valor de acordo com o padrão esperado.
		
		Args:
			value: Valor a ser formatado (pode estar com ou sem formatação).
			
		Returns:
			Valor formatado de acordo com o padrão brasileiro.
			
		Raises:
			ValidationError: Se o valor não puder ser formatado.
		"""
		pass
	
	@abstractmethod
	def clean(self, value: str) -> str:
		"""Remove toda formatação do valor, mantendo apenas dados puros.
		
		Args:
			value: Valor formatado ou parcialmente formatado.
			
		Returns:
			Valor sem nenhuma formatação (geralmente apenas dígitos).
		"""
		pass
	
	def _only_digits(self, value: str) -> str:
		"""Extrai apenas os dígitos numéricos de uma string.
		
		Método utilitário que remove todos os caracteres não numéricos,
		mantendo apenas dígitos de 0-9.
		
		Args:
			value: String que pode conter letras, pontos, hífens, etc.
			
		Returns:
			String contendo apenas os dígitos presentes no valor original.
			
		Examples:
			>>> validator._only_digits("123.456.789-09")
			"12345678909"
			>>> validator._only_digits("(11) 98765-4321")
			"11987654321"
			>>> validator._only_digits("ABC123XYZ")
			"123"
		"""
		return "".join(filter(str.isdigit, value))