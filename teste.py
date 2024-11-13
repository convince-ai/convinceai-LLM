from groq import Groq

client = Groq(api_key="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")

messages = [
    {
        "role": "system",
        "content": "Voce eh um vendedor da NetShoes."
    }
]
#user_message vem da api
def chatbot_conversation(user_message):
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

def receive_user_input(): # jogar fora dps
    while True:
        user_message = input("Usuário: ")
        chatbot_conversation(user_message)

receive_user_input()
