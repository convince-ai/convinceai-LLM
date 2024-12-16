import requests
import json

def send_whatsapp_message(apikey, url, number, text, delay=0, quoted=None, link_preview=True, mentions_everyone=False, mentioned=[]):
    """
    Envia mensagem para o WhatsApp usando a API Jimibrasil.

    :param apikey: Chave da API fornecida pela Jimibrasil.
    :param url: URL base da API Jimibrasil.
    :param number: Número do WhatsApp do destinatário.
    :param text: Texto da mensagem a ser enviada.
    :param delay: Delay opcional (em milissegundos).
    :param quoted: Referência a uma mensagem específica (opcional).
    :param link_preview: Mostrar preview de links na mensagem.
    :param mentions_everyone: Mencionar todos na conversa.
    :param mentioned: Lista de números mencionados.
    :return: Resposta da API.
    """
    headers = {
        "Content-Type": "application/json",
        "apikey": apikey,
    }

    payload = {
        "number": number,
        "text": text,
    }

    try:
        print(f"Enviando mensagem para {number} com payload:", json.dumps(payload, indent=2))
        response = requests.post(
            f"{url}/message/sendText/Enzo",
            headers=headers,
            json=payload  # Usando json em vez de data
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            error_message = f"Erro na API do WhatsApp: Status {response.status_code}"
            try:
                error_detail = response.json()
                error_message += f" - {json.dumps(error_detail)}"
            except:
                error_message += f" - {response.text}"
            raise Exception(error_message)
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao enviar mensagem: {str(e)}")
