class EnvironmentalAnomalyDetector:

    def detect(self, observations):

        alerts = []

        thresholds = {
            "temperature_2m": 40,
            "pm2_5": 60,
            "pm10": 150,
            "wind_speed_10m": 100
        }

        for metric, threshold in thresholds.items():

            value = observations.get(metric)

            if value is None:
                continue

            try:
                value = float(value)
            except (TypeError, ValueError):
                continue

            if value > threshold:

                alerts.append({
                    "metric": metric,
                    "observed_value": value,
                    "reference_threshold": threshold,
                    "status": "THRESHOLD_EXCEEDED",
                    "message": (
                        f"{metric} exceeded the "
                        "configured screening threshold."
                    )
                })

        return alerts
