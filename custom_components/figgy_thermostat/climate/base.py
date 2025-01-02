"""Base climate platform for Figgy Thermostat."""
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from ..const import DOMAIN, MODE_CONSTANT

class FiggyThermostatBase(ClimateEntity):
    """Base class for Figgy Thermostat."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(self, hass, name, temp_sensor, external_temp_sensor, switch_entity):
        """Initialize the thermostat."""
        self._hass = hass
        self._name = name
        self._temp_sensor = temp_sensor
        self._external_temp_sensor = external_temp_sensor
        self._switch_entity = switch_entity
        self._target_temperature = 20.0
        self._current_temperature = None
        self._mode = MODE_CONSTANT

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"{DOMAIN}_{self._name}"

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        return self._target_temperature