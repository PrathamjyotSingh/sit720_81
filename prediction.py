import joblib
import pandas as pd


MODEL_PATH = "housing_price_model_final.pkl"


def load_model():
    """Load and return the trained housing price model."""
    return joblib.load(MODEL_PATH)


def predict_price(
    model,
    suburb,
    property_type,
    beds,
    baths,
    parking,
    sale_year,
    sale_month
):
    """Generate a housing price prediction from property details."""

    input_df = pd.DataFrame([{
        "Suburb": suburb,
        "Type": property_type,
        "Beds": beds,
        "Baths": baths,
        "Parking": parking,
        "Sale Year": sale_year,
        "Sale Month": sale_month
    }])

    prediction = model.predict(input_df)[0]

    return prediction
