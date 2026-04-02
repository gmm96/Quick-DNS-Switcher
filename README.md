# Quick DNS Switcher

![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge&logo=statuspage)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python)
![Qt](https://img.shields.io/badge/Qt-PyQt6-green?style=for-the-badge&logo=qt)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey?style=for-the-badge&logo=linux)
![NetworkManager](https://img.shields.io/badge/network-NetworkManager-red?style=for-the-badge&logo=red)
[![License](https://img.shields.io/badge/license-GPLv3-orange?style=for-the-badge&logo=gplv3)
](LICENSE)

A lightweight system tray application that allows you to quickly switch between configured DNS providers with just two clicks. Built with PyQt6, it supports both IPv4 and IPv6 DNS servers and runs on Linux ~~and Windows~~ platforms.


## Features
- **Quick DNS switching**: Change your DNS settings in just 2 clicks from the system tray.
- **IPv4 & IPv6 support**: Full dual-stack compatibility
- **Real-time Monitoring**: Automatically detects network changes and updates DNS status.
- **System Tray Integration**: Runs silently in the background with minimal resource usage.
- **Cross-Platform**: Supports Linux (via NetworkManager) ~~and Windows~~.
- **Notifications**: Desktop notifications when DNS settings change.
- **Multiple DNS providers**: Pre-configured with 7 popular DNS providers:
  - Cloudflare
  - Google
  - Quad9
  - AdGuard
  - OpenDNS
  - Mullvad
  - Yandex
- **Customizable**: Easy to personalize or add custom DNS providers via JSON configuration.


## Requirements
### System Requirements
- **Linux**: NetworkManager with `nmcli` command-line tool
- ~~**Windows**: Windows 10/11~~
- **Python 3.8+**

### Python Dependencies
- PyQt6
- dbus-python

## Installation

### From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gmm96/Quick-DNS-Switcher.git
   cd Quick-DNS-Switcher
   ```
2. **Install dependencies**:
    ```bash
    pip install PyQt6
   ```
3. **Run the application**:
    ```bash
    python3 src/main.py
    ```


## Configuration
DNS providers are configured in [src/resources/dns_providers.json](src/resources/dns_providers.json):

```json
{
    "Provider Name": {
        "ipv4_1": "primary_ipv4_address",
        "ipv4_2": "secondary_ipv4_address", 
        "ipv6_1": "primary_ipv6_address",
        "ipv6_2": "secondary_ipv6_address",
        "icon": "icon_filename.svg",
        "icon_from_theme": false
    }
}
```

### Adding a custom DNS provider:

- Open src/resources/dns_providers.json
- Add a new entry following the format above
- Restart the application
- Your custom provider will appear in the menu


# Support
If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem
4. Include your operating system, Python version, and any error messages


## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
