from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from emb import generate_embeddings
from readTxt import load_and_split_document

def retrieve_relevant_section(user_message, sections, embeddings):
    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    user_embedding = embedding_model.encode(user_message)  
    similarities = [1 - cosine(user_embedding, section_embedding) for section_embedding in embeddings]
    best_match_index = similarities.index(max(similarities))
    return sections[best_match_index]

# Para testar a função
if __name__ == "__main__":
    sections = load_and_split_document("products.txt")
    embeddings = generate_embeddings(sections)
    user_message = "Tem alguma camiseta vendendo?"
    relevant_section = retrieve_relevant_section(user_message, sections, embeddings)
    print("Seção relevante encontrada:\n", relevant_section)
