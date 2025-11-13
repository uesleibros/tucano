"""Validador de CEP (Código de Endereçamento Postal)."""

from ..core.base import BaseValidator
from ..core.exceptions import InvalidCEP


class CEPValidator(BaseValidator[str]):
    """Validador de CEP com suporte a formatação.
    
    O CEP (Código de Endereçamento Postal) é composto por 8 dígitos numéricos.
    
    Formato padrão: XXXXX-XXX
    
    Para consultar endereço por CEP, use o módulo `tucano.consultas.cep`.
        
    Examples:
        >>> from tucano import cep
        >>> cep.validate("01310-100")
        True
        >>> cep.format("01310100")
        "01310-100"
    """
    
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


cep: CEPValidator = CEPValidator()