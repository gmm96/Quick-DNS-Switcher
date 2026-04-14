#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from src.infrastructure.monitoring.netlink_network_monitor import NetlinkNetworkMonitor
from src.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from src.infrastructure.monitoring.polling_network_monitor import PollingNetworkMonitor


class HybridNetworkMonitor(NetworkMonitorBase):
    def __init__(self, interval: Optional[int] = None) -> None:
        super().__init__()
        self._netlink: NetlinkNetworkMonitor = NetlinkNetworkMonitor()
        self._polling: PollingNetworkMonitor = PollingNetworkMonitor(interval) if interval else PollingNetworkMonitor()
        self._netlink.on_event(self._emit)
        self._polling.on_event(self._emit)
