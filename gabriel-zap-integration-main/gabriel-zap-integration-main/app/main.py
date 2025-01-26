from fastapi import FastAPI, Request
from app.services.whatsapp_service import send_whatsapp_message
from app.dependencies.config import get_api_config
from app.utils.llm import chatbot_conversation
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Recebe o payload do webhook
        payload = await request.json()
        
        # Extrai os dados necessários
        sender = payload.get("sender")
        message = payload.get("message")
        
        if not sender or not message:
            return {"error": "Sender e message são obrigatórios"}
        
        # Garante que o número está no formato correto (com 55)
        if not sender.startswith("55"):
            sender = f"55{sender}"
            
        # Processa a mensagem usando o RAG e Grok
        response = chatbot_conversation(sender, message)
        
        # Obtém as configurações da API do WhatsApp
        config = get_api_config()
        
        # Envia a resposta via WhatsApp
        send_whatsapp_message(
            apikey=config["apikey"],
            url=config["url"],
            number=sender,
            text=response
        )
        
        return {"status": "success", "message": "Mensagem processada com sucesso"}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
