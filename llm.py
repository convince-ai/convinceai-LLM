from fastapi import APIRouter, Form, Request, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
from readTxt import load_and_split_document
from emb import generate_embeddings
from retrieveData import retrieve_top_matches
from databaseUpdate import get_user_messages_from_db, update_user_messages_in_db
import json
import logging
client = Groq(api_key="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")

sections = load_and_split_document("products.txt")
embeddings = generate_embeddings(sections)

# Prompt do sistema
SYSTEM_PROMPT = (
    "Você é um vendedor serio especializado em nossos produtos. Responda somente o que for perguntado, "
    "sem enrolar demais. Se o cliente perguntar sobre algo que nao tem na loja, simplesmente responda "
    "'Nao encontrei exatamente, pode ser mais especifico?'. Nao de informacao de nada que nao tenha a ver "
    "com a pergunta do usuario. Se o cliente perguntar de algo que nao esta nas informacoes adicionais, "
    "diga que nao tem certeza, para confirmar no site oficial."
)

MAX_MESSAGES = 20  

def chatbot_conversation(user_id, user_message):
    messages = get_user_messages_from_db(user_id, MAX_MESSAGES)
    top_matches = retrieve_top_matches(user_message, sections, embeddings, top_n=2)
    
    if top_matches:
        retrieved_info = "\n\n".join(
            [f"Informação relevante {i+1}: {section}\nSimilaridade: {similarity:.4f}" 
             for i, (section, similarity) in enumerate(top_matches)]
        )
        messages.append({"role": "system", "content": f"Informações adicionais:\n{retrieved_info}"})

    messages = messages[-MAX_MESSAGES:]

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,  
            stop=None,
        )

        bot_response = completion.choices[0].message['content']

    except Exception as e:
        logging.error(f"Erro na comunicação com a API Groq: {e}")
        bot_response = "Desculpe, estou enfrentando dificuldades no momento. Por favor, tente novamente mais tarde."

    messages.append({"role": "assistant", "content": bot_response})

    update_user_messages_in_db(user_id, user_message, bot_response)

    logging.info(f"Resposta para {user_id}: {bot_response}")

    return bot_response


#API FICA DAQUI PRA BAIXO (MINEIRO OLHA PF)
'''@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    incoming_msg = Body.strip()
    from_number = From

    logging.info(f"Recebido mensagem de {from_number}: {incoming_msg}")

    if not incoming_msg:
        logging.warning("Mensagem vazia recebida.")
        return MessagingResponse().to_xml()

    response_text = chatbot_conversation(from_number, incoming_msg)

    resp = MessagingResponse()
    resp.message(response_text)
    logging.info(f"Enviado resposta para {from_number}: {response_text}")
    return str(resp)
'''