```python
"""Constants for Smart Thermostat 2.0."""
from typing import Final

DOMAIN: Final = "smart_thermostat_2"

# Configuration
CONF_SENSOR: Final = "sensor"
CONF_EXTERNAL_SENSOR: Final = "external_temp_sensor"
CONF_WEATHER_ENTITY: Final = "weather_entity"
CONF_SWITCH_ENTITY: Final = "switch_entity"
CONF_TARGET_TEMP: Final = "target_temperature"
CONF_MODE: Final = "mode"
CONF_LEARNING_ENABLED: Final = "learning_enabled"
CONF_FORECAST_HOURS: Final = "forecast_hours"

# Mode Configuration
CONF_NIGHT_MODE: Final = "night_mode"
CONF_NIGHT_START: Final = "night_start"
CONF_NIGHT_END: Final = "night_end"
CONF_NIGHT_TEMP: Final = "night_temperature"
CONF_ARRIVAL_MODE: Final = "arrival_mode"
CONF_ARRIVAL_TIME: Final = "arrival_time"
CONF_ARRIVAL_TEMP: Final = "arrival_temperature"

# Heating Modes
MODE_FAST: Final = "fast"
MODE_CONSTANT: Final = "constant"
MODE_INTERMITTENT: Final = "intermittent"
MODE_AUTO: Final = "auto"
MODE_NIGHT: Final = "night"
MODE_ARRIVAL: Final = "arrival"

# Default Values
DEFAULT_FORECAST_HOURS: Final = 24
DEFAULT_NIGHT_TEMP: Final = 17.0
DEFAULT_ARRIVAL_TEMP: Final = 20.0
DEFAULT_PREHEAT_DURATION: Final = 60  # minutes

# ML Parameters
LEARNING_WINDOW: Final = 7  # days
MIN_LEARNING_SAMPLES: Final = 100
PREDICTION_HORIZON: Final = 24  # hours
WEATHER_WEIGHT: Final = 0.3  # Impact of weather forecast on predictions

# Thermal Parameters
MIN_CYCLE_TIME: Final = 10  # minutes
THERMAL_MEMORY: Final = 3  # hours - for learning thermal inertia
```