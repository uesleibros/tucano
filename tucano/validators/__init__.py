"""Módulo de validadores de documentos brasileiros."""

from tucano.validators.cpf import cpf
from tucano.validators.cnpj import cnpj
from tucano.validators.cep import cep
from tucano.validators.telefone import telefone
from tucano.validators.pix import pix
from tucano.validators.placa import placa

__all__ = ["cpf", "cnpj", "cep", "telefone", "pix", "placa"]