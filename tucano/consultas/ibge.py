"""Consulta de dados do IBGE para estados e municípios."""

from typing import Dict, Any, List, Optional
from ..core.http import http_client
from ..core.exceptions import InvalidUF


class IBGEConsulta:
    """Consulta de dados geográficos do IBGE através de APIs públicas.
    
    Utiliza BrasilAPI para obter listas de estados (UFs) e municípios.
    
    Attributes:
        BRASILAPI_UF_URL: URL base para estados.
        BRASILAPI_MUNICIPIOS_URL: URL base para municípios por UF.
        
    Examples:
        >>> from tucano.consultas import ibge
        >>> estados = ibge.listar_estados()
        >>> len(estados)
        27
        >>> municipios_sp = ibge.listar_municipios("SP")
        >>> "São Paulo" in [m["nome"] for m in municipios_sp]
        True
    """
    
    BRASILAPI_UF_URL: str = "https://brasilapi.com.br/api/ibge/uf/v1"
    BRASILAPI_MUNICIPIOS_URL: str = "https://brasilapi.com.br/api/ibge/municipios/v1/{}"
    
    UFS_VALIDAS: List[str] = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
        'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
        'SP', 'SE', 'TO'
    ]
    
    def listar_estados(self, timeout: int = 10) -> List[Dict[str, Any]]:
        """Lista todos os estados (UFs) do Brasil.
        
        Args:
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de dicionários com informações dos estados, contendo:
            - id: ID do estado
            - sigla: Sigla (ex: "SP")
            - nome: Nome do estado (ex: "São Paulo")
            - regiao: Dicionário com informações da região
            
        Examples:
            >>> from tucano.consultas import ibge
            >>> estados = ibge.listar_estados()
            >>> len(estados)
            27
            >>> estados[0]["nome"]
            "Rondônia"
        """
        data = http_client.get(self.BRASILAPI_UF_URL)
        return data
    
    def listar_municipios(
        self,
        uf: str,
        timeout: int = 10
    ) -> List[Dict[str, Any]]:
        """Lista todos os municípios de um estado (UF).
        
        Args:
            uf: Sigla do estado (ex: "SP").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de dicionários com informações dos municípios, contendo:
            - nome: Nome do município
            - codigo_ibge: Código IBGE do município
            
        Raises:
            InvalidUF: Se a sigla do estado for inválida.
            
        Examples:
            >>> from tucano.consultas import ibge
            >>> municipios = ibge.listar_municipios("SP")
            >>> len(municipios) > 600
            True
        """
        uf_upper = uf.upper()
        
        if uf_upper not in self.UFS_VALIDAS:
            raise InvalidUF(f"Sigla de UF inválida: {uf}")
        
        data = http_client.get(self.BRASILAPI_MUNICIPIOS_URL.format(uf_upper))
        return data
    
    def buscar_estado_por_sigla(self, sigla: str) -> Optional[Dict[str, Any]]:
        """Busca um estado específico pela sua sigla.
        
        Args:
            sigla: Sigla do estado (ex: "SP").
            
        Returns:
            Dicionário com informações do estado, ou None se não encontrado.
            
        Examples:
            >>> from tucano.consultas import ibge
            >>> sp = ibge.buscar_estado_por_sigla("SP")
            >>> sp["nome"]
            "São Paulo"
        """
        sigla_upper = sigla.upper()
        
        if sigla_upper not in self.UFS_VALIDAS:
            return None
        
        estados = self.listar_estados()
        
        for estado in estados:
            if estado.get("sigla") == sigla_upper:
                return estado
        
        return None
    
    def buscar_municipio_por_nome(
        self,
        nome: str,
        uf: str
    ) -> List[Dict[str, Any]]:
        """Busca municípios por nome dentro de um estado.
        
        A busca é case-insensitive e parcial.
        
        Args:
            nome: Nome ou parte do nome do município.
            uf: Sigla do estado onde a busca será realizada.
            
        Returns:
            Lista de municípios que correspondem à busca.
            
        Raises:
            InvalidUF: Se a sigla do estado for inválida.
            
        Examples:
            >>> from tucano.consultas import ibge
            >>> resultados = ibge.buscar_municipio_por_nome("Campinas", "SP")
            >>> len(resultados)
            1
            >>> resultados[0]["nome"]
            "Campinas"
        """
        municipios = self.listar_municipios(uf)
        nome_lower = nome.lower()
        
        return [
            municipio for municipio in municipios
            if nome_lower in municipio.get("nome", "").lower()
        ]


ibge: IBGEConsulta = IBGEConsulta()