import streamlit as st

from prediction import load_model, predict_price


model = load_model()

st.title("Sydney Housing Price Predictor")

st.write("Enter property details to get a predicted sale price.")

suburb = st.selectbox(
    "Suburb",
    ["PEN", "PAR", "SUR"]
)

property_type = st.selectbox(
    "Type",
    ["House", "Apartment", "Unit", "Townhouse", "Villa"]
)

beds = st.number_input(
    "Bedrooms",
    min_value=0,
    max_value=10,
    value=2
)

baths = st.number_input(
    "Bathrooms",
    min_value=0,
    max_value=10,
    value=1
)

parking = st.number_input(
    "Parking Spaces",
    min_value=0,
    max_value=10,
    value=1
)

sale_year = st.number_input(
    "Sale Year",
    min_value=2020,
    max_value=2030,
    value=2026
)

sale_month = st.number_input(
    "Sale Month",
    min_value=1,
    max_value=12,
    value=6
)


if st.button("Predict Price"):

    prediction = predict_price(
        model,
        suburb,
        property_type,
        beds,
        baths,
        parking,
        sale_year,
        sale_month
    )

    st.success(f"Predicted Sale Price: ${prediction:,.2f}")