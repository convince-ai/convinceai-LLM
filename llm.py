from groq import Groq
from readTxt import load_and_split_document
from emb import generate_embeddings
from retrieveData import retrieve_relevant_section

client = Groq(api_key="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")

messages = [
    {"role": "system", "content": "Você é um vendedor serio especializado em nossos produtos. Responda somente o que for perguntado, sem enrolar demais. Se o cliente perguntar sobre algo que nao tem na loja, simplesmente responda 'Nao encontrei exatamente, pode ser mais especifico?'. Nao de informacao de  nada que nao tenha a ver com a pergunta do usuario. Se o cliente perguntar de algo que nao esta nas informacoes adicionais, diga que nao tem certeza, para confirmar no site oficial."}
]

def chatbot_conversation(user_message, sections, embeddings):
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
        print(content, end="")
        bot_response += content

    messages.append({"role": "assistant", "content": bot_response})
    print("\n")
    return bot_response

def receive_user_input():
    sections = load_and_split_document("products.txt")
    embeddings = generate_embeddings(sections)
    while True:
        user_message = input("Usuário: ")
        chatbot_conversation(user_message, sections, embeddings)

if __name__ == "__main__":
    receive_user_input()
