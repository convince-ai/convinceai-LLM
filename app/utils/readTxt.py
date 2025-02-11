from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = "mongodb+srv://convinceai:c0QzGclHBI6KxYwR@convinceai-cluster.zh3r2.mongodb.net/events?retryWrites=true&w=majority&appName=convinceai-cluster"

def load_and_split_from_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client["events"]  
        collection = db["products"] 

        documents = list(collection.find())  

        if not documents:
            print("A coleção está vazia.")
            return []

        document_text = "\n\n".join([
            f"Nome: {doc.get('name', 'N/A')}\n"
            f"ID do Produto: {doc.get('productId', 'N/A')}\n"
            f"Preço: {doc.get('price', 'N/A')}\n"
            f"Descrição: {doc.get('description', 'N/A')}\n"
            for doc in documents
        ])

        sections = document_text.split("\n\n")  
        return sections
    
    except Exception as e:
        print(f"Erro ao carregar dados do banco: {e}")
        return []
    
    finally:
        client.close()

if __name__ == '__main__':
    sections = load_and_split_from_db()
    for section in sections:
        print(section)
        print("=" * 50)  
