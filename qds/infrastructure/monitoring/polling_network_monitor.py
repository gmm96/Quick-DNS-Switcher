#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import QTimer, QObject
from qds.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from qds.ui.ui_context import UiContext


class PollingNetworkMonitor(QObject, NetworkMonitorBase):
    def __init__(self, interval: int = 3000):
        QObject.__init__(self)
        NetworkMonitorBase.__init__(self)
        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(UiContext.safe_callback(self._emit))
        self._timer.start(interval)
