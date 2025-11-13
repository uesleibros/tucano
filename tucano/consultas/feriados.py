"""Consulta de feriados nacionais brasileiros."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.http import http_client


class FeriadosConsulta:
    """Consulta feriados nacionais brasileiros.
    
    Utiliza BrasilAPI para obter lista de feriados.
    
    Attributes:
        BRASILAPI_URL: URL base da API BrasilAPI.
        
    Examples:
        >>> from tucano.consultas import feriados
        >>> lista = feriados.listar(2024)
        >>> len(lista) > 0
        True
    """
    
    BRASILAPI_URL: str = "https://brasilapi.com.br/api/feriados/v1/{}"
    
    def listar(self, ano: int, timeout: int = 10) -> List[Dict[str, Any]]:
        """Lista todos os feriados nacionais de um ano.
        
        Args:
            ano: Ano para consulta de feriados.
            timeout: Tempo máximo de espera em segundos.
            
        Returns:
            Lista de feriados com data, nome e tipo.
            
        Examples:
            >>> from tucano.consultas import feriados
            >>> lista = feriados.listar(2024)
            >>> lista[0]["name"]
            "Confraternização Universal"
        """
        data = http_client.get(self.BRASILAPI_URL.format(ano))
        return data
    
    def is_feriado(self, data: str, ano: Optional[int] = None) -> bool:
        """Verifica se uma data é feriado nacional.
        
        Args:
            data: Data no formato "YYYY-MM-DD".
            ano: Ano (opcional, extrai da data se não fornecido).
            
        Returns:
            True se for feriado nacional, False caso contrário.
            
        Examples:
            >>> from tucano.consultas import feriados
            >>> feriados.is_feriado("2024-12-25")
            True
            >>> feriados.is_feriado("2024-12-26")
            False
        """
        if not ano:
            ano = int(data.split("-")[0])
        
        feriados_ano = self.listar(ano)
        
        return any(f["date"] == data for f in feriados_ano)
    
    def proximo_feriado(self, ano: Optional[int] = None) -> Dict[str, Any]:
        """Retorna o próximo feriado nacional.
        
        Args:
            ano: Ano para busca (opcional, usa ano atual se não fornecido).
            
        Returns:
            Dicionário com informações do próximo feriado.
            
        Examples:
            >>> from tucano.consultas import feriados
            >>> proximo = feriados.proximo_feriado()
            >>> "name" in proximo
            True
        """
        if not ano:
            ano = datetime.now().year
        
        hoje = datetime.now().date()
        feriados_ano = self.listar(ano)
        
        for feriado in feriados_ano:
            data_feriado = datetime.strptime(feriado["date"], "%Y-%m-%d").date()
            if data_feriado >= hoje:
                return feriado
        
        feriados_prox_ano = self.listar(ano + 1)
        return feriados_prox_ano[0] if feriados_prox_ano else {}


feriados: FeriadosConsulta = FeriadosConsulta()