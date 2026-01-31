import os
import sys
import joblib
from data_processing_and_features import text_data_cleaning, tfidf_features_transform

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "model_classifier.pkl")
TFIDF_PATH = os.path.join(MODELS_DIR, "tfidf.pkl")

def predict_sentiment(text):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(TFIDF_PATH)
    cleaned = text_data_cleaning(text)
    X = tfidf_features_transform(cleaned, vectorizer)
    pred = model.predict(X)[0]
    return "positive" if int(pred) == 1 else "negative"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prediction.py \"your text here\"")
        sys.exit(1)
    text = sys.argv[1]
    result = predict_sentiment(text)
    print(f"Sentiment: {result}")
