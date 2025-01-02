"""Constants for the Smart Thermostat integration."""

DOMAIN = "smart_thermostat"

# Configuration
CONF_SENSOR = "sensor"
CONF_TARGET_TEMP = "target_temperature"
CONF_MODE = "mode"

# Modes disponibles
MODE_FAST = "fast"
MODE_CONSTANT = "constant"
MODE_INTERMITTENT = "intermittent"

# PID Constants
DEFAULT_KP = 1.0
DEFAULT_KI = 0.1
DEFAULT_KD = 0.05

# ML Parameters
LEARNING_RATE = 0.01
PREDICTION_HORIZON = 24  # heures