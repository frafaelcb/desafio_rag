from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional

from .config import Config
from .vector_store import VectorStoreManager

class RAGChain:
    """Pipeline RAG com LangChain e PostgreSQL"""
    
    def __init__(self, vector_store_manager: Optional[VectorStoreManager] = None):
        """
        Inicializa o pipeline RAG
        
        Args:
            vector_store_manager: Gerenciador do vector store (opcional)
        """
        if not Config.validate_config():
            raise ValueError("Configurações inválidas. Verifique as variáveis de ambiente.")
        
        # Vector store manager
        self.vector_store_manager = vector_store_manager or VectorStoreManager()
        
        # LLM
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            openai_api_key=Config.OPENAI_API_KEY,
            temperature=0.1
        )
        
        # Retriever
        self.retriever = self.vector_store_manager.get_retriever()
        
        # Pipeline RAG
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,
            chain_type="stuff"
        )
    
    def chat(self, query: str, show_sources: bool = True) -> Dict[str, Any]:
        """
        Processa uma pergunta e retorna a resposta baseada nos documentos indexados
        
        Args:
            query: Pergunta do usuário
            show_sources: Se deve mostrar as fontes utilizadas
            
        Returns:
            Dicionário com resposta e fontes
        """
        try:
            print(f"\n❓ Pergunta: {query}")
            
            # Processar pergunta
            result = self.qa_chain.invoke({"query": query})
            
            # Exibir resposta
            print(f"💡 Resposta: {result['result']}")
            
            # Exibir fontes se solicitado
            if show_sources and result.get("source_documents"):
                print(f"\n📚 Fontes utilizadas:")
                for i, doc in enumerate(result["source_documents"], 1):
                    source = doc.metadata.get("source", "Desconhecido")
                    page = doc.metadata.get("page", "N/A")
                    print(f"   {i}. {source} | Página: {page}")
                    
                    # Mostrar trecho do documento
                    content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    print(f"      Trecho: {content_preview}")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {str(e)}")
            raise
    
    def search_only(self, query: str, k: Optional[int] = None) -> list:
        """
        Apenas busca documentos similares sem gerar resposta
        
        Args:
            query: Query de busca
            k: Número de resultados
            
        Returns:
            Lista de documentos similares
        """
        return self.vector_store_manager.search_similar(query, k)
    
    def index_pdf(self, pdf_path: str) -> int:
        """
        Indexa um PDF no vector store
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Returns:
            Número de chunks indexados
        """
        return self.vector_store_manager.index_pdf(pdf_path)
    
    def get_collection_info(self) -> dict:
        """
        Retorna informações sobre a coleção
        
        Returns:
            Dicionário com informações da coleção
        """
        return self.vector_store_manager.get_collection_info()
