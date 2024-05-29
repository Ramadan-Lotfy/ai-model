# utils.preprocessing.py
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [word for word in tokens if word not in string.punctuation]

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    processed_text = ' '.join(tokens)

    return processed_text
