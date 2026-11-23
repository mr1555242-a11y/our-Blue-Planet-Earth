from core.validation import EnvironmentalValidator


def test_valid_temperature():

    result = EnvironmentalValidator.validate(
        "temperature_2m",
        28.5
    )

    assert result["valid"] is True


def test_invalid_humidity():

    result = EnvironmentalValidator.validate(
        "relative_humidity_2m",
        150
    )

    assert result["valid"] is False


def test_missing_value():

    result = EnvironmentalValidator.validate(
        "pm2_5",
        None
    )

    assert result["valid"] is False


def test_unknown_metric():

    result = EnvironmentalValidator.validate(
        "unknown_metric",
        10
    )

    assert result["valid"] is False
