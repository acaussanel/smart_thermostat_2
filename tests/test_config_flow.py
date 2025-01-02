"""Test the Smart Thermostat config flow."""
from unittest.mock import patch
import pytest
from homeassistant import config_entries, data_entry_flow
from custom_components.smart_thermostat_2.const import DOMAIN

async def test_form_user(hass):
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.smart_thermostat_2.config_flow.SmartThermostatConfigFlow.async_step_user",
        return_value={"title": "Test Thermostat"},
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "name": "Test Thermostat",
                "sensor": "sensor.temp",
                "external_temp_sensor": "sensor.outside_temp",
                "switch_entity": "switch.heater",
                "target_temperature": 20.0,
                "mode": "constant",
                "use_weather": False,
            },
        )
        assert result2["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
        assert result2["title"] == "Test Thermostat"

async def test_form_invalid_weather(hass):
    """Test we handle invalid weather config."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "Test Thermostat",
            "sensor": "sensor.temp",
            "external_temp_sensor": "sensor.outside_temp",
            "switch_entity": "switch.heater",
            "target_temperature": 20.0,
            "mode": "constant",
            "use_weather": True,
        },
    )
    assert result2["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result2["errors"]["base"] == "met_no_required"