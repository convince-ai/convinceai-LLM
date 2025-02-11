from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

def retrieve_relevant_section(user_message, sections, embeddings):
    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    user_embedding = embedding_model.encode(user_message)  
    similarities = [1 - cosine(user_embedding, section_embedding) for section_embedding in embeddings]
    best_match_index = similarities.index(max(similarities))
    print("best_macth foi" ,similarities[best_match_index])
    if similarities[best_match_index] >= 0.4:
        return sections[best_match_index]
    else:
        return ""
