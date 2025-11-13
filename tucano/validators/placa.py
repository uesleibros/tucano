"""Validador de placas de veículos brasileiras (antiga e Mercosul)."""

import re
import random
from typing import Literal, Optional
from ..core.base import BaseValidator
from ..core.exceptions import InvalidPlaca


TipoPlaca = Literal["antiga", "mercosul"]


class PlacaValidator(BaseValidator[str]):
    """Validador de placas de veículos com suporte aos formatos antigo e Mercosul.
    
    Formatos suportados:
    - Antiga: ABC-1234 (3 letras + hífen + 4 números)
    - Mercosul: ABC1D23 (3 letras + 1 número + 1 letra + 2 números)
    
    A placa Mercosul foi implementada em 2018 e substitui gradualmente
    o formato antigo no Brasil.
    
    Attributes:
        PLACA_ANTIGA_REGEX: Expressão regular para validação de placa antiga.
        PLACA_MERCOSUL_REGEX: Expressão regular para validação de placa Mercosul.
        
    Examples:
        >>> from tucano import placa
        >>> placa.validate("ABC-1234")
        True
        >>> placa.validate("ABC1D23")
        True
        >>> placa.get_tipo("ABC-1234")
        "antiga"
        >>> placa.get_tipo("ABC1D23")
        "mercosul"
    """
    
    PLACA_ANTIGA_REGEX = re.compile(r'^[A-Z]{3}-?\d{4}$')
    PLACA_MERCOSUL_REGEX = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')
    
    def validate(self, value: str, raise_error: bool = False) -> bool:
        """Valida uma placa de veículo (qualquer formato).
        
        Aceita tanto placas antigas quanto Mercosul, com ou sem hífen.
        
        Args:
            value: Placa a ser validada.
            raise_error: Se True, levanta InvalidPlaca ao invés de retornar False.
                        
        Returns:
            True se a placa é válida, False caso contrário.
            
        Raises:
            InvalidPlaca: Se raise_error=True e a placa for inválida.
            
        Examples:
            >>> placa.validate("ABC-1234")
            True
            >>> placa.validate("ABC1234")
            True
            >>> placa.validate("ABC1D23")
            True
            >>> placa.validate("123-ABCD")
            False
        """
        try:
            # Verificar caracteres inválidos ANTES de limpar
            value_stripped = value.strip().upper()
            
            # Permitir apenas letras, números e hífen
            for char in value_stripped:
                if not (char.isalnum() or char == '-'):
                    raise InvalidPlaca(
                        f"Placa contém caracteres inválidos: {value}"
                    )
            
            cleaned = self.clean(value).upper()
            
            if len(cleaned) < 7 or len(cleaned) > 8:
                raise InvalidPlaca(
                    f"Placa deve ter 7 ou 8 caracteres, recebido: {len(cleaned)}"
                )
            
            if not self._is_valid_format(cleaned):
                raise InvalidPlaca(f"Formato de placa inválido: {value}")
            
            return True
            
        except InvalidPlaca:
            if raise_error:
                raise
            return False
    
    def validate_antiga(self, value: str, raise_error: bool = False) -> bool:
        """Valida uma placa no formato antigo (ABC-1234).
        
        Args:
            value: Placa a ser validada.
            raise_error: Se True, levanta InvalidPlaca ao invés de retornar False.
                        
        Returns:
            True se a placa antiga é válida, False caso contrário.
            
        Raises:
            InvalidPlaca: Se raise_error=True e a placa for inválida.
            
        Examples:
            >>> placa.validate_antiga("ABC-1234")
            True
            >>> placa.validate_antiga("ABC1234")
            True
            >>> placa.validate_antiga("ABC1D23")
            False
        """
        try:
            cleaned = self.clean(value).upper()
            
            if not self.PLACA_ANTIGA_REGEX.match(cleaned):
                raise InvalidPlaca(f"Formato de placa antiga inválido: {value}")
            
            return True
            
        except InvalidPlaca:
            if raise_error:
                raise
            return False
    
    def validate_mercosul(self, value: str, raise_error: bool = False) -> bool:
        """Valida uma placa no formato Mercosul (ABC1D23).
        
        Args:
            value: Placa a ser validada.
            raise_error: Se True, levanta InvalidPlaca ao invés de retornar False.
                        
        Returns:
            True se a placa Mercosul é válida, False caso contrário.
            
        Raises:
            InvalidPlaca: Se raise_error=True e a placa for inválida.
            
        Examples:
            >>> placa.validate_mercosul("ABC1D23")
            True
            >>> placa.validate_mercosul("ABC-1234")
            False
        """
        try:
            cleaned = self.clean(value).upper()
            
            if not self.PLACA_MERCOSUL_REGEX.match(cleaned):
                raise InvalidPlaca(f"Formato de placa Mercosul inválido: {value}")
            
            return True
            
        except InvalidPlaca:
            if raise_error:
                raise
            return False
    
    def _is_valid_format(self, cleaned: str) -> bool:
        """Verifica se a placa está em formato válido (antiga ou Mercosul).
        
        Args:
            cleaned: Placa limpa (apenas letras e números).
            
        Returns:
            True se o formato é válido, False caso contrário.
        """
        return (
            self.PLACA_ANTIGA_REGEX.match(cleaned) or
            self.PLACA_MERCOSUL_REGEX.match(cleaned)
        )
    
    def get_tipo(self, value: str) -> TipoPlaca:
        """Identifica o tipo de placa (antiga ou Mercosul).
        
        Args:
            value: Placa a ser identificada.
            
        Returns:
            Tipo da placa: "antiga" ou "mercosul".
            
        Raises:
            InvalidPlaca: Se a placa for inválida.
            
        Examples:
            >>> placa.get_tipo("ABC-1234")
            "antiga"
            >>> placa.get_tipo("ABC1D23")
            "mercosul"
        """
        cleaned = self.clean(value).upper()
        
        if not self.validate(cleaned, raise_error=True):
            raise InvalidPlaca(f"Placa inválida: {value}")
        
        if self.PLACA_MERCOSUL_REGEX.match(cleaned):
            return "mercosul"
        else:
            return "antiga"
    
    def is_antiga(self, value: str) -> bool:
        """Verifica se a placa é do formato antigo.
        
        Args:
            value: Placa a ser verificada.
            
        Returns:
            True se for placa antiga, False caso contrário.
            
        Raises:
            InvalidPlaca: Se a placa for inválida.
            
        Examples:
            >>> placa.is_antiga("ABC-1234")
            True
            >>> placa.is_antiga("ABC1D23")
            False
        """
        return self.get_tipo(value) == "antiga"
    
    def is_mercosul(self, value: str) -> bool:
        """Verifica se a placa é do formato Mercosul.
        
        Args:
            value: Placa a ser verificada.
            
        Returns:
            True se for placa Mercosul, False caso contrário.
            
        Raises:
            InvalidPlaca: Se a placa for inválida.
            
        Examples:
            >>> placa.is_mercosul("ABC1D23")
            True
            >>> placa.is_mercosul("ABC-1234")
            False
        """
        return self.get_tipo(value) == "mercosul"
    
    def format(self, value: str) -> str:
        """Formata uma placa de acordo com seu tipo.
        
        - Placa antiga: ABC-1234 (com hífen)
        - Placa Mercosul: ABC1D23 (sem hífen)
        
        Args:
            value: Placa a ser formatada.
            
        Returns:
            Placa formatada.
            
        Raises:
            InvalidPlaca: Se a placa for inválida.
            
        Examples:
            >>> placa.format("ABC1234")
            "ABC-1234"
            >>> placa.format("ABC1D23")
            "ABC1D23"
            >>> placa.format("abc-1234")
            "ABC-1234"
        """
        cleaned = self.clean(value).upper()
        
        if not self.validate(cleaned, raise_error=True):
            raise InvalidPlaca(f"Placa inválida: {value}")
        
        tipo = self.get_tipo(cleaned)
        
        if tipo == "antiga":
            return f"{cleaned[:3]}-{cleaned[3:]}"
        else:
            return cleaned
    
    def clean(self, value: str) -> str:
        """Remove formatação da placa, mantendo apenas letras e números.
        
        Args:
            value: Placa formatada ou não.
            
        Returns:
            Placa contendo apenas letras e números em uppercase.
            
        Examples:
            >>> placa.clean("ABC-1234")
            "ABC1234"
            >>> placa.clean("abc1d23")
            "ABC1D23"
            >>> placa.clean("  ABC-1234  ")
            "ABC1234"
        """
        value = value.strip().upper()
        value = value.replace("-", "").replace(" ", "")
        return "".join(c for c in value if c.isalnum())
    
    def generate(
        self, 
        tipo: TipoPlaca = "mercosul",
        formatted: bool = True
    ) -> str:
        """Gera uma placa válida aleatória.
        
        Args:
            tipo: Tipo de placa a gerar ("antiga" ou "mercosul").
            formatted: Se True, retorna a placa formatada.
                      
        Returns:
            Placa válida gerada aleatoriamente.
            
        Raises:
            InvalidPlaca: Se o tipo for inválido.
            
        Examples:
            >>> placa_gerada = placa.generate(tipo="antiga")
            >>> placa.validate(placa_gerada)
            True
            >>> placa_gerada = placa.generate(tipo="mercosul")
            >>> placa.is_mercosul(placa_gerada)
            True
        """
        if tipo not in ["antiga", "mercosul"]:
            raise InvalidPlaca(f"Tipo deve ser 'antiga' ou 'mercosul', recebido: {tipo}")
        
        letras1 = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        
        if tipo == "antiga":
            numeros = "".join(random.choices("0123456789", k=4))
            placa_gerada = f"{letras1}{numeros}"
        else:
            num1 = random.choice("0123456789")
            letra2 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            num2 = "".join(random.choices("0123456789", k=2))
            placa_gerada = f"{letras1}{num1}{letra2}{num2}"
        
        return self.format(placa_gerada) if formatted else placa_gerada
    
    def converter_para_mercosul(self, placa_antiga: str) -> str:
        """Converte uma placa antiga para o formato visual Mercosul.
        
        ATENÇÃO: Esta é apenas uma conversão de FORMATO, não é a conversão
        oficial que acontece no DETRAN. A placa real Mercosul terá número diferente.
        
        Esta função é útil apenas para demonstração do formato Mercosul.
        
        Args:
            placa_antiga: Placa no formato antigo (ABC-1234).
            
        Returns:
            String no formato Mercosul (apenas demonstrativo).
            
        Raises:
            InvalidPlaca: Se a placa não for do formato antigo.
            
        Examples:
            >>> placa.converter_para_mercosul("ABC-1234")
            "ABC1B34"
        """
        if not self.validate_antiga(placa_antiga):
            raise InvalidPlaca("Placa deve ser do formato antigo (ABC-1234)")
        
        cleaned = self.clean(placa_antiga)
        
        letras = cleaned[:3]
        numeros = cleaned[3:]
        
        letra_mercosul = chr(65 + int(numeros[1]))
        if letra_mercosul > 'Z':
            letra_mercosul = 'A'
        
        placa_mercosul = f"{letras}{numeros[0]}{letra_mercosul}{numeros[2:]}"
        
        return placa_mercosul


placa: PlacaValidator = PlacaValidator()