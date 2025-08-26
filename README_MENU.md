# 🤖 Sistema RAG - Menu Interativo

## 🚀 Como Executar o Sistema

### **Opção 1: Menu Interativo (Recomendado)**
```bash
# Execute diretamente o arquivo main.py
python main.py
```

### **Opção 2: Comandos de Linha**
```bash
# Ver informações
python -m src.main info

# Indexar PDF
python -m src.main index documento.pdf

# Fazer pergunta
python -m src.main chat "Sua pergunta aqui"

# Buscar documentos
python -m src.main search "termo de busca"

# Modo interativo
python -m src.main interactive
```

## 📋 Menu Interativo

Quando você executa `python main.py`, o sistema apresenta um menu amigável com as seguintes opções:

### 🎯 **Opções do Menu:**

1. **📊 Ver informações do sistema**
   - Mostra status da coleção
   - Número de documentos indexados
   - Modelo de embedding usado

2. **📄 Indexar um PDF**
   - Lista PDFs disponíveis em `data/documents/`
   - Permite especificar caminho manual
   - Processa e indexa o documento automaticamente

3. **💬 Fazer uma pergunta**
   - Sugestões de perguntas pré-definidas
   - Opção para pergunta personalizada
   - Resposta baseada nos documentos indexados

4. **🔍 Buscar documentos similares**
   - Sugestões de termos de busca
   - Configuração do número de resultados
   - Mostra trechos relevantes dos documentos

5. **🤖 Modo chat interativo**
   - Conversa contínua com o sistema
   - Múltiplas perguntas em sequência
   - Digite 'sair' para encerrar

6. **🧪 Testar conexões**
   - Verifica conexão com PostgreSQL
   - Testa API da OpenAI
   - Diagnóstico do sistema

7. **📖 Ver ajuda**
   - Explicação do sistema RAG
   - Instruções de uso
   - Comandos disponíveis

0. **🚪 Sair**
   - Encerra o sistema

## 🎮 **Exemplo de Uso:**

```bash
$ python main.py

🤖 Sistema RAG - Menu Interativo
==================================================

📋 Opções disponíveis:
1. 📊 Ver informações do sistema
2. 📄 Indexar um PDF
3. 💬 Fazer uma pergunta
4. 🔍 Buscar documentos similares
5. 🤖 Modo chat interativo
6. 🧪 Testar conexões
7. 📖 Ver ajuda
0. 🚪 Sair

🎯 Escolha uma opção (0-7): 3

💬 Fazer Pergunta
------------------------------
💡 Sugestões de perguntas:
  1. O que é inteligência artificial?
  2. Quais são os tipos de IA?
  3. Quais são as aplicações da IA?
  4. Quais são os desafios da IA?
  5. Resuma o conteúdo em 3 pontos
  6. Pergunta personalizada...

🎯 Escolha uma pergunta (1-6): 1

❓ Pergunta: O que é inteligência artificial?
💡 Resposta: Inteligência Artificial (IA) é um campo da ciência da computação...
```

## 📁 **Estrutura de Arquivos:**

```
desafio_rag/
├── main.py              # 🎯 Script principal (execute este!)
├── src/
│   ├── main.py          # Lógica do menu interativo
│   ├── rag_chain.py     # Sistema RAG
│   ├── vector_store.py  # Gerenciador do banco
│   └── config.py        # Configurações
├── data/
│   └── documents/       # 📁 Coloque seus PDFs aqui
├── .env                 # 🔑 Configurações (OpenAI API key)
└── docker-compose.yml   # 🐳 Banco de dados
```

## 🔧 **Configuração Necessária:**

1. **Docker e Docker Compose** instalados
2. **Python 3.11+** com ambiente virtual
3. **Arquivo .env** configurado com:
   - `OPENAI_API_KEY=sua_chave_aqui`
   - `POSTGRES_PASSWORD=admin`

## 🚀 **Primeiros Passos:**

1. **Iniciar o banco de dados:**
   ```bash
   docker compose up -d
   ```

2. **Executar o sistema:**
   ```bash
   python main.py
   ```

3. **Seguir o menu:**
   - Escolha opção 6 para testar conexões
   - Escolha opção 2 para indexar um PDF
   - Escolha opção 3 para fazer perguntas

## 💡 **Dicas de Uso:**

- **PDFs**: Coloque seus documentos em `data/documents/`
- **Perguntas**: Use perguntas específicas para melhores respostas
- **Busca**: Experimente diferentes termos para encontrar conteúdo relevante
- **Chat**: Use o modo interativo para conversas mais longas

## 🆘 **Solução de Problemas:**

- **Erro de conexão**: Verifique se Docker está rodando
- **Erro de API**: Confirme sua chave OpenAI no arquivo `.env`
- **PDF não encontrado**: Verifique o caminho do arquivo
- **Sem documentos**: Indexe um PDF primeiro (opção 2)

---

**🎉 Agora você pode usar o Sistema RAG de forma simples e intuitiva!**
