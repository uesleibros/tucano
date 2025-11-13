"""Módulo de consultas em APIs externas brasileiras."""

from tucano.consultas.cep import cep
from tucano.consultas.cnpj import cnpj
from tucano.consultas.banco import banco
from tucano.consultas.fipe import fipe
from tucano.consultas.feriados import feriados
from tucano.consultas.ddd import ddd
from tucano.consultas.ibge import ibge

__all__ = [
    "cep",
    "cnpj",
    "banco",
    "fipe",
    "feriados",
    "ddd",
    "ibge",
]