"""Consulta de dados de CNPJ em APIs externas."""

from typing import Dict, Any, Optional
from ..core.http import http_client
from ..core.exceptions import InvalidCNPJ
from ..validators.cnpj import cnpj as cnpj_validator


class CNPJConsulta:
    """Consulta de dados de empresas por CNPJ via APIs públicas.
    
    Utiliza BrasilAPI e ReceitaWS como fontes de dados.
    
    Attributes:
        BRASILAPI_URL: URL base da API BrasilAPI.
        RECEITAWS_URL: URL base da API ReceitaWS.
        
    Examples:
        >>> from tucano.consultas import cnpj
        >>> empresa = cnpj.consultar("11.222.333/0001-81")
        >>> print(empresa["razao_social"])
        "EMPRESA EXEMPLO LTDA"
    """
    
    BRASILAPI_URL: str = "https://brasilapi.com.br/api/cnpj/v1/{}"
    RECEITAWS_URL: str = "https://www.receitaws.com.br/v1/cnpj/{}"
    
    def consultar(
        self, 
        value: str, 
        timeout: int = 15,
        use_receitaws: bool = False
    ) -> Dict[str, Any]:
        """Consulta informações de empresa por CNPJ.
        
        Retorna dados cadastrais da empresa junto à Receita Federal.
        
        Args:
            value: CNPJ a ser consultado (com ou sem formatação).
            timeout: Tempo máximo de espera em segundos.
            use_receitaws: Se True, usa ReceitaWS ao invés de BrasilAPI.
            
        Returns:
            Dicionário com informações da empresa contendo:
            - razao_social: Razão social da empresa
            - nome_fantasia: Nome fantasia
            - cnpj: CNPJ formatado
            - situacao_cadastral: Situação (ATIVA, BAIXADA, etc)
            - data_abertura: Data de abertura
            - capital_social: Capital social
            - cnae_fiscal: CNAE principal
            - municipio: Município
            - uf: Estado
            - logradouro: Endereço
            - numero: Número
            - complemento: Complemento
            - bairro: Bairro
            - cep: CEP
            - email: Email (quando disponível)
            - telefone: Telefone (quando disponível)
            
        Raises:
            InvalidCNPJ: Se o CNPJ for inválido.
            Exception: Se houver erro na consulta.
            
        Examples:
            >>> from tucano.consultas import cnpj
            >>> empresa = cnpj.consultar("00.000.000/0001-91")
            >>> empresa["razao_social"]
            "EMPRESA EXEMPLO LTDA"
        """
        cleaned = cnpj_validator.clean(value)
        
        if not cnpj_validator.validate(cleaned, raise_error=True):
            raise InvalidCNPJ(f"CNPJ inválido: {value}")
        
        if use_receitaws:
            return self._consultar_receitaws(cleaned)
        else:
            return self._consultar_brasilapi(cleaned)
    
    def _consultar_brasilapi(self, cnpj_limpo: str) -> Dict[str, Any]:
        """Consulta CNPJ na BrasilAPI.
        
        Args:
            cnpj_limpo: CNPJ sem formatação (14 dígitos).
            
        Returns:
            Dicionário com dados da empresa.
        """
        data = http_client.get(self.BRASILAPI_URL.format(cnpj_limpo))
        
        # Normalizar resposta
        qsa = data.get("qsa", [])
        socios = [
            {
                "nome": socio.get("nome_socio", ""),
                "qualificacao": socio.get("qualificacao_socio", "")
            }
            for socio in qsa
        ]
        
        return {
            "cnpj": data.get("cnpj", ""),
            "razao_social": data.get("razao_social", ""),
            "nome_fantasia": data.get("nome_fantasia", ""),
            "situacao_cadastral": data.get("descricao_situacao_cadastral", ""),
            "data_abertura": data.get("data_inicio_atividade", ""),
            "capital_social": data.get("capital_social", 0),
            "cnae_fiscal": data.get("cnae_fiscal_descricao", ""),
            "cnae_codigo": data.get("cnae_fiscal", ""),
            "municipio": data.get("municipio", ""),
            "uf": data.get("uf", ""),
            "logradouro": data.get("logradouro", ""),
            "numero": data.get("numero", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "cep": data.get("cep", ""),
            "email": data.get("email", ""),
            "telefone": data.get("ddd_telefone_1", ""),
            "socios": socios,
            "fonte": "BrasilAPI"
        }
    
    def _consultar_receitaws(self, cnpj_limpo: str) -> Dict[str, Any]:
        """Consulta CNPJ na ReceitaWS (alternativa).
        
        Args:
            cnpj_limpo: CNPJ sem formatação (14 dígitos).
            
        Returns:
            Dicionário com dados da empresa.
        """
        data = http_client.get(self.RECEITAWS_URL.format(cnpj_limpo))
        
        # Normalizar resposta
        qsa = data.get("qsa", [])
        socios = [
            {
                "nome": socio.get("nome", ""),
                "qualificacao": socio.get("qual", "")
            }
            for socio in qsa
        ]
        
        return {
            "cnpj": data.get("cnpj", ""),
            "razao_social": data.get("nome", ""),
            "nome_fantasia": data.get("fantasia", ""),
            "situacao_cadastral": data.get("situacao", ""),
            "data_abertura": data.get("abertura", ""),
            "capital_social": data.get("capital_social", ""),
            "cnae_fiscal": data.get("atividade_principal", [{}])[0].get("text", ""),
            "cnae_codigo": data.get("atividade_principal", [{}])[0].get("code", ""),
            "municipio": data.get("municipio", ""),
            "uf": data.get("uf", ""),
            "logradouro": data.get("logradouro", ""),
            "numero": data.get("numero", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "cep": data.get("cep", ""),
            "email": data.get("email", ""),
            "telefone": data.get("telefone", ""),
            "socios": socios,
            "fonte": "ReceitaWS"
        }


cnpj: CNPJConsulta = CNPJConsulta()