"""Testes para o validador de CEP."""

import pytest
from unittest.mock import patch, Mock
import httpx
from tucano import cep
from tucano.core.exceptions import InvalidCEP, CEPNotFound, CEPAPIError


class TestCEPValidation:
    """Testes de validação de CEP."""
    
    def test_validate_valid_cep_formatted(self) -> None:
        """Testa validação de CEP válido formatado."""
        assert cep.validate("01310-100") is True
    
    def test_validate_valid_cep_unformatted(self) -> None:
        """Testa validação de CEP válido sem formatação."""
        assert cep.validate("01310100") is True
    
    def test_validate_cep_all_zeros(self) -> None:
        """Testa validação de CEP com todos os dígitos zero."""
        assert cep.validate("00000-000") is False
        assert cep.validate("00000000") is False
    
    def test_validate_cep_wrong_length_short(self) -> None:
        """Testa validação de CEP com menos de 8 dígitos."""
        assert cep.validate("0131-010") is False
        assert cep.validate("013101") is False
    
    def test_validate_cep_wrong_length_long(self) -> None:
        """Testa validação de CEP com mais de 8 dígitos."""
        assert cep.validate("01310-1000") is False
        assert cep.validate("013101000") is False
    
    def test_validate_with_raise_error_valid(self) -> None:
        """Testa validação com raise_error para CEP válido."""
        assert cep.validate("01310-100", raise_error=True) is True
    
    def test_validate_with_raise_error_wrong_length(self) -> None:
        """Testa validação com raise_error para CEP com tamanho incorreto."""
        with pytest.raises(InvalidCEP, match="deve ter 8 dígitos"):
            cep.validate("0131-010", raise_error=True)
    
    def test_validate_with_raise_error_all_zeros(self) -> None:
        """Testa validação com raise_error para CEP com apenas zeros."""
        with pytest.raises(InvalidCEP, match="não pode ser composto apenas por zeros"):
            cep.validate("00000000", raise_error=True)


class TestCEPFormat:
    """Testes de formatação de CEP."""
    
    def test_format_unformatted_cep(self) -> None:
        """Testa formatação de CEP sem formatação."""
        assert cep.format("01310100") == "01310-100"
    
    def test_format_already_formatted_cep(self) -> None:
        """Testa formatação de CEP já formatado (idempotência)."""
        formatted = "01310-100"
        assert cep.format(formatted) == formatted
    
    def test_format_cep_with_spaces(self) -> None:
        """Testa formatação de CEP com espaços."""
        assert cep.format("01310 100") == "01310-100"
    
    def test_format_cep_wrong_length(self) -> None:
        """Testa formatação de CEP com tamanho incorreto."""
        with pytest.raises(InvalidCEP, match="deve ter 8 dígitos"):
            cep.format("0131010")


class TestCEPClean:
    """Testes de limpeza de CEP."""
    
    def test_clean_formatted_cep(self) -> None:
        """Testa limpeza de CEP formatado."""
        assert cep.clean("01310-100") == "01310100"
    
    def test_clean_unformatted_cep(self) -> None:
        """Testa limpeza de CEP sem formatação (idempotência)."""
        assert cep.clean("01310100") == "01310100"
    
    def test_clean_cep_with_spaces(self) -> None:
        """Testa limpeza de CEP com espaços."""
        assert cep.clean("01310 100") == "01310100"
        assert cep.clean(" 01310-100 ") == "01310100"
    
    def test_clean_cep_with_letters(self) -> None:
        """Testa limpeza de CEP com letras."""
        assert cep.clean("CEP: 01310-100") == "01310100"


class TestCEPConsultar:
    """Testes de consulta de CEP."""
    
    @patch("httpx.get")
    def test_consultar_cep_sucesso(self, mock_get: Mock) -> None:
        """Testa consulta de CEP com sucesso."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "cep": "01310-100",
            "logradouro": "Avenida Paulista",
            "complemento": "lado ímpar",
            "bairro": "Bela Vista",
            "localidade": "São Paulo",
            "uf": "SP",
            "ibge": "3550308",
            "gia": "1004",
            "ddd": "11",
            "siafi": "7107"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        resultado = cep.consultar("01310-100")
        
        assert resultado["logradouro"] == "Avenida Paulista"
        assert resultado["localidade"] == "São Paulo"
        assert resultado["uf"] == "SP"
        mock_get.assert_called_once()
    
    @patch("httpx.get")
    def test_consultar_cep_nao_encontrado(self, mock_get: Mock) -> None:
        """Testa consulta de CEP não encontrado."""
        mock_response = Mock()
        mock_response.json.return_value = {"erro": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(CEPNotFound, match="CEP não encontrado"):
            cep.consultar("99999-999", use_fallback=False)
    
    @patch("httpx.get")
    def test_consultar_cep_invalido(self, mock_get: Mock) -> None:
        """Testa consulta de CEP inválido."""
        with pytest.raises(InvalidCEP):
            cep.consultar("123")
        
        mock_get.assert_not_called()
    
    @patch("httpx.get")
    def test_consultar_erro_http(self, mock_get: Mock) -> None:
        """Testa erro HTTP na consulta."""
        mock_get.side_effect = httpx.HTTPStatusError(
            "Error",
            request=Mock(),
            response=Mock(status_code=500)
        )
        
        with pytest.raises(CEPAPIError, match="Erro HTTP"):
            cep.consultar("01310-100", use_fallback=False)
    
    @patch("httpx.get")
    def test_consultar_erro_conexao(self, mock_get: Mock) -> None:
        """Testa erro de conexão na consulta."""
        mock_get.side_effect = httpx.RequestError("Connection error")
        
        with pytest.raises(CEPAPIError, match="Erro de conexão"):
            cep.consultar("01310-100", use_fallback=False)
    
    @patch("httpx.get")
    def test_consultar_com_fallback(self, mock_get: Mock) -> None:
        """Testa consulta com fallback para BrasilAPI."""
        mock_response_viacep = Mock()
        mock_response_viacep.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error",
            request=Mock(),
            response=Mock(status_code=500)
        )
        
        mock_response_brasilapi = Mock()
        mock_response_brasilapi.json.return_value = {
            "cep": "01310-100",
            "street": "Avenida Paulista",
            "neighborhood": "Bela Vista",
            "city": "São Paulo",
            "state": "SP"
        }
        mock_response_brasilapi.raise_for_status = Mock()
        
        mock_get.side_effect = [mock_response_viacep, mock_response_brasilapi]
        
        resultado = cep.consultar("01310-100", use_fallback=True)
        
        assert resultado["logradouro"] == "Avenida Paulista"
        assert resultado["localidade"] == "São Paulo"
        assert mock_get.call_count == 2


class TestCEPEdgeCases:
    """Testes de casos extremos."""
    
    def test_validate_empty_string(self) -> None:
        """Testa validação de string vazia."""
        assert cep.validate("") is False
    
    def test_validate_only_special_chars(self) -> None:
        """Testa validação de string com apenas caracteres especiais."""
        assert cep.validate("-----") is False
    
    def test_format_cep_with_only_numbers(self) -> None:
        """Testa que formatação preserva apenas números."""
        formatted = cep.format("01310100")
        assert formatted.replace("-", "") == "01310100"