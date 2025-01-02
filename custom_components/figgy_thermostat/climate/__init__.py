"""Climate platform for Figgy Thermostat."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base import FiggyThermostatBase
from .controller import TemperatureController
from .weather import WeatherManager
from ..const import (
    CONF_SENSOR,
    CONF_EXTERNAL_SENSOR,
    CONF_SWITCH_ENTITY,
    CONF_WEATHER_ENTITY,
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Figgy thermostat platform."""
    name = config.get("name")
    temp_sensor = config.get(CONF_SENSOR)
    external_temp_sensor = config.get(CONF_EXTERNAL_SENSOR)
    switch_entity = config.get(CONF_SWITCH_ENTITY)
    weather_entity = config.get(CONF_WEATHER_ENTITY)

    async_add_entities([
        FiggyThermostat(
            hass,
            name,
            temp_sensor,
            external_temp_sensor,
            switch_entity,
            weather_entity,
        )
    ])

class FiggyThermostat(FiggyThermostatBase):
    """Representation of a Figgy Thermostat."""

    def __init__(
        self,
        hass,
        name,
        temp_sensor,
        external_temp_sensor,
        switch_entity,
        weather_entity=None,
    ):
        """Initialize the thermostat."""
        super().__init__(hass, name, temp_sensor, external_temp_sensor, switch_entity)
        self._controller = TemperatureController(
            mode=self._mode,
            min_temp=self._attr_min_temp,
            max_temp=self._attr_max_temp,
        )
        self._weather = WeatherManager(hass, weather_entity) if weather_entity else None