#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbus
from dbus.bus import BusConnection
from dbus.proxies import ProxyObject, Interface
from typing import Optional
from src.infrastructure.notifications.notifier_base import NotifierBase
from src.ui.models.app_icon import AppIcon
from src.ui.ui_constants import UiConstants


class DbusNotifier(NotifierBase):
    BUS_NAME: str = "org.freedesktop.Notifications"
    OBJECT_PATH: str = "/org/freedesktop/Notifications"
    INTERFACE_NAME: str = "org.freedesktop.Notifications"

    def __init__(self) -> None:
        self.dbus_interface: Optional[Interface] = None

    def _init_dbus(self) -> None:
        bus: BusConnection = dbus.SessionBus()
        notify_object: ProxyObject = bus.get_object(DbusNotifier.BUS_NAME, DbusNotifier.OBJECT_PATH)
        self.dbus_interface: Interface = dbus.Interface(notify_object, DbusNotifier.INTERFACE_NAME)

    def notify(self, title: str, body: str, icon: AppIcon, timeout: int = 5000) -> None:
        if self.dbus_interface is None:
            self._init_dbus()
        if self.dbus_interface is None:
            return
        try:
            self.dbus_interface.Notify(UiConstants.APP_NAME, 0, icon.name, title, body, [], {}, timeout)
        except dbus.exceptions.DBusException:
            self._init_dbus()
            self.dbus_interface.Notify(UiConstants.APP_NAME, 0, icon.name, title, body, [], {}, timeout)
