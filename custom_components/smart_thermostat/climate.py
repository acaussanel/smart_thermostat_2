"""Climate platform for Smart Thermostat."""
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from .const import DOMAIN, MODE_CONSTANT
from .control.pid_controller import PIDController
from .ml.predictor import TemperaturePredictor

class SmartThermostat(ClimateEntity):
    """Smart Thermostat with PID and ML capabilities."""

    def __init__(self, hass, name, sensor_entity_id):
        """Initialize the thermostat."""
        self._hass = hass
        self._name = name
        self._sensor_entity_id = sensor_entity_id
        self._hvac_mode = HVAC_MODE_OFF
        self._target_temperature = 20
        self._current_temperature = None
        self._mode = MODE_CONSTANT

        # Initialize controllers
        self._pid = PIDController()
        self._predictor = TemperaturePredictor()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def hvac_mode(self):
        """Return current operation."""
        return self._hvac_mode

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._target_temperature = temperature

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        self._hvac_mode = hvac_mode