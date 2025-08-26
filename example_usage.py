#!/usr/bin/env python3
"""
Exemplo de uso do Sistema RAG com PostgreSQL e pgvector
Este arquivo demonstra como usar o sistema programaticamente
"""

import os
from src.rag_chain import RAGChain
from src.config import Config

def main():
    """Exemplo completo de uso do sistema RAG"""
    
    print("🚀 Sistema RAG - Exemplo de Uso")
    print("=" * 50)
    
    # Verificar configurações
    if not Config.validate_config():
        print("❌ Configurações inválidas. Verifique o arquivo .env")
        return
    
    try:
        # Inicializar sistema RAG
        print("🔧 Inicializando sistema RAG...")
        rag = RAGChain()
        
        # Verificar informações da coleção
        print("\n📊 Informações da coleção:")
        info = rag.get_collection_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Exemplo 1: Indexar um PDF
        pdf_path = "exemplo.pdf"  # Substitua pelo caminho do seu PDF
        if os.path.exists(pdf_path):
            print(f"\n📖 Indexando PDF: {pdf_path}")
            chunks_count = rag.index_pdf(pdf_path)
            print(f"✅ Indexados {chunks_count} chunks")
        else:
            print(f"\n⚠️ PDF não encontrado: {pdf_path}")
            print("   Pule esta etapa ou adicione um PDF válido")
        
        # Exemplo 2: Buscar documentos similares
        print(f"\n🔍 Buscando documentos similares...")
        query = "inteligência artificial"
        docs = rag.search_only(query, k=2)
        
        print(f"Documentos encontrados para '{query}':")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Desconhecido")
            page = doc.metadata.get("page", "N/A")
            print(f"   {i}. {source} | Página: {page}")
            print(f"      Trecho: {doc.page_content[:100]}...")
        
        # Exemplo 3: Fazer perguntas
        print(f"\n❓ Fazendo perguntas...")
        questions = [
            "Qual é o tema principal do documento?",
            "Quais são os pontos mais importantes?",
            "Resuma o conteúdo em 3 frases"
        ]
        
        for question in questions:
            print(f"\nPergunta: {question}")
            try:
                result = rag.chat(question, show_sources=True)
                print(f"Resposta: {result['result']}")
            except Exception as e:
                print(f"Erro: {str(e)}")
        
        # Exemplo 4: Modo interativo simples
        print(f"\n🤖 Modo interativo (digite 'sair' para encerrar):")
        while True:
            try:
                user_input = input("\n❓ Sua pergunta: ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    break
                
                if user_input:
                    result = rag.chat(user_input, show_sources=False)
                    print(f"💡 {result['result']}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
        
        print("\n👋 Exemplo concluído!")
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")

def exemplo_avancado():
    """Exemplo com configurações avançadas"""
    
    print("\n🔬 Exemplo Avançado")
    print("=" * 30)
    
    try:
        # Configurar com parâmetros customizados
        from src.vector_store import VectorStoreManager
        
        # Vector store manager customizado
        vector_manager = VectorStoreManager()
        
        # RAG chain com configurações específicas
        rag = RAGChain(vector_store_manager=vector_manager)
        
        # Buscar com mais resultados
        print("🔍 Busca avançada...")
        docs = rag.search_only("tecnologia", k=5)
        
        print(f"Encontrados {len(docs)} documentos:")
        for i, doc in enumerate(docs, 1):
            print(f"   {i}. {doc.metadata.get('source', 'N/A')}")
        
        # Pergunta com resposta detalhada
        print("\n❓ Pergunta detalhada...")
        result = rag.chat(
            "Explique detalhadamente os conceitos principais",
            show_sources=True
        )
        
        print("✅ Exemplo avançado concluído!")
        
    except Exception as e:
        print(f"❌ Erro no exemplo avançado: {str(e)}")

if __name__ == "__main__":
    # Executar exemplo básico
    main()
    
    # Executar exemplo avançado
    exemplo_avancado()
