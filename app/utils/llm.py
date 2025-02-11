from groq import Groq
from readTxt import load_and_split_from_db
from emb import generate_embeddings
from retrieveData import retrieve_relevant_section
import logging
from sendToDb import sendData


client = Groq(api_key="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")

sections = load_and_split_from_db()
vectorizer_and_embeddings = generate_embeddings(sections)

# Prompt do sistema
SYSTEM_PROMPT = (
  "Você é um vendedor especializado nos produtos disponíveis em nossa loja. "
    "Se o cliente perguntar sobre algo que tenha informações disponíveis, responda fornecendo os detalhes do produto. "
    "Se não houver informações suficientes, responda com: 'Não encontrei exatamente, pode ser mais específico?'. "
    "Nunca invente informações e nunca mencione produtos que não estejam na base de dados. ")

MAX_MESSAGES = 20  

def chatbot_conversation(user_id, user_message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    retrieved_info = retrieve_relevant_section(user_message, sections, vectorizer_and_embeddings)
    print(retrieved_info)
    if retrieved_info:
        messages.append({"role": "system", "content": f"Informações adicionais: {retrieved_info}"})

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

if __name__ == "__main__":
    
    user_id = "3597537147"
    while True:
        user_message = input("Você: ")
        if user_message.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chatbot.")
            break
        response = chatbot_conversation(user_id, user_message)
        #sendData(user_message,user_id)
        print(f"Chatbot: {response}")
