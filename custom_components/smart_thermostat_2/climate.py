"""Climate platform for Smart Thermostat 2.0."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_NAME,
    PRECISION_HALVES,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_SENSOR,
    CONF_EXTERNAL_SENSOR,
    CONF_WEATHER_ENTITY,
    CONF_SWITCH_ENTITY,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the smart thermostat platform."""
    name = config.get(CONF_NAME)
    temp_sensor = config.get(CONF_SENSOR)
    external_temp_sensor = config.get(CONF_EXTERNAL_SENSOR)
    weather_entity = config.get(CONF_WEATHER_ENTITY)
    switch_entity = config.get(CONF_SWITCH_ENTITY)

    async_add_entities([
        SmartThermostat(
            hass,
            name,
            temp_sensor,
            external_temp_sensor,
            weather_entity,
            switch_entity,
        )
    ])

class SmartThermostat(ClimateEntity):
    """Smart Thermostat Climate Entity."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_precision = PRECISION_HALVES
    _attr_target_temperature_step = PRECISION_HALVES
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
    )

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        temp_sensor: str,
        external_temp_sensor: str,
        weather_entity: str,
        switch_entity: str,
    ) -> None:
        """Initialize the thermostat."""
        self._hass = hass
        self._name = name
        self._temp_sensor = temp_sensor
        self._external_temp_sensor = external_temp_sensor
        self._weather_entity = weather_entity
        self._switch_entity = switch_entity
        self._target_temperature = 20.0
        self._current_temperature = None
        self._hvac_mode = HVACMode.OFF

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

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation ie. heat, cool mode."""
        return self._hvac_mode

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        self._target_temperature = temperature
        await self.async_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        self._hvac_mode = hvac_mode
        await self.async_update_ha_state()