"""Consulta de endereços por CEP em APIs externas."""

from typing import Dict, Any
from ..core.http import http_client
from ..core.exceptions import InvalidCEP, CEPNotFound, CEPAPIError
from ..validators.cep import cep as cep_validator


class CEPConsulta:
    """Consulta de endereço por CEP via APIs públicas.
    
    Utiliza ViaCEP como API principal e BrasilAPI como fallback.
    
    Attributes:
        VIACEP_URL: URL base da API ViaCEP.
        BRASILAPI_URL: URL base da API BrasilAPI.
        
    Examples:
        >>> from tucano.consultas import cep
        >>> endereco = cep.consultar("01310-100")
        >>> print(endereco["logradouro"])
        "Avenida Paulista"
    """
    
    VIACEP_URL: str = "https://viacep.com.br/ws/{}/json/"
    BRASILAPI_URL: str = "https://brasilapi.com.br/api/cep/v1/{}"
    
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
            >>> from tucano.consultas import cep
            >>> endereco = cep.consultar("01310-100")
            >>> endereco["logradouro"]
            "Avenida Paulista"
            >>> endereco["localidade"]
            "São Paulo"
        """
        cleaned = cep_validator.clean(value)
        
        if not cep_validator.validate(cleaned, raise_error=True):
            raise InvalidCEP(f"CEP inválido: {value}")
        
        try:
            data = http_client.get(
                self.VIACEP_URL.format(cleaned),
            )
            
            if data.get("erro"):
                raise CEPNotFound(f"CEP não encontrado: {value}")
            
            return data
            
        except Exception as e:
            if use_fallback and not isinstance(e, CEPNotFound):
                return self._consultar_fallback(cleaned)
            
            if isinstance(e, (CEPNotFound, InvalidCEP)):
                raise
            
            raise CEPAPIError(f"Erro ao consultar CEP: {str(e)}")
    
    def _consultar_fallback(self, cep_limpo: str) -> Dict[str, Any]:
        """Consulta CEP usando API alternativa (BrasilAPI).
        
        Args:
            cep_limpo: CEP sem formatação (8 dígitos).
            
        Returns:
            Dicionário com informações do endereço.
            
        Raises:
            CEPNotFound: Se o CEP não for encontrado.
            CEPAPIError: Se houver erro na comunicação.
        """
        try:
            data = http_client.get(self.BRASILAPI_URL.format(cep_limpo))
            
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
            
        except Exception as e:
            raise CEPAPIError(f"Erro na API alternativa: {str(e)}")
    
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
            >>> from tucano.consultas import cep
            >>> async def main():
            ...     endereco = await cep.consultar_async("01310-100")
            ...     print(endereco["logradouro"])
            >>> asyncio.run(main())
            "Avenida Paulista"
        """
        cleaned = cep_validator.clean(value)
        
        if not cep_validator.validate(cleaned, raise_error=True):
            raise InvalidCEP(f"CEP inválido: {value}")
        
        try:
            data = await http_client.get_async(
                self.VIACEP_URL.format(cleaned)
            )
            
            if data.get("erro"):
                raise CEPNotFound(f"CEP não encontrado: {value}")
            
            return data
            
        except Exception as e:
            if use_fallback and not isinstance(e, CEPNotFound):
                return await self._consultar_fallback_async(cleaned)
            
            if isinstance(e, (CEPNotFound, InvalidCEP)):
                raise
            
            raise CEPAPIError(f"Erro ao consultar CEP: {str(e)}")
    
    async def _consultar_fallback_async(self, cep_limpo: str) -> Dict[str, Any]:
        """Consulta CEP usando API alternativa de forma assíncrona.
        
        Args:
            cep_limpo: CEP sem formatação (8 dígitos).
            
        Returns:
            Dicionário com informações do endereço.
            
        Raises:
            CEPNotFound: Se o CEP não for encontrado.
            CEPAPIError: Se houver erro na comunicação.
        """
        try:
            data = await http_client.get_async(self.BRASILAPI_URL.format(cep_limpo))
            
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
            
        except Exception as e:
            raise CEPAPIError(f"Erro na API alternativa: {str(e)}")


# Instância singleton
cep: CEPConsulta = CEPConsulta()