import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stemmer = PorterStemmer()
STOPWORDS = set(stopwords.words('english'))

def text_data_cleaning(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in STOPWORDS]
    return " ".join(words)

def tfidf_features_transform(text, vectorizer):
    return vectorizer.transform([text])
