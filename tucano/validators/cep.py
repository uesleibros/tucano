"""Validador de CEP (Código de Endereçamento Postal) com consulta de endereço."""

import re
from typing import Dict, Optional, Any
import httpx
from ..core.base import BaseValidator
from ..core.exceptions import InvalidCEP, CEPNotFound, CEPAPIError


class CEPValidator(BaseValidator[str]):
	"""Validador de CEP com suporte a consulta de endereço.
	
	O CEP (Código de Endereçamento Postal) é composto por 8 dígitos numéricos.
	Esta classe permite validar, formatar e consultar endereços via API ViaCEP.
	
	Formato padrão: XXXXX-XXX
	
	Attributes:
		VIACEP_URL: URL base da API ViaCEP.
		BRASILAPI_URL: URL base da API BrasilAPI (fallback).
		
	Examples:
		>>> from tucano import cep
		>>> cep.validate("01310-100")
		True
		>>> cep.format("01310100")
		"01310-100"
		>>> endereco = cep.consultar("01310-100")
		>>> endereco["logradouro"]
		"Avenida Paulista"
	"""
	
	VIACEP_URL: str = "https://viacep.com.br/ws/{}/json/"
	BRASILAPI_URL: str = "https://brasilapi.com.br/api/cep/v1/{}"
	
	def validate(self, value: str, raise_error: bool = False) -> bool:
		"""Valida um CEP brasileiro.
		
		Verifica se o CEP fornecido é válido de acordo com as regras:
		- Deve ter exatamente 8 dígitos
		- Não pode ser composto apenas por zeros
		
		Args:
			value: CEP a ser validado (aceita com ou sem formatação).
			raise_error: Se True, levanta InvalidCEP ao invés de retornar False.
						
		Returns:
			True se o CEP é válido, False caso contrário.
			
		Raises:
			InvalidCEP: Se raise_error=True e o CEP for inválido.
			
		Examples:
			>>> cep.validate("01310-100")
			True
			>>> cep.validate("01310100")
			True
			>>> cep.validate("00000-000")
			False
			>>> cep.validate("123", raise_error=True)
			Traceback (most recent call last):
			...
			InvalidCEP: CEP deve ter 8 dígitos, recebido: 3
		"""
		try:
			cleaned = self.clean(value)
			
			if len(cleaned) != 8:
				raise InvalidCEP(f"CEP deve ter 8 dígitos, recebido: {len(cleaned)}")
			
			if cleaned == "00000000":
				raise InvalidCEP("CEP inválido: não pode ser composto apenas por zeros")
			
			return True
			
		except InvalidCEP:
			if raise_error:
				raise
			return False
	
	def format(self, value: str) -> str:
		"""Formata um CEP no padrão brasileiro XXXXX-XXX.
		
		Args:
			value: CEP a ser formatado (com ou sem formatação prévia).
			
		Returns:
			CEP formatado com hífen.
			
		Raises:
			InvalidCEP: Se o CEP não tiver exatamente 8 dígitos.
			
		Examples:
			>>> cep.format("01310100")
			"01310-100"
			>>> cep.format("01310-100")
			"01310-100"
		"""
		cleaned = self.clean(value)
		
		if len(cleaned) != 8:
			raise InvalidCEP(f"CEP deve ter 8 dígitos para formatação")
		
		return f"{cleaned[:5]}-{cleaned[5:]}"
	
	def clean(self, value: str) -> str:
		"""Remove toda formatação do CEP, mantendo apenas dígitos.
		
		Args:
			value: CEP formatado ou não formatado.
			
		Returns:
			CEP contendo apenas os 8 dígitos numéricos.
			
		Examples:
			>>> cep.clean("01310-100")
			"01310100"
			>>> cep.clean("01310100")
			"01310100"
		"""
		return self._only_digits(value)
	
	def consultar(
		self, 
		value: str, 
		timeout: int = 10,
		use_fallback: bool = True
	) -> Dict[str, Any]:
		"""Consulta informações de endereço para um CEP via API ViaCEP.
		
		Realiza uma requisição HTTP síncrona para obter dados do endereço.
		Se a API principal falhar e use_fallback=True, tenta a BrasilAPI.
		
		Args:
			value: CEP a ser consultado (com ou sem formatação).
			timeout: Tempo máximo de espera em segundos.
			use_fallback: Se True, tenta BrasilAPI em caso de falha do ViaCEP.
			
		Returns:
			Dicionário com informações do endereço contendo:
			- cep: CEP formatado
			- logradouro: Nome da rua/avenida
			- complemento: Complemento do endereço
			- bairro: Nome do bairro
			- localidade: Nome da cidade
			- uf: Sigla do estado (2 letras)
			- ibge: Código IBGE do município
			- gia: Código GIA (SP)
			- ddd: Código DDD
			- siafi: Código SIAFI
			
		Raises:
			InvalidCEP: Se o CEP for inválido.
			CEPNotFound: Se o CEP não for encontrado na base de dados.
			CEPAPIError: Se houver erro na comunicação com a API.
			
		Examples:
			>>> endereco = cep.consultar("01310-100")
			>>> endereco["logradouro"]
			"Avenida Paulista"
			>>> endereco["localidade"]
			"São Paulo"
			>>> endereco["uf"]
			"SP"
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidCEP(f"CEP inválido: {value}")
		
		try:
			response = httpx.get(
				self.VIACEP_URL.format(cleaned),
				timeout=timeout,
				follow_redirects=True
			)
			response.raise_for_status()
			data = response.json()
			
			if data.get("erro"):
				raise CEPNotFound(f"CEP não encontrado: {value}")
			
			return data
			
		except httpx.HTTPStatusError as e:
			if use_fallback:
				return self._consultar_fallback(cleaned, timeout)
			raise CEPAPIError(f"Erro HTTP ao consultar CEP: {e.response.status_code}")
			
		except httpx.RequestError as e:
			if use_fallback:
				return self._consultar_fallback(cleaned, timeout)
			raise CEPAPIError(f"Erro de conexão ao consultar CEP: {str(e)}")
			
		except (KeyError, ValueError) as e:
			raise CEPAPIError(f"Erro ao processar resposta da API: {str(e)}")
	
	def _consultar_fallback(self, cep_limpo: str, timeout: int) -> Dict[str, Any]:
		"""Consulta CEP usando API alternativa (BrasilAPI).
		
		Args:
			cep_limpo: CEP sem formatação (8 dígitos).
			timeout: Tempo máximo de espera em segundos.
			
		Returns:
			Dicionário com informações do endereço.
			
		Raises:
			CEPNotFound: Se o CEP não for encontrado.
			CEPAPIError: Se houver erro na comunicação.
		"""
		try:
			response = httpx.get(
				self.BRASILAPI_URL.format(cep_limpo),
				timeout=timeout,
				follow_redirects=True
			)
			response.raise_for_status()
			data = response.json()
			
			return {
				"cep": data.get("cep", ""),
				"logradouro": data.get("street", ""),
				"complemento": "",
				"bairro": data.get("neighborhood", ""),
				"localidade": data.get("city", ""),
				"uf": data.get("state", ""),
				"ibge": "",
				"gia": "",
				"ddd": "",
				"siafi": "",
			}
			
		except httpx.HTTPStatusError as e:
			if e.response.status_code == 404:
				raise CEPNotFound(f"CEP não encontrado: {cep_limpo}")
			raise CEPAPIError(f"Erro HTTP na API alternativa: {e.response.status_code}")
			
		except httpx.RequestError as e:
			raise CEPAPIError(f"Erro de conexão na API alternativa: {str(e)}")
			
		except (KeyError, ValueError) as e:
			raise CEPAPIError(f"Erro ao processar resposta da API alternativa: {str(e)}")
	
	async def consultar_async(
		self, 
		value: str, 
		timeout: int = 10,
		use_fallback: bool = True
	) -> Dict[str, Any]:
		"""Consulta informações de endereço para um CEP de forma assíncrona.
		
		Versão assíncrona da consulta de CEP, útil para aplicações async/await.
		
		Args:
			value: CEP a ser consultado (com ou sem formatação).
			timeout: Tempo máximo de espera em segundos.
			use_fallback: Se True, tenta BrasilAPI em caso de falha do ViaCEP.
			
		Returns:
			Dicionário com informações do endereço (mesma estrutura do consultar()).
			
		Raises:
			InvalidCEP: Se o CEP for inválido.
			CEPNotFound: Se o CEP não for encontrado na base de dados.
			CEPAPIError: Se houver erro na comunicação com a API.
			
		Examples:
			>>> import asyncio
			>>> async def main():
			...     endereco = await cep.consultar_async("01310-100")
			...     print(endereco["logradouro"])
			>>> asyncio.run(main())
			"Avenida Paulista"
		"""
		cleaned = self.clean(value)
		
		if not self.validate(cleaned, raise_error=True):
			raise InvalidCEP(f"CEP inválido: {value}")
		
		async with httpx.AsyncClient() as client:
			try:
				response = await client.get(
					self.VIACEP_URL.format(cleaned),
					timeout=timeout,
					follow_redirects=True
				)
				response.raise_for_status()
				data = response.json()
				
				if data.get("erro"):
					raise CEPNotFound(f"CEP não encontrado: {value}")
				
				return data
				
			except httpx.HTTPStatusError as e:
				if use_fallback:
					return await self._consultar_fallback_async(cleaned, timeout, client)
				raise CEPAPIError(f"Erro HTTP ao consultar CEP: {e.response.status_code}")
				
			except httpx.RequestError as e:
				if use_fallback:
					return await self._consultar_fallback_async(cleaned, timeout, client)
				raise CEPAPIError(f"Erro de conexão ao consultar CEP: {str(e)}")
				
			except (KeyError, ValueError) as e:
				raise CEPAPIError(f"Erro ao processar resposta da API: {str(e)}")
	
	async def _consultar_fallback_async(
		self, 
		cep_limpo: str, 
		timeout: int,
		client: httpx.AsyncClient
	) -> Dict[str, Any]:
		"""Consulta CEP usando API alternativa de forma assíncrona.
		
		Args:
			cep_limpo: CEP sem formatação (8 dígitos).
			timeout: Tempo máximo de espera em segundos.
			client: Cliente HTTP assíncrono.
			
		Returns:
			Dicionário com informações do endereço.
			
		Raises:
			CEPNotFound: Se o CEP não for encontrado.
			CEPAPIError: Se houver erro na comunicação.
		"""
		try:
			response = await client.get(
				self.BRASILAPI_URL.format(cep_limpo),
				timeout=timeout,
				follow_redirects=True
			)
			response.raise_for_status()
			data = response.json()
			
			return {
				"cep": data.get("cep", ""),
				"logradouro": data.get("street", ""),
				"complemento": "",
				"bairro": data.get("neighborhood", ""),
				"localidade": data.get("city", ""),
				"uf": data.get("state", ""),
				"ibge": "",
				"gia": "",
				"ddd": "",
				"siafi": "",
			}
			
		except httpx.HTTPStatusError as e:
			if e.response.status_code == 404:
				raise CEPNotFound(f"CEP não encontrado: {cep_limpo}")
			raise CEPAPIError(f"Erro HTTP na API alternativa: {e.response.status_code}")
			
		except httpx.RequestError as e:
			raise CEPAPIError(f"Erro de conexão na API alternativa: {str(e)}")
			
		except (KeyError, ValueError) as e:
			raise CEPAPIError(f"Erro ao processar resposta da API alternativa: {str(e)}")


cep: CEPValidator = CEPValidator()