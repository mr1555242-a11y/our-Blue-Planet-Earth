import math


class EnvironmentalValidator:

    RANGES = {
        "temperature_2m": (-90, 65),
        "relative_humidity_2m": (0, 100),
        "pm2_5": (0, 2000),
        "pm10": (0, 5000),
        "wind_speed_10m": (0, 500),
        "precipitation": (0, 2000),
        "nitrogen_dioxide": (0, 5000),
        "ozone": (0, 5000),
        "T2M": (-90, 65),
        "RH2M": (0, 100),
        "PRECTOTCORR": (0, 2000)
    }

    @classmethod
    def validate(cls, metric, value):

        if value is None:

            return {
                "valid": False,
                "reason": "Missing value"
            }

        try:
            number = float(value)

        except (TypeError, ValueError):

            return {
                "valid": False,
                "reason": "Non-numeric value"
            }

        if not math.isfinite(number):

            return {
                "valid": False,
                "reason": "Non-finite value"
            }

        if metric not in cls.RANGES:

            return {
                "valid": False,
                "reason": "Unknown metric"
            }

        low, high = cls.RANGES[metric]

        if not low <= number <= high:

            return {
                "valid": False,
                "reason": "Outside screening range"
            }

        return {
            "valid": True,
            "value": number
        }

    @classmethod
    def validate_record(cls, record):

        results = {}

        for metric, value in record.items():

            results[metric] = cls.validate(
                metric,
                value
            )

        return results
          
