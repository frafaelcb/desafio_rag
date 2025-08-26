# 🐳 Setup com Docker - Sistema RAG

Este guia explica como configurar o sistema RAG usando PostgreSQL com pgvector em containers Docker.

## 📋 Pré-requisitos

### 1. **Docker e Docker Compose**
```bash
# Verificar se Docker está instalado
docker --version

# Verificar se Docker Compose está instalado
docker-compose --version
```

### 2. **Python 3.11+**
```bash
# Verificar versão do Python
python --version
```

### 3. **Chave da API OpenAI**
- Obtenha sua chave em: https://platform.openai.com/api-keys

## 🚀 Setup Rápido

### **Opção 1: Script Automatizado (Recomendado)**

```bash
# 1. Navegar para o projeto
cd /caminho/para/seu/projeto

# 2. Executar script de setup
./scripts/setup_docker.sh
```

### **Opção 2: Setup Manual**

```bash
# 1. Iniciar containers
docker-compose up -d

# 2. Aguardar PostgreSQL estar pronto
docker-compose logs -f postgres

# 3. Verificar se pgvector foi criado
docker-compose exec postgres psql -U admin -d rag_database -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

## ⚙️ Configuração do Projeto

### 1. **Configurar variáveis de ambiente**
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar com suas configurações
nano .env
```

**Conteúdo do arquivo `.env`:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# PostgreSQL Configuration (Docker)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_database
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

# Vector Store Configuration
COLLECTION_NAME=docs_pdf

# Chunking Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Retrieval Configuration
SEARCH_K=3
```

### 2. **Configurar ambiente Python**
```bash
# Com pyenv
pyenv virtualenv 3.11.0 desafio_rag_env
pyenv local desafio_rag_env
pip install -r requirements.txt

# Ou com pipenv
pipenv install
```

### 3. **Testar conexões**
```bash
# Testar PostgreSQL e OpenAI
python scripts/test_connection.py

# Ou testar apenas o sistema RAG
python src/main.py info
```

## 🐳 Comandos Docker Úteis

### **Gerenciar Containers**
```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Parar e remover volumes (cuidado: apaga dados)
docker-compose down -v

# Ver logs
docker-compose logs -f postgres
docker-compose logs -f pgadmin

# Reiniciar containers
docker-compose restart
```

### **Acessar PostgreSQL**
```bash
# Conectar via psql
docker-compose exec postgres psql -U admin -d rag_database

# Executar comando específico
docker-compose exec postgres psql -U admin -d rag_database -c "SELECT version();"

# Backup do banco
docker-compose exec postgres pg_dump -U admin rag_database > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U admin -d rag_database < backup.sql
```

### **Acessar pgAdmin**
```bash
# Abrir no navegador
open http://localhost:8080

# Credenciais:
# Email: admin@rag.local
# Senha: admin123
```

## 🧪 Testando o Sistema

### 1. **Teste de Conexões**
```bash
# Testar todas as conexões
python scripts/test_connection.py
```

### 2. **Teste do Sistema RAG**
```bash
# Ver informações da coleção
python src/main.py info

# Indexar um PDF de teste
python src/main.py index exemplo.pdf

# Fazer uma pergunta
python src/main.py chat "Qual é o tema principal?"
```

### 3. **Teste com Dados de Exemplo**
```bash
# Criar PDF de teste
echo "Este é um documento de teste sobre inteligência artificial." > teste.txt
# Converter para PDF (se tiver pandoc instalado)
pandoc teste.txt -o teste.pdf

# Indexar e testar
python src/main.py index teste.pdf
python src/main.py chat "Sobre o que fala o documento?"
```

## 🔧 Troubleshooting

### **Container não inicia**
```bash
# Verificar logs
docker-compose logs postgres

# Verificar se a porta 5432 está livre
sudo lsof -i :5432

# Parar containers conflitantes
docker stop $(docker ps -q)
```

### **Erro de conexão com PostgreSQL**
```bash
# Verificar se o container está rodando
docker-compose ps

# Verificar logs
docker-compose logs postgres

# Testar conexão manual
docker-compose exec postgres pg_isready -U admin -d rag_database
```

### **Erro de extensão pgvector**
```bash
# Verificar se a extensão foi criada
docker-compose exec postgres psql -U admin -d rag_database -c "SELECT * FROM pg_extension WHERE extname = 'vector';"

# Recriar extensão se necessário
docker-compose exec postgres psql -U admin -d rag_database -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### **Problemas de permissão**
```bash
# Dar permissão ao script
chmod +x scripts/setup_docker.sh
chmod +x scripts/test_connection.py

# Verificar permissões dos volumes
ls -la postgres_data/
```

## 📊 Monitoramento

### **Verificar Status dos Containers**
```bash
# Status geral
docker-compose ps

# Uso de recursos
docker stats

# Logs em tempo real
docker-compose logs -f
```

### **Verificar Banco de Dados**
```bash
# Estatísticas do PostgreSQL
docker-compose exec postgres psql -U admin -d rag_database -c "SELECT * FROM pg_stat_activity;"

# Tamanho do banco
docker-compose exec postgres psql -U admin -d rag_database -c "SELECT pg_size_pretty(pg_database_size('rag_database'));"

# Tabelas criadas pelo LangChain
docker-compose exec postgres psql -U admin -d rag_database -c "\dt"
```

## 🚀 Próximos Passos

1. **Indexar seus documentos PDF**
2. **Testar diferentes tipos de perguntas**
3. **Ajustar parâmetros de chunking**
4. **Implementar interface web (opcional)**
5. **Adicionar mais tipos de documentos**

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker-compose logs -f`
2. Execute o teste de conexão: `python scripts/test_connection.py`
3. Verifique a configuração: `python src/main.py info`
4. Consulte a documentação do pgvector e LangChain
