"""
Gerenciador de menu interativo refatorado
Implementa Strategy Pattern + State Pattern + Builder Pattern
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from src.rag_chain import RAGChain
from src.commands.command_factory import CommandFactory
from .menu_state import MenuContext


class MenuStrategy(ABC):
    """Estratégia base para interfaces de menu"""
    
    @abstractmethod
    def display_menu(self, options: Dict[str, str]) -> str:
        """Exibe o menu e retorna a escolha do usuário"""
        pass
    
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Obtém input do usuário"""
        pass
    
    @abstractmethod
    def display_message(self, message: str):
        """Exibe uma mensagem"""
        pass


class ConsoleMenuStrategy(MenuStrategy):
    """Estratégia para menu no console"""
    
    def display_menu(self, options: Dict[str, str]) -> str:
        """Exibe menu no console"""
        print("\n📋 Opções disponíveis:")
        for key, description in options.items():
            print(f"{key}. {description}")
        
        return input("\n🎯 Escolha uma opção: ").strip()
    
    def get_input(self, prompt: str) -> str:
        """Obtém input do console"""
        return input(prompt).strip()
    
    def display_message(self, message: str):
        """Exibe mensagem no console"""
        print(message)


class MenuManager:
    """Gerenciador de menu principal refatorado"""
    
    def __init__(self, rag: RAGChain, strategy: MenuStrategy = None):
        self.rag = rag
        self.strategy = strategy or ConsoleMenuStrategy()
        self.context = MenuContext(rag, self.strategy)
    
    def run(self):
        """Executa o menu principal usando State Pattern"""
        self.strategy.display_message("🤖 Sistema RAG - Menu Interativo")
        self.strategy.display_message("=" * 50)
        
        try:
            self.context.run()
        except KeyboardInterrupt:
            self.strategy.display_message("\n👋 Encerrando...")
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
    
