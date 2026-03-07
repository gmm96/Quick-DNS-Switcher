# !/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import QObject, QTimer, pyqtSlot


class QtNetworkMonitor(QObject):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(update_state)

    @pyqtSlot(int)
    def properties_changed(self, state):
        self.timer.start(500)
