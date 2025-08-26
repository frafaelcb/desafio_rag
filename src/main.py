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
except ImportError:
    # Fallback para imports relativos quando executado como módulo
    from .rag_chain import RAGChain
    from .config import Config

def main():
    """Função principal da interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description="Sistema RAG - Indexar PDFs e fazer perguntas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Indexar um PDF
  python -m src.main index /caminho/para/documento.pdf
  
  # Fazer uma pergunta
  python -m src.main chat "Qual é o tema principal do documento?"
  
  # Buscar documentos similares
  python -m src.main search "palavra-chave"
  
  # Ver informações da coleção
  python -m src.main info
  
  # Menu interativo (sem argumentos)
  python -m src.main
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
        
        # Inicializar RAG
        rag = RAGChain()
        
        # Executar comando
        if args.command == 'index':
            index_pdf(rag, args.pdf_path, args.force)
        elif args.command == 'chat':
            chat(rag, args.query, not args.no_sources)
        elif args.command == 'search':
            search(rag, args.query, args.k)
        elif args.command == 'info':
            show_info(rag)
        elif args.command == 'interactive':
            interactive_mode(rag)
            
    except KeyboardInterrupt:
        print("\n👋 Encerrando...")
        return 0
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1
    
    return 0

def show_menu():
    """Mostra o menu interativo principal"""
    print("🤖 Sistema RAG - Menu Interativo")
    print("=" * 50)
    
    try:
        # Validar configurações
        if not Config.validate_config():
            print("❌ Configurações inválidas. Verifique o arquivo .env")
            print("\nVariáveis necessárias:")
            print("  - OPENAI_API_KEY")
            print("  - POSTGRES_PASSWORD")
            return 1
        
        # Inicializar RAG
        rag = RAGChain()
        
        while True:
            print("\n📋 Opções disponíveis:")
            print("1. 📊 Ver informações do sistema")
            print("2. 📄 Indexar um PDF")
            print("3. 💬 Fazer uma pergunta")
            print("4. 🔍 Buscar documentos similares")
            print("5. 🤖 Modo chat interativo")
            print("6. 🧪 Testar conexões")
            print("7. 📖 Ver ajuda")
            print("0. 🚪 Sair")
            
            try:
                choice = input("\n🎯 Escolha uma opção (0-7): ").strip()
                
                if choice == '0':
                    print("👋 Obrigado por usar o Sistema RAG!")
                    break
                elif choice == '1':
                    show_info(rag)
                elif choice == '2':
                    menu_index_pdf(rag)
                elif choice == '3':
                    menu_chat(rag)
                elif choice == '4':
                    menu_search(rag)
                elif choice == '5':
                    interactive_mode(rag)
                elif choice == '6':
                    test_connections()
                elif choice == '7':
                    show_help()
                else:
                    print("❌ Opção inválida. Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\n👋 Encerrando...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {str(e)}")
        return 1
    
    return 0

def menu_index_pdf(rag: RAGChain):
    """Menu para indexar PDF"""
    print("\n📄 Indexar PDF")
    print("-" * 30)
    
    # Verificar se há PDFs no diretório data/documents
    docs_dir = Path("data/documents")
    if docs_dir.exists():
        pdf_files = list(docs_dir.glob("*.pdf"))
        if pdf_files:
            print("📁 PDFs encontrados em data/documents:")
            for i, pdf in enumerate(pdf_files, 1):
                print(f"  {i}. {pdf.name}")
            print(f"  {len(pdf_files) + 1}. Especificar caminho manualmente")
            
            try:
                choice = input(f"\n🎯 Escolha um PDF (1-{len(pdf_files) + 1}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(pdf_files):
                    pdf_path = str(pdf_files[choice_num - 1])
                    index_pdf(rag, pdf_path)
                elif choice_num == len(pdf_files) + 1:
                    manual_index_pdf(rag)
                else:
                    print("❌ Opção inválida.")
            except ValueError:
                print("❌ Por favor, digite um número válido.")
        else:
            manual_index_pdf(rag)
    else:
        manual_index_pdf(rag)

def manual_index_pdf(rag: RAGChain):
    """Indexar PDF com caminho manual"""
    pdf_path = input("📁 Digite o caminho completo do PDF: ").strip()
    if pdf_path:
        # Perguntar se quer forçar reindexação
        force_input = input("🔄 Forçar reindexação se já existir? (s/N): ").strip().lower()
        force = force_input in ['s', 'sim', 'y', 'yes']
        index_pdf(rag, pdf_path, force)
    else:
        print("❌ Caminho não fornecido.")

def menu_chat(rag: RAGChain):
    """Menu para fazer perguntas"""
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
        choice = input(f"\n🎯 Escolha uma pergunta (1-{len(suggestions)}): ").strip()
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(suggestions) - 1:
            query = suggestions[choice_num - 1]
            chat(rag, query, True)
        elif choice_num == len(suggestions):
            query = input("❓ Digite sua pergunta: ").strip()
            if query:
                chat(rag, query, True)
            else:
                print("❌ Pergunta não fornecida.")
        else:
            print("❌ Opção inválida.")
    except ValueError:
        print("❌ Por favor, digite um número válido.")

def menu_search(rag: RAGChain):
    """Menu para busca de documentos"""
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
        choice = input(f"\n🎯 Escolha um termo (1-{len(suggestions)}): ").strip()
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(suggestions) - 1:
            query = suggestions[choice_num - 1]
        elif choice_num == len(suggestions):
            query = input("🔍 Digite o termo de busca: ").strip()
            if not query:
                print("❌ Termo não fornecido.")
                return
        else:
            print("❌ Opção inválida.")
            return
        
        # Perguntar número de resultados
        try:
            k = input("📊 Número de resultados (padrão: 3): ").strip()
            k = int(k) if k else 3
            search(rag, query, k)
        except ValueError:
            print("❌ Número inválido. Usando padrão: 3")
            search(rag, query, 3)
            
    except ValueError:
        print("❌ Por favor, digite um número válido.")

def test_connections():
    """Testar conexões do sistema"""
    print("\n🧪 Testando Conexões")
    print("-" * 30)
    
    try:
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
        
    except Exception as e:
        print(f"❌ Erro nos testes: {str(e)}")

def show_help():
    """Mostrar ajuda"""
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
• python -m src.main info          # Ver informações
• python -m src.main index file.pdf # Indexar PDF
• python -m src.main chat "pergunta" # Fazer pergunta
• python -m src.main search "termo"  # Buscar documentos

📁 Estrutura de arquivos:
• data/documents/     # Coloque seus PDFs aqui
• .env               # Configurações (OpenAI API key, etc.)
• docker-compose.yml # Configuração do banco de dados

🔧 Configuração necessária:
• Docker e Docker Compose
• Chave da API OpenAI
• Python 3.11+
    """)

def index_pdf(rag: RAGChain, pdf_path: str, force: bool = False):
    """Indexa um PDF"""
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(pdf_path):
            print(f"❌ Arquivo não encontrado: {pdf_path}")
            return
        
        # Verificar se é um PDF
        if not pdf_path.lower().endswith('.pdf'):
            print(f"❌ Arquivo deve ser um PDF: {pdf_path}")
            return
        
        print(f"🚀 Iniciando indexação do PDF: {pdf_path}")
        chunks_count = rag.index_pdf(pdf_path, force)
        print(f"✅ Indexação concluída! {chunks_count} chunks processados")
        
    except Exception as e:
        print(f"❌ Erro ao indexar PDF: {str(e)}")

def chat(rag: RAGChain, query: str, show_sources: bool = True):
    """Processa uma pergunta"""
    try:
        result = rag.chat(query, show_sources)
        return result
    except Exception as e:
        print(f"❌ Erro ao processar pergunta: {str(e)}")

def search(rag: RAGChain, query: str, k: int):
    """Busca documentos similares"""
    try:
        print(f"🔍 Buscando documentos similares a: '{query}'")
        docs = rag.search_only(query, k)
        
        print(f"\n📚 Documentos encontrados ({len(docs)}):")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Desconhecido")
            page = doc.metadata.get("page", "N/A")
            print(f"\n{i}. {source} | Página: {page}")
            print(f"   Conteúdo: {doc.page_content[:300]}...")
            
    except Exception as e:
        print(f"❌ Erro na busca: {str(e)}")

def show_info(rag: RAGChain):
    """Mostra informações da coleção"""
    try:
        info = rag.get_collection_info()
        print("📊 Informações da Coleção:")
        print(f"   Nome: {info['collection_name']}")
        print(f"   Tem documentos: {'✅ Sim' if info['has_documents'] else '❌ Não'}")
        print(f"   Modelo de embedding: {info['embedding_model']}")
        
    except Exception as e:
        print(f"❌ Erro ao obter informações: {str(e)}")

def interactive_mode(rag: RAGChain):
    """Modo interativo"""
    print("🤖 Modo Interativo - Sistema RAG")
    print("Digite 'sair' para encerrar")
    print("Digite 'info' para ver informações da coleção")
    print("-" * 50)
    
    while True:
        try:
            # Obter input do usuário
            user_input = input("\n❓ Digite sua pergunta: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando modo interativo...")
                break
                
            if user_input.lower() == 'info':
                show_info(rag)
                continue
            
            # Processar pergunta
            rag.chat(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 Encerrando modo interativo...")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    sys.exit(main())
