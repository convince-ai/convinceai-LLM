from fastapi import FastAPI, Request
from app.services.whatsapp_service import send_whatsapp_message
from app.dependencies.config import get_api_config
from app.utils.llm import chatbot_conversation
import uvicorn
import asyncio
import aio_pika
import json


# Configuração de conexão com RabbitMQ
RABBITMQ_URL = "amqps://cubmgxvd:aQQMh2vs43A_MuVmU-z33rJ1eB6hZ9-G@shark.rmq.cloudamqp.com/cubmgxvd"  # Substitua pela sua URL de conexão
QUEUE_NAME = "abandoned-cart-events"  # Nome da fila que você está usando

async def consume_from_queue():
    """
    Consome mensagens da fila RabbitMQ e processa com a função webhook.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()  # Cria um canal
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)  # Declara a fila

        async for message in queue:  # Consome mensagens da fila
            async with message.process():
                payload = message.body.decode()  # Decodifica a mensagem da fila
                print(f"Mensagem recebida da fila: {payload}")
                try:
                    # Converte o payload da fila para um JSON e o passa para o webhook
                    request = MockRequest(json.loads(payload))
                    response = await webhook(request)
                    print(f"Resposta do webhook: {response}")
                except Exception as e:
                    print(f"Erro ao processar mensagem da fila: {e}")


class MockRequest:
    """
    Classe para simular um objeto Request do FastAPI.
    """
    def __init__(self, payload: dict):
        self._payload = payload

    async def json(self):
        return self._payload

# Configurando o ciclo de vida da aplicação
async def lifespan(app: FastAPI):
    # Inicialização (startup)
    task = asyncio.create_task(consume_from_queue())
    print("Consumidor RabbitMQ iniciado.")
    
    # Yield para liberar execução
    yield
    
    # Encerramento (shutdown)
    task.cancel()
    print("Consumidor RabbitMQ encerrado.")

app = FastAPI(
    title="WhatsApp Integration API",
    description="API para integração com WhatsApp e processamento de mensagens via LLM",
    version="1.0.0",
     lifespan=lifespan
)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Recebe o payload do webhook
        payload = await request.json()
        
        # Extrai os dados necessários
        sender = payload.get("phone")
        product = payload.get("product")

        print(sender)
        print(product)
        
        if not sender or not product:
            return {"error": "Sender e product são obrigatórios"}
        
        # Garante que o número está no formato correto (com 55)
        if not sender.startswith("55"):
            sender = f"55{sender}"
            
        # Processa a mensagem usando o RAG e Grok
        response = chatbot_conversation(sender, product)
        
        # Obtém as configurações da API do WhatsApp
        config = get_api_config()
        
        # Envia a resposta via WhatsApp
        send_whatsapp_message(
            apikey=config["apikey"],
            url=config["url"],
            number=sender,
            text=response
        )
        
        # Retorna a resposta do LLM junto com o status
        return {
            "status": "success", 
            "message": "Mensagem processada com sucesso",
            "llm_response": response
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/webhook_zap")
async def webhook_zap(request: Request):
    try:
        # Recebe o payload do webhook
        payload = await request.json()
        
        # Verifica se é um evento de mensagem
        if payload.get("event") != "messages.upsert":
            return {"status": "ignored", "message": "Evento não é messages.upsert"}
            
        # Extrai os dados da mensagem
        data = payload.get("data", {})
        message_data = data.get("message", {})
        conversation = message_data.get("conversation")
        
        if not conversation:
            return {"status": "error", "message": "Mensagem não encontrada"}
            
        # Extrai o número do remetente do campo key.remoteJid
        sender = data.get("key", {}).get("remoteJid")
        if not sender:
            return {"status": "error", "message": "Remetente não encontrado"}
            
        # Remove o sufixo @s.whatsapp.net se presente
        sender = sender.replace("@s.whatsapp.net", "")
        
        # Processa a mensagem usando o RAG e Grok
        response = chatbot_conversation(sender, conversation)
        
        # Obtém as configurações da API do WhatsApp
        config = get_api_config()
        
        # Envia a resposta via WhatsApp
        send_whatsapp_message(
            apikey=config["apikey"],
            url=config["url"],
            number=sender,
            text=response
        )
        
        return {
            "status": "success",
            "message": "Mensagem processada com sucesso",
            "llm_response": response
        }
        
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
