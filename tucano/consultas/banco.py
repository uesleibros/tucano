"""Consulta de informações de bancos brasileiros."""

from typing import Dict, Any, List, Optional
from ..core.http import http_client


class BancoConsulta:
    """Consulta informações de bancos brasileiros por código.
    
    Utiliza BrasilAPI para obter dados dos bancos.
    
    Attributes:
        BRASILAPI_URL: URL base da API BrasilAPI.
        
    Examples:
        >>> from tucano.consultas import banco
        >>> bb = banco.consultar("001")
        >>> print(bb["name"])
        "Banco do Brasil S.A."
    """
    
    BRASILAPI_BANCOS_URL: str = "https://brasilapi.com.br/api/banks/v1"
    BRASILAPI_BANCO_URL: str = "https://brasilapi.com.br/api/banks/v1/{}"
    
    def consultar(self, codigo: str, timeout: int = 10) -> Dict[str, Any]:
        """Consulta informações de um banco por código.
        
        Args:
            codigo: Código do banco (3 dígitos, com ou sem zeros à esquerda).
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Dicionário com informações do banco contendo:
            - ispb: Código ISPB
            - name: Nome do banco
            - code: Código do banco (número)
            - fullName: Nome completo
            
        Examples:
            >>> from tucano.consultas import banco
            >>> bb = banco.consultar("001")
            >>> bb["name"]
            "Banco do Brasil S.A."
            >>> bb["code"]
            1
        """
        # Garantir 3 dígitos
        codigo_formatado = str(int(codigo)).zfill(3)
        
        data = http_client.get(
            self.BRASILAPI_BANCO_URL.format(codigo_formatado),
        )
        
        return {
            "ispb": data.get("ispb", ""),
            "name": data.get("name", ""),
            "code": data.get("code"),
            "fullName": data.get("fullName", ""),
            "codigo": codigo_formatado
        }
    
    def listar_todos(self, timeout: int = 10) -> List[Dict[str, Any]]:
        """Lista todos os bancos brasileiros.
        
        Args:
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de dicionários com informações dos bancos.
            
        Examples:
            >>> from tucano.consultas import banco
            >>> bancos = banco.listar_todos()
            >>> len(bancos) > 100
            True
        """
        data = http_client.get(self.BRASILAPI_BANCOS_URL)
        return data
    
    def buscar_por_nome(self, nome: str) -> List[Dict[str, Any]]:
        """Busca bancos por nome (parcial).
        
        Args:
            nome: Nome ou parte do nome do banco.
            
        Returns:
            Lista de bancos que correspondem à busca.
            
        Examples:
            >>> from tucano.consultas import banco
            >>> resultados = banco.buscar_por_nome("Brasil")
            >>> len(resultados) > 0
            True
        """
        todos = self.listar_todos()
        nome_lower = nome.lower()
        
        return [
            banco for banco in todos
            if nome_lower in banco.get("name", "").lower() or
               nome_lower in banco.get("fullName", "").lower()
        ]


banco: BancoConsulta = BancoConsulta()