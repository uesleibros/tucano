"""Consulta de informações de DDD."""

from typing import Dict, Any
from ..core.http import http_client


class DDDConsulta:
    """Consulta informações de DDD (código de área).
    
    Utiliza BrasilAPI para obter cidades por DDD.
    
    Attributes:
        BRASILAPI_URL: URL base da API BrasilAPI.
        
    Examples:
        >>> from tucano.consultas import ddd
        >>> info = ddd.consultar("11")
        >>> info["state"]
        "SP"
    """
    
    BRASILAPI_URL: str = "https://brasilapi.com.br/api/ddd/v1/{}"
    
    def consultar(self, codigo_ddd: str, timeout: int = 10) -> Dict[str, Any]:
        """Consulta informações de um DDD.
        
        Args:
            codigo_ddd: Código DDD (2 dígitos).
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Dicionário com estado e cidades do DDD.
            
        Examples:
            >>> from tucano.consultas import ddd
            >>> info = ddd.consultar("11")
            >>> info["state"]
            "SP"
            >>> "São Paulo" in info["cities"]
            True
        """
        data = http_client.get(self.BRASILAPI_URL.format(codigo_ddd))
        return {
            "state": data.get("state", ""),
            "cities": data.get("cities", [])
        }


ddd: DDDConsulta = DDDConsulta()