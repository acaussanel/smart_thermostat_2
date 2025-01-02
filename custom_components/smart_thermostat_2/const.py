"""Constants for Smart Thermostat 2.0."""
from typing import Final

DOMAIN: Final = "smart_thermostat_2"

# Configuration
CONF_SENSOR: Final = "sensor"
CONF_EXTERNAL_SENSOR: Final = "external_temp_sensor"
CONF_POWER_SENSOR: Final = "power_sensor"
CONF_TARGET_TEMP: Final = "target_temperature"
CONF_MODE: Final = "mode"
CONF_LEARNING_ENABLED: Final = "learning_enabled"
CONF_SCHEDULE: Final = "schedule"

# Modes de chauffage
MODE_FAST: Final = "fast"
MODE_CONSTANT: Final = "constant"
MODE_INTERMITTENT: Final = "intermittent"
MODE_AUTO: Final = "auto"

# Paramètres PID par mode
PID_PARAMS = {
    MODE_FAST: {"kp": 2.0, "ki": 0.2, "kd": 0.1},
    MODE_CONSTANT: {"kp": 1.0, "ki": 0.1, "kd": 0.05},
    MODE_INTERMITTENT: {"kp": 1.5, "ki": 0.05, "kd": 0.15}
}

# ML Parameters
LEARNING_WINDOW: Final = 7  # jours
MIN_LEARNING_SAMPLES: Final = 100
PREDICTION_HORIZON: Final = 24  # heures

# Schedule
DEFAULT_SCHEDULE = {
    "weekday": [
        {"time": "06:00", "temp": 20, "mode": MODE_FAST},
        {"time": "08:00", "temp": 18, "mode": MODE_INTERMITTENT},
        {"time": "17:00", "temp": 20, "mode": MODE_CONSTANT},
        {"time": "22:00", "temp": 17, "mode": MODE_INTERMITTENT}
    ],
    "weekend": [
        {"time": "08:00", "temp": 20, "mode": MODE_CONSTANT},
        {"time": "23:00", "temp": 17, "mode": MODE_INTERMITTENT}
    ]
}