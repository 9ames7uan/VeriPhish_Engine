import os
import joblib

MODEL_PATH = "models/phishing_risk_model.joblib"
_ml_model = None

def get_ml_model():
    global _ml_model
    if _ml_model is None:
        if os.path.exists(MODEL_PATH):
            _ml_model = joblib.load(MODEL_PATH)
    return _ml_model

def ml_predict_label(content: str, input_type: str):
    model = get_ml_model()
    if model is None:
        return None, {}
    
    try:
        model_input = f"{input_type} {content}"
        label = model.predict([model_input])[0]
        proba = model.predict_proba([model_input])[0]
        classes = model.classes_
        scores = {cls: float(round(p, 3)) for cls, p in zip(classes, proba)}
        return label, scores
    except Exception:
        return None, {}
