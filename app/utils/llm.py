from groq import Groq
from readTxt import load_and_split_from_db
from emb import generate_embeddings
from retrieveData import retrieve_relevant_section
from sendToDb import sendData
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_KEY = os.getenv("GROQ_KEY")
client = Groq(api_key=GROQ_KEY)
sections = load_and_split_from_db()
embeddings = generate_embeddings(sections)

messages = [
    {
        "role": "system",
        "content": (
            "Você é um vendedor especializado em nossos produtos. "
            "Seu objetivo é responder diretamente às perguntas do cliente, sempre com base nas informações adicionais disponíveis. "
            "Consulte as informações adicionais fornecidas antes de responder. "
            "Se as informações adicionais não forem suficientes para responder ou se a pergunta não estiver clara, peça mais detalhes ao cliente ou sugira verificar o site oficial para confirmar. "
            "NUNCA invente informações que não constem nas informações adicionais."
        )
    }
]

def chatbot_conversation(number, user_message):
    sendData(user_message, number)
    retrieved_info = retrieve_relevant_section(user_message, sections, embeddings)
    
    if retrieved_info:
        messages.append({"role": "system", "content": f"Informações adicionais: {retrieved_info}"})
    print(retrieved_info)
    messages.append({"role": "user", "content": user_message})
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192", #aqui é possível mudar o modelo a qualquer momento ( como um adapter)
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
        print(content, end="")
        bot_response += content

    messages.append({"role": "assistant", "content": bot_response})
    print("\n")
    return bot_response