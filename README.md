# Home Assistant integration for Ouman EH-800 heating controller
This Home Assistant integration provides data read from [EH-800 heating controller](https://ouman.fi/en/product/ouman-eh-800-and-eh-800b/).

![Screenshot of integration](/media/eh800_ui.png)
## Why?
This integration was made to get heating controller data to Home Assistant for:
- Get important information from device
- Alert when something is wrong in your heating system
- Automate home based on data received

## Features
- Automatically updates the devices sensors status on a periodic basis.
- Scanning interval can be configured

## EH-800 requirements
To use the integration you need to have a EH-800 heating controller, that has network interface and has been configured a static IP addrress and username / password.

## Installation through HACS (NOT AVAILABLE UNTIL THIS COMMENT IS REMOVED)
To install the EH-800 integration using HACS:

1. Open Home Assistant, go to HACS -> Integrations.
2. Search for EH-800 and install it.
3. Restart Home Assistant.
4. After restart, add the integration from Settings -> Devices & services -> Add integration and add configuration, when asked. You need to have the IP address of the device and username & password.

## Manual Installation
To install this integration manually:

1. Copy the eh_800_heating_controller directory into the custom_components directory of your Home Assistant installation.
2. Restart Home Assistant.
3. After restart, add the integration from Settings -> Devices & services -> Add integration and add configuration, when asked. You need to have the IP address of the device and username & password.

## TODO
1. Make changes to be approved to HACS
2. Make finnish transaltions

## Contributing
Contributions to this integration are welcome. Please refer to the project's GitHub repository for contributing guidelines.
