import os
import joblib
import logging
from src.utils import BASE_DIR

logger = logging.getLogger(__name__)

class InferenceEngine:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InferenceEngine, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        model_path = os.path.join(BASE_DIR, "models", "phishing_risk_model.joblib")
        if os.path.exists(model_path):
            try:
                self._model = joblib.load(model_path)
                logger.info(f"Model successfully loaded from {model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self._model = None
        else:
            logger.warning(f"Model file not found at {model_path}")

    def predict(self, content: str, input_type: str):
        if self._model is None:
            return None, {}
        
        try:
            model_input = f"{input_type} {content}"
            label = self._model.predict([model_input])[0]
            proba = self._model.predict_proba([model_input])[0]
            classes = self._model.classes_
            scores = {cls: float(round(p, 3)) for cls, p in zip(classes, proba)}
            return label, scores
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return None, {}

def ml_predict_label(content: str, input_type: str):
    engine = InferenceEngine()
    return engine.predict(content, input_type)
