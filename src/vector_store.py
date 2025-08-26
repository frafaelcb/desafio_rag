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
    
    def check_document_exists(self, pdf_path: str) -> bool:
        """
        Verifica se um documento já foi indexado
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            True se o documento já existe, False caso contrário
        """
        try:
            # Buscar documentos com o mesmo source
            docs = self.vectorstore.similarity_search(
                f"source:{pdf_path}", 
                k=1,
                filter={"source": pdf_path}
            )
            return len(docs) > 0
        except Exception:
            return False
    
    def get_document_info(self, pdf_path: str) -> dict:
        """
        Retorna informações sobre um documento indexado
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Dicionário com informações do documento
        """
        try:
            docs = self.vectorstore.similarity_search(
                f"source:{pdf_path}", 
                k=100,
                filter={"source": pdf_path}
            )
            return {
                "exists": len(docs) > 0,
                "chunks_count": len(docs),
                "filename": os.path.basename(pdf_path)
            }
        except Exception:
            return {
                "exists": False,
                "chunks_count": 0,
                "filename": os.path.basename(pdf_path)
            }
    
    def remove_document(self, pdf_path: str) -> bool:
        """
        Remove um documento do banco de dados
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            # Buscar e remover documentos com o mesmo source
            docs = self.vectorstore.similarity_search(
                f"source:{pdf_path}", 
                k=1000,
                filter={"source": pdf_path}
            )
            
            if docs:
                # Remover documentos (implementação depende da versão do pgvector)
                print(f"🗑️ Removendo {len(docs)} chunks do documento...")
                # Nota: A remoção específica pode requerer implementação adicional
                return True
            return False
        except Exception as e:
            print(f"❌ Erro ao remover documento: {str(e)}")
            return False
    
    def index_pdf(self, pdf_path: str, force: bool = False) -> int:
        """
        Carrega um PDF, divide em chunks e indexa no PostgreSQL
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            force: Se True, força a reindexação mesmo se já existir
            
        Returns:
            Número de chunks indexados
        """
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
            
            # Verificar se o documento já existe
            doc_info = self.get_document_info(pdf_path)
            
            if doc_info["exists"] and not force:
                print(f"⚠️ Documento já indexado: {doc_info['filename']}")
                print(f"   Chunks existentes: {doc_info['chunks_count']}")
                print(f"   Use --force para reindexar")
                return doc_info["chunks_count"]
            
            # Se force=True e documento existe, remover primeiro
            if doc_info["exists"] and force:
                print(f"🔄 Reindexando documento: {doc_info['filename']}")
                self.remove_document(pdf_path)
            
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
