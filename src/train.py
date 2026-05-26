import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "phishing_training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_risk_model.joblib")

def train():
    df = pd.read_csv(DATA_PATH)
    df["model_input"] = df["input_type"].astype(str) + " " + df["message"].astype(str)

    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    model.fit(df["model_input"], df["label"])

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ 模型已成功訓練並儲存至 {MODEL_PATH}")

if __name__ == "__main__":
    train()
