import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações do sistema RAG"""
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # PostgreSQL
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "rag_database")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    
    # Vector Store
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docs_pdf")
    
    # Chunking
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Retrieval
    SEARCH_K = int(os.getenv("SEARCH_K", "3"))
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Retorna a string de conexão do PostgreSQL"""
        return f"postgresql+psycopg2://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida se todas as configurações necessárias estão presentes"""
        required_vars = [
            cls.OPENAI_API_KEY,
            cls.POSTGRES_PASSWORD
        ]
        
        missing_vars = [var for var in required_vars if not var]
        
        if missing_vars:
            print("❌ Variáveis de ambiente faltando:")
            for var in missing_vars:
                print(f"   - {var}")
            return False
        
        return True
