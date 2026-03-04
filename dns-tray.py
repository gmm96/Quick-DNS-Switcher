#!/usr/bin/env python3

import sys
import subprocess
import os
import json
from functools import partial
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtCore import QTimer


DIR = os.path.dirname(os.path.realpath(__file__))
JSON = os.path.join(DIR, "dns-providers.json")
DNS_SWITCH = os.path.join(DIR, "bin", "dns-switch")
DNS_CURRENT = os.path.join(DIR, "bin", "dns-current")
ICONS = os.path.join(DIR, "icons")



import subprocess
import ipaddress


def get_current_dns():
    dns_list = []

    try:
        output = subprocess.check_output(
            ["nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active"],
            encoding="utf-8", errors="ignore"
        ).strip().splitlines()

        for line in output:
            if not line:
                continue
            parts = line.split(":", 1)
            if len(parts) != 2:
                continue
            name, device = parts
            if device in ("lo", ""):
                continue

            # IPv4
            try:
                raw_ipv4 = subprocess.check_output(
                    ["nmcli", "-g", "ipv4.dns", "connection", "show", name],
                    encoding="utf-8", errors="ignore"
                ).strip()
                ipv4_dns = [ip.strip() for ip in raw_ipv4.split(",") if ip.strip()]
            except subprocess.CalledProcessError:
                ipv4_dns = []

            # IPv6
            try:
                raw_ipv6 = subprocess.check_output(
                    ["nmcli", "-g", "ipv6.dns", "connection", "show", name],
                    encoding="utf-8", errors="ignore"
                ).strip()
                ipv6_dns = [ip.replace("\\:", ":").strip() for ip in raw_ipv6.split(",") if ip.strip()]
            except subprocess.CalledProcessError:
                ipv6_dns = []

            # Validar y añadir, evitando duplicados
            for ip in ipv4_dns + ipv6_dns:
                try:
                    ipaddress.ip_address(ip)
                    dns_list.append(ip)
                except ValueError:
                    continue

        # eliminar duplicados manteniendo orden
        dns_list = list(dict.fromkeys(dns_list))
        return " ".join(dns_list)

    except Exception:
        return ""


def set_dns(v4, v6):
    subprocess.Popen([DNS_SWITCH, v4, v6])
    QTimer.singleShot(1200, update_state)


def get_active_connections_with_dns():
    """
    Devuelve lista de tuplas: (name, device, ipv4_dns, ipv6_dns)
    """
    conns_info = []
    try:
        output = subprocess.check_output([
            "nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active"
        ]).decode().strip().splitlines()

        for line in output:
            if not line:
                continue
            name, device = line.split(":", 1)
            if device in ("lo", ""):
                continue

            try:
                ipv4_dns = subprocess.check_output(
                    ["nmcli", "-g", "ipv4.dns", "connection", "show", name]
                ).decode().strip()
            except subprocess.CalledProcessError:
                ipv4_dns = ""

            try:
                ipv6_dns = subprocess.check_output(
                    ["nmcli", "-g", "ipv6.dns", "connection", "show", name]
                ).decode().strip()
            except subprocess.CalledProcessError:
                ipv6_dns = ""

            conns_info.append((name, device, ipv4_dns, ipv6_dns))

    except subprocess.CalledProcessError:
        pass

    return conns_info


def is_manual_dns(active_conns):
    return any(dns4 or dns6 for _, _, dns4, dns6 in active_conns)


def detect_active_provider(current_dns, active_conns):
    if not is_manual_dns(active_conns):
        return "Automatic (DHCP)"

    for name, data in DNS_PROVIDERS.items():
        v4 = data["v4"]
        if v4 and all(ip in current_dns for ip in v4.split()):
            return name
    return None



def update_state():
    # Obtener DNS actual como lista de IPv4 e IPv6
    current_dns = get_current_dns()  # tu función devuelve "IP1 IP2 ... IPn"
    active_conns = get_active_connections_with_dns()
    manual = is_manual_dns(active_conns)
    active = detect_active_provider(current_dns, active_conns)

    if not manual:
        auto_action.setText("✔ Automatic (DHCP)")
        tray.setIcon(QIcon.fromTheme("network-workgroup"))
    else:
        auto_action.setText("Automatic (DHCP)")
        if active and active in DNS_PROVIDERS:
            icon_name = DNS_PROVIDERS[active].get("icon")
            icon_file = os.path.join(ICONS, icon_name)
            if icon_name and os.path.exists(icon_file):
                tray.setIcon(QIcon(icon_file))
            else:
                tray.setIcon(QIcon.fromTheme("network-server"))

    for name, action in actions.items():
        if name == active:
            action.setText(f"✔ {name}")
        else:
            action.setText(name)

    # Format IPs 
    ipv4_list = []
    ipv6_list = []
    for ip in current_dns.split():
        try:
            import ipaddress
            if ipaddress.ip_address(ip).version == 4:
                ipv4_list.append(ip)
            else:
                ipv6_list.append(ip)
        except ValueError:
            continue

    display_ipv4 = ", ".join(ipv4_list) if ipv4_list else "–"
    display_ipv6 = ", ".join(ipv6_list) if ipv6_list else "–"

    # Tooltip con IPv4 e IPv6 en líneas separadas
    tooltip_text = (
        f"Quick DNS switcher\n"
        f"Active: {active}\n"
        f"IPv4:\n{display_ipv4}\n"
        f"IPv6:\n{display_ipv6}"
    )

    if current_dns:
        ipv4_list = []
        ipv6_list = []
        for ip in current_dns.split():
            try:
                import ipaddress
                if ipaddress.ip_address(ip).version == 4:
                    ipv4_list.append(ip)
                else:
                    ipv6_list.append(ip)
            except ValueError:
                continue

        display_ipv4 = ", ".join(ipv4_list) if ipv4_list else "–"
        display_ipv6 = ", ".join(ipv6_list) if ipv6_list else "–"
        tooltip_text = (
            f"Quick DNS switcher\n"
            f"{active}\n"
            f"{display_ipv4}\n"
            f"{display_ipv6}"
        )
    else:
        tooltip_text = (
        f"Quick DNS switcher\n"
        f"{active}"
    )

    tray.setToolTip(tooltip_text)



def make_set_dns_action(v4, v6):
    def handler(checked=False):
        set_dns(v4, v6)
    return handler


def open_config():
    editor = os.environ.get("EDITOR", "xdg-open")
    subprocess.Popen([editor, JSON])


def restart_app():
    python = sys.executable
    QApplication.quit()
    subprocess.Popen([python] + sys.argv)


##########################


if os.path.exists(JSON):
    with open(JSON, "r") as f:
        DNS_PROVIDERS = json.load(f)
else:
    DNS_PROVIDERS = {}

# Menu
app = QApplication(sys.argv)
tray = QSystemTrayIcon()
menu = QMenu()
actions = {}

title_action = QAction("Quick DNS switcher")
title_action.setEnabled(False)
menu.addAction(title_action)

menu.addSeparator()

auto_action = QAction(QIcon.fromTheme("network-workgroup"), "Automatic (DHCP)")
auto_action.triggered.connect(make_set_dns_action("", ""))
menu.addAction(auto_action)

menu.addSeparator()

for name in sorted(DNS_PROVIDERS.keys()):
    data = DNS_PROVIDERS[name]
    v4 = data["v4"]
    v6 = data["v6"]
    icon_name = data.get("icon")
    icon_file = os.path.join(ICONS, icon_name)
    if icon_name and os.path.exists(icon_file):
        action = QAction(QIcon(icon_file), name)
    else:
        action = QAction(QIcon.fromTheme("network-server"), name)
    action.triggered.connect(make_set_dns_action(v4, v6))
    menu.addAction(action)
    actions[name] = action

menu.addSeparator()

options_title_action = QAction("Options")
options_title_action.setEnabled(False)
menu.addAction(options_title_action)

edit_action = QAction(QIcon.fromTheme("edit"), "Edit DNS providers")
edit_action.triggered.connect(open_config)
menu.addAction(edit_action)

restart_action = QAction(QIcon.fromTheme("vm-restart"), "Restart")
restart_action.triggered.connect(restart_app)
menu.addAction(restart_action)

exit_action = QAction(QIcon.fromTheme("exit"), "Exit")
exit_action.triggered.connect(app.quit)
menu.addAction(exit_action)

tray.setContextMenu(menu)
tray.setIcon(QIcon.fromTheme("network-server"))
tray.show()

# Update every 2 seconds
timer = QTimer()
timer.timeout.connect(update_state)
timer.start(2000)

update_state()

sys.exit(app.exec())
