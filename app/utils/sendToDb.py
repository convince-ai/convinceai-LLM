from readTxt import load_and_split_from_db
from emb import generate_embeddings
from retrieveData import retrieve_relevant_section
from groq import Groq
import re
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = "postgresql://postgres:xbWgboNUGCJJOjgfnHmDZnCcdJBavZFM@monorail.proxy.rlwy.net:30453/railway"
GROQ_KEY = "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"
client = Groq(api_key=GROQ_KEY)
messages = [
    {"role": "system", "content": "Voce é um classificador autómatico de dúvida. Classifique se for uma dúvida ou não. Se NÃO FOR, responda 'Nao' para QUALQUER coisa que voce receber. Se for, quero que voce retorne SEMPRE NESSE EXATO FORMATO ( isso é importante ): Produto: 'nome ESPECIFICO do produto (se tiver mais de um coloca o primeiro)', Duvida:'duvida descrita pelo usuario(Exemplo: a duvida foi sobre o preco)'. Não responda absolutamente NADA diferente do que te instrui. Eu vou te mandar umas informações adicionais para ajudar a entender o nome do PRODUTO que voce deve colocar. Se não tiver alguma informacao adicional, responda que nao eh uma duvida."}
]

# Função principal
def sendData(user_message, user_number):
    sections = load_and_split_from_db()
    embeddings = generate_embeddings(sections)
    retrieved_info = retrieve_relevant_section(user_message, sections, embeddings)
    
    if retrieved_info:
        messages.append({"role": "system", "content": f"Informações adicionais: {retrieved_info}"})

    messages.append({"role": "user", "content": user_message})
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    bot_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        bot_response += content
        match = re.search(r"Produto:\s*'([^']*)',\s*Duvida:\s*'([^']*)'", bot_response)
    
    if match:
        produto = match.group(1)
        duvida = match.group(2)
        conn = psycopg2.connect(DATABASE_URL)
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tdoubts (produto, duvida, number) VALUES (%s, %s, %s)",
                    (produto, duvida, user_number)
                )
                conn.commit()
            db_message = "Added in database"
        except Exception as e:
            db_message = f"Error: {e}"
        finally:
            conn.close()
        
        return f"{bot_response}\n{db_message}"
    else:
        return "Não é dúvida."