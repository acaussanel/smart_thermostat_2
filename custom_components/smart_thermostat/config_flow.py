"""Config flow for Smart Thermostat."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_SENSOR, CONF_TARGET_TEMP, CONF_MODE

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
        if user_input is not None:
            return self.async_create_entry(
                title="Smart Thermostat",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SENSOR): str,
                vol.Required(CONF_TARGET_TEMP, default=20): float,
                vol.Required(CONF_MODE, default="constant"): vol.In([
                    "fast", "constant", "intermittent"
                ]),
            })
        )