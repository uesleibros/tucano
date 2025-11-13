"""Consulta de preços de veículos na Tabela FIPE."""

from typing import Dict, Any, List, Optional
from ..core.http import http_client


class FIPEConsulta:
    """Consulta preços de veículos na Tabela FIPE.
    
    Utiliza BrasilAPI e Parallelum FIPE API para obter dados da tabela FIPE.
    
    Attributes:
        BRASILAPI_URL: URL base da BrasilAPI.
        PARALLELUM_URL: URL base da Parallelum FIPE API.
        
    Examples:
        >>> from tucano.consultas import fipe
        >>> marcas = fipe.listar_marcas()
        >>> len(marcas) > 0
        True
    """
    
    BRASILAPI_URL: str = "https://brasilapi.com.br/api/fipe/preco/v1"
    PARALLELUM_URL: str = "https://parallelum.com.br/fipe/api/v1"
    
    def listar_marcas(
        self, 
        tipo_veiculo: str = "carros",
        timeout: int = 10
    ) -> List[Dict[str, Any]]:
        """Lista todas as marcas de veículos.
        
        Args:
            tipo_veiculo: Tipo do veículo ("carros", "motos" ou "caminhoes").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de marcas com nome e código.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> marcas = fipe.listar_marcas("carros")
            >>> len(marcas) > 0
            True
        """
        url = f"{self.PARALLELUM_URL}/{tipo_veiculo}/marcas"
        data = http_client.get(url)
        return data
    
    def listar_modelos(
        self, 
        codigo_marca: str,
        tipo_veiculo: str = "carros",
        timeout: int = 10
    ) -> Dict[str, Any]:
        """Lista modelos de uma marca específica.
        
        Args:
            codigo_marca: Código da marca.
            tipo_veiculo: Tipo do veículo ("carros", "motos" ou "caminhoes").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Dicionário com anos e modelos da marca.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> modelos = fipe.listar_modelos("59")  # Fiat
            >>> len(modelos["modelos"]) > 0
            True
        """
        url = f"{self.PARALLELUM_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos"
        data = http_client.get(url)
        return data
    
    def listar_anos(
        self,
        codigo_marca: str,
        codigo_modelo: str,
        tipo_veiculo: str = "carros",
        timeout: int = 10
    ) -> List[Dict[str, Any]]:
        """Lista anos disponíveis de um modelo específico.
        
        Args:
            codigo_marca: Código da marca.
            codigo_modelo: Código do modelo.
            tipo_veiculo: Tipo do veículo ("carros", "motos" ou "caminhoes").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de anos disponíveis.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> anos = fipe.listar_anos("59", "5940")
            >>> len(anos) > 0
            True
        """
        url = f"{self.PARALLELUM_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
        data = http_client.get(url)
        return data
    
    def consultar_preco(
        self,
        codigo_marca: str,
        codigo_modelo: str,
        codigo_ano: str,
        tipo_veiculo: str = "carros",
        timeout: int = 10
    ) -> Dict[str, Any]:
        """Consulta preço de um veículo específico.
        
        Args:
            codigo_marca: Código da marca.
            codigo_modelo: Código do modelo.
            codigo_ano: Código do ano.
            tipo_veiculo: Tipo do veículo ("carros", "motos" ou "caminhoes").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Dicionário com informações e preço do veículo.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> veiculo = fipe.consultar_preco("59", "5940", "2014-3")
            >>> "Valor" in veiculo
            True
        """
        url = f"{self.PARALLELUM_URL}/{tipo_veiculo}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
        data = http_client.get(url)
        return data
    
    def consultar_por_codigo_fipe(
        self,
        codigo_fipe: str,
        timeout: int = 10
    ) -> List[Dict[str, Any]]:
        """Consulta veículo pelo código FIPE (BrasilAPI).
        
        Args:
            codigo_fipe: Código FIPE do veículo (ex: "004340-1").
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista com histórico de preços do veículo.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> historico = fipe.consultar_por_codigo_fipe("004340-1")
            >>> len(historico) > 0
            True
        """
        url = f"{self.BRASILAPI_URL}/{codigo_fipe}"
        data = http_client.get(url)
        return data
    
    def buscar_por_nome(
        self,
        nome: str,
        tipo_veiculo: str = "carros"
    ) -> List[Dict[str, Any]]:
        """Busca veículo por nome (busca em marcas).
        
        Args:
            nome: Nome ou parte do nome para buscar.
            tipo_veiculo: Tipo do veículo ("carros", "motos" ou "caminhoes").
            
        Returns:
            Lista de marcas que correspondem à busca.
            
        Examples:
            >>> from tucano.consultas import fipe
            >>> resultados = fipe.buscar_por_nome("fiat")
            >>> len(resultados) > 0
            True
        """
        marcas = self.listar_marcas(tipo_veiculo)
        nome_lower = nome.lower()
        
        return [
            marca for marca in marcas
            if nome_lower in marca.get("nome", "").lower()
        ]


fipe: FIPEConsulta = FIPEConsulta()