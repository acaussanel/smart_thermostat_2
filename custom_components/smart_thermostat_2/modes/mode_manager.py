```python
"""Mode management for Smart Thermostat."""
from datetime import datetime, time, timedelta
from typing import Optional

class ModeManager:
    """Manages different thermostat modes including night and arrival."""
    
    def __init__(self):
        """Initialize the mode manager."""
        self.night_mode_enabled = False
        self.night_start_time: Optional[time] = None
        self.night_end_time: Optional[time] = None
        self.night_temperature: float = 17.0
        
        self.arrival_mode_enabled = False
        self.arrival_time: Optional[time] = None
        self.arrival_temperature: float = 20.0
        self.preheating_duration = timedelta(hours=1)
        
    def set_night_mode(self, enabled: bool, start_time: time, end_time: time, temperature: float):
        """Configure night mode."""
        self.night_mode_enabled = enabled
        self.night_start_time = start_time
        self.night_end_time = end_time
        self.night_temperature = temperature
        
    def set_arrival_mode(self, enabled: bool, arrival_time: time, temperature: float):
        """Configure arrival mode."""
        self.arrival_mode_enabled = enabled
        self.arrival_time = arrival_time
        self.arrival_temperature = temperature
        
    def get_target_temperature(self, base_temperature: float) -> float:
        """Get the current target temperature based on active modes."""
        current_time = datetime.now().time()
        
        # Check night mode
        if self.night_mode_enabled and self._is_night_time(current_time):
            return self.night_temperature
            
        # Check arrival mode
        if self.arrival_mode_enabled and self._is_preheating_time(current_time):
            return self.arrival_temperature
            
        return base_temperature
        
    def _is_night_time(self, current_time: time) -> bool:
        """Check if current time is within night mode period."""
        if not all([self.night_start_time, self.night_end_time]):
            return False
            
        if self.night_start_time <= self.night_end_time:
            return self.night_start_time <= current_time <= self.night_end_time
        else:  # Handles overnight periods
            return current_time >= self.night_start_time or current_time <= self.night_end_time
            
    def _is_preheating_time(self, current_time: time) -> bool:
        """Check if current time is within preheating period."""
        if not self.arrival_time:
            return False
            
        # Calculate preheating start time
        arrival_dt = datetime.combine(datetime.today(), self.arrival_time)
        preheat_start = (arrival_dt - self.preheating_duration).time()
        
        return preheat_start <= current_time <= self.arrival_time
```