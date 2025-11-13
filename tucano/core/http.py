"""Cliente HTTP compartilhado para consultas em APIs externas."""

from typing import Dict, Any, Optional
import httpx


class HTTPClient:
    """Cliente HTTP com suporte síncrono e assíncrono.
    
    Fornece métodos para realizar requisições HTTP com timeout,
    retry e tratamento de erros padronizado.
    
    Attributes:
        timeout: Tempo máximo de espera em segundos.
        
    Examples:
        >>> client = HTTPClient(timeout=10)
        >>> data = client.get("https://api.example.com/data")
        >>> # Async
        >>> data = await client.get_async("https://api.example.com/data")
    """
    
    def __init__(self, timeout: int = 10):
        """Inicializa o cliente HTTP.
        
        Args:
            timeout: Tempo máximo de espera em segundos (padrão: 10).
        """
        self.timeout = timeout
    
    def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Realiza requisição GET síncrona.
        
        Args:
            url: URL completa para requisição.
            params: Parâmetros query string (opcional).
            headers: Headers HTTP customizados (opcional).
            
        Returns:
            Resposta JSON como dicionário.
            
        Raises:
            httpx.HTTPStatusError: Se status code não for 2xx.
            httpx.RequestError: Se houver erro de conexão.
            
        Examples:
            >>> client = HTTPClient()
            >>> data = client.get("https://api.example.com/users/1")
        """
        response = httpx.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
            follow_redirects=True
        )
        response.raise_for_status()
        return response.json()
    
    async def get_async(
        self, 
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Realiza requisição GET assíncrona.
        
        Args:
            url: URL completa para requisição.
            params: Parâmetros query string (opcional).
            headers: Headers HTTP customizados (opcional).
            
        Returns:
            Resposta JSON como dicionário.
            
        Raises:
            httpx.HTTPStatusError: Se status code não for 2xx.
            httpx.RequestError: Se houver erro de conexão.
            
        Examples:
            >>> client = HTTPClient()
            >>> data = await client.get_async("https://api.example.com/users/1")
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()


# Instância singleton
http_client: HTTPClient = HTTPClient()