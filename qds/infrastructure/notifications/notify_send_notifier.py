#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qds.infrastructure.system.command_executor import CommandExecutor
from qds.infrastructure.notifications.notifier_base import NotifierBase
from qds.ui.models.app_icon import AppIcon
from qds.ui.ui_constants import UiConstants


class NotifySendNotifier(NotifierBase):
    def __init__(self) -> None:
        pass

    def notify(self, title: str, body: str, icon: AppIcon, timeout: int = 5000) -> None:
        CommandExecutor.execute(
            [
                "notify-send",
                "-a", UiConstants.APP_NAME,
                "-t", str(timeout),
                "-i", icon.name,
                title,
                body,
            ],
            check=False
        )
