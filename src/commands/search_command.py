"""
Comando para busca de documentos
"""

from typing import Dict, Any
from .base_command import BaseCommand


class SearchCommand(BaseCommand):
    """Comando para buscar documentos similares"""
    
    def get_description(self) -> str:
        return "Buscar documentos similares"
    
    def validate(self, **kwargs) -> bool:
        """Valida parâmetros do comando"""
        query = kwargs.get('query')
        
        if not query or not query.strip():
            print("❌ Termo de busca não fornecido")
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa o comando de busca"""
        try:
            query = kwargs.get('query')
            k = kwargs.get('k', 3)
            
            if not self.validate(query=query):
                return {
                    "success": False,
                    "error": "Termo de busca não fornecido"
                }
            
            print(f"🔍 Buscando documentos similares a: '{query}'")
            docs = self.rag.search_only(query, k)
            
            print(f"\n📚 Documentos encontrados ({len(docs)}):")
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "Desconhecido")
                page = doc.metadata.get("page", "N/A")
                print(f"\n{i}. {source} | Página: {page}")
                print(f"   Conteúdo: {doc.page_content[:300]}...")
            
            return {
                "success": True,
                "query": query,
                "results": docs,
                "count": len(docs),
                "message": f"Busca concluída: {len(docs)} documentos encontrados"
            }
            
        except Exception as e:
            error_msg = f"Erro na busca: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
