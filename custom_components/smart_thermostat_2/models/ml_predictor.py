"""ML predictor with weather forecast integration for binary control."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class WeatherAwarePredictor:
    """ML predictor that determines optimal heating timing."""
    
    def __init__(self, forecast_hours: int = 24):
        """Initialize the predictor."""
        self.model = RandomForestClassifier(n_estimators=100)
        self.forecast_hours = forecast_hours
        self._is_trained = False
        self.thermal_memory = []
        
    def prepare_features(self,
                        temperatures: List[float],
                        outside_temps: List[float],
                        heating_states: List[bool],
                        weather_forecasts: List[Dict]) -> np.ndarray:
        """Prepare feature matrix including weather forecasts."""
        # Calculate temperature gradients
        temp_gradients = np.diff(temperatures)
        
        # Basic features
        features = np.column_stack([
            temperatures[:-1],
            outside_temps[:-1],
            [int(state) for state in heating_states[:-1]],
            temp_gradients
        ])
        
        # Add weather forecast features
        forecast_temps = [f['temperature'] for f in weather_forecasts]
        forecast_conditions = [self._encode_condition(f['condition']) for f in weather_forecasts]
        
        # Add forecast features to matrix
        features = np.column_stack([
            features,
            forecast_temps,
            forecast_conditions
        ])
        
        return features
        
    def _encode_condition(self, condition: str) -> float:
        """Encode weather condition as numeric value."""
        conditions = {
            'sunny': 1.0,
            'cloudy': 0.5,
            'rainy': 0.0
        }
        return conditions.get(condition, 0.5)
        
    def train(self,
             temperatures: List[float],
             outside_temps: List[float],
             heating_states: List[bool],
             weather_forecasts: List[Dict]):
        """Train the prediction model."""
        X = self.prepare_features(
            temperatures,
            outside_temps,
            heating_states,
            weather_forecasts
        )
        
        # Target is whether heating was beneficial
        y = self._calculate_heating_benefit(temperatures, outside_temps)
        
        self.model.fit(X, y)
        self._is_trained = True
        
    def _calculate_heating_benefit(self,
                                 temperatures: List[float],
                                 outside_temps: List[float]) -> List[bool]:
        """Determine if heating was beneficial based on temperature trends."""
        benefits = []
        for i in range(1, len(temperatures)):
            temp_gain = temperatures[i] - temperatures[i-1]
            natural_loss = (temperatures[i-1] - outside_temps[i-1]) * 0.1
            benefits.append(temp_gain > natural_loss)
        return benefits
        
    def should_heat(self,
                   current_temp: float,
                   target_temp: float,
                   outside_temp: float,
                   weather_forecasts: List[Dict]) -> bool:
        """Predict if heating should be turned on."""
        if not self._is_trained:
            # Fallback to simple threshold
            return current_temp < target_temp
            
        features = self.prepare_features(
            [current_temp, current_temp],  # Need two points for gradient
            [outside_temp, outside_temp],
            [False, False],  # Previous heating states
            weather_forecasts
        )
        
        # Predict if heating would be beneficial
        return self.model.predict(features)[0] and current_temp < target_temp