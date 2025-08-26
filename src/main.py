#!/usr/bin/env python3
"""
Sistema RAG com PostgreSQL e pgvector
Interface de linha de comando para indexar PDFs e fazer perguntas
"""

import argparse
import sys
import os
from pathlib import Path

# Adicionar o diretório pai ao path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.rag_chain import RAGChain
    from src.config import Config
    from src.commands.command_factory import CommandFactory
    from src.ui.menu_manager import MenuManager
except ImportError:
    # Fallback para imports relativos quando executado como módulo
    from .rag_chain import RAGChain
    from .config import Config
    from .commands.command_factory import CommandFactory
    from .ui.menu_manager import MenuManager


def main():
    """Função principal da interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description="Sistema RAG - Indexar PDFs e fazer perguntas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Indexar um PDF
  python src/main.py index /caminho/para/documento.pdf
  
  # Fazer uma pergunta
  python src/main.py chat "Qual é o tema principal do documento?"
  
  # Buscar documentos similares
  python src/main.py search "palavra-chave"
  
  # Ver informações da coleção
  python src/main.py info
  
  # Menu interativo (sem argumentos)
  python src/main.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando para indexar PDF
    index_parser = subparsers.add_parser('index', help='Indexar um PDF')
    index_parser.add_argument('pdf_path', help='Caminho para o arquivo PDF')
    index_parser.add_argument('--force', action='store_true', help='Forçar reindexação mesmo se já existir')
    
    # Comando para chat
    chat_parser = subparsers.add_parser('chat', help='Fazer uma pergunta')
    chat_parser.add_argument('query', help='Pergunta a ser respondida')
    chat_parser.add_argument('--no-sources', action='store_true', help='Não mostrar fontes')
    
    # Comando para busca
    search_parser = subparsers.add_parser('search', help='Buscar documentos similares')
    search_parser.add_argument('query', help='Query de busca')
    search_parser.add_argument('-k', type=int, default=3, help='Número de resultados (padrão: 3)')
    
    # Comando para informações
    info_parser = subparsers.add_parser('info', help='Ver informações da coleção')
    
    # Comando para teste
    test_parser = subparsers.add_parser('test', help='Testar conexões')
    
    # Comando interativo
    interactive_parser = subparsers.add_parser('interactive', help='Modo interativo')
    
    args = parser.parse_args()
    
    # Se não há comando, mostrar menu interativo
    if not args.command:
        return show_menu()
    
    try:
        # Validar configurações
        if not Config.validate_config():
            print("❌ Configurações inválidas. Verifique o arquivo .env")
            print("\nVariáveis necessárias:")
            print("  - OPENAI_API_KEY")
            print("  - POSTGRES_PASSWORD")
            return 1
        
        # Inicializar RAG e Command Factory
        rag = RAGChain()
        command_factory = CommandFactory()
        
        # Executar comando usando Command Pattern
        if command_factory.has_command(args.command):
            command = command_factory.create_command(args.command, rag)
            
            # Preparar parâmetros baseado no comando
            params = {}
            if args.command == 'index':
                params = {'pdf_path': args.pdf_path, 'force': args.force}
            elif args.command == 'chat':
                params = {'query': args.query, 'show_sources': not args.no_sources}
            elif args.command == 'search':
                params = {'query': args.query, 'k': args.k}
            elif args.command == 'interactive':
                return show_menu()
            
            # Executar comando
            result = command.execute(**params)
            
            if not result.get('success', True):
                return 1
        else:
            print(f"❌ Comando '{args.command}' não reconhecido")
            return 1
            
    except KeyboardInterrupt:
        print("\n👋 Encerrando...")
        return 0
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1
    
    return 0


def show_menu():
    """Mostra o menu interativo principal"""
    try:
        # Validar configurações
        if not Config.validate_config():
            print("❌ Configurações inválidas. Verifique o arquivo .env")
            print("\nVariáveis necessárias:")
            print("  - OPENAI_API_KEY")
            print("  - POSTGRES_PASSWORD")
            return 1
        
        # Inicializar RAG e Menu Manager
        rag = RAGChain()
        menu_manager = MenuManager(rag)
        
        # Executar menu
        menu_manager.run()
                
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
