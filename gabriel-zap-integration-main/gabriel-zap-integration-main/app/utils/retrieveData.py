from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from .emb import generate_embeddings
from .readTxt import load_and_split_document
import numpy as np  

def retrieve_top_matches(user_message, sections, embeddings, top_n=2):
    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    user_embedding = embedding_model.encode(user_message)
    similarities = [1 - cosine(user_embedding, section_embedding) for section_embedding in embeddings]
    
    top_indices = np.argsort(similarities)[-top_n:][::-1]  
    top_matches = [(sections[i], similarities[i]) for i in top_indices]
    return top_matches

if __name__ == "__main__":
    sections = load_and_split_document("products.txt")
    embeddings = generate_embeddings(sections)
    user_message = "Tem curso de python?"
    top_matches = retrieve_top_matches(user_message, sections, embeddings, top_n=2)
    
    print("Melhores seções relevantes encontradas:")
    for i, (section, similarity) in enumerate(top_matches, 1):
        print(f"\nMatch {i}:")
        print(f"Seção: {section}")
        print(f"Similaridade: {similarity:.4f}")
