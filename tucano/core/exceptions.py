"""Exceções customizadas do Tucano."""


class TucanoException(Exception):
	"""Exceção base para todas as exceções do Tucano.
	
	Esta é a classe base da qual todas as outras exceções do Tucano herdam.
	Permite capturar todas as exceções do Tucano com um único except.
	"""
	
	pass


class ValidationError(TucanoException):
	"""Exceção levantada quando a validação de um dado falha.
	
	Esta exceção é levantada quando um valor não passa na validação,
	mas não se encaixa em nenhuma categoria mais específica.
	"""
	
	pass


class InvalidCPF(ValidationError):
	"""Exceção levantada quando um CPF é inválido.
	
	Pode ser levantada por diversos motivos:
	- Tamanho incorreto
	- Dígitos verificadores inválidos
	- Sequência de dígitos iguais
	- Formato inválido
	"""
	
	pass


class InvalidCNPJ(ValidationError):
	"""Exceção levantada quando um CNPJ é inválido.
	
	Pode ser levantada por diversos motivos:
	- Tamanho incorreto
	- Dígitos verificadores inválidos
	- Sequência de dígitos iguais
	- Formato inválido
	"""
	
	pass


class InvalidCEP(ValidationError):
	"""Exceção levantada quando um CEP é inválido.
	
	Pode ser levantada por:
	- Tamanho incorreto
	- Formato inválido
	- CEP composto apenas por zeros
	"""
	
	pass


class CEPNotFound(TucanoException):
	"""Exceção levantada quando um CEP não é encontrado na consulta.
	
	Esta exceção indica que o CEP está em formato válido,
	mas não existe na base de dados da API consultada.
	"""
	
	pass


class CEPAPIError(TucanoException):
	"""Exceção levantada quando há erro ao consultar a API de CEP.
	
	Pode indicar:
	- Timeout na requisição
	- Erro de conexão
	- Erro HTTP (4xx, 5xx)
	- API indisponível
	"""
	
	pass


class InvalidTelefone(ValidationError):
	"""Exceção levantada quando um número de telefone é inválido.
	
	Pode ser levantada por:
	- Tamanho incorreto
	- DDD inválido
	- Formato inválido
	"""
	
	pass


class InvalidPIX(ValidationError):
	"""Exceção levantada quando uma chave PIX é inválida.
	
	Pode ser levantada quando a chave não se encaixa em nenhum
	dos formatos válidos: CPF, CNPJ, email, telefone ou EVP.
	"""
	
	pass

class InvalidPlaca(ValidationError):
    """Placa de veículo inválida."""
    
    pass

class InvalidUF(ValidationError):
    """Sigla de UF (Estado) inválida."""
    
    pass