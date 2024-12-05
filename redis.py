import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True) #seta uma porta

def get_user_messages(user_id, system_prompt): #puxa no redis o historico da conversa inteira
    session_key = f"user_session:{user_id}"
    session = redis_client.get(session_key)
    if session:
        return json.loads(session)
    else:
        initial_messages = [
            {"role": "system", "content": system_prompt}
        ]
        redis_client.set(session_key, json.dumps(initial_messages))
        return initial_messages

def update_user_messages(user_id, messages): #joga no redis a conversa inteira
    session_key = f"user_session:{user_id}"
    redis_client.set(session_key, json.dumps(messages))
