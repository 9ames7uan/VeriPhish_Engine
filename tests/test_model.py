import joblib
import pytest
import os
import pandas as pd
from src.utils import BASE_DIR

MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_risk_model.joblib")

def test_model_prediction():
    model = joblib.load("models/phishing_risk_model.joblib")

    test_messages = [
        {
            "input_type": "SMS",
            "message": "【銀行通知】您的帳戶異常，請立即點擊 https://bit.ly/verify 重新輸入密碼與OTP，否則帳戶將被凍結。"
        },
        {
            "input_type": "LINE",
            "message": "明天下午三點開會，請記得帶筆電。"
        },
        {
            "input_type": "SMS",
            "message": "您的包裹配送狀態異常，請盡快確認收件資訊。"
        }
    ]

    for item in test_messages:
        text = item["input_type"] + " " + item["message"]
        pred = model.predict([text])[0]
        proba = model.predict_proba([text])[0]
        classes = model.classes_

        print("\n訊息：", item["message"])
        print("模型判斷：", pred)
        print("信心分數：", dict(zip(classes, proba.round(3))))
        print("-" * 60)

        assert pred in ["RED", "YELLOW", "GREEN"]

def test_path_and_model_load():
    assert os.path.exists(MODEL_PATH), "Model file missing!"
    model = joblib.load(MODEL_PATH)
    assert hasattr(model, "predict"), "Invalid model format"

@pytest.mark.parametrize("bad_input", ["", "   ", "A"*1000])
def test_robustness_input(bad_input):
    model = joblib.load(MODEL_PATH)
    pred = model.predict([bad_input])[0]
    assert pred in ["RED", "YELLOW", "GREEN"]

def test_data_deduplication():
    df = pd.DataFrame([{"message": "A", "input_type": "SMS", "label": "RED"},
                       {"message": "A", "input_type": "SMS", "label": "RED"}])
    deduplicated = df.drop_duplicates(subset=["message", "input_type", "label"])
    assert len(deduplicated) == 1

def test_feedback_schema():
    payload = {"message": "Test", "predicted_label": "GREEN", "correct_label": "RED"}
    assert "message" in payload and "correct_label" in payload
