"""Exemplos de uso de consultas de CNPJ."""

from tucano.consultas import cnpj


def exemplo_consulta_simples() -> None:
    """Demonstra uma consulta simples de CNPJ."""
    print("=" * 60)
    print("CONSULTA SIMPLES DE CNPJ (BANCO DO BRASIL)")
    print("=" * 60)
    
    try:
        # CNPJ público do Banco do Brasil
        empresa = cnpj.consultar("00.000.000/0001-91")
        
        print(f"Razão Social: {empresa['razao_social']}")
        print(f"Nome Fantasia: {empresa['nome_fantasia']}")
        print(f"Situação: {empresa['situacao_cadastral']}")
        print(f"Data de Abertura: {empresa['data_abertura']}")
        print(f"Município: {empresa['municipio']}/{empresa['uf']}")
        print(f"CNAE Principal: {empresa['cnae_fiscal_descricao']}")
        
    except Exception as e:
        print(f"Erro ao consultar CNPJ: {e}")


def exemplo_consulta_detalhada() -> None:
    """Demonstra uma consulta detalhada, incluindo sócios."""
    print("\n" + "=" * 60)
    print("CONSULTA DETALHADA DE CNPJ (PETROBRAS)")
    print("=" * 60)
    
    try:
        # CNPJ público da Petrobras
        empresa = cnpj.consultar("33.000.167/0001-01")
        
        print(f"Razão Social: {empresa['razao_social']}")
        print(f"Capital Social: R$ {empresa['capital_social']:.2f}")
        print(f"Endereço: {empresa['logradouro']}, {empresa['numero']} - {empresa['bairro']}")
        
        if empresa['socios']:
            print("\nQuadro de Sócios/Administradores:")
            for socio in empresa['socios'][:5]: # Mostra os primeiros 5
                print(f"  - {socio['nome']} ({socio['qualificacao']})")
        else:
            print("\nQuadro de sócios não disponível.")
            
    except Exception as e:
        print(f"Erro ao consultar CNPJ: {e}")


def main() -> None:
    """Executa todos os exemplos."""
    print("🦜 TUCANO - DEMONSTRAÇÃO DE CONSULTA DE CNPJ\n")
    
    exemplo_consulta_simples()
    exemplo_consulta_detalhada()
    
    print("\n" + "=" * 60)
    print("✅ Demonstração completa!")
    print("=" * 60)


if __name__ == "__main__":
    main()