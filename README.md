# Smart Thermostat 2.0

A smart thermostat integration for Home Assistant with PID control and machine learning capabilities.

## Features

- Advanced PID control with machine learning optimization
- Three heating modes: Fast, Constant, and Intermittent
- Automatic learning of thermal characteristics
- Custom dashboard card with schedule management
- Energy consumption analysis

## Installation

### HACS Installation
1. Open HACS
2. Go to "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL with category "Integration"
5. Click "Install"

### Manual Installation
1. Copy the `custom_components/smart_thermostat_2` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

Add to your `configuration.yaml`:

```yaml
climate:
  - platform: smart_thermostat_2
    name: "Smart Thermostat"
    sensor: sensor.room_temperature
    external_temp_sensor: sensor.outside_temperature
    power_sensor: sensor.heater_power
    learning_enabled: true
```

## Configuration Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| sensor | Temperature sensor entity ID | yes | - |
| external_temp_sensor | Outside temperature sensor entity ID | yes | - |
| power_sensor | Power consumption sensor entity ID | yes | - |
| learning_enabled | Enable ML features | no | true |

## Dashboard Card

The integration includes a custom card for Lovelace UI. Add it to your dashboard: