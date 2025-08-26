"""
Comando para chat com o sistema RAG
"""

from typing import Dict, Any
from .base_command import BaseCommand


class ChatCommand(BaseCommand):
    """Comando para fazer perguntas ao sistema"""
    
    def get_description(self) -> str:
        return "Fazer uma pergunta"
    
    def validate(self, **kwargs) -> bool:
        """Valida parâmetros do comando"""
        query = kwargs.get('query')
        
        if not query or not query.strip():
            print("❌ Pergunta não fornecida")
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa o comando de chat"""
        try:
            query = kwargs.get('query')
            show_sources = kwargs.get('show_sources', True)
            
            if not self.validate(query=query):
                return {
                    "success": False,
                    "error": "Pergunta não fornecida"
                }
            
            result = self.rag.chat(query, show_sources)
            
            return {
                "success": True,
                "query": query,
                "result": result,
                "message": "Pergunta processada com sucesso"
            }
            
        except Exception as e:
            error_msg = f"Erro ao processar pergunta: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
