"""
Comando para mostrar informações do sistema
"""

from typing import Dict, Any
from .base_command import BaseCommand


class InfoCommand(BaseCommand):
    """Comando para mostrar informações da coleção"""
    
    def get_description(self) -> str:
        return "Ver informações da coleção"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa o comando de informações"""
        try:
            info = self.rag.get_collection_info()
            
            print("📊 Informações da Coleção:")
            print(f"   Nome: {info['collection_name']}")
            print(f"   Tem documentos: {'✅ Sim' if info['has_documents'] else '❌ Não'}")
            print(f"   Modelo de embedding: {info['embedding_model']}")
            
            return {
                "success": True,
                "info": info,
                "message": "Informações exibidas com sucesso"
            }
            
        except Exception as e:
            error_msg = f"Erro ao obter informações: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
