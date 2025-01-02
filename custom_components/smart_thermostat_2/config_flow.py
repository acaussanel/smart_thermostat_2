"""Config flow for Smart Thermostat."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    CONF_SENSOR,
    CONF_EXTERNAL_SENSOR,
    CONF_WEATHER_ENTITY,
    CONF_SWITCH_ENTITY,
    CONF_TARGET_TEMP,
    CONF_MODE,
    CONF_LEARNING_ENABLED,
    CONF_FORECAST_HOURS,
    DEFAULT_FORECAST_HOURS,
)

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
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_SENSOR): str,
                vol.Required(CONF_EXTERNAL_SENSOR): str,
                vol.Required(CONF_WEATHER_ENTITY): str,
                vol.Required(CONF_SWITCH_ENTITY): str,
                vol.Required(CONF_TARGET_TEMP, default=20): vol.Coerce(float),
                vol.Optional(CONF_MODE, default="constant"): vol.In([
                    "fast", "constant", "intermittent", "auto"
                ]),
                vol.Optional(CONF_LEARNING_ENABLED, default=True): bool,
                vol.Optional(CONF_FORECAST_HOURS, default=DEFAULT_FORECAST_HOURS): int,
            }),
            errors=errors,
        )