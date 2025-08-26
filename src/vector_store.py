from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from typing import List, Optional
import os

from .config import Config

class VectorStoreManager:
    """Gerenciador do vector store PostgreSQL com pgvector"""
    
    def __init__(self):
        """Inicializa o vector store manager"""
        if not Config.validate_config():
            raise ValueError("Configurações inválidas. Verifique as variáveis de ambiente.")
        
        # Embeddings
        self.embeddings = OpenAIEmbeddings(
            model=Config.OPENAI_EMBEDDING_MODEL,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Vector store
        self.vectorstore = PGVector(
            connection_string=Config.get_connection_string(),
            embedding_function=self.embeddings,
            collection_name=Config.COLLECTION_NAME,
        )
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def index_pdf(self, pdf_path: str) -> int:
        """
        Carrega um PDF, divide em chunks e indexa no PostgreSQL
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Número de chunks indexados
        """
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
            
            # Carregar PDF
            print(f"📖 Carregando PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            
            # Dividir em chunks
            print(f"✂️ Dividindo em chunks...")
            chunks = self.text_splitter.split_documents(docs)
            
            # Indexar no PostgreSQL
            print(f"💾 Indexando {len(chunks)} chunks no PostgreSQL...")
            self.vectorstore.add_documents(chunks)
            
            print(f"✅ PDF {pdf_path} indexado com sucesso! ({len(chunks)} chunks)")
            return len(chunks)
            
        except Exception as e:
            print(f"❌ Erro ao indexar PDF {pdf_path}: {str(e)}")
            raise
    
    def search_similar(self, query: str, k: Optional[int] = None) -> List:
        """
        Busca documentos similares no vector store
        
        Args:
            query: Query de busca
            k: Número de resultados (padrão: Config.SEARCH_K)
            
        Returns:
            Lista de documentos similares
        """
        k = k or Config.SEARCH_K
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            print(f"🔍 Encontrados {len(results)} documentos similares")
            return results
            
        except Exception as e:
            print(f"❌ Erro na busca: {str(e)}")
            raise
    
    def get_retriever(self, k: Optional[int] = None):
        """
        Retorna um retriever configurado
        
        Args:
            k: Número de resultados (padrão: Config.SEARCH_K)
            
        Returns:
            Retriever configurado
        """
        k = k or Config.SEARCH_K
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
    
    def get_collection_info(self) -> dict:
        """
        Retorna informações sobre a coleção
        
        Returns:
            Dicionário com informações da coleção
        """
        try:
            # Tentar buscar um documento para verificar se a coleção existe
            docs = self.vectorstore.similarity_search("test", k=1)
            return {
                "collection_name": Config.COLLECTION_NAME,
                "has_documents": len(docs) > 0,
                "embedding_model": Config.OPENAI_EMBEDDING_MODEL
            }
        except Exception:
            return {
                "collection_name": Config.COLLECTION_NAME,
                "has_documents": False,
                "embedding_model": Config.OPENAI_EMBEDDING_MODEL
            }
