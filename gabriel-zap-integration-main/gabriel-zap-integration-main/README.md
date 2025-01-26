# Integração WhatsApp com RAG e LLM

Este projeto implementa um chatbot integrado ao WhatsApp utilizando RAG (Retrieval Augmented Generation) e LLM (Large Language Model) para processar e responder mensagens de forma contextualizada.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta na plataforma Jimibrasil WhatsApp API
- Chave de API da Groq

## Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd gabriel-zap-integration-main
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
- No arquivo `app/dependencies/config.py`:
  - Substitua a `apikey` pela sua chave da API Jimibrasil
  - Verifique se a `url` está correta

- No arquivo `app/utils/llm.py`:
  - Substitua a chave da API Groq

## Executando o Projeto

1. Inicie o servidor FastAPI:
```bash
python -m uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

## Endpoints

### POST /webhook
Recebe mensagens do WhatsApp no formato:
```json
{
  "sender": "5511999999999",
  "message": "texto da mensagem"
}
```

## Executando os Testes de Integração

1. Certifique-se que o servidor FastAPI está rodando em um terminal

2. Em outro terminal, execute:
```bash
python test_integration.py
```

O script de teste irá:
- Testar o webhook enviando uma mensagem de teste
- Testar o envio direto de mensagem para um número específico
- Mostrar os resultados detalhados de cada teste

### Estrutura dos Testes

O arquivo `test_integration.py` contém dois testes principais:

1. `test_webhook()`: Testa o endpoint do webhook
   - Simula o recebimento de uma mensagem
   - Verifica o processamento e resposta

2. `test_direct_message()`: Testa o envio direto de mensagem
   - Envia uma mensagem para um número específico
   - Verifica a resposta da API

## Estrutura do Projeto

```
.
├── app/
│   ├── dependencies/
│   │   └── config.py         # Configurações da API
│   ├── services/
│   │   └── whatsapp_service.py  # Serviço de envio de mensagens
│   └── utils/
│       ├── emb.py           # Geração de embeddings
│       ├── llm.py           # Integração com LLM
│       ├── products.txt     # Catálogo de produtos
│       ├── readTxt.py       # Leitura de arquivos
│       └── retrieveData.py  # Recuperação de dados
├── test_integration.py      # Testes de integração
└── requirements.txt         # Dependências do projeto
```

## Troubleshooting

1. Erro de conexão com o webhook:
   - Verifique se o servidor FastAPI está rodando
   - Confirme se a porta 8000 está disponível

2. Erro na API do WhatsApp:
   - Verifique se a apikey está correta
   - Confirme se o número está no formato correto (com código do país 55)

3. Erro no processamento LLM:
   - Verifique se a chave da API Groq está correta
   - Confirme se o arquivo products.txt existe e está acessível
