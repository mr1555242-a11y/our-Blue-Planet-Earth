from core.reconciliation import DataReconciliationEngine


def test_comparable_observations():

    engine = DataReconciliationEngine()

    a = {
        "metric": "temperature",
        "value": 25,
        "unit": "C",
        "time_basis": "hourly",
        "observed_at": "2026-01-01T10:00:00+00:00",
        "source": "Source A"
    }

    b = {
        "metric": "temperature",
        "value": 25.5,
        "unit": "C",
        "time_basis": "hourly",
        "observed_at": "2026-01-01T10:10:00+00:00",
        "source": "Source B"
    }

    result = engine.compare(a, b)

    assert result["status"] == "CONSISTENT"


def test_different_units_are_not_comparable():

    engine = DataReconciliationEngine()

    a = {
        "metric": "temperature",
        "value": 25,
        "unit": "C",
        "time_basis": "hourly",
        "observed_at": "2026-01-01T10:00:00+00:00",
        "source": "Source A"
    }

    b = {
        "metric": "temperature",
        "value": 77,
        "unit": "F",
        "time_basis": "hourly",
        "observed_at": "2026-01-01T10:00:00+00:00",
        "source": "Source B"
    }

    result = engine.compare(a, b)

    assert result["status"] == "NOT_COMPARABLE"
