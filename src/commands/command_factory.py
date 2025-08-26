"""
Factory para criação de comandos
Implementa o Factory Pattern
"""

from typing import Dict, Type
from .base_command import BaseCommand
from .info_command import InfoCommand
from .index_command import IndexCommand
from .chat_command import ChatCommand
from .search_command import SearchCommand
from .test_command import TestCommand
from src.rag_chain import RAGChain


class CommandFactory:
    """Factory para criação de comandos"""
    
    def __init__(self):
        self._commands: Dict[str, Type[BaseCommand]] = {
            'info': InfoCommand,
            'index': IndexCommand,
            'chat': ChatCommand,
            'search': SearchCommand,
            'test': TestCommand,
        }
    
    def create_command(self, command_name: str, rag: RAGChain) -> BaseCommand:
        """
        Cria um comando baseado no nome
        
        Args:
            command_name: Nome do comando
            rag: Instância do RAGChain
            
        Returns:
            Instância do comando
            
        Raises:
            ValueError: Se o comando não existir
        """
        command_class = self._commands.get(command_name.lower())
        
        if not command_class:
            available_commands = ', '.join(self._commands.keys())
            raise ValueError(f"Comando '{command_name}' não encontrado. Comandos disponíveis: {available_commands}")
        
        return command_class(rag)
    
    def get_available_commands(self) -> Dict[str, str]:
        """
        Retorna lista de comandos disponíveis
        
        Returns:
            Dicionário com nome e descrição dos comandos
        """
        return {
            name: command_class.__doc__ or "Sem descrição"
            for name, command_class in self._commands.items()
        }
    
    def register_command(self, name: str, command_class: Type[BaseCommand]):
        """
        Registra um novo comando
        
        Args:
            name: Nome do comando
            command_class: Classe do comando
        """
        self._commands[name.lower()] = command_class
    
    def has_command(self, command_name: str) -> bool:
        """
        Verifica se um comando existe
        
        Args:
            command_name: Nome do comando
            
        Returns:
            True se existe, False caso contrário
        """
        return command_name.lower() in self._commands
