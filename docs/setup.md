# 🚀 Setup do Sistema RAG

Este guia explica como configurar e usar o sistema RAG com PostgreSQL e pgvector.

## 📋 Pré-requisitos

### 1. **Python 3.11+**
```bash
# Verificar versão do Python
python --version
```

### 2. **PostgreSQL com pgvector**
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Instalar pgvector
sudo apt install postgresql-14-pgvector  # Ajuste a versão conforme necessário
```

### 3. **Configurar PostgreSQL**
```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco de dados
CREATE DATABASE rag_database;

# Criar usuário
CREATE USER rag_user WITH PASSWORD 'sua_senha';

# Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE rag_database TO rag_user;

# Conectar ao banco
\c rag_database

# Habilitar extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

# Sair
\q
```

## ⚙️ Configuração do Projeto

### 1. **Clonar e configurar ambiente**
```bash
# Navegar para o projeto
cd /home/francisco-rafael/development/pessoal/desafio_rag

# Criar ambiente virtual com pyenv
pyenv virtualenv 3.11.0 desafio_rag_env
pyenv local desafio_rag_env

# Ou usar pipenv
pipenv install
```

### 2. **Instalar dependências**
```bash
# Com pyenv
pip install -r requirements.txt

# Ou com pipenv
pipenv install
```

### 3. **Configurar variáveis de ambiente**
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

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_database
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=sua_senha

# Vector Store Configuration
COLLECTION_NAME=docs_pdf

# Chunking Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Retrieval Configuration
SEARCH_K=3
```

## 🧪 Testando a Instalação

### 1. **Executar testes**
```bash
# Executar todos os testes
pytest tests/

# Executar com verbose
pytest -v tests/

# Executar testes específicos
pytest tests/test_rag_system.py::TestConfig
```

### 2. **Verificar configuração**
```bash
# Ver informações da coleção
python -m src.main info
```

## 📚 Uso Básico

### 1. **Indexar um PDF**
```bash
# Indexar um documento
python -m src.main index /caminho/para/documento.pdf
```

### 2. **Fazer perguntas**
```bash
# Pergunta simples
python -m src.main chat "Qual é o tema principal do documento?"

# Pergunta sem mostrar fontes
python -m src.main chat "Resuma o documento" --no-sources
```

### 3. **Buscar documentos similares**
```bash
# Buscar por palavra-chave
python -m src.main search "palavra-chave"

# Buscar com mais resultados
python -m src.main search "palavra-chave" -k 5
```

### 4. **Modo interativo**
```bash
# Iniciar modo interativo
python -m src.main interactive
```

## 🔧 Troubleshooting

### **Erro de conexão com PostgreSQL**
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Iniciar se necessário
sudo systemctl start postgresql

# Verificar conexão
psql -h localhost -U rag_user -d rag_database
```

### **Erro de API Key do OpenAI**
```bash
# Verificar se a chave está correta
echo $OPENAI_API_KEY

# Testar com curl
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

### **Erro de dependências**
```bash
# Reinstalar dependências
pip uninstall -r requirements.txt
pip install -r requirements.txt

# Ou com pipenv
pipenv --rm
pipenv install
```

## 📊 Monitoramento

### **Verificar logs do PostgreSQL**
```bash
# Ver logs em tempo real
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Ver estatísticas
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

### **Verificar uso de memória**
```bash
# Ver processos Python
ps aux | grep python

# Ver uso de memória do PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_bgwriter;"
```

## 🚀 Próximos Passos

1. **Indexar seus documentos PDF**
2. **Testar diferentes tipos de perguntas**
3. **Ajustar parâmetros de chunking**
4. **Implementar interface web (opcional)**
5. **Adicionar mais tipos de documentos**

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs de erro
2. Execute os testes: `pytest tests/`
3. Verifique a configuração: `python -m src.main info`
4. Consulte a documentação do LangChain e pgvector
