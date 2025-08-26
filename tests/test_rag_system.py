import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from pathlib import Path

from src.config import Config
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain

class TestConfig:
    """Testes para a configuração"""
    
    def test_connection_string(self):
        """Testa a geração da string de conexão"""
        Config.POSTGRES_USER = "test_user"
        Config.POSTGRES_PASSWORD = "test_pass"
        Config.POSTGRES_HOST = "localhost"
        Config.POSTGRES_PORT = "5432"
        Config.POSTGRES_DB = "test_db"
        
        expected = "postgresql+psycopg2://test_user:test_pass@localhost:5432/test_db"
        assert Config.get_connection_string() == expected
    
    def test_validate_config_missing_vars(self):
        """Testa validação com variáveis faltando"""
        with patch.dict(os.environ, {}, clear=True):
            Config.OPENAI_API_KEY = None
            Config.POSTGRES_PASSWORD = None
            assert Config.validate_config() is False

class TestVectorStoreManager:
    """Testes para o gerenciador de vector store"""
    
    @patch('src.vector_store.OpenAIEmbeddings')
    @patch('src.vector_store.PGVector')
    def test_init(self, mock_pgvector, mock_embeddings):
        """Testa inicialização do vector store manager"""
        with patch('src.config.Config.validate_config', return_value=True):
            manager = VectorStoreManager()
            assert manager is not None
            mock_embeddings.assert_called_once()
            mock_pgvector.assert_called_once()
    
    def test_index_pdf_file_not_found(self):
        """Testa indexação com arquivo inexistente"""
        with patch('src.config.Config.validate_config', return_value=True):
            with patch('src.vector_store.OpenAIEmbeddings'):
                with patch('src.vector_store.PGVector'):
                    manager = VectorStoreManager()
                    
                    with pytest.raises(FileNotFoundError):
                        manager.index_pdf("arquivo_inexistente.pdf")

class TestRAGChain:
    """Testes para o pipeline RAG"""
    
    @patch('src.rag_chain.ChatOpenAI')
    @patch('src.rag_chain.VectorStoreManager')
    def test_init(self, mock_vector_store, mock_llm):
        """Testa inicialização do RAG chain"""
        with patch('src.config.Config.validate_config', return_value=True):
            rag = RAGChain()
            assert rag is not None
            mock_llm.assert_called_once()
    
    @patch('src.rag_chain.ChatOpenAI')
    @patch('src.rag_chain.VectorStoreManager')
    def test_chat(self, mock_vector_store, mock_llm):
        """Testa o método chat"""
        with patch('src.config.Config.validate_config', return_value=True):
            # Mock do resultado da chain
            mock_result = {
                'result': 'Resposta de teste',
                'source_documents': [
                    Mock(metadata={'source': 'test.pdf', 'page': 1}, page_content='Conteúdo de teste')
                ]
            }
            
            # Mock da chain
            mock_chain = Mock()
            mock_chain.invoke.return_value = mock_result
            
            rag = RAGChain()
            rag.qa_chain = mock_chain
            
            result = rag.chat("Pergunta de teste")
            assert result == mock_result
            mock_chain.invoke.assert_called_once_with({"query": "Pergunta de teste"})

class TestIntegration:
    """Testes de integração"""
    
    def test_config_loading(self):
        """Testa carregamento de configurações"""
        # Testa se as configurações padrão são carregadas
        assert hasattr(Config, 'OPENAI_MODEL')
        assert hasattr(Config, 'POSTGRES_HOST')
        assert hasattr(Config, 'COLLECTION_NAME')
    
    def test_required_dependencies(self):
        """Testa se as dependências necessárias estão disponíveis"""
        try:
            import langchain
            import openai
            import psycopg2
            import pgvector
            assert True
        except ImportError as e:
            pytest.fail(f"Dependência não encontrada: {e}")

# Fixtures para testes
@pytest.fixture
def sample_pdf_path():
    """Cria um arquivo PDF temporário para testes"""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        # Conteúdo mínimo de PDF
        f.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n')
        f.flush()
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_env_vars():
    """Mock das variáveis de ambiente"""
    env_vars = {
        'OPENAI_API_KEY': 'test_key',
        'POSTGRES_PASSWORD': 'test_password',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'POSTGRES_USER': 'test_user'
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars
