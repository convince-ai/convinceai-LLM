from sklearn.feature_extraction.text import TfidfVectorizer
from .readTxt import load_and_split_document

def generate_embeddings(sections):
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(sections)
    return vectorizer, embeddings

