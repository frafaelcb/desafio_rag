#!/usr/bin/env python3
"""
Script para testar conexão com PostgreSQL Docker
"""

import os
import sys
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_postgres_connection():
    """Testa conexão com PostgreSQL"""
    try:
        import psycopg2
        
        # Configurações do banco
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "rag_database")
        user = os.getenv("POSTGRES_USER", "admin")
        password = os.getenv("POSTGRES_PASSWORD", "admin")
        
        print(f"🔍 Testando conexão com PostgreSQL...")
        print(f"   Host: {host}:{port}")
        print(f"   Database: {database}")
        print(f"   User: {user}")
        
        # Tentar conectar
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # Testar query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexão bem-sucedida!")
        print(f"   PostgreSQL: {version[0]}")
        
        # Verificar extensão pgvector
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        pgvector = cursor.fetchone()
        
        if pgvector:
            print(f"✅ Extensão pgvector encontrada!")
        else:
            print(f"❌ Extensão pgvector não encontrada!")
            return False
        
        # Verificar tabela de teste
        cursor.execute("SELECT COUNT(*) FROM test_vectors;")
        count = cursor.fetchone()[0]
        print(f"   Tabela test_vectors: {count} registros")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("❌ psycopg2 não está instalado. Execute: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

def test_openai_connection():
    """Testa conexão com OpenAI"""
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY não configurada no arquivo .env")
            return False
        
        print(f"🔍 Testando conexão com OpenAI...")
        
        # Configurar cliente
        client = openai.OpenAI(api_key=api_key)
        
        # Testar listagem de modelos
        models = client.models.list()
        
        print(f"✅ Conexão com OpenAI bem-sucedida!")
        print(f"   Modelos disponíveis: {len(models.data)}")
        
        return True
        
    except ImportError:
        print("❌ openai não está instalado. Execute: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Erro na conexão com OpenAI: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🧪 Teste de Conexões - Sistema RAG")
    print("=" * 40)
    
    # Testar PostgreSQL
    postgres_ok = test_postgres_connection()
    print()
    
    # Testar OpenAI
    openai_ok = test_openai_connection()
    print()
    
    # Resumo
    print("📊 Resumo dos Testes:")
    print(f"   PostgreSQL: {'✅ OK' if postgres_ok else '❌ FALHOU'}")
    print(f"   OpenAI: {'✅ OK' if openai_ok else '❌ FALHOU'}")
    
    if postgres_ok and openai_ok:
        print("\n🎉 Todos os testes passaram! O sistema está pronto para uso.")
        return 0
    else:
        print("\n⚠️ Alguns testes falharam. Verifique as configurações.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
