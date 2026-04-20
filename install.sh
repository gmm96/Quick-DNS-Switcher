#!/usr/bin/env bash

set -euo pipefail

APP_NAME="quick-dns-switcher"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${EUID}" -eq 0 ]];
then
    MODE="system"
    INSTALL_DIR="/opt/${APP_NAME}"
    BIN_DIR="/usr/bin"
    DESKTOP_FILE="/usr/share/applications/${APP_NAME}.desktop"
    AUTOSTART_FILE="/etc/xdg/autostart/${APP_NAME}.desktop"
    ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
    SHARE_DIR="/usr/share/${APP_NAME}"
else
    MODE="user"
    INSTALL_DIR="${HOME}/.local/opt/${APP_NAME}"
    BIN_DIR="${HOME}/.local/bin"
    DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"
    AUTOSTART_FILE="${HOME}/.config/autostart/${APP_NAME}.desktop"
    ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"
    SHARE_DIR="${HOME}/.local/share/${APP_NAME}"
fi

BIN_FILE="${BIN_DIR}/${APP_NAME}"

echo "Installing ${APP_NAME} (${MODE})..."



#######################################
# DEPENDENCIES
#######################################

# Install required dependencies
install_dependencies()
{
    if command -v pacman >/dev/null 2>&1;
    then
        pacman -Sy --needed --noconfirm python python-pyqt6 networkmanager python-dbus
    elif command -v apt >/dev/null 2>&1;
    then
        apt update && apt install -y python3 python3-pyqt6 network-manager python3-dbus
    elif command -v dnf >/dev/null 2>&1;
    then
        dnf install -y python3 python3-pyqt6 NetworkManager python3-dbus
    else
        echo "Package manager not supported by install script. You may need to install dependencies manually."
        echo "Aborting installation."
        exit 1
    fi
}

if [[ "${MODE}" == "system" ]]; then
    echo "Installing required dependencies..."
    install_dependencies
fi



# Check dependencies
failed_dependency()
{
    echo "ERROR: missing dependency ${1}"
    echo "Aborting installation."
    exit 1
}

echo "Checking dependencies..."

if ! command -v python3 >/dev/null 2>&1; then
    failed_dependency "python3"
fi
if ! python3 -c "import PyQt6" >/dev/null 2>&1; then
    failed_dependency "python-pyqt6"
fi
if ! python3 -c "import dbus" >/dev/null 2>&1; then
    failed_dependency "python-dbus"
fi
if ! command -v nmcli >/dev/null 2>&1; then
    failed_dependency "networkmanager (nmcli)"
fi

echo "Dependencies OK"



#######################################
# INSTALL
#######################################

echo "Installing application files..."

# Source
rm -rf "${INSTALL_DIR}"
install -dm755 "${INSTALL_DIR}"
cp -r "${SCRIPT_DIR}/qds" "${INSTALL_DIR}/"
find "${INSTALL_DIR}/qds" -type d -exec chmod 755 {} \;
find "${INSTALL_DIR}/qds" -type f -exec chmod 644 {} \;
install -Dm755 "${SCRIPT_DIR}/${APP_NAME}.sh" "${INSTALL_DIR}/${APP_NAME}.sh"
install -Dm644 "${SCRIPT_DIR}/README.md" "${INSTALL_DIR}/README.md" 2>/dev/null || true
install -Dm644 "${SCRIPT_DIR}/LICENSE" "${INSTALL_DIR}/LICENSE" 2>/dev/null || true

# Bin
install -dm755 "${BIN_DIR}"
ln -sf "${INSTALL_DIR}/${APP_NAME}.sh" "${BIN_FILE}"

# Config
install -Dm644 "${SCRIPT_DIR}/qds/resources/config/dns_providers.json" "${SHARE_DIR}/dns_providers.json"

# App shortcut
install -Dm644 "${SCRIPT_DIR}/qds/resources/assets/${APP_NAME}.desktop" "${DESKTOP_FILE}"

# Autostart
install -Dm644 "${SCRIPT_DIR}/qds/resources/assets/${APP_NAME}.desktop" "${AUTOSTART_FILE}"

# Icons
install -dm755 "${ICON_DIR}"
shopt -s nullglob
rm -f "${ICON_DIR}/qds-"* 2>/dev/null
rm -f "${ICON_DIR}/quick-dns-switcher-"* 2>/dev/null
for icon in "${SCRIPT_DIR}/qds/resources/assets/icons/"*".svg";
do
    install -Dm644 "${icon}" "${ICON_DIR}/$(basename "${icon}")"
done
shopt -u nullglob
if command -v gtk-update-icon-cache >/dev/null 2>&1;
then
    if [[ "${MODE}" == "system" ]];
    then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
    else
        gtk-update-icon-cache -f -t "${HOME}/.local/share/icons/hicolor" || true
    fi
fi

echo "Quick DNS Switcher installation completed (${MODE})!"
echo "Run with: quick-dns-switcher"
