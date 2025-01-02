"""Temperature controller for Figgy Thermostat."""
import numpy as np
from datetime import datetime, timedelta

class TemperatureController:
    """Manages temperature control logic."""

    def __init__(self, mode: str, min_temp: float, max_temp: float):
        """Initialize the controller."""
        self.mode = mode
        self.min_temp = min_temp
        self.max_temp = max_temp
        self._last_update = datetime.now()
        self._integral = 0
        self._last_error = 0

    def compute_heating_power(
        self,
        current_temp: float,
        target_temp: float,
        external_temp: float,
        weather_forecast: list | None = None
    ) -> float:
        """Compute required heating power."""
        if self.mode == "fast":
            return self._compute_fast_mode(current_temp, target_temp)
        elif self.mode == "constant":
            return self._compute_constant_mode(current_temp, target_temp, external_temp)
        else:  # intermittent
            return self._compute_intermittent_mode(current_temp, target_temp)

    def _compute_fast_mode(self, current_temp: float, target_temp: float) -> float:
        """Compute power for fast heating."""
        error = target_temp - current_temp
        return 1.0 if error > 0.5 else 0.0

    def _compute_constant_mode(
        self,
        current_temp: float,
        target_temp: float,
        external_temp: float
    ) -> float:
        """Compute power for constant temperature."""
        now = datetime.now()
        dt = (now - self._last_update).total_seconds()
        
        error = target_temp - current_temp
        self._integral += error * dt
        derivative = (error - self._last_error) / dt if dt > 0 else 0
        
        # PID coefficients
        kp, ki, kd = 1.0, 0.1, 0.05
        
        power = (
            kp * error +
            ki * self._integral +
            kd * derivative
        )
        
        # Update state
        self._last_error = error
        self._last_update = now
        
        return np.clip(power, 0, 1)

    def _compute_intermittent_mode(
        self,
        current_temp: float,
        target_temp: float
    ) -> float:
        """Compute power for intermittent mode."""
        error = target_temp - current_temp
        cycle_time = 30  # minutes
        current_minute = datetime.now().minute
        
        # Heat during first half of cycle if below target
        return 1.0 if current_minute < cycle_time/2 and error > 0 else 0.0