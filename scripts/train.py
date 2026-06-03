import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import os

def run_training():
    data_path = "data/phishing_training_data.csv"
    model_output = "models/phishing_risk_model.joblib"
    
    df = pd.read_csv(data_path)
    X = df["message"]
    y = df["label"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression())
    ])

    model.fit(X, y)

    if not os.path.exists("models"):
        os.makedirs("models")
        
    joblib.dump(model, model_output)
    print(f"✅ 模型已成功訓練並儲存至 {model_output}")

if __name__ == "__main__":
    run_training()
