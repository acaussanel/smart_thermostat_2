# Smart Thermostat 2.0

A smart thermostat integration for Home Assistant with advanced features including weather forecasting and machine learning capabilities.

## Features

- Advanced PID control with machine learning optimization
- Weather forecast integration for predictive heating
- Switch-based power control
- Three heating modes: Fast, Constant, and Intermittent
- Automatic learning of thermal characteristics
- Custom dashboard card with schedule management
- Energy consumption analysis and optimization

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
    weather_entity: weather.home
    switch_entity: switch.heater
    learning_enabled: true
    forecast_hours: 24
    min_power: 0
    max_power: 100
```

## Configuration Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| name | Name of the thermostat | yes | - |
| sensor | Temperature sensor entity ID | yes | - |
| external_temp_sensor | Outside temperature sensor entity ID | yes | - |
| weather_entity | Weather entity ID for forecasts | yes | - |
| switch_entity | Switch entity ID for heater control | yes | - |
| learning_enabled | Enable ML features | no | true |
| forecast_hours | Number of hours for weather forecast | no | 24 |
| min_power | Minimum power level | no | 0 |
| max_power | Maximum power level | no | 100 |

## Services

The integration provides the following services:

- `smart_thermostat_2.set_mode`: Set the heating mode
- `smart_thermostat_2.set_learning`: Enable/disable machine learning

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.