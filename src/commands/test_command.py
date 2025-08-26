"""
Comando para testar conexões do sistema
"""

from typing import Dict, Any
from .base_command import BaseCommand


class TestCommand(BaseCommand):
    """Comando para testar conexões do sistema"""
    
    def get_description(self) -> str:
        return "Testar conexões do sistema"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa o comando de teste"""
        try:
            print("\n🧪 Testando Conexões")
            print("-" * 30)
            
            # Testar PostgreSQL
            print("🔍 Testando PostgreSQL...")
            try:
                from src.vector_store import VectorStoreManager
            except ImportError:
                from .vector_store import VectorStoreManager
            
            vsm = VectorStoreManager()
            print("✅ PostgreSQL: OK")
            
            # Testar OpenAI
            print("🔍 Testando OpenAI...")
            try:
                from src.config import Config
            except ImportError:
                from .config import Config
            
            import openai
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            models = client.models.list()
            print(f"✅ OpenAI: OK ({len(models.data)} modelos disponíveis)")
            
            print("\n🎉 Todas as conexões estão funcionando!")
            
            return {
                "success": True,
                "postgresql": "OK",
                "openai": f"OK ({len(models.data)} modelos)",
                "message": "Todas as conexões estão funcionando"
            }
            
        except Exception as e:
            error_msg = f"Erro nos testes: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
