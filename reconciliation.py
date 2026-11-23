class DataReconciliationEngine:

    def __init__(self, tolerance=0.20):
        self.tolerance = tolerance

    def compare(self, source_a, source_b):

        comparisons = {}

        common_fields = (
            set(source_a.keys())
            & set(source_b.keys())
        )

        for field in common_fields:

            try:
                a = float(source_a[field])
                b = float(source_b[field])

                scale = max(
                    abs(a),
                    abs(b),
                    1e-9
                )

                difference = abs(a - b) / scale

                comparisons[field] = {
                    "source_a": a,
                    "source_b": b,
                    "relative_difference": difference,
                    "discrepancy": (
                        difference > self.tolerance
                    )
                }

            except (TypeError, ValueError):
                continue

        return comparisons

    def reconcile(self, comparison):

        result = {}

        for field, values in comparison.items():

            result[field] = {
                "status": (
                    "DISCREPANCY"
                    if values["discrepancy"]
                    else "CONSISTENT"
                ),
                "source_values": {
                    "source_a": values["source_a"],
                    "source_b": values["source_b"]
                },
                "relative_difference": (
                    values["relative_difference"]
                ),
                "final_value": None,
                "note": (
                    "Requires contextual source review"
                )
            }

        return result
