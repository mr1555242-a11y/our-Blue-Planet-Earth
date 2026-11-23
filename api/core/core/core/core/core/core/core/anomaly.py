import statistics


class EnvironmentalAnomalyDetector:

    THRESHOLDS = {
        "temperature_2m": 40,
        "pm2_5": 60,
        "pm10": 150,
        "wind_speed_10m": 100
    }

    def statistical_check(
        self,
        history,
        current_value,
        z_threshold=3.0
    ):

        if len(history) < 10:

            return {
                "status": "INSUFFICIENT_HISTORY"
            }

        values = [
            float(x)
            for x in history
        ]

        mean = statistics.mean(values)

        deviation = statistics.pstdev(values)

        if deviation == 0:

            return {
                "status": "NO_VARIATION",
                "mean": mean
            }

        z_score = (
            float(current_value) - mean
        ) / deviation

        return {
            "status": (
                "POTENTIAL_ANOMALY"
                if abs(z_score) >= z_threshold
                else "NORMAL_PATTERN"
            ),
            "mean": mean,
            "standard_deviation": deviation,
            "z_score": z_score
        }

    def detect_thresholds(self, measurements):

        alerts = []

        for metric, threshold in self.THRESHOLDS.items():

            value = measurements.get(metric)

            if value is None:
                continue

            try:
                number = float(value)
            except (ValueError, TypeError):
                continue

            if number > threshold:

                alerts.append({
                    "metric": metric,
                    "observed_value": number,
                    "screening_threshold": threshold,
                    "status": "THRESHOLD_EXCEEDED"
                })

        return alerts
