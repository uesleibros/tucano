"""Módulo core com classes base e exceções do Tucano."""

from tucano.core.base import BaseValidator
from tucano.core.exceptions import (
	CEPAPIError,
	CEPNotFound,
	InvalidCEP,
	InvalidCNPJ,
	InvalidCPF,
	InvalidPIX,
	InvalidTelefone,
	TucanoException,
	ValidationError,
)

__all__ = [
	"BaseValidator",
	"TucanoException",
	"ValidationError",
	"InvalidCPF",
	"InvalidCNPJ",
	"InvalidCEP",
	"CEPNotFound",
	"CEPAPIError",
	"InvalidTelefone",
	"InvalidPIX",
]