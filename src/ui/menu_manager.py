"""
Gerenciador de menu interativo
Implementa Strategy Pattern para diferentes tipos de interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from src.rag_chain import RAGChain
from src.commands.command_factory import CommandFactory


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
    """Gerenciador de menu principal"""
    
    def __init__(self, rag: RAGChain, strategy: MenuStrategy = None):
        self.rag = rag
        self.strategy = strategy or ConsoleMenuStrategy()
        self.command_factory = CommandFactory()
        self.running = True
    
    def get_menu_options(self) -> Dict[str, str]:
        """Retorna opções do menu principal"""
        return {
            "1": "📊 Ver informações do sistema",
            "2": "📄 Indexar um PDF",
            "3": "💬 Fazer uma pergunta",
            "4": "🔍 Buscar documentos similares",
            "5": "🤖 Modo chat interativo",
            "6": "🧪 Testar conexões",
            "7": "📖 Ver ajuda",
            "0": "🚪 Sair"
        }
    
    def handle_menu_choice(self, choice: str) -> bool:
        """
        Processa escolha do menu
        
        Returns:
            True se deve continuar, False se deve sair
        """
        handlers = {
            "0": self._handle_exit,
            "1": self._handle_info,
            "2": self._handle_index,
            "3": self._handle_chat,
            "4": self._handle_search,
            "5": self._handle_interactive,
            "6": self._handle_test,
            "7": self._handle_help
        }
        
        handler = handlers.get(choice)
        if handler:
            return handler()
        else:
            self.strategy.display_message("❌ Opção inválida. Tente novamente.")
            return True
    
    def _handle_exit(self) -> bool:
        """Manipula saída do sistema"""
        self.strategy.display_message("👋 Obrigado por usar o Sistema RAG!")
        return False
    
    def _handle_info(self) -> bool:
        """Manipula comando de informações"""
        try:
            command = self.command_factory.create_command('info', self.rag)
            command.execute()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_index(self) -> bool:
        """Manipula comando de indexação"""
        try:
            self._show_index_menu()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_chat(self) -> bool:
        """Manipula comando de chat"""
        try:
            self._show_chat_menu()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_search(self) -> bool:
        """Manipula comando de busca"""
        try:
            self._show_search_menu()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_interactive(self) -> bool:
        """Manipula modo interativo"""
        try:
            self._start_interactive_mode()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_test(self) -> bool:
        """Manipula comando de teste"""
        try:
            command = self.command_factory.create_command('test', self.rag)
            command.execute()
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
        return True
    
    def _handle_help(self) -> bool:
        """Manipula comando de ajuda"""
        self._show_help()
        return True
    
    def _show_index_menu(self):
        """Mostra menu de indexação"""
        from pathlib import Path
        
        print("\n📄 Menu de Indexação")
        print("=" * 50)
        
        # Verificar se há PDFs no diretório data/documents
        docs_dir = Path("data/documents")
        if docs_dir.exists():
            pdf_files = list(docs_dir.glob("*.pdf"))
            if pdf_files:
                print("📁 PDFs encontrados em data/documents:")
                for i, pdf in enumerate(pdf_files, 1):
                    # Verificar se o documento já está indexado
                    doc_info = self.rag.vector_store_manager.get_document_info(str(pdf))
                    status = "✅ Indexado" if doc_info["exists"] else "❌ Não indexado"
                    chunks_info = f"({doc_info['chunks_count']} chunks)" if doc_info["exists"] else ""
                    print(f"  {i}. {pdf.name} - {status} {chunks_info}")
                
                print(f"  {len(pdf_files) + 1}. 📁 Especificar caminho manualmente")
                print(f"  {len(pdf_files) + 2}. 🔄 Reindexar documento existente")
                print(f"  {len(pdf_files) + 3}. 🗑️ Remover documento indexado")
                print(f"  {len(pdf_files) + 4}. ⬅️ Voltar ao menu principal")
                
                try:
                    choice = self.strategy.get_input(f"\n🎯 Escolha uma opção (1-{len(pdf_files) + 4}): ")
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(pdf_files):
                        pdf_path = str(pdf_files[choice_num - 1])
                        self._show_pdf_options(pdf_path)
                    elif choice_num == len(pdf_files) + 1:
                        self._manual_index_pdf()
                    elif choice_num == len(pdf_files) + 2:
                        self._reindex_existing_pdf()
                    elif choice_num == len(pdf_files) + 3:
                        self._remove_indexed_pdf()
                    elif choice_num == len(pdf_files) + 4:
                        return  # Voltar ao menu principal
                    else:
                        self.strategy.display_message("❌ Opção inválida.")
                except ValueError:
                    self.strategy.display_message("❌ Por favor, digite um número válido.")
            else:
                print("📁 Nenhum PDF encontrado em data/documents/")
                print("1. 📁 Especificar caminho manualmente")
                print("2. ⬅️ Voltar ao menu principal")
                
                choice = self.strategy.get_input("\n🎯 Escolha uma opção (1-2): ")
                if choice == "1":
                    self._manual_index_pdf()
                elif choice == "2":
                    return
                else:
                    self.strategy.display_message("❌ Opção inválida.")
        else:
            print("📁 Diretório data/documents/ não encontrado")
            print("1. 📁 Especificar caminho manualmente")
            print("2. ⬅️ Voltar ao menu principal")
            
            choice = self.strategy.get_input("\n🎯 Escolha uma opção (1-2): ")
            if choice == "1":
                self._manual_index_pdf()
            elif choice == "2":
                return
            else:
                self.strategy.display_message("❌ Opção inválida.")
    
    def _show_pdf_options(self, pdf_path: str):
        """Mostra opções específicas para um PDF"""
        from pathlib import Path
        
        pdf_name = Path(pdf_path).name
        doc_info = self.rag.vector_store_manager.get_document_info(pdf_path)
        
        print(f"\n📄 Opções para: {pdf_name}")
        print("-" * 40)
        
        if doc_info["exists"]:
            print(f"✅ Status: Indexado ({doc_info['chunks_count']} chunks)")
            print("\nOpções disponíveis:")
            print("1. 🔄 Reindexar (substituir)")
            print("2. 📊 Ver informações")
            print("3. ⬅️ Voltar")
            
            choice = self.strategy.get_input("\n🎯 Escolha uma opção (1-3): ")
            
            if choice == "1":
                self._confirm_reindex(pdf_path)
            elif choice == "2":
                self._show_pdf_info(pdf_path)
            elif choice == "3":
                return
            else:
                self.strategy.display_message("❌ Opção inválida.")
        else:
            print("❌ Status: Não indexado")
            print("\nOpções disponíveis:")
            print("1. 📥 Indexar")
            print("2. ⬅️ Voltar")
            
            choice = self.strategy.get_input("\n🎯 Escolha uma opção (1-2): ")
            
            if choice == "1":
                self._index_pdf(pdf_path)
            elif choice == "2":
                return
            else:
                self.strategy.display_message("❌ Opção inválida.")
    
    def _confirm_reindex(self, pdf_path: str):
        """Confirma reindexação de um PDF"""
        from pathlib import Path
        
        pdf_name = Path(pdf_path).name
        print(f"\n🔄 Reindexar: {pdf_name}")
        print("⚠️  Isso irá substituir o documento atual no banco de dados.")
        
        confirm = self.strategy.get_input("Tem certeza? (s/N): ").lower()
        if confirm in ['s', 'sim', 'y', 'yes']:
            self._index_pdf(pdf_path, force=True)
        else:
            self.strategy.display_message("❌ Reindexação cancelada.")
    
    def _show_pdf_info(self, pdf_path: str):
        """Mostra informações detalhadas de um PDF"""
        from pathlib import Path
        
        pdf_name = Path(pdf_path).name
        doc_info = self.rag.vector_store_manager.get_document_info(pdf_path)
        
        print(f"\n📊 Informações do PDF: {pdf_name}")
        print("-" * 40)
        print(f"📁 Caminho: {pdf_path}")
        print(f"📄 Status: {'✅ Indexado' if doc_info['exists'] else '❌ Não indexado'}")
        if doc_info["exists"]:
            print(f"🔢 Chunks: {doc_info['chunks_count']}")
        
        self.strategy.get_input("\nPressione Enter para continuar...")
    
    def _reindex_existing_pdf(self):
        """Menu para reindexar PDFs existentes"""
        from pathlib import Path
        
        print("\n🔄 Reindexar PDFs Existentes")
        print("-" * 40)
        
        docs_dir = Path("data/documents")
        if docs_dir.exists():
            pdf_files = list(docs_dir.glob("*.pdf"))
            indexed_pdfs = []
            
            for pdf in pdf_files:
                doc_info = self.rag.vector_store_manager.get_document_info(str(pdf))
                if doc_info["exists"]:
                    indexed_pdfs.append((str(pdf), doc_info))
            
            if indexed_pdfs:
                print("📁 PDFs já indexados:")
                for i, (pdf_path, doc_info) in enumerate(indexed_pdfs, 1):
                    pdf_name = Path(pdf_path).name
                    print(f"  {i}. {pdf_name} ({doc_info['chunks_count']} chunks)")
                
                print(f"  {len(indexed_pdfs) + 1}. ⬅️ Voltar")
                
                try:
                    choice = self.strategy.get_input(f"\n🎯 Escolha um PDF para reindexar (1-{len(indexed_pdfs) + 1}): ")
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(indexed_pdfs):
                        pdf_path = indexed_pdfs[choice_num - 1][0]
                        self._confirm_reindex(pdf_path)
                    elif choice_num == len(indexed_pdfs) + 1:
                        return
                    else:
                        self.strategy.display_message("❌ Opção inválida.")
                except ValueError:
                    self.strategy.display_message("❌ Por favor, digite um número válido.")
            else:
                print("❌ Nenhum PDF indexado encontrado.")
                self.strategy.get_input("\nPressione Enter para continuar...")
        else:
            print("❌ Diretório data/documents/ não encontrado.")
            self.strategy.get_input("\nPressione Enter para continuar...")
    
    def _remove_indexed_pdf(self):
        """Menu para remover PDFs indexados"""
        from pathlib import Path
        
        print("\n🗑️ Remover PDFs Indexados")
        print("-" * 40)
        
        docs_dir = Path("data/documents")
        if docs_dir.exists():
            pdf_files = list(docs_dir.glob("*.pdf"))
            indexed_pdfs = []
            
            for pdf in pdf_files:
                doc_info = self.rag.vector_store_manager.get_document_info(str(pdf))
                if doc_info["exists"]:
                    indexed_pdfs.append((str(pdf), doc_info))
            
            if indexed_pdfs:
                print("📁 PDFs indexados:")
                for i, (pdf_path, doc_info) in enumerate(indexed_pdfs, 1):
                    pdf_name = Path(pdf_path).name
                    print(f"  {i}. {pdf_name} ({doc_info['chunks_count']} chunks)")
                
                print(f"  {len(indexed_pdfs) + 1}. ⬅️ Voltar")
                
                try:
                    choice = self.strategy.get_input(f"\n🎯 Escolha um PDF para remover (1-{len(indexed_pdfs) + 1}): ")
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(indexed_pdfs):
                        pdf_path = indexed_pdfs[choice_num - 1][0]
                        self._confirm_remove(pdf_path)
                    elif choice_num == len(indexed_pdfs) + 1:
                        return
                    else:
                        self.strategy.display_message("❌ Opção inválida.")
                except ValueError:
                    self.strategy.display_message("❌ Por favor, digite um número válido.")
            else:
                print("❌ Nenhum PDF indexado encontrado.")
                self.strategy.get_input("\nPressione Enter para continuar...")
        else:
            print("❌ Diretório data/documents/ não encontrado.")
            self.strategy.get_input("\nPressione Enter para continuar...")
    
    def _confirm_remove(self, pdf_path: str):
        """Confirma remoção de um PDF"""
        from pathlib import Path
        
        pdf_name = Path(pdf_path).name
        print(f"\n🗑️ Remover: {pdf_name}")
        print("⚠️  Isso irá remover o documento do banco de dados.")
        
        confirm = self.strategy.get_input("Tem certeza? (s/N): ").lower()
        if confirm in ['s', 'sim', 'y', 'yes']:
            try:
                success = self.rag.vector_store_manager.remove_document(pdf_path)
                if success:
                    self.strategy.display_message(f"✅ {pdf_name} removido com sucesso!")
                else:
                    self.strategy.display_message(f"❌ Erro ao remover {pdf_name}")
            except Exception as e:
                self.strategy.display_message(f"❌ Erro: {str(e)}")
        else:
            self.strategy.display_message("❌ Remoção cancelada.")
    
    def _manual_index_pdf(self):
        """Indexar PDF com caminho manual"""
        pdf_path = self.strategy.get_input("📁 Digite o caminho completo do PDF: ")
        if pdf_path:
            # Perguntar se quer forçar reindexação
            force_input = self.strategy.get_input("🔄 Forçar reindexação se já existir? (s/N): ").lower()
            force = force_input in ['s', 'sim', 'y', 'yes']
            self._index_pdf(pdf_path, force)
        else:
            self.strategy.display_message("❌ Caminho não fornecido.")
    
    def _index_pdf(self, pdf_path: str, force: bool = False):
        """Indexa um PDF"""
        try:
            command = self.command_factory.create_command('index', self.rag)
            result = command.execute(pdf_path=pdf_path, force=force)
            
            if not result.get('success', True):
                self.strategy.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
    
    def _show_chat_menu(self):
        """Mostra menu de chat"""
        print("\n💬 Fazer Pergunta")
        print("-" * 30)
        
        # Sugestões de perguntas
        suggestions = [
            "O que é inteligência artificial?",
            "Quais são os tipos de IA?",
            "Quais são as aplicações da IA?",
            "Quais são os desafios da IA?",
            "Resuma o conteúdo em 3 pontos",
            "Pergunta personalizada..."
        ]
        
        print("💡 Sugestões de perguntas:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        try:
            choice = self.strategy.get_input(f"\n🎯 Escolha uma pergunta (1-{len(suggestions)}): ")
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(suggestions) - 1:
                query = suggestions[choice_num - 1]
                self._chat(query)
            elif choice_num == len(suggestions):
                query = self.strategy.get_input("❓ Digite sua pergunta: ")
                if query:
                    self._chat(query)
                else:
                    self.strategy.display_message("❌ Pergunta não fornecida.")
            else:
                self.strategy.display_message("❌ Opção inválida.")
        except ValueError:
            self.strategy.display_message("❌ Por favor, digite um número válido.")
    
    def _chat(self, query: str):
        """Processa uma pergunta"""
        try:
            command = self.command_factory.create_command('chat', self.rag)
            result = command.execute(query=query, show_sources=True)
            
            if not result.get('success', True):
                self.strategy.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
    
    def _show_search_menu(self):
        """Mostra menu de busca"""
        print("\n🔍 Buscar Documentos")
        print("-" * 30)
        
        # Sugestões de termos de busca
        suggestions = [
            "inteligência artificial",
            "machine learning",
            "deep learning",
            "processamento de linguagem natural",
            "aplicações da IA",
            "desafios da IA",
            "Termo personalizado..."
        ]
        
        print("🔍 Sugestões de busca:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        try:
            choice = self.strategy.get_input(f"\n🎯 Escolha um termo (1-{len(suggestions)}): ")
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(suggestions) - 1:
                query = suggestions[choice_num - 1]
            elif choice_num == len(suggestions):
                query = self.strategy.get_input("🔍 Digite o termo de busca: ")
                if not query:
                    self.strategy.display_message("❌ Termo não fornecido.")
                    return
            else:
                self.strategy.display_message("❌ Opção inválida.")
                return
            
            # Perguntar número de resultados
            try:
                k_input = self.strategy.get_input("📊 Número de resultados (padrão: 3): ")
                k = int(k_input) if k_input else 3
                self._search(query, k)
            except ValueError:
                self.strategy.display_message("❌ Número inválido. Usando padrão: 3")
                self._search(query, 3)
                
        except ValueError:
            self.strategy.display_message("❌ Por favor, digite um número válido.")
    
    def _search(self, query: str, k: int):
        """Busca documentos similares"""
        try:
            command = self.command_factory.create_command('search', self.rag)
            result = command.execute(query=query, k=k)
            
            if not result.get('success', True):
                self.strategy.display_message(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        except Exception as e:
            self.strategy.display_message(f"❌ Erro: {str(e)}")
    
    def _start_interactive_mode(self):
        """Inicia modo interativo"""
        print("🤖 Modo Interativo - Sistema RAG")
        print("Digite 'sair' para encerrar")
        print("Digite 'info' para ver informações da coleção")
        print("-" * 50)
        
        while True:
            try:
                # Obter input do usuário
                user_input = self.strategy.get_input("\n❓ Digite sua pergunta: ")
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    self.strategy.display_message("👋 Encerrando modo interativo...")
                    break
                    
                if user_input.lower() == 'info':
                    command = self.command_factory.create_command('info', self.rag)
                    command.execute()
                    continue
                
                # Processar pergunta
                self._chat(user_input)
                
            except KeyboardInterrupt:
                self.strategy.display_message("\n👋 Encerrando modo interativo...")
                break
            except Exception as e:
                self.strategy.display_message(f"❌ Erro: {str(e)}")
    
    def _show_help(self):
        """Mostra ajuda"""
        print("\n📖 Ajuda - Sistema RAG")
        print("=" * 50)
        print("""
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
    
    def run(self):
        """Executa o menu principal"""
        self.strategy.display_message("🤖 Sistema RAG - Menu Interativo")
        self.strategy.display_message("=" * 50)
        
        while self.running:
            try:
                options = self.get_menu_options()
                choice = self.strategy.display_menu(options)
                self.running = self.handle_menu_choice(choice)
            except KeyboardInterrupt:
                self.strategy.display_message("\n👋 Encerrando...")
                break
            except Exception as e:
                self.strategy.display_message(f"❌ Erro: {str(e)}")
