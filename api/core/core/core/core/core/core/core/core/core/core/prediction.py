import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


class EnvironmentalPredictor:

    def __init__(self, minimum_records=30):

        self.minimum_records = minimum_records

        self.model = RandomForestRegressor(
            n_estimators=150,
            max_depth=8,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        self.trained = False
        self.validation_mae = None

    @staticmethod
    def create_features(values):

        features = []

        for index in range(3, len(values)):

            features.append([
                values[index - 1],
                values[index - 2],
                values[index - 3],
                index
            ])

        return np.asarray(features, dtype=float)

    def train(self, historical_values):

        values = np.asarray(
            historical_values,
            dtype=float
        )

        values = values[np.isfinite(values)]

        if len(values) < self.minimum_records:

            return {
                "status": "INSUFFICIENT_DATA",
                "required": self.minimum_records,
                "available": len(values)
            }

        features = self.create_features(values)

        targets = values[3:]

        # Keep the most recent observations for temporal validation.
        split = int(len(features) * 0.8)

        if split < 5 or len(features) - split < 2:

            return {
                "status": "INSUFFICIENT_VALIDATION_DATA"
            }

        x_train = features[:split]
        x_test = features[split:]

        y_train = targets[:split]
        y_test = targets[split:]

        self.model.fit(
            x_train,
            y_train
        )

        predictions = self.model.predict(
            x_test
        )

        self.validation_mae = float(
            mean_absolute_error(
                y_test,
                predictions
            )
        )

        # Refit using all available historical observations.
        self.model.fit(
            features,
            targets
        )

        self.trained = True

        return {
            "status": "TRAINED",
            "training_records": len(x_train),
            "validation_records": len(x_test),
            "validation_mae": self.validation_mae
        }

    def predict_next(self, historical_values):

        values = np.asarray(
            historical_values,
            dtype=float
        )

        values = values[np.isfinite(values)]

        if not self.trained:

            training = self.train(values)

            if training["status"] != "TRAINED":

                return {
                    "status": "PREDICTION_UNAVAILABLE",
                    "training": training
                }

        if len(values) < 3:

            return {
                "status": "INSUFFICIENT_HISTORY"
            }

        index = len(values)

        features = np.asarray([[
            values[-1],
            values[-2],
            values[-3],
            index
        ]])

        predicted = float(
            self.model.predict(features)[0]
        )

        return {
            "status": "PREDICTION_GENERATED",
            "predicted_value": predicted,
            "validation_mae": self.validation_mae,
            "model": "RandomForestRegressor",
            "warning": (
                "Experimental short-term estimate; "
                "not a validated climate forecast."
            )
        }
