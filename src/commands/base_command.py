"""
Classe base para todos os comandos do sistema RAG
Implementa o Command Pattern
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from src.rag_chain import RAGChain


class BaseCommand(ABC):
    """Classe base abstrata para todos os comandos"""
    
    def __init__(self, rag: RAGChain):
        self.rag = rag
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Executa o comando
        
        Returns:
            Dicionário com resultado da execução
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Retorna descrição do comando"""
        pass
    
    def get_name(self) -> str:
        """Retorna nome do comando"""
        return self.__class__.__name__.lower().replace('command', '')
    
    def validate(self, **kwargs) -> bool:
        """
        Valida parâmetros do comando
        
        Returns:
            True se válido, False caso contrário
        """
        return True
    
    def get_help(self) -> str:
        """Retorna ajuda do comando"""
        return f"{self.get_name()}: {self.get_description()}"
