"""Weather integration for Figgy Thermostat."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class WeatherManager:
    """Manages weather forecast integration."""

    def __init__(self, hass, weather_entity: str):
        """Initialize weather manager."""
        self._hass = hass
        self._weather_entity = weather_entity
        self._forecast_cache = None
        self._last_update = None
        self._update_interval = timedelta(minutes=30)

    async def get_forecast(self) -> Optional[List[Dict]]:
        """Get weather forecast data."""
        now = datetime.now()
        if (not self._forecast_cache or 
            not self._last_update or 
            now - self._last_update > self._update_interval):
            
            weather = self._hass.states.get(self._weather_entity)
            if weather and weather.attributes.get("forecast"):
                self._forecast_cache = weather.attributes["forecast"]
                self._last_update = now
            
        return self._forecast_cache

    def should_preheat(self, forecast: List[Dict], threshold_temp: float) -> bool:
        """Determine if preheating is needed based on forecast."""
        if not forecast:
            return False
            
        # Check if temperature will drop below threshold
        next_hours = forecast[:6]  # Next 6 hours
        return any(f.get("temperature", 100) < threshold_temp for f in next_hours)