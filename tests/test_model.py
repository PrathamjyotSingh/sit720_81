import joblib


MODEL_PATH = "housing_price_model_final.pkl"


def test_model_file_exists():
    """Test that the trained model file exists."""
    import os

    assert os.path.exists(MODEL_PATH)


def test_model_has_predict_method():
    """Test that the loaded model supports prediction."""
    model = joblib.load(MODEL_PATH)

    assert hasattr(model, "predict")


def test_model_accepts_expected_features():
    """Test that the model can process the expected input features."""
    import pandas as pd

    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([{
        "Suburb": "PEN",
        "Type": "House",
        "Beds": 3,
        "Baths": 2,
        "Parking": 1,
        "Sale Year": 2026,
        "Sale Month": 6
    }])

    prediction = model.predict(input_df)

    assert len(prediction) == 1
