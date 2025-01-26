import requests
import json
from app.dependencies.config import get_api_config

def test_webhook():
    # URL do webhook
    webhook_url = "http://localhost:8000/webhook"
    
    # Dados do teste - formato correto do body
    payload = {
        "sender": "5511932187933",
        "message": "Oi"
    }
    
    try:
        print("Enviando payload para o webhook:", json.dumps(payload, indent=2))
        # Faz a requisição POST para o webhook
        response = requests.post(webhook_url, json=payload)
        
        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            print("Teste do webhook bem sucedido!")
            print("Status code:", response.status_code)
            print("Resposta:", response.json())
        else:
            print(f"Erro no webhook! Status code: {response.status_code}")
            print("Resposta:", response.text)
            
    except Exception as e:
        print(f"Erro ao fazer a requisição para o webhook: {str(e)}")

def test_direct_message():
    # Configurações da API
    config = get_api_config()
    
    # Headers para a requisição
    headers = {
        "Content-Type": "application/json",
        "apikey": config["apikey"]
    }
    
    # Payload para envio direto
    payload = {
        "number": "5537999472404",
        "text": "Teste de integração direto para a API"
    }
    
    try:
        print("Enviando mensagem direta com payload:", json.dumps(payload, indent=2))
        # Faz a requisição POST direta para a API do WhatsApp
        response = requests.post(
            f"{config['url']}/message/sendText/Enzo",
            headers=headers,
            json=payload
        )
        
        # Verifica se a requisição foi bem sucedida
        if response.status_code in [200, 201]:
            print("\nTeste de envio direto bem sucedido!")
            print("Status code:", response.status_code)
            print("Resposta:", json.dumps(response.json(), indent=2))
        else:
            print(f"\nErro no envio direto! Status code: {response.status_code}")
            print("Resposta:", response.text)
            
    except Exception as e:
        print(f"\nErro ao fazer o envio direto: {str(e)}")

if __name__ == "__main__":
    print("Iniciando testes de integração...")
    print("\n1. Testando webhook:")
    test_webhook()
    print("\n2. Testando envio direto para o número específico:")
    test_direct_message()
