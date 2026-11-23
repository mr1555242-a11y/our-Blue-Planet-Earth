import numpy as np

from core.prediction import EnvironmentalPredictor


def test_insufficient_prediction_history():

    model = EnvironmentalPredictor(
        minimum_records=30
    )

    result = model.predict_next(
        [10, 11, 12, 13, 14]
    )

    assert result["status"] == "PREDICTION_UNAVAILABLE"


def test_prediction_training():

    model = EnvironmentalPredictor(
        minimum_records=30
    )

    history = [
        float(x)
        for x in range(1, 61)
    ]

    result = model.predict_next(history)

    assert result["status"] == "PREDICTION_GENERATED"

    assert np.isfinite(
        result["predicted_value"]
    )
