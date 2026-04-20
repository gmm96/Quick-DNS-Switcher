#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
from qds.infrastructure.backend.network_manager_backend import NetworkManagerBackend
from qds.infrastructure.monitoring.hybrid_network_monitor import HybridNetworkMonitor
from qds.infrastructure.notifications.dbus_notifier import DbusNotifier
from qds.infrastructure.dns.dns_reader.linux_dns_reader import LinuxDnsReader
from qds.startup.platform_factory import PlatformFactory


class LinuxFactory(PlatformFactory):
    def create_backend(self) -> NetworkManagerBackend:
        if shutil.which("nmcli"):
            return NetworkManagerBackend()
        raise Exception("NetworkManager is not installed.")

    def create_notifier(self) -> DbusNotifier:
        return DbusNotifier()

    def create_monitor(self) -> HybridNetworkMonitor:
        return HybridNetworkMonitor()

    def create_system_dns_reader(self) -> LinuxDnsReader:
        return LinuxDnsReader()
