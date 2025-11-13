"""Módulo core com classes base e exceções do Tucano."""

from tucano.core.base import BaseValidator
from tucano.core.http import HTTPClient, http_client
from tucano.core.exceptions import (
    CEPAPIError,
    CEPNotFound,
    InvalidCEP,
    InvalidCNPJ,
    InvalidCPF,
    InvalidPIX,
    InvalidPlaca,
    InvalidTelefone,
    TucanoException,
    ValidationError,
    InvalidUF,
)

__all__ = [
    "BaseValidator",
    "HTTPClient",
    "http_client",
    "TucanoException",
    "ValidationError",
    "InvalidUF",
    "InvalidCPF",
    "InvalidCNPJ",
    "InvalidCEP",
    "CEPNotFound",
    "CEPAPIError",
    "InvalidTelefone",
    "InvalidPIX",
    "InvalidPlaca",
]