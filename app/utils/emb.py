from sklearn.feature_extraction.text import TfidfVectorizer
from .readTxt import load_and_split_document

def generate_embeddings(sections):
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(sections)
    return vectorizer, embeddings

if __name__ == "__main__":
    sections = load_and_split_document("products.txt")
    vectorizer, embeddings = generate_embeddings(sections)
    print("Embeddings done.")
