from sklearn.metrics.pairwise import cosine_similarity
from .emb import generate_embeddings
from .readTxt import load_and_split_document

def retrieve_top_matches(user_message, sections, vectorizer_and_embeddings, top_n=2):
    vectorizer, embeddings = vectorizer_and_embeddings
    user_vector = vectorizer.transform([user_message])
    
    # Calcular similaridade entre a mensagem do usuário e todas as seções
    similarities = cosine_similarity(user_vector, embeddings).flatten()
    
    # Pegar os top_n índices com maior similaridade
    top_indices = similarities.argsort()[-top_n:][::-1]
    top_matches = [(sections[i], similarities[i]) for i in top_indices]
    return top_matches

if __name__ == "__main__":
    sections = load_and_split_document("products.txt")
    vectorizer_and_embeddings = generate_embeddings(sections)
    user_message = "Tem curso de python?"
    top_matches = retrieve_top_matches(user_message, sections, vectorizer_and_embeddings, top_n=2)
    
    print("Melhores seções relevantes encontradas:")
    for i, (section, similarity) in enumerate(top_matches, 1):
        print(f"\nMatch {i}:")
        print(f"Seção: {section}")
        print(f"Similaridade: {similarity:.4f}")
