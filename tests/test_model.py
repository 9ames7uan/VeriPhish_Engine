import joblib

def test_model_loading():
    model = joblib.load("models/phishing_risk_model.joblib")
    assert model is not None
    print("✅ Model loaded successfully for testing")
