import requests
import json

def send_whatsapp_message(apikey, url, number, text):
    """
    Envia mensagem para o WhatsApp usando a API zap-go.
    """
    headers = {
        "apikey": apikey,
        "Content-Type": "application/json"
    }

    payload = {
        "number": number,
        "text": text,
        "delay": 0,
        "linkPreview": True,
        "mentionsEveryOne": False,
        "mentioned": [number]  # Incluindo o número do destinatário no campo mentioned
    }

    try:
        print("\nEnviando mensagem WhatsApp:")
        print(f"URL: {url}/message/sendText/Gabriel")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.request(
            "POST",
            f"{url}/message/sendText/Gabriel",
            json=payload,
            headers=headers
        )
        
        print(f"\nResposta da API: {response.text}")
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Erro ao enviar mensagem: {response.text}")
            
    except Exception as e:
        print(f"\nErro ao enviar mensagem: {str(e)}")
        raise e
