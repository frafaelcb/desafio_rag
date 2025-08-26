#!/usr/bin/env python3
"""
Script executável para o Sistema RAG
Execute este arquivo para acessar o menu interativo
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        from src.main import main
        sys.exit(main())
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Certifique-se de que está no diretório raiz do projeto")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
