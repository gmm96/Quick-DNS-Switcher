#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from pyroute2 import IPRoute


class NetlinkWorker(QThread):
    event_detected = pyqtSignal()

    def __init__(self, groups: int, parent: QObject = None) -> None:
        super().__init__(parent)
        self.groups: int = groups

    def run(self) -> None:
        try:
            with IPRoute() as ipr:
                ipr.bind(groups=self.groups)
                while True:
                    ipr.get()
                    self.event_detected.emit()
        except Exception as e:
            print(f"[NetlinkWorker] ❌ Error fatal: {e}", flush=True)
