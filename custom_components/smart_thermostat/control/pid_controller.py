"""PID Controller implementation."""
import time
from typing import Optional

class PIDController:
    """PID controller for temperature regulation."""

    def __init__(self, kp: float = 1.0, ki: float = 0.1, kd: float = 0.05):
        """Initialize the PID controller."""
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error: Optional[float] = None
        self.integral = 0.0
        self.last_time = time.time()

    def compute(self, setpoint: float, current_value: float) -> float:
        """Compute the PID output."""
        current_time = time.time()
        dt = current_time - self.last_time

        # Calculate error
        error = setpoint - current_value

        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error * dt
        i_term = self.ki * self.integral

        # Derivative term
        d_term = 0.0
        if self.last_error is not None:
            d_term = self.kd * (error - self.last_error) / dt

        # Update state
        self.last_error = error
        self.last_time = current_time

        return p_term + i_term + d_term