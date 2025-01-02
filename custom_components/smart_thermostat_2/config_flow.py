"""Config flow for Smart Thermostat."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_SENSOR,
    CONF_EXTERNAL_SENSOR,
    CONF_SWITCH_ENTITY,
    CONF_TARGET_TEMP,
    CONF_MODE,
    CONF_USE_WEATHER,
    CONF_WEATHER_ENTITY,
    DEFAULT_TARGET_TEMP,
    DEFAULT_WEATHER_ENABLED,
    METNO_DOMAIN,
    MIN_TEMP,
    MAX_TEMP,
    TEMP_STEP,
)

_LOGGER = logging.getLogger(__name__)

class SmartThermostatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Thermostat."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            if user_input.get(CONF_USE_WEATHER):
                # Check if Met.no integration is configured
                if not self.hass.config_entries.async_entries(METNO_DOMAIN):
                    errors["base"] = "met_no_required"
                elif not user_input.get(CONF_WEATHER_ENTITY):
                    errors[CONF_WEATHER_ENTITY] = "weather_entity_required"

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )

        schema = {
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required(CONF_EXTERNAL_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required(CONF_SWITCH_ENTITY): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch")
            ),
            vol.Required(CONF_TARGET_TEMP, default=DEFAULT_TARGET_TEMP): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=MIN_TEMP,
                    max=MAX_TEMP,
                    step=TEMP_STEP,
                    unit_of_measurement="°C"
                )
            ),
            vol.Required(CONF_MODE, default="constant"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=["fast", "constant", "intermittent", "auto"],
                    translation_key="modes"
                )
            ),
            vol.Optional(CONF_USE_WEATHER, default=DEFAULT_WEATHER_ENABLED): bool,
        }

        if user_input and user_input.get(CONF_USE_WEATHER):
            schema[vol.Required(CONF_WEATHER_ENTITY)] = selector.EntitySelector(
                selector.EntitySelectorConfig(domain="weather")
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(schema),
            errors=errors,
        )