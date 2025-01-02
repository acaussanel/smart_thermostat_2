{% if prerelease %}
### NB!: This is a Beta version!
{% endif %}

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

# Smart Thermostat 2.0

Advanced thermostat integration with PID control and machine learning capabilities.

### Features

- PID control with machine learning optimization
- Three heating modes: Fast, Constant, and Intermittent
- Automatic learning of thermal characteristics
- Custom dashboard card
- Energy consumption analysis

{% if not installed %}
## Installation

1. Click install
2. Restart Home Assistant
3. Configure the integration in your `configuration.yaml`

{% endif %}

[releases-shield]: https://img.shields.io/github/release/your_username/smart_thermostat_2.svg
[releases]: https://github.com/your_username/smart_thermostat_2/releases