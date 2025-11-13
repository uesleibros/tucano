<div align="center">

# 🦜 Tucano

### Validação e consulta de dados brasileiros com as cores de um tucano

[![PyPI version](https://badge.fury.io/py/tucano.svg)](https://badge.fury.io/py/tucano)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-blue.svg)](http://mypy-lang.org/)

[Quick Start](#-quick-start) • [Funcionalidades](#-funcionalidades) • [Instalação](#-instalação) • [Como Usar](#%EF%B8%8F-como-usar) • [Contribuir](#-contribuindo)

</div>

## 📖 Sobre

**Tucano** é uma biblioteca Python moderna para **validação**, **formatação**, **geração** e **consulta** de documentos e dados brasileiros. Construída com foco em simplicidade, performance, confiabilidade e uma API intuitiva para desenvolvedores.

O objetivo é ser a ferramenta definitiva para lidar com dados do Brasil, combinando validações locais rápidas com consultas a APIs públicas, tudo em um pacote coeso e bem documentado.

## ✨ Funcionalidades

### 📦 Validadores (Offline e Rápidos)
-   ✅ **CPF**: Validação, formatação e geração.
-   ✅ **CNPJ**: Validação, formatação, geração e identificação de matriz/filial.
-   ✅ **CEP**: Validação de formato.
-   ✅ **Telefone**: Validação de fixo/celular, identificação de DDD e estado.
-   ✅ **PIX**: Validação de todos os tipos de chaves (CPF, CNPJ, Email, Telefone, Aleatória), mascaramento e normalização.
-   ✅ **Placa de Veículo**: Validação dos formatos antigo e Mercosul.

### 🔍 Consultas (Online, Requer Internet)
-   ✅ **CEP**: Consulta de endereço via ViaCEP com fallback para BrasilAPI.
-   ✅ **CNPJ**: Consulta de dados cadastrais de empresas.
-   ✅ **Bancos**: Listagem e consulta de bancos brasileiros por código.
-   ✅ **FIPE**: Consulta de preços de veículos.
-   ✅ **Feriados**: Lista de feriados nacionais por ano.
-   ✅ **DDD**: Consulta de estados e cidades por DDD.
-   ✅ **IBGE**: Consulta de estados e municípios.

### 💎 Qualidade e Features Técnicas
-   🔒 **100% Type-Safe**: Totalmente tipado e verificado com MyPy em modo `strict`.
-   ⚡ **Suporte Async**: Consultas de API com versões `_async` para aplicações modernas.
-   🧪 **Extensivamente Testado**: Mais de **250 testes** garantindo a confiabilidade.
-   🏗️ **Arquitetura Limpa**: Clara separação entre validações locais e consultas de rede.
-   📄 **Documentação Completa**: Docstrings e exemplos para todas as funcionalidades.
-   🐍 **Python 3.8+**: Compatível com as versões modernas do Python.

## 🚀 Instalação

```bash
# Em breve no PyPI!
pip install tucano
```

Para instalar a partir do código-fonte:
```bash
git clone https://github.com/uesleibros/tucano.git
cd tucano
pip install .
```

Para desenvolvimento:
```bash
pip install -e ".[dev]"
```

## ⚡ Quick Start

```python
# --- Validações rápidas (offline) ---
from tucano.validadores import cpf, placa, pix

# Validar CPF
print(f"CPF válido? {cpf.validate('123.456.789-09')}")

# Validar Placa Mercosul
print(f"Placa válida? {placa.validate('ABC1D23')}")

# Mascarar chave PIX para exibição
print(f"PIX mascarado: {pix.mascarar('usuario@example.com')}")


# --- Consultas (online) ---
from tucano.consultas import cep as cep_api
from tucano.consultas import cnpj as cnpj_api

# Consultar endereço por CEP
try:
    endereco = cep_api.consultar('01310-100')
    print(f"Endereço: {endereco['logradouro']}, {endereco['localidade']}")
except Exception as e:
    print(f"Erro na consulta de CEP: {e}")

# Consultar dados de uma empresa por CNPJ
try:
    empresa = cnpj_api.consultar('00.000.000/0001-91') # Banco do Brasil
    print(f"Empresa: {empresa['razao_social']} - Situação: {empresa['situacao_cadastral']}")
except Exception as e:
    print(f"Erro na consulta de CNPJ: {e}")
```

## 🛠️ Como Usar

A biblioteca é dividida em dois namespaces principais para clareza:

### 1. `tucano.validadores` (Validadores)
Contém todos os validadores que rodam **localmente**, sem necessidade de internet. São rápidos e ideais para validação de formulários.

```python
from tucano.validadores import cpf, telefone

# Formatar um telefone
telefone_formatado = telefone.format("11987654321")
# (11) 98765-4321

# Gerar um CPF válido para testes
cpf_teste = cpf.generate()
```

### 2. `tucano.consultas` (Consultas)
Contém todas as funções que fazem **chamadas a APIs externas**. Elas requerem conexão com a internet e podem ser mais lentas.

```python
from tucano.consultas import feriados, banco

# Verificar se hoje é feriado
from datetime import date
hoje = date.today().strftime("%Y-%m-%d")
if feriados.is_feriado(hoje):
    print("Hoje é feriado nacional! 🎉")

# Consultar nome de um banco
banco_itau = banco.consultar("341")
print(banco_itau['name']) # Itaú Unibanco S.A.
```

## 🧪 Testes

O Tucano preza pela qualidade e confiabilidade. Todos os módulos são cobertos por uma suíte de testes robusta.

```bash
# Rodar todos os testes
pytest -v

# Rodar testes com relatório de cobertura
pytest --cov=tucano --cov-report=html
```

## 🗺️ Roadmap

-   [ ] **Integrações:** Adicionar suporte nativo para Pydantic e Django.
-   [ ] **CLI:** Criar uma interface de linha de comando para usar o Tucano no terminal.
-   [ ] **Cache:** Implementar um sistema de cache opcional para as consultas de API.
-   [ ] **Publicação:** Disponibilizar no PyPI para fácil instalação.

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Se você tem uma ideia para uma nova feature, uma melhoria ou encontrou um bug, sinta-se à vontade para abrir uma **Issue** ou um **Pull Request**.

1.  **Fork** o projeto.
2.  Crie uma **branch** para sua feature (`git checkout -b feature/NovaFeature`).
3.  Faça suas alterações e **commit** (`git commit -m 'feat: Adiciona nova feature'`).
4.  Faça o **push** para a branch (`git push origin feature/NovaFeature`).
5.  Abra um **Pull Request**.

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.