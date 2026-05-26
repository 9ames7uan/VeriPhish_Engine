import pandas as pd
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_model():
    df = pd.read_csv("data/phishing_training_data.csv")
    df["model_input"] = df["input_type"].astype(str) + " " + df["message"].astype(str)
    
    X = df["model_input"]
    y = df["label"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/phishing_risk_model.joblib")
    print("✅ Model trained and saved to models/phishing_risk_model.joblib")

if __name__ == "__main__":
    train_model()
