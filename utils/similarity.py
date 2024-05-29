# utils.similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
# Function to calculate cosine similarity between two text documents
def calculate_cosine_similarity(text1, text2):
    # Load Spacy model
    nlp = spacy.load('en_core_web_sm')

    # Tokenize and lemmatize using Spacy
    tokens1 = ' '.join([token.lemma_ for token in nlp(text1.lower())])
    tokens2 = ' '.join([token.lemma_ for token in nlp(text2.lower())])

    # Use scikit-learn for TF-IDF vectorization
    vectorizer = TfidfVectorizer()

    # Transform the text data to TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([tokens1, tokens2])

    # Calculate cosine similarity between tfidf vectors
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_similarities[0][0]
