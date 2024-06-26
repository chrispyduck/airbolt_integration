# Airbolt Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

Integrates [Airbolt](https://theairbolt.com/) GPS tracker devices.

## Features
* Create a tracker entity for each registered device
* Sensors for some basic info like modem voltage and temperature, operating mode, and device type
* Battery level percentage (guesstimated based on observations)

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `airbolt`.
1. Download _all_ the files from the `custom_components/airbolt/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

## Configuration

Configuration is done in the HA UI and only requires providing your Airbolt credentials.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[integration_blueprint]: https://github.com/chrispyduck/airbolt_integration
[commits-shield]: https://img.shields.io/github/commit-activity/y/chrispyduck/airbolt_integration.svg?style=for-the-badge
[commits]: https://github.com/chrispyduck/airbolt_integration/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[license-shield]: https://img.shields.io/github/license/chrispyduck/airbolt_integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-chrispyduck-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/chrispyduck/airbolt_integration.svg?style=for-the-badge
[releases]: https://github.com/chrispyduck/airbolt_integration/releases
