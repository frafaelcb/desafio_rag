-- Script de inicialização do banco de dados RAG
-- Este script é executado automaticamente quando o container PostgreSQL é criado

-- Habilitar extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar se a extensão foi criada com sucesso
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Criar tabela de exemplo para testar (opcional)
CREATE TABLE IF NOT EXISTS test_vectors (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- Dimensão padrão do text-embedding-3-small
);

-- Criar índice para busca vetorial (opcional)
CREATE INDEX IF NOT EXISTS test_vectors_embedding_idx 
ON test_vectors 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Verificar se tudo foi criado corretamente
SELECT 
    'pgvector extension' as check_item,
    CASE 
        WHEN EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') 
        THEN 'OK' 
        ELSE 'FAILED' 
    END as status
UNION ALL
SELECT 
    'test_vectors table' as check_item,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'test_vectors') 
        THEN 'OK' 
        ELSE 'FAILED' 
    END as status;
