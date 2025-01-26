from fastapi import APIRouter
from groq import Groq
from .readTxt import load_and_split_document
from .emb import generate_embeddings
from .retrieveData import retrieve_top_matches
import logging

client = Groq(api_key="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")

sections = load_and_split_document("app/utils/products.txt")
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
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    top_matches = retrieve_top_matches(user_message, sections, embeddings, top_n=2)
    
    if top_matches:
        retrieved_info = "\n\n".join(
            [f"Informação relevante {i+1}: {section}\nSimilaridade: {similarity:.4f}" 
             for i, (section, similarity) in enumerate(top_matches)]
        )
        messages.append({"role": "system", "content": f"Informações adicionais:\n{retrieved_info}"})

    messages.append({"role": "user", "content": user_message})

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

        bot_response = completion.choices[0].message.content

    except Exception as e:
        logging.error(f"Erro na comunicação com a API Groq: {e}")
        bot_response = "Desculpe, estou enfrentando dificuldades no momento. Por favor, tente novamente mais tarde."

    logging.info(f"Resposta para {user_id}: {bot_response}")

    return bot_response
