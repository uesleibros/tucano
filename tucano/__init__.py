"""Tucano - Validação de dados brasileiros.

Biblioteca Python para validação, formatação e geração de documentos
e dados brasileiros como CPF, CNPJ, CEP, telefone e PIX.

Examples:
	>>> from tucano import cpf, cnpj, cep
	>>> cpf.validate("123.456.789-09")
	True
	>>> cnpj.validate("11.222.333/0001-81")
	True
	>>> endereco = cep.consultar("01310-100")
	>>> endereco["logradouro"]
	"Avenida Paulista"
"""

from tucano.validators.cpf import cpf
from tucano.validators.cnpj import cnpj
from tucano.validators.cep import cep
from tucano.validators.telefone import telefone

__version__ = "0.1.0"

__all__ = [
	"cpf",
	"cnpj",
	"cep",
	"telefone",
	"__version__",
]