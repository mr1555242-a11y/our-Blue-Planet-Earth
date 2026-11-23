from datetime import datetime


class DataReconciliationEngine:

    def __init__(self, tolerance=0.20):

        self.tolerance = tolerance

    def compare(self, a, b):

        if a["metric"] != b["metric"]:

            return {
                "status": "NOT_COMPARABLE",
                "reason": "Different metrics"
            }

        if a.get("unit") != b.get("unit"):

            return {
                "status": "NOT_COMPARABLE",
                "reason": "Different units"
            }

        if a.get("time_basis") != b.get("time_basis"):

            return {
                "status": "NOT_COMPARABLE",
                "reason": "Different time basis"
            }

        time_a = datetime.fromisoformat(
            a["observed_at"]
        )

        time_b = datetime.fromisoformat(
            b["observed_at"]
        )

        if abs((time_a - time_b).total_seconds()) > 3600:

            return {
                "status": "NOT_COMPARABLE",
                "reason": "Observation times are too far apart"
            }

        value_a = float(a["value"])
        value_b = float(b["value"])

        denominator = max(
            abs(value_a),
            abs(value_b),
            1e-9
        )

        difference = abs(
            value_a - value_b
        ) / denominator

        return {
            "status": (
                "DISCREPANCY"
                if difference > self.tolerance
                else "CONSISTENT"
            ),
            "metric": a["metric"],
            "source_a": a["source"],
            "source_b": b["source"],
            "value_a": value_a,
            "value_b": value_b,
            "relative_difference": difference,
            "automatic_winner": None
        }
