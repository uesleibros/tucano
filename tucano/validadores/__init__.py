"""Módulo de validadores de documentos brasileiros."""

from tucano.validadores.cpf import cpf
from tucano.validadores.cnpj import cnpj
from tucano.validadores.cep import cep
from tucano.validadores.telefone import telefone
from tucano.validadores.pix import pix
from tucano.validadores.placa import placa

__all__ = ["cpf", "cnpj", "cep", "telefone", "pix", "placa"]