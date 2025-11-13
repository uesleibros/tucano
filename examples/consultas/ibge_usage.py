"""Exemplos de uso de consultas de IBGE."""

from tucano.consultas import ibge


def exemplo_estados() -> None:
    """Demonstra listagem e busca de estados."""
    print("=" * 60)
    print("CONSULTA DE ESTADOS (UF)")
    print("=" * 60)
    
    try:
        estados = ibge.listar_estados()
        print(f"Total de estados encontrados: {len(estados)}")
        
        print("\nPrimeiros 5 estados:")
        for estado in estados[:5]:
            print(f"  - {estado['nome']} ({estado['sigla']})")
        
        print("\nBuscando estado 'RJ':")
        rj = ibge.buscar_estado_por_sigla("RJ")
        if rj:
            print(f"  Encontrado: {rj['nome']} - Região: {rj['regiao']['nome']}")
            
    except Exception as e:
        print(f"Erro ao consultar estados: {e}")


def exemplo_municipios() -> None:
    """Demonstra listagem e busca de municípios."""
    print("\n" + "=" * 60)
    print("CONSULTA DE MUNICÍPIOS")
    print("=" * 60)
    
    uf = "SP"
    
    try:
        municipios = ibge.listar_municipios(uf)
        print(f"Total de municípios em {uf}: {len(municipios)}")
        
        print(f"\nBuscando municípios com 'Santo' em {uf}:")
        resultados = ibge.buscar_municipio_por_nome("Santo", uf)
        
        if resultados:
            print(f"Encontrados {len(resultados)} municípios:")
            for municipio in resultados[:5]:
                print(f"  - {municipio['nome']}")
        else:
            print("Nenhum município encontrado.")
            
    except Exception as e:
        print(f"Erro ao consultar municípios: {e}")


def main() -> None:
    """Executa todos os exemplos."""
    print("🦜 TUCANO - DEMONSTRAÇÃO DE CONSULTAS IBGE\n")
    
    exemplo_estados()
    exemplo_municipios()
    
    print("\n" + "=" * 60)
    print("✅ Demonstração completa!")
    print("=" * 60)


if __name__ == "__main__":
    main()