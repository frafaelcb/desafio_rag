"""
Comando para indexar PDFs
"""

import os
from typing import Dict, Any
from .base_command import BaseCommand


class IndexCommand(BaseCommand):
    """Comando para indexar PDFs"""
    
    def get_description(self) -> str:
        return "Indexar um PDF"
    
    def validate(self, **kwargs) -> bool:
        """Valida parâmetros do comando"""
        pdf_path = kwargs.get('pdf_path')
        
        if not pdf_path:
            print("❌ Caminho do PDF não fornecido")
            return False
        
        if not os.path.exists(pdf_path):
            print(f"❌ Arquivo não encontrado: {pdf_path}")
            return False
        
        if not pdf_path.lower().endswith('.pdf'):
            print(f"❌ Arquivo deve ser um PDF: {pdf_path}")
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa o comando de indexação"""
        try:
            pdf_path = kwargs.get('pdf_path')
            force = kwargs.get('force', False)
            
            if not self.validate(pdf_path=pdf_path):
                return {
                    "success": False,
                    "error": "Parâmetros inválidos"
                }
            
            print(f"🚀 Iniciando indexação do PDF: {pdf_path}")
            chunks_count = self.rag.index_pdf(pdf_path, force)
            print(f"✅ Indexação concluída! {chunks_count} chunks processados")
            
            return {
                "success": True,
                "chunks_count": chunks_count,
                "pdf_path": pdf_path,
                "message": f"PDF indexado com sucesso: {chunks_count} chunks"
            }
            
        except Exception as e:
            error_msg = f"Erro ao indexar PDF: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
