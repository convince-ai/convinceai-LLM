import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
def load_and_split_from_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tProducts;")  
        rows = cursor.fetchall()

        document_text = "\n\n".join([f"{row[1]} - {row[2]}" for row in rows])
        sections = document_text.split("\n\n")
        return sections

    except Exception as e:
        print(f"Erro ao carregar dados do banco: {e}")
        return []

    finally:
        if conn:
            conn.close()

