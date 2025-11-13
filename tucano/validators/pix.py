"""Validador de chaves PIX brasileiras."""

import re
import uuid
import random
from typing import Literal, Optional, Dict, List, Any
from ..core.base import BaseValidator
from ..core.exceptions import InvalidPIX
from .cpf import cpf as cpf_validator
from .cnpj import cnpj as cnpj_validator
from .telefone import telefone as telefone_validator


TipoChavePIX = Literal["cpf", "cnpj", "email", "telefone", "aleatoria"]


class PIXValidator(BaseValidator[str]):
    """Validador completo de chaves PIX com todas as funcionalidades.
    
    O PIX aceita 5 tipos de chaves:
    - CPF: 11 dígitos
    - CNPJ: 14 dígitos
    - Email: formato email válido (máx 77 caracteres)
    - Telefone: +5511987654321 (com código do país +55)
    - Aleatória (EVP): UUID v4
    
    Attributes:
        EMAIL_REGEX: Expressão regular para validação de email.
        TELEFONE_REGEX: Expressão regular para validação de telefone PIX.
        
    Examples:
        >>> from tucano import pix
        >>> pix.validate_cpf("123.456.789-09")
        True
        >>> pix.validate_email("usuario@example.com")
        True
        >>> pix.detectar_tipo("11987654321")
        "telefone"
        >>> pix.mascarar("123.456.789-09")
        "***.***.*89-09"
    """
    
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    TELEFONE_REGEX = re.compile(
        r'^\+55\d{2}9?\d{8}$'
    )
    
    def validate(self, value: str, raise_error: bool = False) -> bool:
        """Valida uma chave PIX (qualquer tipo).
        
        Tenta validar como qualquer tipo de chave PIX válida.
        
        Args:
            value: Chave PIX a ser validada.
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se a chave é válida, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e a chave for inválida.
            
        Examples:
            >>> pix.validate("123.456.789-09")
            True
            >>> pix.validate("usuario@example.com")
            True
            >>> pix.validate("invalid")
            False
        """
        try:
            value = self.sanitizar(value)
            tipo = self.detectar_tipo(value)
            if tipo is None:
                raise InvalidPIX(f"Chave PIX inválida: {value}")
            return True
            
        except InvalidPIX:
            if raise_error:
                raise
            return False
    
    def validate_cpf(self, value: str, raise_error: bool = False) -> bool:
        """Valida chave PIX do tipo CPF.
        
        Args:
            value: CPF a ser validado (com ou sem formatação).
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se o CPF é válido, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e o CPF for inválido.
            
        Examples:
            >>> pix.validate_cpf("123.456.789-09")
            True
            >>> pix.validate_cpf("12345678909")
            True
            >>> pix.validate_cpf("000.000.000-00")
            False
        """
        try:
            value = self.sanitizar(value)
            if not cpf_validator.validate(value):
                raise InvalidPIX(f"CPF inválido para chave PIX: {value}")
            return True
            
        except Exception as e:
            if raise_error:
                raise InvalidPIX(f"CPF inválido para chave PIX: {value}") from e
            return False
    
    def validate_cnpj(self, value: str, raise_error: bool = False) -> bool:
        """Valida chave PIX do tipo CNPJ.
        
        Args:
            value: CNPJ a ser validado (com ou sem formatação).
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se o CNPJ é válido, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e o CNPJ for inválido.
            
        Examples:
            >>> pix.validate_cnpj("11.222.333/0001-81")
            True
            >>> pix.validate_cnpj("11222333000181")
            True
            >>> pix.validate_cnpj("00.000.000/0000-00")
            False
        """
        try:
            value = self.sanitizar(value)
            if not cnpj_validator.validate(value):
                raise InvalidPIX(f"CNPJ inválido para chave PIX: {value}")
            return True
            
        except Exception as e:
            if raise_error:
                raise InvalidPIX(f"CNPJ inválido para chave PIX: {value}") from e
            return False
    
    def validate_email(self, value: str, raise_error: bool = False) -> bool:
        """Valida chave PIX do tipo email com regras rigorosas do PIX.
        
        Regras PIX para email:
        - Mínimo 5 caracteres (a@b.c)
        - Máximo 77 caracteres
        - Não pode conter espaços
        - Não pode começar ou terminar com ponto
        - Não pode ter pontos consecutivos
        
        Args:
            value: Email a ser validado.
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se o email é válido, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e o email for inválido.
            
        Examples:
            >>> pix.validate_email("usuario@example.com")
            True
            >>> pix.validate_email("user.name@domain.com.br")
            True
            >>> pix.validate_email("invalid-email")
            False
            >>> pix.validate_email("a" * 78 + "@example.com")
            False
        """
        try:
            value = self.sanitizar(value)
            
            if len(value) < 5:
                raise InvalidPIX("Email deve ter no mínimo 5 caracteres")
            
            if len(value) > 77:
                raise InvalidPIX("Email deve ter no máximo 77 caracteres")
            
            if " " in value:
                raise InvalidPIX("Email não pode conter espaços")
            
            if not self.EMAIL_REGEX.match(value):
                raise InvalidPIX(f"Formato de email inválido: {value}")
            
            if ".." in value:
                raise InvalidPIX("Email não pode ter pontos consecutivos")
            
            local_part = value.split("@")[0]
            if local_part.startswith(".") or local_part.endswith("."):
                raise InvalidPIX("Email não pode começar ou terminar com ponto")
            
            return True
            
        except InvalidPIX:
            if raise_error:
                raise
            return False
    
    def validate_telefone(self, value: str, raise_error: bool = False) -> bool:
        """Valida chave PIX do tipo telefone.
        
        Formato PIX: +5511987654321 (+55 + DDD + número)
        - Deve começar com +55
        - DDD com 2 dígitos válidos
        - Celular: 9 dígitos (9XXXXXXXX)
        - Fixo: 8 dígitos
        
        Args:
            value: Telefone a ser validado.
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se o telefone é válido, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e o telefone for inválido.
            
        Examples:
            >>> pix.validate_telefone("+5511987654321")
            True
            >>> pix.validate_telefone("+551134567890")
            True
            >>> pix.validate_telefone("11987654321")
            False
            >>> pix.validate_telefone("+5500987654321")
            False
        """
        try:
            value = self.sanitizar(value)
            
            if not value.startswith("+55"):
                raise InvalidPIX("Telefone PIX deve começar com +55")
            
            if not self.TELEFONE_REGEX.match(value):
                raise InvalidPIX(f"Formato de telefone PIX inválido: {value}")
            
            ddd = value[3:5]
            numero = value[5:]
            
            telefone_sem_codigo = ddd + numero
            if not telefone_validator.validate(telefone_sem_codigo):
                raise InvalidPIX(f"Telefone inválido para PIX: {value}")
            
            return True
            
        except InvalidPIX:
            if raise_error:
                raise
            return False
    
    def validate_aleatoria(self, value: str, raise_error: bool = False) -> bool:
        """Valida chave PIX do tipo aleatória (EVP - Endereço Virtual de Pagamento).
        
        Chave aleatória é um UUID v4 no formato:
        xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        
        Args:
            value: Chave aleatória a ser validada.
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se a chave é válida, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e a chave for inválida.
            
        Examples:
            >>> pix.validate_aleatoria("a1b2c3d4-e5f6-4789-a1b2-c3d4e5f6a7b8")
            True
            >>> pix.validate_aleatoria("invalid-uuid")
            False
        """
        try:
            value = self.sanitizar(value)
            parsed_uuid = uuid.UUID(value, version=4)
            
            if parsed_uuid.version != 4:
                raise InvalidPIX("Chave aleatória deve ser UUID v4")
            
            return True
            
        except (ValueError, AttributeError):
            if raise_error:
                raise InvalidPIX(f"Chave aleatória inválida: {value}")
            return False
    
    def detectar_tipo(self, value: str) -> Optional[TipoChavePIX]:
        """Detecta automaticamente o tipo de chave PIX.
        
        Tenta identificar o tipo baseado no formato da chave.
        
        Args:
            value: Chave PIX a ser identificada.
            
        Returns:
            Tipo da chave PIX ou None se não for válida.
            
        Examples:
            >>> pix.detectar_tipo("123.456.789-09")
            "cpf"
            >>> pix.detectar_tipo("usuario@example.com")
            "email"
            >>> pix.detectar_tipo("+5511987654321")
            "telefone"
            >>> pix.detectar_tipo("a1b2c3d4-e5f6-4789-a1b2-c3d4e5f6a7b8")
            "aleatoria"
            >>> pix.detectar_tipo("invalid")
            None
        """
        value = self.sanitizar(value)
        
        if self.validate_cpf(value):
            return "cpf"
        
        if self.validate_cnpj(value):
            return "cnpj"
        
        if self.validate_email(value):
            return "email"
        
        if self.validate_telefone(value):
            return "telefone"
        
        if self.validate_aleatoria(value):
            return "aleatoria"
        
        return None
    
    def validate_auto(self, value: str, raise_error: bool = False) -> bool:
        """Valida automaticamente detectando o tipo de chave PIX.
        
        Detecta o tipo e valida de acordo.
        
        Args:
            value: Chave PIX a ser validada.
            raise_error: Se True, levanta InvalidPIX ao invés de retornar False.
                        
        Returns:
            True se a chave é válida, False caso contrário.
            
        Raises:
            InvalidPIX: Se raise_error=True e a chave for inválida.
            
        Examples:
            >>> pix.validate_auto("123.456.789-09")
            True
            >>> pix.validate_auto("usuario@example.com")
            True
            >>> pix.validate_auto("invalid")
            False
        """
        return self.validate(value, raise_error=raise_error)
    
    def format(self, value: str) -> str:
        """Formata uma chave PIX de acordo com seu tipo.
        
        Args:
            value: Chave PIX a ser formatada.
            
        Returns:
            Chave PIX formatada.
            
        Raises:
            InvalidPIX: Se a chave for inválida.
            
        Examples:
            >>> pix.format("12345678909")
            "123.456.789-09"
            >>> pix.format("11222333000181")
            "11.222.333/0001-81"
            >>> pix.format("USUARIO@EXAMPLE.COM")
            "usuario@example.com"
        """
        value = self.sanitizar(value)
        tipo = self.detectar_tipo(value)
        
        if tipo is None:
            raise InvalidPIX(f"Chave PIX inválida: {value}")
        
        if tipo == "cpf":
            return cpf_validator.format(value)
        elif tipo == "cnpj":
            return cnpj_validator.format(value)
        elif tipo == "telefone":
            return value
        elif tipo == "email":
            return value.lower()
        elif tipo == "aleatoria":
            return str(uuid.UUID(value)).lower()
        
        return value
    
    def clean(self, value: str) -> str:
        """Remove formatação de uma chave PIX.
        
        Args:
            value: Chave PIX formatada.
            
        Returns:
            Chave PIX sem formatação.
            
        Examples:
            >>> pix.clean("123.456.789-09")
            "12345678909"
            >>> pix.clean("(11) 98765-4321")
            "11987654321"
        """
        value = self.sanitizar(value)
        tipo = self.detectar_tipo(value)
        
        if tipo == "cpf":
            return cpf_validator.clean(value)
        elif tipo == "cnpj":
            return cnpj_validator.clean(value)
        elif tipo == "telefone":
            return value.replace("+", "").replace(" ", "")
        elif tipo == "email":
            return value.lower()
        elif tipo == "aleatoria":
            return str(uuid.UUID(value)).lower()
        
        return self._only_digits(value)
    
    def sanitizar(self, value: str) -> str:
        """Sanitiza uma entrada de chave PIX.
        
        Remove caracteres invisíveis, espaços extras, quebras de linha, etc.
        
        Args:
            value: Chave PIX possivelmente suja.
            
        Returns:
            Chave PIX limpa.
            
        Examples:
            >>> pix.sanitizar("  123.456.789-09  ")
            "123.456.789-09"
            >>> pix.sanitizar("\\t\\nusuario@example.com\\n")
            "usuario@example.com"
        """
        value = value.strip()
        
        value = value.replace("\n", "").replace("\r", "").replace("\t", "")
        
        value = " ".join(value.split())
        
        value = value.replace("\u200b", "")
        value = value.replace("\ufeff", "")
        
        return value
    
    def normalizar(self, value: str) -> str:
        """Normaliza uma chave PIX para formato padrão.
        
        Remove espaços, converte para lowercase quando apropriado,
        converte telefones para formato PIX, etc.
        
        Args:
            value: Chave PIX em qualquer formato.
            
        Returns:
            Chave PIX normalizada.
            
        Raises:
            InvalidPIX: Se a chave for inválida.
            
        Examples:
            >>> pix.normalizar("  123.456.789-09  ")
            "123.456.789-09"
            >>> pix.normalizar("USUARIO@EXAMPLE.COM")
            "usuario@example.com"
            >>> pix.normalizar("(11) 98765-4321")
            "+5511987654321"
        """
        value = self.sanitizar(value)
        
        if telefone_validator.validate(value) and not value.startswith("+55"):
            return self.telefone_para_pix(value)
        
        tipo = self.detectar_tipo(value)
        
        if tipo == "email":
            return value.lower().strip()
        
        elif tipo == "aleatoria":
            return str(uuid.UUID(value)).lower()
        
        return value
    
    def telefone_para_pix(self, telefone: str) -> str:
        """Converte telefone brasileiro para formato PIX.
        
        Aceita telefone em qualquer formato brasileiro e converte
        para o formato PIX (+5511987654321).
        
        Args:
            telefone: Telefone em qualquer formato brasileiro.
            
        Returns:
            Telefone no formato PIX (+5511987654321).
            
        Raises:
            InvalidPIX: Se o telefone for inválido.
            
        Examples:
            >>> pix.telefone_para_pix("(11) 98765-4321")
            "+5511987654321"
            >>> pix.telefone_para_pix("11987654321")
            "+5511987654321"
            >>> pix.telefone_para_pix("1134567890")
            "+551134567890"
        """
        telefone = self.sanitizar(telefone)
        
        if telefone.startswith("+55"):
            return telefone
        
        if not telefone_validator.validate(telefone):
            raise InvalidPIX(f"Telefone inválido: {telefone}")
        
        cleaned = telefone_validator.clean(telefone)
        return f"+55{cleaned}"
    
    def mascarar(self, value: str, mostrar_final: int = 4) -> str:
        """Mascara uma chave PIX para exibição segura.
        
        Oculta parte da chave PIX, mantendo apenas os caracteres finais visíveis.
        Útil para exibir chaves sem expor dados sensíveis completamente.
        
        Args:
            value: Chave PIX a ser mascarada.
            mostrar_final: Quantos caracteres finais mostrar (padrão: 4).
            
        Returns:
            Chave mascarada.
            
        Raises:
            InvalidPIX: Se a chave for inválida.
            
        Examples:
            >>> pix.mascarar("123.456.789-09")
            "***.***.*89-09"
            >>> pix.mascarar("usuario@example.com")
            "usua***@example.com"
            >>> pix.mascarar("+5511987654321")
            "+55119****4321"
        """
        value = self.sanitizar(value)
        tipo = self.detectar_tipo(value)
        
        if tipo is None:
            raise InvalidPIX(f"Chave PIX inválida: {value}")
        
        if tipo == "cpf":
            formatted = cpf_validator.format(value)
            return f"***.***.*{formatted[-5:]}"
        
        elif tipo == "cnpj":
            formatted = cnpj_validator.format(value)
            return f"**.***.***/****-{formatted[-2:]}"
        
        elif tipo == "email":
            parts = value.split("@")
            if len(parts) != 2:
                return value
            username = parts[0]
            domain = parts[1]
            if len(username) > 4:
                masked_user = username[:4] + "***"
            else:
                masked_user = "***"
            return f"{masked_user}@{domain}"
        
        elif tipo == "telefone":
            return f"{value[:6]}****{value[-mostrar_final:]}"
        
        elif tipo == "aleatoria":
            return f"{value[:8]}****-****-****-{value[-12:]}"
        
        return value
    
    def sao_iguais(self, chave1: str, chave2: str) -> bool:
        """Verifica se duas chaves PIX são iguais.
        
        Compara independente de formatação, maiúsculas/minúsculas, etc.
        
        Args:
            chave1: Primeira chave PIX.
            chave2: Segunda chave PIX.
            
        Returns:
            True se as chaves são iguais, False caso contrário.
            
        Examples:
            >>> pix.sao_iguais("123.456.789-09", "12345678909")
            True
            >>> pix.sao_iguais("USUARIO@EXAMPLE.COM", "usuario@example.com")
            True
            >>> pix.sao_iguais("(11) 98765-4321", "+5511987654321")
            True
        """
        try:
            chave1 = self.sanitizar(chave1)
            chave2 = self.sanitizar(chave2)
            
            # Tentar normalizar telefones para formato PIX
            if telefone_validator.validate(chave1) and not chave1.startswith("+55"):
                chave1 = self.telefone_para_pix(chave1)
            
            if telefone_validator.validate(chave2) and not chave2.startswith("+55"):
                chave2 = self.telefone_para_pix(chave2)
            
            tipo1 = self.detectar_tipo(chave1)
            tipo2 = self.detectar_tipo(chave2)
            
            if tipo1 != tipo2:
                return False
            
            if tipo1 is None or tipo2 is None:
                return False
            
            cleaned1 = self.clean(chave1)
            cleaned2 = self.clean(chave2)
            
            return cleaned1 == cleaned2
        
        except Exception:
            return False
    
    def info(self, value: str) -> Dict[str, Any]:
        """Retorna informações detalhadas sobre uma chave PIX.
        
        Args:
            value: Chave PIX a ser analisada.
            
        Returns:
            Dicionário com informações da chave incluindo:
            - valida: Se a chave é válida
            - tipo: Tipo da chave (cpf, cnpj, email, telefone, aleatoria)
            - formatada: Chave formatada
            - limpa: Chave sem formatação
            - mascarada: Chave mascarada
            - extras: Informações adicionais específicas do tipo
            
        Examples:
            >>> pix.info("123.456.789-09")
            {
                'valida': True,
                'tipo': 'cpf',
                'formatada': '123.456.789-09',
                'limpa': '12345678909',
                'mascarada': '***.***.*89-09',
                'extras': {'documento': 'CPF'}
            }
        """
        value = self.sanitizar(value)
        tipo = self.detectar_tipo(value)
        valida = tipo is not None
        
        info_dict: Dict[str, Any] = {
            'valida': valida,
            'tipo': tipo,
            'formatada': None,
            'limpa': None,
            'mascarada': None,
            'extras': {}
        }
        
        if valida and tipo is not None:
            try:
                info_dict['formatada'] = self.format(value)
                info_dict['limpa'] = self.clean(value)
                info_dict['mascarada'] = self.mascarar(value)
                
                if tipo == "telefone":
                    tel_normalizado = self.normalizar(value)
                    ddd = tel_normalizado[3:5]
                    info_dict['extras']['ddd'] = ddd
                    info_dict['extras']['estado'] = telefone_validator.get_estado_por_ddd(ddd)
                    info_dict['extras']['tipo_telefone'] = telefone_validator.get_tipo(
                        tel_normalizado.replace("+55", "")
                    )
                
                elif tipo == "cpf":
                    info_dict['extras']['documento'] = 'CPF'
                
                elif tipo == "cnpj":
                    info_dict['extras']['documento'] = 'CNPJ'
                    cleaned_cnpj = self.clean(value)
                    info_dict['extras']['matriz'] = cnpj_validator.is_matriz(cleaned_cnpj)
                    info_dict['extras']['numero_filial'] = cnpj_validator.get_numero_filial(cleaned_cnpj)
            
            except Exception:
                pass
        
        return info_dict
    
    def gerar_aleatoria(self) -> str:
        """Gera uma chave PIX aleatória (EVP) válida.
        
        Gera um UUID v4 que pode ser usado como chave PIX aleatória.
        
        Returns:
            Chave PIX aleatória no formato UUID v4.
            
        Examples:
            >>> chave = pix.gerar_aleatoria()
            >>> pix.validate_aleatoria(chave)
            True
            >>> len(chave)
            36
        """
        return str(uuid.uuid4())
    
    def validar_lote(self, chaves: List[str]) -> List[Dict[str, Any]]:
        """Valida múltiplas chaves PIX de uma vez.
        
        Útil para validar várias chaves simultaneamente, retornando
        o resultado de cada uma.
        
        Args:
            chaves: Lista de chaves PIX para validar.
            
        Returns:
            Lista de dicionários com resultado de cada validação contendo:
            - chave: Chave original
            - valida: Se é válida
            - tipo: Tipo da chave
            - erro: Mensagem de erro (se houver)
            
        Examples:
            >>> chaves = ["123.456.789-09", "invalid", "user@example.com"]
            >>> pix.validar_lote(chaves)
            [
                {'chave': '123.456.789-09', 'valida': True, 'tipo': 'cpf', 'erro': None},
                {'chave': 'invalid', 'valida': False, 'tipo': None, 'erro': 'Tipo não identificado'},
                {'chave': 'user@example.com', 'valida': True, 'tipo': 'email', 'erro': None}
            ]
        """
        resultados: List[Dict[str, Any]] = []
        
        for chave in chaves:
            resultado: Dict[str, Any] = {
                'chave': chave,
                'valida': False,
                'tipo': None,
                'erro': None
            }
            
            try:
                tipo = self.detectar_tipo(chave)
                if tipo:
                    resultado['valida'] = True
                    resultado['tipo'] = tipo
                else:
                    resultado['erro'] = "Tipo não identificado"
            except Exception as e:
                resultado['erro'] = str(e)
            
            resultados.append(resultado)
        
        return resultados
    
    def gerar_chaves_teste(self, quantidade: int = 5) -> Dict[str, List[str]]:
        """Gera múltiplas chaves PIX válidas para testes.
        
        Útil para popular bancos de dados de teste, criar fixtures, etc.
        
        Args:
            quantidade: Quantas chaves gerar de cada tipo (padrão: 5).
            
        Returns:
            Dicionário com listas de chaves de cada tipo.
            
        Examples:
            >>> chaves = pix.gerar_chaves_teste(3)
            >>> len(chaves['cpf'])
            3
            >>> len(chaves['email'])
            3
        """
        chaves: Dict[str, List[str]] = {
            'cpf': [cpf_validator.generate() for _ in range(quantidade)],
            'cnpj': [cnpj_validator.generate() for _ in range(quantidade)],
            'email': [f"teste{i}@example.com" for i in range(quantidade)],
            'telefone': [],
            'aleatoria': [self.gerar_aleatoria() for _ in range(quantidade)]
        }
        
        for i in range(quantidade):
            numero = "9" + "".join([str(random.randint(0, 9)) for _ in range(8)])
            telefone_pix = f"+5511{numero}"
            chaves['telefone'].append(telefone_pix)
        
        return chaves


pix: PIXValidator = PIXValidator()