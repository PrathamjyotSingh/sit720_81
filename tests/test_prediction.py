from prediction import load_model, predict_price


def test_model_loads():
    """Test that the trained model can be loaded successfully."""
    model = load_model()

    assert model is not None


def test_prediction_is_numeric():
    """Test that the model returns a numeric prediction."""
    model = load_model()

    prediction = predict_price(
        model,
        "PEN",
        "House",
        3,
        2,
        1,
        2026,
        6
    )

    assert isinstance(prediction, (int, float))


def test_prediction_is_positive():
    """Test that the predicted house price is positive."""
    model = load_model()

    prediction = predict_price(
        model,
        "PEN",
        "House",
        3,
        2,
        1,
        2026,
        6
    )

    assert prediction > 0


def test_different_property_configurations():
    """Test that different valid property configurations can be processed."""
    model = load_model()

    prediction_1 = predict_price(
        model,
        "PEN",
        "House",
        3,
        2,
        2,
        2026,
        6
    )

    prediction_2 = predict_price(
        model,
        "PAR",
        "Apartment",
        2,
        1,
        1,
        2025,
        12
    )

    assert isinstance(prediction_1, (int, float))
    assert isinstance(prediction_2, (int, float))
    assert prediction_1 > 0
    assert prediction_2 > 0