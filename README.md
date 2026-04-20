# Quick DNS Switcher

![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge&logo=statuspage&logoColor=brightgreen)
[![Platform](https://img.shields.io/badge/platform-GNU%2Flinux%20%28nmcli%29-yellow?style=for-the-badge&logo=linux&logoColor=gold)](https://networkmanager.dev)
[![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=blue)](https://python.org)
[![Qt](https://img.shields.io/badge/Qt-PyQt6-orange?style=for-the-badge&logo=qt&logoColor=orange)](https://doc.qt.io/qtforpython-6)
[![License](https://img.shields.io/badge/license-GPLv3-green?style=for-the-badge&logo=gplv3&logoColor=green)](LICENSE)

A lightweight system tray application that allows you to **quickly switch between configured DNS providers** with just two clicks.
Built with PyQt6, it supports both IPv4 and IPv6 DNS servers and runs on GNU/Linux platforms with NetworkManager as network configuration tool suite.

![Menu](qds/resources/docs/screenshots/menu.png)


## Features
- **Quick DNS switching**: Change your DNS settings in just 2 clicks from the system tray.
- **IPv4 & IPv6 support**: Full dual-stack compatibility
- **Real-time Monitoring**: Automatically detects network changes and updates DNS status.
- **System Tray Integration**: Runs silently in the background with minimal resource usage.
- **Cross-Platform**: Supports Linux (via NetworkManager).
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
- **Python 3.8+**

### Python Dependencies
- PyQt6


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
    python3 qds/main.py
    ```


## Configuration
DNS providers are configured in [qds/resources/config/dns_providers.json](qds/resources/config/dns_providers.json). Providers have next format in configuration file:

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

Icon field value can be icon name from your system theme or an SVG/PNG file.

If you choose an SVG/PNG file, it should placed in [qds/resources/assets/icons](qds/resources/assets/icons) directory. Then, fill provider variable ```icon``` with its filename (just filename with extension, no path) and adjust ```icon_from_theme``` variable in configuration file.


### Adding a custom DNS provider:

- Right click on app icon in system tray.
- Select ```Edit DNS providers``` from the context menu to open configuration file [qds/resources/config/dns_providers.json](qds/resources/config/dns_providers.json).
- Add a new entry following the format above and save the file.
- Restart application using ```Restart``` app menu option.
- Your custom provider will now appear in the menu.


## Support
If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem
4. Include your operating system, Python version, and any error messages


## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.


## Screenshots

![Menu](qds/resources/docs/screenshots/menu.png)

![Notification](qds/resources/docs/screenshots/notification.png)

![Tooltip](qds/resources/docs/screenshots/tooltip.png)

![System tray](qds/resources/docs/screenshots/tray.png)

