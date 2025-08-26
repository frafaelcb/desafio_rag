"""
Sistema de estados para navegação de menus
Implementa State Pattern
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from .menu_builder import Menu, MenuFactory
from src.rag_chain import RAGChain
from src.commands.command_factory import CommandFactory


class MenuState(ABC):
    """Estado base para navegação de menus"""
    
    def __init__(self, context: 'MenuContext'):
        self.context = context
    
    @abstractmethod
    def display(self) -> Optional['MenuState']:
        """Exibe o menu e retorna o próximo estado"""
        pass
    
    @abstractmethod
    def handle_input(self, choice: str) -> Optional['MenuState']:
        """Processa input do usuário e retorna o próximo estado"""
        pass


class MainMenuState(MenuState):
    """Estado do menu principal"""
    
    def display(self) -> Optional['MenuState']:
        menu = MenuFactory.create_main_menu()
        self.context.display_menu(menu)
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        handlers = {
            "0": lambda: None,  # Sair
            "1": lambda: InfoState(self.context),
            "2": lambda: IndexMenuState(self.context),
            "3": lambda: ChatMenuState(self.context),
            "4": lambda: SearchMenuState(self.context),
            "5": lambda: InteractiveModeState(self.context),
            "6": lambda: TestState(self.context),
            "7": lambda: HelpState(self.context)
        }
        
        handler = handlers.get(choice)
        if handler:
            return handler()
        else:
            self.context.display_message("❌ Opção inválida. Tente novamente.")
            return self


class IndexMenuState(MenuState):
    """Estado do menu de indexação"""
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        docs_dir = Path("data/documents")
        pdf_files = []
        indexed_pdfs = []
        
        if docs_dir.exists():
            pdf_files = [str(pdf) for pdf in docs_dir.glob("*.pdf")]
            for pdf_path in pdf_files:
                doc_info = self.context.rag.vector_store_manager.get_document_info(pdf_path)
                if doc_info["exists"]:
                    indexed_pdfs.append(pdf_path)
        
        if pdf_files:
            menu = MenuFactory.create_index_menu(pdf_files, indexed_pdfs)
            self.context.display_menu(menu)
        else:
            self.context.display_message("📁 Nenhum PDF encontrado em data/documents/")
            self.context.display_message("1. 📁 Especificar caminho manualmente")
            self.context.display_message("2. ⬅️ Voltar ao menu principal")
        
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        from pathlib import Path
        
        docs_dir = Path("data/documents")
        if not docs_dir.exists():
            if choice == "1":
                return ManualIndexState(self.context)
            elif choice == "2":
                return MainMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        
        pdf_files = [str(pdf) for pdf in docs_dir.glob("*.pdf")]
        
        if not pdf_files:
            if choice == "1":
                return ManualIndexState(self.context)
            elif choice == "2":
                return MainMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        
        try:
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(pdf_files):
                pdf_path = pdf_files[choice_num - 1]
                return PDFOptionsState(self.context, pdf_path)
            elif choice_num == len(pdf_files) + 1:
                return ManualIndexState(self.context)
            elif choice_num == len(pdf_files) + 2:
                return ReindexMenuState(self.context)
            elif choice_num == len(pdf_files) + 3:
                return RemoveMenuState(self.context)
            elif choice_num == len(pdf_files) + 4:
                return MainMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        except ValueError:
            self.context.display_message("❌ Por favor, digite um número válido.")
            return self


class PDFOptionsState(MenuState):
    """Estado para opções de um PDF específico"""
    
    def __init__(self, context: 'MenuContext', pdf_path: str):
        super().__init__(context)
        self.pdf_path = pdf_path
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        pdf_name = Path(self.pdf_path).name
        doc_info = self.context.rag.vector_store_manager.get_document_info(self.pdf_path)
        
        menu = MenuFactory.create_pdf_options_menu(
            pdf_name, 
            doc_info["exists"], 
            doc_info["chunks_count"]
        )
        self.context.display_menu(menu)
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        from pathlib import Path
        
        pdf_name = Path(self.pdf_path).name
        doc_info = self.context.rag.vector_store_manager.get_document_info(self.pdf_path)
        
        if doc_info["exists"]:
            if choice == "1":
                return ConfirmReindexState(self.context, self.pdf_path)
            elif choice == "2":
                return PDFInfoState(self.context, self.pdf_path)
            elif choice == "3":
                return IndexMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        else:
            if choice == "1":
                return self._index_pdf()
            elif choice == "3":
                return IndexMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
    
    def _index_pdf(self) -> 'MenuState':
        try:
            command = self.context.command_factory.create_command('index', self.context.rag)
            result = command.execute(pdf_path=self.pdf_path, force=False)
            
            if result.get('success', True):
                self.context.display_message("✅ PDF indexado com sucesso!")
            else:
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return IndexMenuState(self.context)


class ConfirmReindexState(MenuState):
    """Estado para confirmação de reindexação"""
    
    def __init__(self, context: 'MenuContext', pdf_path: str):
        super().__init__(context)
        self.pdf_path = pdf_path
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        pdf_name = Path(self.pdf_path).name
        menu = MenuFactory.create_confirm_menu(
            "Reindexar", 
            pdf_name, 
            "Isso irá substituir o documento atual no banco de dados."
        )
        self.context.display_menu(menu)
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if choice.lower() in ['s', 'sim', 'y', 'yes']:
            return self._reindex_pdf()
        elif choice.lower() in ['n', 'não', 'nao', 'no']:
            self.context.display_message("❌ Reindexação cancelada.")
            return IndexMenuState(self.context)
        else:
            self.context.display_message("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
            return self
    
    def _reindex_pdf(self) -> 'MenuState':
        try:
            command = self.context.command_factory.create_command('index', self.context.rag)
            result = command.execute(pdf_path=self.pdf_path, force=True)
            
            if result.get('success', True):
                self.context.display_message("✅ PDF reindexado com sucesso!")
            else:
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return IndexMenuState(self.context)


class ManualIndexState(MenuState):
    """Estado para indexação manual"""
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("📁 Digite o caminho completo do PDF:")
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if not choice.strip():
            self.context.display_message("❌ Caminho não fornecido.")
            return IndexMenuState(self.context)
        
        pdf_path = choice.strip()
        
        # Perguntar se quer forçar reindexação
        self.context.display_message("🔄 Forçar reindexação se já existir? (s/N):")
        return ConfirmForceIndexState(self.context, pdf_path)


class ConfirmForceIndexState(MenuState):
    """Estado para confirmação de força na indexação"""
    
    def __init__(self, context: 'MenuContext', pdf_path: str):
        super().__init__(context)
        self.pdf_path = pdf_path
    
    def display(self) -> Optional['MenuState']:
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        force = choice.lower() in ['s', 'sim', 'y', 'yes']
        
        try:
            command = self.context.command_factory.create_command('index', self.context.rag)
            result = command.execute(pdf_path=self.pdf_path, force=force)
            
            if result.get('success', True):
                self.context.display_message("✅ PDF indexado com sucesso!")
            else:
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return IndexMenuState(self.context)


class ChatMenuState(MenuState):
    """Estado do menu de chat"""
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("\n💬 Fazer Pergunta")
        self.context.display_message("-" * 30)
        
        suggestions = [
            "O que é inteligência artificial?",
            "Quais são os tipos de IA?",
            "Quais são as aplicações da IA?",
            "Quais são os desafios da IA?",
            "Resuma o conteúdo em 3 pontos",
            "Pergunta personalizada..."
        ]
        
        self.context.display_message("💡 Sugestões de perguntas:")
        for i, suggestion in enumerate(suggestions, 1):
            self.context.display_message(f"  {i}. {suggestion}")
        
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        suggestions = [
            "O que é inteligência artificial?",
            "Quais são os tipos de IA?",
            "Quais são as aplicações da IA?",
            "Quais são os desafios da IA?",
            "Resuma o conteúdo em 3 pontos",
            "Pergunta personalizada..."
        ]
        
        try:
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(suggestions) - 1:
                query = suggestions[choice_num - 1]
                return self._process_chat(query)
            elif choice_num == len(suggestions):
                self.context.display_message("❓ Digite sua pergunta:")
                return CustomChatState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        except ValueError:
            self.context.display_message("❌ Por favor, digite um número válido.")
            return self
    
    def _process_chat(self, query: str) -> 'MenuState':
        try:
            command = self.context.command_factory.create_command('chat', self.context.rag)
            result = command.execute(query=query, show_sources=True)
            
            if not result.get('success', True):
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return MainMenuState(self.context)


class CustomChatState(MenuState):
    """Estado para chat personalizado"""
    
    def display(self) -> Optional['MenuState']:
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if not choice.strip():
            self.context.display_message("❌ Pergunta não fornecida.")
            return ChatMenuState(self.context)
        
        try:
            command = self.context.command_factory.create_command('chat', self.context.rag)
            result = command.execute(query=choice.strip(), show_sources=True)
            
            if not result.get('success', True):
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return MainMenuState(self.context)


class SearchMenuState(MenuState):
    """Estado do menu de busca"""
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("\n🔍 Buscar Documentos")
        self.context.display_message("-" * 30)
        
        suggestions = [
            "inteligência artificial",
            "machine learning",
            "deep learning",
            "processamento de linguagem natural",
            "aplicações da IA",
            "desafios da IA",
            "Termo personalizado..."
        ]
        
        self.context.display_message("🔍 Sugestões de busca:")
        for i, suggestion in enumerate(suggestions, 1):
            self.context.display_message(f"  {i}. {suggestion}")
        
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        suggestions = [
            "inteligência artificial",
            "machine learning",
            "deep learning",
            "processamento de linguagem natural",
            "aplicações da IA",
            "desafios da IA",
            "Termo personalizado..."
        ]
        
        try:
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(suggestions) - 1:
                query = suggestions[choice_num - 1]
                return SearchResultsState(self.context, query)
            elif choice_num == len(suggestions):
                self.context.display_message("🔍 Digite o termo de busca:")
                return CustomSearchState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        except ValueError:
            self.context.display_message("❌ Por favor, digite um número válido.")
            return self


class CustomSearchState(MenuState):
    """Estado para busca personalizada"""
    
    def display(self) -> Optional['MenuState']:
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if not choice.strip():
            self.context.display_message("❌ Termo não fornecido.")
            return SearchMenuState(self.context)
        
        return SearchResultsState(self.context, choice.strip())


class SearchResultsState(MenuState):
    """Estado para resultados de busca"""
    
    def __init__(self, context: 'MenuContext', query: str):
        super().__init__(context)
        self.query = query
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("📊 Número de resultados (padrão: 3):")
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        try:
            k = int(choice) if choice.strip() else 3
        except ValueError:
            self.context.display_message("❌ Número inválido. Usando padrão: 3")
            k = 3
        
        try:
            command = self.context.command_factory.create_command('search', self.context.rag)
            result = command.execute(query=self.query, k=k)
            
            if not result.get('success', True):
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return MainMenuState(self.context)


class InteractiveModeState(MenuState):
    """Estado do modo interativo"""
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("🤖 Modo Interativo - Sistema RAG")
        self.context.display_message("Digite 'sair' para encerrar")
        self.context.display_message("Digite 'info' para ver informações da coleção")
        self.context.display_message("-" * 50)
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if not choice.strip():
            return self
        
        if choice.lower() in ['sair', 'exit', 'quit']:
            self.context.display_message("👋 Encerrando modo interativo...")
            return MainMenuState(self.context)
        
        if choice.lower() == 'info':
            try:
                command = self.context.command_factory.create_command('info', self.context.rag)
                command.execute()
            except Exception as e:
                self.context.display_message(f"❌ Erro: {str(e)}")
            return self
        
        # Processar pergunta
        try:
            command = self.context.command_factory.create_command('chat', self.context.rag)
            result = command.execute(query=choice, show_sources=True)
            
            if not result.get('success', True):
                self.context.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return self


class TestState(MenuState):
    """Estado para teste de conexões"""
    
    def display(self) -> Optional['MenuState']:
        try:
            command = self.context.command_factory.create_command('test', self.context.rag)
            command.execute()
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return MainMenuState(self.context)
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        return MainMenuState(self.context)


class HelpState(MenuState):
    """Estado para ajuda"""
    
    def display(self) -> Optional['MenuState']:
        self.context.display_message("\n📖 Ajuda - Sistema RAG")
        self.context.display_message("=" * 50)
        self.context.display_message("""
🤖 O que é o Sistema RAG?

RAG (Retrieval-Augmented Generation) é uma técnica que combina:
• Recuperação: Busca documentos relevantes em uma base de conhecimento
• Geração: Usa um modelo de linguagem para gerar respostas baseadas nos documentos

📋 Como usar:

1. 📄 Indexar PDFs: Adicione documentos PDF ao sistema
2. 💬 Fazer perguntas: O sistema responde baseado nos documentos indexados
3. 🔍 Buscar documentos: Encontre trechos similares aos seus termos de busca

🛠️ Comandos de linha de comando:
• python src/main.py info          # Ver informações
• python src/main.py index file.pdf # Indexar PDF
• python src/main.py chat "pergunta" # Fazer pergunta
• python src/main.py search "termo"  # Buscar documentos

📁 Estrutura de arquivos:
• data/documents/     # Coloque seus PDFs aqui
• .env               # Configurações (OpenAI API key, etc.)
• docker-compose.yml # Configuração do banco de dados

🔧 Configuração necessária:
• Docker e Docker Compose
• Chave da API OpenAI
• Python 3.11+
        """)
        return MainMenuState(self.context)
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        return MainMenuState(self.context)


class InfoState(MenuState):
    """Estado para informações do sistema"""
    
    def display(self) -> Optional['MenuState']:
        try:
            command = self.context.command_factory.create_command('info', self.context.rag)
            command.execute()
        except Exception as e:
            self.context.display_message(f"❌ Erro: {str(e)}")
        
        return MainMenuState(self.context)
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        return MainMenuState(self.context)


class ReindexMenuState(MenuState):
    """Estado para reindexar PDFs existentes"""
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        self.context.display_message("\n🔄 Reindexar PDFs Existentes")
        self.context.display_message("-" * 40)
        
        docs_dir = Path("data/documents")
        if docs_dir.exists():
            pdf_files = list(docs_dir.glob("*.pdf"))
            indexed_pdfs = []
            
            for pdf in pdf_files:
                doc_info = self.context.rag.vector_store_manager.get_document_info(str(pdf))
                if doc_info["exists"]:
                    indexed_pdfs.append((str(pdf), doc_info))
            
            if indexed_pdfs:
                self.context.display_message("📁 PDFs já indexados:")
                for i, (pdf_path, doc_info) in enumerate(indexed_pdfs, 1):
                    pdf_name = Path(pdf_path).name
                    self.context.display_message(f"  {i}. {pdf_name} ({doc_info['chunks_count']} chunks)")
                
                self.context.display_message(f"  {len(indexed_pdfs) + 1}. ⬅️ Voltar")
            else:
                self.context.display_message("❌ Nenhum PDF indexado encontrado.")
                return IndexMenuState(self.context)
        else:
            self.context.display_message("❌ Diretório data/documents/ não encontrado.")
            return IndexMenuState(self.context)
        
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        from pathlib import Path
        
        docs_dir = Path("data/documents")
        if not docs_dir.exists():
            return IndexMenuState(self.context)
        
        pdf_files = list(docs_dir.glob("*.pdf"))
        indexed_pdfs = []
        
        for pdf in pdf_files:
            doc_info = self.context.rag.vector_store_manager.get_document_info(str(pdf))
            if doc_info["exists"]:
                indexed_pdfs.append((str(pdf), doc_info))
        
        if not indexed_pdfs:
            return IndexMenuState(self.context)
        
        try:
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(indexed_pdfs):
                pdf_path = indexed_pdfs[choice_num - 1][0]
                return ConfirmReindexState(self.context, pdf_path)
            elif choice_num == len(indexed_pdfs) + 1:
                return IndexMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        except ValueError:
            self.context.display_message("❌ Por favor, digite um número válido.")
            return self


class RemoveMenuState(MenuState):
    """Estado para remover PDFs indexados"""
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        self.context.display_message("\n🗑️ Remover PDFs Indexados")
        self.context.display_message("-" * 40)
        
        docs_dir = Path("data/documents")
        if docs_dir.exists():
            pdf_files = list(docs_dir.glob("*.pdf"))
            indexed_pdfs = []
            
            for pdf in pdf_files:
                doc_info = self.context.rag.vector_store_manager.get_document_info(str(pdf))
                if doc_info["exists"]:
                    indexed_pdfs.append((str(pdf), doc_info))
            
            if indexed_pdfs:
                self.context.display_message("📁 PDFs indexados:")
                for i, (pdf_path, doc_info) in enumerate(indexed_pdfs, 1):
                    pdf_name = Path(pdf_path).name
                    self.context.display_message(f"  {i}. {pdf_name} ({doc_info['chunks_count']} chunks)")
                
                self.context.display_message(f"  {len(indexed_pdfs) + 1}. ⬅️ Voltar")
            else:
                self.context.display_message("❌ Nenhum PDF indexado encontrado.")
                return IndexMenuState(self.context)
        else:
            self.context.display_message("❌ Diretório data/documents/ não encontrado.")
            return IndexMenuState(self.context)
        
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        from pathlib import Path
        
        docs_dir = Path("data/documents")
        if not docs_dir.exists():
            return IndexMenuState(self.context)
        
        pdf_files = list(docs_dir.glob("*.pdf"))
        indexed_pdfs = []
        
        for pdf in pdf_files:
            doc_info = self.context.rag.vector_store_manager.get_document_info(str(pdf))
            if doc_info["exists"]:
                indexed_pdfs.append((str(pdf), doc_info))
        
        if not indexed_pdfs:
            return IndexMenuState(self.context)
        
        try:
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(indexed_pdfs):
                pdf_path = indexed_pdfs[choice_num - 1][0]
                return ConfirmRemoveState(self.context, pdf_path)
            elif choice_num == len(indexed_pdfs) + 1:
                return IndexMenuState(self.context)
            else:
                self.context.display_message("❌ Opção inválida.")
                return self
        except ValueError:
            self.context.display_message("❌ Por favor, digite um número válido.")
            return self


class ConfirmRemoveState(MenuState):
    """Estado para confirmação de remoção"""
    
    def __init__(self, context: 'MenuContext', pdf_path: str):
        super().__init__(context)
        self.pdf_path = pdf_path
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        pdf_name = Path(self.pdf_path).name
        menu = MenuFactory.create_confirm_menu(
            "Remover", 
            pdf_name, 
            "Isso irá remover o documento do banco de dados."
        )
        self.context.display_menu(menu)
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        if choice.lower() in ['s', 'sim', 'y', 'yes']:
            try:
                success = self.context.rag.vector_store_manager.remove_document(self.pdf_path)
                if success:
                    from pathlib import Path
                    pdf_name = Path(self.pdf_path).name
                    self.context.display_message(f"✅ {pdf_name} removido com sucesso!")
                else:
                    self.context.display_message(f"❌ Erro ao remover documento")
            except Exception as e:
                self.context.display_message(f"❌ Erro: {str(e)}")
        elif choice.lower() in ['n', 'não', 'nao', 'no']:
            self.context.display_message("❌ Remoção cancelada.")
        else:
            self.context.display_message("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
            return self
        
        return RemoveMenuState(self.context)


class PDFInfoState(MenuState):
    """Estado para informações de PDF"""
    
    def __init__(self, context: 'MenuContext', pdf_path: str):
        super().__init__(context)
        self.pdf_path = pdf_path
    
    def display(self) -> Optional['MenuState']:
        from pathlib import Path
        
        pdf_name = Path(self.pdf_path).name
        doc_info = self.context.rag.vector_store_manager.get_document_info(self.pdf_path)
        
        self.context.display_message(f"\n📊 Informações do PDF: {pdf_name}")
        self.context.display_message("-" * 40)
        self.context.display_message(f"📁 Caminho: {self.pdf_path}")
        self.context.display_message(f"📄 Status: {'✅ Indexado' if doc_info['exists'] else '❌ Não indexado'}")
        if doc_info["exists"]:
            self.context.display_message(f"🔢 Chunks: {doc_info['chunks_count']}")
        
        self.context.display_message("\nPressione Enter para continuar...")
        return None
    
    def handle_input(self, choice: str) -> Optional['MenuState']:
        return PDFOptionsState(self.context, self.pdf_path)


class MenuContext:
    """Contexto para gerenciamento de estados de menu"""
    
    def __init__(self, rag: RAGChain, strategy):
        self.rag = rag
        self.strategy = strategy
        self.command_factory = CommandFactory()
        self.current_state: Optional[MenuState] = None
        self.running = True
    
    def set_state(self, state: MenuState):
        """Define o estado atual"""
        self.current_state = state
    
    def display_menu(self, menu: Menu):
        """Exibe um menu"""
        print(f"\n{menu.title}")
        if menu.subtitle:
            print(menu.subtitle)
        print(menu.separator * menu.separator_length)
        
        for option in menu.options:
            if option.key:  # Não exibir separadores
                print(f"{option.key}. {option.icon}{option.description}")
    
    def display_message(self, message: str):
        """Exibe uma mensagem"""
        self.strategy.display_message(message)
    
    def get_input(self) -> str:
        """Obtém input do usuário"""
        return self.strategy.get_input("\n🎯 Escolha uma opção: ")
    
    def run(self):
        """Executa o loop principal do menu"""
        self.set_state(MainMenuState(self))
        
        while self.running and self.current_state:
            try:
                # Exibir estado atual
                next_state = self.current_state.display()
                
                if next_state:
                    self.set_state(next_state)
                    continue
                
                # Obter input do usuário
                choice = self.get_input()
                
                # Processar input
                next_state = self.current_state.handle_input(choice)
                
                if next_state:
                    self.set_state(next_state)
                elif next_state is None and choice == "0":
                    self.running = False
                    
            except KeyboardInterrupt:
                self.display_message("\n👋 Encerrando...")
                break
            except Exception as e:
                self.display_message(f"❌ Erro: {str(e)}")
                self.set_state(MainMenuState(self))
