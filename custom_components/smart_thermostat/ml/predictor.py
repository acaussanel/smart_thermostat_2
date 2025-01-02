"""Temperature prediction using machine learning."""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import List, Optional

class TemperaturePredictor:
    """ML-based temperature predictor."""

    def __init__(self):
        """Initialize the predictor."""
        self.model = RandomForestRegressor(n_estimators=100)
        self._is_trained = False

    def prepare_features(self, 
                        temperatures: List[float],
                        outside_temps: List[float],
                        heating_powers: List[float]) -> np.ndarray:
        """Prepare feature matrix for prediction."""
        # Combine all features
        features = np.column_stack([
            temperatures,
            outside_temps,
            heating_powers
        ])
        return features

    def train(self, 
             temperatures: List[float],
             outside_temps: List[float],
             heating_powers: List[float],
             target_temps: List[float]):
        """Train the prediction model."""
        X = self.prepare_features(temperatures, outside_temps, heating_powers)
        self.model.fit(X, target_temps)
        self._is_trained = True

    def predict(self,
               current_temp: float,
               outside_temp: float,
               heating_power: float) -> Optional[float]:
        """Predict future temperature."""
        if not self._is_trained:
            return None

        features = np.array([[current_temp, outside_temp, heating_power]])
        return self.model.predict(features)[0]