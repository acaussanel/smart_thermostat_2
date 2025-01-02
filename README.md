# Figgy Thermostat

A smart thermostat integration for Home Assistant with advanced features including weather forecasting and machine learning capabilities.

## Prerequisites

- Home Assistant 2023.8.0 or newer
- Met.no integration configured in Home Assistant (if using weather forecast)
- Temperature sensors (internal and external)
- A switch entity for heater control

## Installation

### HACS Installation
1. Open HACS
2. Go to "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL with category "Integration"
5. Click "Install"

### Manual Installation
1. Copy the `custom_components/figgy_thermostat` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

```yaml
climate:
  - platform: figgy_thermostat
    name: "Figgy Thermostat"
    sensor: sensor.room_temperature
    external_temp_sensor: sensor.outside_temperature
    switch_entity: switch.heater
    target_temperature: 20
    mode: "constant"
    use_weather: true  # Optional, requires Met.no integration
    weather_entity: weather.home  # Required if use_weather is true
```

## Weather Integration

The thermostat can use Met.no weather forecasts to optimize heating. To use this feature:

1. Ensure Met.no integration is configured in Home Assistant
2. Set `use_weather: true` in configuration
3. Specify the Met.no weather entity in `weather_entity`

## Lovelace Card

To add the custom card to your dashboard:

1. Go to Configuration > Lovelace Dashboards
2. Click "Resources"
3. Add new resource:
   - URL: /hacsfiles/figgy_thermostat/card/figgy-thermostat-card.js
   - Type: JavaScript Module

Then add the card to your dashboard:

```yaml
type: custom:figgy-thermostat-card
entity: climate.figgy_thermostat
```