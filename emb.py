from sentence_transformers import SentenceTransformer
from readTxt import load_and_split_document
#pip install sentence-transformers
def generate_embeddings(sections):
    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Modelo de embeddings
    embeddings = [embedding_model.encode(section) for section in sections]
    return embeddings

if __name__ == "__main__":
    sections = load_and_split_document("products.txt")
    embeddings = generate_embeddings(sections)
    print("Embeddings done.")
