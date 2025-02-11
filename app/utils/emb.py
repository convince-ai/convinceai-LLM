from sentence_transformers import SentenceTransformer
def generate_embeddings(sections):
    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Modelo de embeddings
    embeddings = [embedding_model.encode(section) for section in sections]
    return embeddings
