#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import QObject
from qds.infrastructure.monitoring.netlink_worker import NetlinkWorker
from qds.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase


class NetlinkNetworkMonitor(QObject, NetworkMonitorBase):
    RTMGRP_IPV4_ROUTE: int = 0x40
    RTMGRP_IPV6_ROUTE: int = 0x400
    RTMGRP_IPV4_IFADDR: int = 0x10
    RTMGRP_IPV6_IFADDR: int = 0x100
    GROUPS: int = RTMGRP_IPV4_ROUTE | RTMGRP_IPV6_ROUTE | RTMGRP_IPV4_IFADDR | RTMGRP_IPV6_IFADDR

    def __init__(self, parent: QObject = None) -> None:
        QObject.__init__(self, parent)
        NetworkMonitorBase.__init__(self)
        self.worker = NetlinkWorker(self.GROUPS)
        self.worker.event_detected.connect(self._emit)
        self.worker.start()
