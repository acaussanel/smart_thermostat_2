"""Constants for Figgy Thermostat."""
from typing import Final

DOMAIN: Final = "figgy_thermostat"

# Configuration
CONF_SENSOR: Final = "sensor"
CONF_EXTERNAL_SENSOR: Final = "external_temp_sensor"
CONF_SWITCH_ENTITY: Final = "switch_entity"
CONF_TARGET_TEMP: Final = "target_temperature"
CONF_MODE: Final = "mode"
CONF_USE_WEATHER: Final = "use_weather"
CONF_WEATHER_ENTITY: Final = "weather_entity"

# Weather Configuration
DEFAULT_WEATHER_ENABLED: Final = False
METNO_DOMAIN: Final = "met_no"
METNO_WEATHER_PLATFORM: Final = "weather.met_no"

# Modes
MODE_FAST: Final = "fast"
MODE_CONSTANT: Final = "constant"
MODE_INTERMITTENT: Final = "intermittent"
MODE_AUTO: Final = "auto"

# Default Values
DEFAULT_TARGET_TEMP: Final = 20.0
DEFAULT_FORECAST_HOURS: Final = 24
MIN_TEMP: Final = 10.0
MAX_TEMP: Final = 30.0
TEMP_STEP: Final = 0.5