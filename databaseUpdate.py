import sqlite3
import datetime
def connect_to_db():
    conn = sqlite3.connect('database_mensages.db') #aqui ta localmente conectado ao meu banco
    return conn

def get_user_messages_from_db(user_id,MAX_MESSAGES ):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mc.MENSAGEM_CLIENTE, rl.RESP_LLM 
        FROM MENSAGE_CLIENT mc
        INNER JOIN RESP_LLM rl ON mc.TELEFONE_CLIENTE = rl.TELEFONE_CLIENTE
        WHERE mc.TELEFONE_CLIENTE=?
        ORDER BY mc.DATA_RESPOSTA DESC
        LIMIT ?
    """, (user_id, MAX_MESSAGES))
    messages = cursor.fetchall()
    conn.close()
    return messages


def update_user_messages_in_db(user_id, new_message, new_response): #aqui vai dar insert no banco com as info gerada
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MENSAGE_CLIENT (telefone_cliente, mensagem_cliente, data_resposta) VALUES (?, ?, ?)", (user_id, new_message, datetime.now()))
    cursor.execute("INSERT INTO RESP_LLM (telefone_cliente, resp_llm, data_resposta) VALUES (?, ?, ?)", (user_id, new_response, datetime.now()))
    conn.commit()
    conn.close()