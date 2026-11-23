class EnvironmentalValidator:

    VALID_RANGES = {
        "temperature_2m": (-90, 65),
        "relative_humidity_2m": (0, 100),
        "pm2_5": (0, 2000),
        "pm10": (0, 5000),
        "wind_speed_10m": (0, 500),
        "precipitation": (0, 2000)
    }

    @classmethod
    def validate_value(cls, name, value):

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

        if name not in cls.VALID_RANGES:
            return {
                "valid": False,
                "reason": "Unknown measurement"
            }

        lower, upper = cls.VALID_RANGES[name]

        if not lower <= number <= upper:
            return {
                "valid": False,
                "reason": "Outside configured range"
            }

        return {
            "valid": True,
            "value": number
        }

    @classmethod
    def validate_record(cls, record):

        results = {}

        for category, measurements in record.items():

            if not isinstance(measurements, dict):
                continue

            for name, value in measurements.items():

                if name in cls.VALID_RANGES:

                    results[name] = (
                        cls.validate_value(
                            name,
                            value
                        )
                    )

        return results
