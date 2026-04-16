# predictor.py  (SAFE for PyQt + Windows)
import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_model = None
_preprocessor = None
_label_encoder = None


def _load_artifacts():
    """
    Lazy-load ML artifacts.
    This prevents PyQt + TensorFlow startup crashes on Windows.
    """
    global _model, _preprocessor, _label_encoder

    if _model is None:
        from tensorflow.keras.models import load_model  # imported ONLY when needed

        preprocessor_path = os.path.join(BASE_DIR, "preprocessor.joblib")
        encoder_path = os.path.join(BASE_DIR, "label_encoder.joblib")
        model_path = os.path.join(BASE_DIR, "ANN_model.keras")

        if not os.path.exists(model_path):
            raise FileNotFoundError("ANN_model.keras not found in ml folder")

        _preprocessor = joblib.load(preprocessor_path)
        _label_encoder = joblib.load(encoder_path)
        _model = load_model(model_path)


def predict_final_grade(input_data: dict):
    """
    Takes dict from GUI and returns predicted grade safely.
    """
    _load_artifacts()

    df = pd.DataFrame([input_data])

    # Ensure training columns exist
    for col in _preprocessor.feature_names_in_:
        if col not in df.columns:
            df[col] = 0

    X = _preprocessor.transform(df)

    y_pred = np.argmax(_model.predict(X, verbose=0), axis=1)
    return _label_encoder.inverse_transform(y_pred)[0]
