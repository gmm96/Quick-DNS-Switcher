#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import json
import signal
import ipaddress
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusReply
from PyQt6.QtCore import QObject, QTimer, pyqtSlot
from utils.tools import ensure_single_instance, display_error_dialog, execute_command
from utils.constants import Constants
from network.ip_pair import IpPair
from network.dns_configuration import DnsConfiguration
from network.dns_provider import DnsProvider
from network.dns_state import DnsState
from network.network_connection import NetworkConnection


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(PROJECT_DIR, "dns-providers.json")
ICON_DIR = os.path.join(PROJECT_DIR, "icons")


class QtNetworkMonitor(QObject):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(update_state)

    @pyqtSlot(str, dict, list)
    def handle_dbus_change(self, interface, changed, invalidated):
        # Escuchamos cambios en conexiones activas o estado global
        if "ActiveConnections" in changed or "State" in changed:
            self.timer.start(800)



# region Functions

def get_provider_dns(provider):
    ipv4 = [ip for ip in [provider.get("ipv4_1"), provider.get("ipv4_2")] if ip]
    ipv6 = [ip for ip in [provider.get("ipv6_1"), provider.get("ipv6_2")] if ip]
    return ipv4, ipv6


def get_active_connections_with_dns() -> List[NetworkConnection]:
    conns = []
    IGNORED_DEVICES = ("lo", "tun0", "")
    bus = QDBusConnection.systemBus()
    
    nm_iface = QDBusInterface("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager", "org.freedesktop.NetworkManager", bus)
    active_paths = nm_iface.property("ActiveConnections")
    if not active_paths: return conns

    for path in active_paths:
        c_iface = QDBusInterface("org.freedesktop.NetworkManager", path, "org.freedesktop.NetworkManager.Connection.Active", bus)
        name = c_iface.property("Id")
        devices = c_iface.property("Devices")
        if not devices: continue
        dev_iface = QDBusInterface("org.freedesktop.NetworkManager", devices[0], "org.freedesktop.NetworkManager.Device", bus)
        device_name = dev_iface.property("Interface")
        if device_name in IGNORED_DEVICES: continue
        # IPv4 via D-Bus
        ipv4_list = []
        ip4_path = c_iface.property("Ip4Config")
        if ip4_path and ip4_path != "/":
            ip4_iface = QDBusInterface("org.freedesktop.NetworkManager", ip4_path, "org.freedesktop.NetworkManager.IP4Config", bus)
            ns = ip4_iface.property("Nameservers")
            if ns:
                for val in ns:
                    if isinstance(val, int): # Network Byte Order
                        ipv4_list.append(socket.inet_ntoa(struct.pack("<L", val)))
                    else: ipv4_list.append(str(val))

        # IPv6 via D-Bus
        ipv6_list = []
        ip6_path = c_iface.property("Ip6Config")
        if ip6_path and ip6_path != "/":
            ip6_iface = QDBusInterface("org.freedesktop.NetworkManager", ip6_path, "org.freedesktop.NetworkManager.IP6Config", bus)
            ns6 = ip6_iface.property("Nameservers")
            if ns6:
                for b_array in ns6:
                    ipv6_list.append(socket.inet_ntop(socket.AF_INET6, bytes(b_array)))

        conns.append(
            NetworkConnection(
                name,
                device_name, 
                IpPair.from_list(4, ipv4_list), 
                IpPair.from_list(6, ipv6_list)
            )
        )
    return conns


def get_current_dns() -> DnsState:
    v4_total, v6_total = [], []
    for conn in get_active_connections_with_dns():
        v4_total.extend(conn.ipv4.get_ip_list())
        v6_total.extend(conn.ipv6.get_ip_list())
    
    return DnsState(
        IpPair.from_list(4, list(dict.fromkeys(v4_total))),
        IpPair.from_list(6, list(dict.fromkeys(v6_total)))
    )


def set_dns(target_v4: IpPair, target_v6: IpPair):
    v4_str = ",".join(target_v4.get_ip_list())
    v6_str = ",".join(target_v6.get_ip_list())
    
    for conn in get_active_connections_with_dns():
        if conn.ipv4 == target_v4 and conn.ipv6 == target_v6:
            continue

        # IPv4
        mode_v4 = "yes" if v4_str else "no"
        execute_command(["nmcli", "connection", "modify", conn.name, "ipv4.ignore-auto-dns", mode_v4, "ipv4.dns", v4_str], False)
        # IPv6
        mode_v6 = "yes" if v6_str else "no"
        execute_command(["nmcli", "connection", "modify", conn.name, "ipv6.ignore-auto-dns", mode_v6, "ipv6.dns", v6_str], False)

        execute_command(["nmcli", "device", "reapply", conn.device], False, False)


def detect_active_provider(current_dns):
    for name, data in DNS_PROVIDERS.items():
        v4_prov, v6_prov = get_provider_dns(data)
        match_v4 = set(v4_prov) == set(current_dns["ipv4"]) if v4_prov else not current_dns["ipv4"]
        match_v6 = set(v6_prov) == set(current_dns["ipv6"]) if v6_prov else not current_dns["ipv6"]  
        if match_v4 and match_v6:
            return name

    if current_dns["ipv4"] or current_dns["ipv6"]:
        return Constants.AUTO_MODE_NAME

    return "Disconnected"


def monitor_network_changes():
    global nm_monitor
    nm_monitor = QtNetworkMonitor()
    QDBusConnection.systemBus().connect(
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager",
        "org.freedesktop.DBus.Properties",
        "PropertiesChanged",
        nm_monitor.handle_dbus_change
    )


def update_state():
    global last_dns_ips
    state = get_current_dns()
    active_name = Constants.AUTO_MODE_NAME
    
    for provider in dns_config.get_all():
        if state.matches_provider(provider):
            active_name = provider.name
            break

    # Icono
    provider_obj = dns_config.get_by_name(active_name)
    if active_name == Constants.AUTO_MODE_NAME:
        tray.setIcon(QIcon.fromTheme(Constants.AUTO_MODE_ICON))
    elif provider_obj and provider_obj.icon:
        icon_p = os.path.join(ICON_DIR, provider_obj.icon)
        tray.setIcon(QIcon(icon_p) if os.path.exists(icon_p) else QIcon.fromTheme(Constants.DEFAULT_MODE_ICON))
    else:
        tray.setIcon(QIcon.fromTheme(Constants.DEFAULT_MODE_ICON))

    # Menú (Checkmarks)
    auto_action.setText(f"✔ {Constants.AUTO_MODE_NAME}" if active_name == Constants.AUTO_MODE_NAME else Constants.AUTO_MODE_NAME)
    for name, action in provider_actions.items():
        action.setText(f"✔ {name}" if name == active_name else name)

    # Notificación si hay cambio real
    current_ips = state.all_ips
    if last_dns_ips is not None and set(current_ips) != set(last_dns_ips):
        body = "DNS: " + (", ".join(current_ips) if current_ips else "System Default")
        execute_command(["notify-send", "-a", Constants.APP_NAME, "-t", "5000", f"Network: {active_name}", body], False, False)
    last_dns_ips = current_ips

    # Tooltip
    tray.setToolTip(f"{Constants.APP_NAME}\n{active_name}\n\n" + "\n".join(current_ips))


def make_set_dns_action(ipv4: IpPair, ipv6: IpPair):
    def handler(checked=False):
        set_dns(ipv4, ipv6)
    return handler


def open_config():
    subprocess.Popen(["xdg-open", CONFIG_FILE])


def restart_app():
    python = sys.executable
    QApplication.quit()
    subprocess.Popen([python] + sys.argv)

# endregion


###############################################################################


# region App

app = QApplication(sys.argv)
app.server = ensure_single_instance()

dns_config = DnsConfiguration(CONFIG_FILE)
last_dns_ips = None
provider_actions = {}

tray = QSystemTrayIcon()
menu = QMenu()

monitor_network_changes()


# Menu structure
title_action = QAction(Constants.APP_NAME)
title_action.setEnabled(False)
menu.addAction(title_action)

menu.addSeparator()

auto_action = QAction(QIcon.fromTheme(Constants.AUTO_MODE_ICON), Constants.AUTO_MODE_NAME)
auto_action.triggered.connect(make_set_dns_action(IpPair(4), IpPair(6)))
menu.addAction(auto_action)

menu.addSeparator()

for provider in sorted(dns_config.get_all(), key=lambda x: x.name):
    action = QAction(provider.name)
    action.triggered.connect(make_set_dns_action(provider.ipv4, provider.ipv6))
    icon_path = os.path.join(ICON_DIR, provider.icon)
    if provider.icon and os.path.exists(icon_path):
        q_icon = QIcon(icon_path)
    else:
        q_icon = QIcon.fromTheme(Constants.DEFAULT_MODE_ICON)
    action.setIcon(q_icon)
    menu.addAction(action)
    provider_actions[provider.name] = action

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
tray.show()
update_state()

sys.exit(app.exec())

# endregion
