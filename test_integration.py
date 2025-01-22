import requests
import json
from app.utils.llm import chatbot_conversation

def test_integration():
    print("Iniciando teste de integração...")
    
    # Simulando recebimento de mensagem
    sender = "5535997537147"
    message = "Me fale quem você é"
    
    print(f"\nMensagem recebida:")
    print(f"De: {sender}")
    print(f"Mensagem: {message}")
    
    try:
        # Processando com LLM
        print("\nProcessando mensagem com LLM...")
        llm_response = chatbot_conversation(sender, message)
        print(f"\nResposta do LLM: {llm_response}")
        
        # Configurações da API
        url = "https://api.whatsapp.jimibrasil.com.br/message/sendText/Gabriel"
        apikey = "IlTMUUnmBCCtYMnNIkPppLZVvqRsarSb"
        
        # Headers
        headers = {
            "Content-Type": "application/json",
            "apikey": apikey
        }
        
        payload = {
            "number": sender,
            "text": llm_response,
            "delay": 0,
            "quoted": {
                "key": {
                    "remoteJid": f"{sender}@s.whatsapp.net",
                    "fromMe": True,
                    "id": "123",
                    "participant": sender
                },
                "message": {
                    "conversation": message
                }
            },
            "linkPreview": True,
            "mentionsEveryOne": True,
            "mentioned": [sender]
        }
        
        print("\nEnviando resposta via WhatsApp...")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Fazendo a requisição POST
        response = requests.request(
            "POST",
            url,
            json=payload,
            headers=headers
        )
        
        print(f"\nResposta da API: {response.text}")
        
        if response.status_code in [200, 201]:
            print("\nMensagem enviada com sucesso!")
            print("Detalhes da resposta:", json.dumps(response.json(), indent=2))
        else:
            print(f"\nErro ao enviar mensagem: {response.status_code}")
            print("Resposta:", response.text)
            
    except Exception as e:
        print(f"\nErro durante o teste: {str(e)}")

if __name__ == "__main__":
    test_integration()
