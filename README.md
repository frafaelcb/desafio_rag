# 🚀 Desafio RAG - Sistema de Recuperação e Geração de Respostas

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) completo usando **PostgreSQL com pgvector** e **LangChain** para processamento e geração de respostas baseadas em documentos PDF.

## ✨ Funcionalidades

- 📄 **Indexação de PDFs** no PostgreSQL com pgvector
- 🔍 **Busca semântica** usando embeddings da OpenAI
- 💬 **Chat inteligente** baseado nos documentos indexados
- 🎯 **Recuperação precisa** com LangChain
- 🛠️ **Interface CLI** completa
- 🧪 **Testes automatizados**
- 📊 **Monitoramento** e logs detalhados

## 📋 Índice

- [Sistema RAG](#sistema-rag)
- [Ambientes Virtuais Python](#ambientes-virtuais-python)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Comandos Básicos](#comandos-básicos)
- [Uso do Sistema RAG](#uso-do-sistema-rag)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Contribuir](#como-contribuir)

## 🤖 Sistema RAG

### O que é RAG?

**RAG (Retrieval-Augmented Generation)** é uma técnica que combina:
- **Recuperação**: Busca documentos relevantes em uma base de conhecimento
- **Geração**: Usa um modelo de linguagem para gerar respostas baseadas nos documentos recuperados

### Como funciona nosso sistema?

1. **📄 Indexação**: PDFs são divididos em chunks e convertidos em embeddings
2. **💾 Armazenamento**: Embeddings são armazenados no PostgreSQL com pgvector
3. **🔍 Busca**: Quando você faz uma pergunta, o sistema busca chunks similares
4. **💬 Geração**: O LLM gera uma resposta baseada nos chunks encontrados

### Tecnologias utilizadas:

- **LangChain**: Framework para aplicações LLM
- **PostgreSQL + pgvector**: Banco de dados vetorial
- **OpenAI**: Embeddings e modelo de linguagem
- **PyPDF**: Processamento de PDFs

## 🐍 Ambientes Virtuais Python

### O que são e por que usar?

**Ambientes virtuais** são espaços isolados que permitem instalar e gerenciar dependências específicas para cada projeto Python, evitando conflitos entre diferentes versões de bibliotecas.

**Benefícios:**
- ✅ **Isolamento**: Cada projeto tem suas próprias dependências
- ✅ **Reprodutibilidade**: Garante que o projeto funcione em qualquer ambiente
- ✅ **Segurança**: Evita conflitos entre pacotes
- ✅ **Organização**: Mantém o sistema Python limpo

### Ferramentas Disponíveis

#### 1. **pyenv** - Gerenciador de Versões Python
- **Para que serve**: Permite instalar e gerenciar múltiplas versões do Python
- **Por que usar**: Diferentes projetos podem precisar de versões específicas do Python
- **Vantagens**: 
  - Controle total sobre versões do Python
  - Ambientes virtuais integrados
  - Ativação automática por diretório

#### 2. **pipenv** - Gerenciador de Dependências e Ambientes
- **Para que serve**: Combina gerenciamento de ambientes virtuais com controle de dependências
- **Por que usar**: Simplifica o processo de gerenciar dependências e ambientes
- **Vantagens**:
  - Criação automática de ambientes virtuais
  - Arquivo Pipfile para dependências
  - Lockfile para versões exatas
  - Separação entre dependências de produção e desenvolvimento

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.11+
- Git
- curl (para instalação)

### Instalação do pyenv

#### Linux (Ubuntu/Debian):
```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Instalar pyenv
curl https://pyenv.run | bash

# Adicionar ao shell (adicione ao ~/.zshrc ou ~/.bashrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Recarregar shell
source ~/.zshrc

# Instalar plugin pyenv-virtualenv
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
source ~/.zshrc
```

#### macOS:
```bash
# Com Homebrew
brew install pyenv

# Adicionar ao shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

source ~/.zshrc
```

### Instalação do pipenv

```bash
# Instalar pipenv
pip install pipenv

# Verificar instalação
pipenv --version
```

## 🛠️ Comandos Básicos

### PYENV - Comandos Essenciais

#### Gerenciar Versões Python:
```bash
# Listar versões disponíveis
pyenv install --list

# Instalar versão específica
pyenv install 3.11.0

# Listar versões instaladas
pyenv versions

# Definir versão global
pyenv global 3.11.0

# Ver versão atual
pyenv version
```

#### Ambientes Virtuais:
```bash
# Criar ambiente virtual
pyenv virtualenv 3.11.0 desafio_rag_env

# Listar ambientes virtuais
pyenv virtualenvs

# Ativar ambiente
pyenv activate desafio_rag_env

# Desativar ambiente
pyenv deactivate

# Definir ambiente local (para diretório)
pyenv local desafio_rag_env

# Remover ambiente
pyenv uninstall desafio_rag_env
```

#### Troubleshooting:
```bash
# Verificar instalação
pyenv --version

# Atualizar pyenv
pyenv update

# Ver caminho do Python
pyenv which python

# Ver caminho do pip
pyenv which pip
```

### PIPENV - Comandos Essenciais

#### Inicializar Projeto:
```bash
# Navegar para o projeto
cd /caminho/do/projeto

# Inicializar (cria Pipfile)
pipenv install

# Ou inicializar com Python específico
pipenv install --python 3.11
```

#### Gerenciar Dependências:
```bash
# Instalar dependência de produção
pipenv install requests

# Instalar dependência de desenvolvimento
pipenv install --dev pytest

# Instalar todas as dependências
pipenv install

# Instalar apenas produção
pipenv install --deploy

# Remover dependência
pipenv uninstall requests

# Ver dependências
pipenv graph
```

#### Usar Ambiente Virtual:
```bash
# Ativar ambiente virtual
pipenv shell

# Executar comando no ambiente (sem ativar)
pipenv run python app.py
pipenv run pytest

# Sair do ambiente
exit  # ou Ctrl+D
```

#### Informações e Manutenção:
```bash
# Ver informações do ambiente
pipenv --venv

# Ver localização do Python
pipenv --py

# Verificar segurança
pipenv check

# Limpar cache
pipenv clean

# Remover ambiente virtual
pipenv --rm
```

#### Troubleshooting:
```bash
# Verificar instalação
pipenv --version

# Ver logs
pipenv --support

# Forçar recriação do ambiente
pipenv --rm
pipenv install

# Ver variáveis de ambiente
pipenv --env
```

## 🚀 Configuração Rápida do Projeto

### Pré-requisitos

1. **Docker e Docker Compose** (para PostgreSQL)
2. **Python 3.11+**
3. **Chave da API OpenAI**

### Setup com Docker (Recomendado)

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd desafio_rag

# 2. Configurar banco de dados com Docker
./scripts/setup_docker.sh

# 3. Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# 4. Configurar ambiente Python
pyenv virtualenv 3.11.0 desafio_rag_env
pyenv local desafio_rag_env
pip install -r requirements.txt

# 5. Testar conexões
python scripts/test_connection.py

# 6. Testar sistema
python src/main.py info
```

### Setup Manual (Sem Docker)

#### Opção 1: Usando pyenv

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd desafio_rag

# 2. Criar ambiente virtual
pyenv virtualenv 3.11.0 desafio_rag_env

# 3. Definir ambiente local
pyenv local desafio_rag_env

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# 6. Verificar instalação
python --version
which python
```

#### Opção 2: Usando pipenv

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd desafio_rag

# 2. Inicializar projeto
pipenv install

# 3. Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# 4. Ativar ambiente
pipenv shell

# 5. Testar sistema
python -m src.main info
```

## 💬 Uso do Sistema RAG

### Comandos Principais

```bash
# Menu interativo (recomendado)
python src/main.py

# Indexar um PDF
python src/main.py index /caminho/para/documento.pdf

# Fazer uma pergunta
python src/main.py chat "Qual é o tema principal do documento?"

# Buscar documentos similares
python src/main.py search "palavra-chave"

# Ver informações da coleção
python src/main.py info

# Modo interativo
python src/main.py interactive
```

### Exemplo Completo

```bash
# 1. Indexar um documento
python src/main.py index documentos/meu_documento.pdf

# 2. Fazer perguntas
python src/main.py chat "Quais são os principais tópicos?"
python src/main.py chat "Resuma o conteúdo em 3 pontos"

# 3. Buscar por palavras-chave
python src/main.py search "inteligência artificial" -k 5
```

### Uso Programático

```python
from src.rag_chain import RAGChain

# Inicializar sistema
rag = RAGChain()

# Indexar PDF
rag.index_pdf("documento.pdf")

# Fazer pergunta
result = rag.chat("Qual é o tema principal?")
print(result['result'])

# Buscar documentos
docs = rag.search_only("palavra-chave", k=3)
```

## 📁 Estrutura do Projeto

```
desafio_rag/
├── README.md
├── requirements.txt
├── env.example
├── example_usage.py
├── docker-compose.yml     # Configuração Docker
├── init.sql              # Script de inicialização do banco
├── scripts/
│   ├── setup_docker.sh   # Script de setup Docker
│   └── test_connection.py # Teste de conexões
├── src/
│   ├── __init__.py
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── vector_store.py    # Gerenciador do PostgreSQL + pgvector
│   ├── rag_chain.py       # Pipeline RAG com LangChain
│   └── main.py           # Interface CLI
├── tests/
│   ├── __init__.py
│   └── test_rag_system.py # Testes automatizados
├── docs/
│   ├── setup.md          # Documentação de setup
│   └── docker_setup.md   # Documentação Docker
└── data/
    └── documents/        # PDFs para indexar
```

## 🔧 Comandos Úteis

### Resumo dos Comandos Mais Usados:

| Ação | pyenv | pipenv |
|------|-------|--------|
| **Criar ambiente** | `pyenv virtualenv 3.11.0 nome_env` | `pipenv install` |
| **Ativar** | `pyenv activate nome_env` | `pipenv shell` |
| **Desativar** | `pyenv deactivate` | `exit` |
| **Instalar pacote** | `pip install pacote` | `pipenv install pacote` |
| **Executar comando** | `python script.py` | `pipenv run python script.py` |
| **Ver ambiente** | `pyenv version` | `pipenv --venv` |

## 🤝 Como Contribuir

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. Configure o ambiente usando pyenv ou pipenv
4. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. **Push** para a branch (`git push origin feature/AmazingFeature`)
6. Abra um **Pull Request**

### Padrões de Desenvolvimento

- Use **pyenv** para gerenciar versões do Python
- Use **pipenv** para gerenciar dependências
- Mantenha o `requirements.txt` atualizado
- Escreva testes para novas funcionalidades
- Documente mudanças importantes
- Configure variáveis de ambiente no arquivo `.env`
- Use PostgreSQL com pgvector para armazenamento vetorial

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. **Para problemas com Docker**: Consulte [docs/docker_setup.md](docs/docker_setup.md)
2. **Para problemas gerais**: Consulte [docs/setup.md](docs/setup.md)
3. **Execute testes de conexão**: `python scripts/test_connection.py`
4. **Verifique logs Docker**: `docker-compose logs -f`
5. Abra uma [issue](../../issues)

## 🐳 Comandos Docker Úteis

```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Ver logs
docker-compose logs -f postgres

# Acessar PostgreSQL
docker-compose exec postgres psql -U rag_user -d rag_database

# Acessar pgAdmin (http://localhost:8080)
# Email: admin@rag.local | Senha: admin123
```

---

**Desenvolvido com ❤️ pela equipe de desenvolvimento**
