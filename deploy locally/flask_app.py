from flask import Flask, render_template, request
import os
import joblib
from data_processing_and_features import text_data_cleaning, tfidf_features_transform

app = Flask(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "model_classifier.pkl")
TFIDF_PATH = os.path.join(MODELS_DIR, "tfidf.pkl")

try:
    model = joblib.load(MODEL_PATH)
    tfidf_vectorizer = joblib.load(TFIDF_PATH)
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    tfidf_vectorizer = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        text = request.args.get("text", "")
        if not text:
            return render_template("index.html")
        review = text
    else:
        review = request.form.get("Review", "")
    cleaned = text_data_cleaning(review)
    if model and tfidf_vectorizer:
        X = tfidf_features_transform(cleaned, tfidf_vectorizer)
        pred = model.predict(X)[0]
        label = "positive" if int(pred) == 1 else "negative"
        return render_template("index.html", prediction_text=f"The sentiment is {label}")
    return render_template("index.html", prediction_text="Model or Vectorizer not found.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
