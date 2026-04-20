#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from PyQt6.QtWidgets import QSystemTrayIcon
from qds.infrastructure.notifications.notifier_base import NotifierBase
from qds.ui.models.app_icon import AppIcon


class QtNotifier(NotifierBase):
    def __init__(self) -> None:
        self.tray: Optional[QSystemTrayIcon] = None

    def set_tray(self, tray: QSystemTrayIcon) -> None:
        self.tray = tray

    def notify(self, title: str, message: str, icon: AppIcon, timeout: int = 5000) -> None:
        if self.tray is None:
            raise Exception("QtNotifier tray is not initialized")
        self.tray.showMessage(title, message, icon.qicon, timeout)
