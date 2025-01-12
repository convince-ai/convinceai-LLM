import sqlite3
import gradio as gr
from readTxt import load_and_split_document
from emb import generate_embeddings
from retrieveData import retrieve_relevant_section
from groq import Groq
import re

# Inicializando o cliente
client = Groq(api_key="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")
messages = [
    {"role": "system", "content": "Voce é um classificador autómatico de dúvida. Classifique se for uma dúvida ou não. Se NÃO FOR, responda 'Nao' para QUALQUER coisa que voce receber. Se for, quero que voce retorne SEMPRE NESSE EXATO FORMATO ( isso é importante ): Produto: 'nome ESPECIFICO do produto (se tiver mais de um coloca o primeiro)', Duvida:'duvida explicada com os detalhes da duvida. não faça muito longo'. Não responda absolutamente NADA diferente do que te instrui. Eu vou te mandar umas informações adicionais para ajudar a entender o nome do PRODUTO que voce deve colocar. Se não tiver a informação adicional, tudo bem."}
]

# Função principal
def sendData(user_message):
    sections = load_and_split_document(r"products.txt")
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

        # Salvando no banco de dados SQLite
        db_name = "dataBase.db"
        conn = sqlite3.connect(db_name)
        try:
            # Criando tabela se não existir
            conn.execute('''
                CREATE TABLE IF NOT EXISTS t_Doubt (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    duvida TEXT NOT NULL
                )
            ''')

            # Inserindo dados
            conn.execute(
                "INSERT INTO t_Doubt (produto, duvida) VALUES (?, ?)",
                (produto, duvida)
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

# Definindo a interface do Gradio
interface = gr.Interface(
    fn=sendData,
    inputs=gr.Textbox(label="Sua mensagem"),
    outputs=gr.Textbox(label="Resposta do sistema"),
    title="Classificador de Dúvidas",
    description="Envie uma mensagem para classificar se a mensagem do usuário é uma dúvida. Caso seja, o sistema salvará a informação no banco de dados."
)

# Executando a interface
if __name__ == "__main__":
    interface.launch()
