import joblib
import pytest

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
