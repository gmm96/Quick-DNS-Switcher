#!/usr/bin/env bash

set -euo pipefail

APP_NAME="quick-dns-switcher"

if [[ "${EUID}" -eq 0 ]];
then
    MODE="system"
    INSTALL_DIR="/opt/${APP_NAME}"
    BIN_FILE="/usr/bin/${APP_NAME}"
    DESKTOP_FILE="/usr/share/applications/${APP_NAME}.desktop"
    AUTOSTART_FILE="/etc/xdg/autostart/${APP_NAME}.desktop"
    ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
    SHARE_DIR="/usr/share/${APP_NAME}"
else
    MODE="user"
    INSTALL_DIR="${HOME}/.local/opt/${APP_NAME}"
    BIN_FILE="${HOME}/.local/bin/${APP_NAME}"
    DESKTOP_FILE="${HOME}/.local/share/applications/${APP_NAME}.desktop"
    AUTOSTART_FILE="${HOME}/.config/autostart/${APP_NAME}.desktop"
    ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"
    SHARE_DIR="${HOME}/.local/share/${APP_NAME}"
fi

pkill -f "quick-dns-switcher" 2>/dev/null || true

echo "Uninstalling ${APP_NAME} (${MODE})..."



#######################################
# UNINSTALL
#######################################

# Source
rm -rf "${INSTALL_DIR}"

# Bin
rm -f "${BIN_FILE}"

# Config
rm -rf "${SHARE_DIR}"

# App shortcut
rm -f "${DESKTOP_FILE}"

# Autostart
rm -f "${AUTOSTART_FILE}"

# Icons
shopt -s nullglob
rm -f "${ICON_DIR}/qds-"* 2>/dev/null
rm -f "${ICON_DIR}/quick-dns-switcher-"* 2>/dev/null
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

echo "${APP_NAME} successfully uninstalled (${MODE})"
