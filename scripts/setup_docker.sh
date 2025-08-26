#!/bin/bash

# Script de setup para o sistema RAG com Docker
# Este script configura o ambiente completo

set -e  # Para o script se houver erro

echo "🚀 Setup do Sistema RAG com Docker"
echo "=================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"

# Parar containers existentes se houver
echo "🛑 Parando containers existentes..."
docker-compose down -v 2>/dev/null || true

# Iniciar containers
echo "🐳 Iniciando containers PostgreSQL e pgAdmin..."
docker-compose up -d

# Aguardar o PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
until docker-compose exec -T postgres pg_isready -U admin -d rag_database; do
    echo "   Aguardando..."
    sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Verificar se a extensão pgvector foi criada
echo "🔍 Verificando extensão pgvector..."
docker-compose exec -T postgres psql -U admin -d rag_database -c "SELECT * FROM pg_extension WHERE extname = 'vector';"

# Verificar tabela de teste
echo "🔍 Verificando tabela de teste..."
docker-compose exec -T postgres psql -U admin -d rag_database -c "SELECT * FROM test_vectors LIMIT 1;" 2>/dev/null || echo "   Tabela de teste vazia (normal)"

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "📊 Informações dos containers:"
echo "   PostgreSQL: localhost:5432"
echo "   Usuário: admin"
echo "   Senha: admin"
echo "   Banco: rag_database"
echo ""
echo "🌐 pgAdmin (opcional):"
echo "   URL: http://localhost:8080"
echo "   Email: admin@rag.local"
echo "   Senha: admin123"
echo ""
echo "🔧 Próximos passos:"
echo "   1. Configure o arquivo .env com suas credenciais"
echo "   2. Instale as dependências Python: pip install -r requirements.txt"
echo "   3. Teste o sistema: python src/main.py info"
echo ""
echo "📝 Para parar os containers: docker-compose down"
echo "📝 Para ver logs: docker-compose logs -f"
