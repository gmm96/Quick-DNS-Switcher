#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Optional, List
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from qds.config.app_settings import AppSettings
from qds.domain.models.dns.dns_interpretation import DnsInterpretation
from qds.domain.enums.dns_mode import DnsMode
from qds.domain.models.dns.dns_provider import DnsProvider
from qds.infrastructure.backend.network_backend_base import NetworkBackendBase
from qds.infrastructure.network.network_state_provider import NetworkStateProvider
from qds.ui.models.dns_view import DnsView
from qds.domain.services.dns_interpreter import DnsInterpreter
from qds.infrastructure.system.command_executor import CommandExecutor
from qds.domain.models.network_state import NetworkState
from qds.domain.models.network.ip_pair import IpPair
from qds.infrastructure.monitoring.event_debouncer import Debouncer
from qds.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from qds.infrastructure.notifications.notifier_base import NotifierBase
from qds.infrastructure.notifications.qt_notifier import QtNotifier
from qds.ui.models.app_icon import AppIcon
from qds.ui.tray_controller import TrayController
from qds.ui.ui_constants import UiConstants
from qds.ui.ui_context import UiContext


class QuickDnsSwitcher:
    def __init__(self,
        app: QApplication,
        backend: NetworkBackendBase,
        network_state_provider: NetworkStateProvider,
        dns_interpreter: DnsInterpreter,
        notifier: NotifierBase,
        monitor: NetworkMonitorBase,
        dns_providers: List[DnsProvider],
        app_settings: AppSettings
    ) -> None:
        # Dependencies
        self.backend: NetworkBackendBase = backend
        self.network_state_provider: NetworkStateProvider = network_state_provider
        self.dns_interpreter: DnsInterpreter = dns_interpreter
        self.notifier: NotifierBase = notifier
        self.monitor: NetworkMonitorBase = monitor
        self.dns_providers: List[DnsProvider] = dns_providers
        self.app_settings: AppSettings = app_settings
        # UI
        self.app: QApplication = app
        self.app.setDesktopFileName(app_settings.app_name)
        self.app.setApplicationName(UiConstants.APP_NAME)
        self.app.setApplicationDisplayName(UiConstants.APP_NAME)
        self.app.setQuitOnLastWindowClosed(False)
        self._ensure_single_instance()
        self.tray: TrayController = TrayController(
            app=self.app,
            dns_providers=self.dns_providers,
            set_dns_callback=self._set_dns,
            open_config_callback=self._open_config,
            restart_callback=self._restart_app,
            quit_callback=self._quit_app
        )
        if isinstance(self.notifier, QtNotifier):
            self.notifier.set_tray(self.tray.tray)
        # Listen for changes
        self.network_state: Optional[NetworkState] = None
        self.debouncer: Debouncer = Debouncer(self._update_state)
        self.monitor.on_event(self._on_network_event)
        QTimer.singleShot(0, UiContext.safe_callback(self._update_state))

    def run(self) -> None:
        sys.exit(self.app.exec())

    def _ensure_single_instance(self) -> None:
        socket: QLocalSocket = QLocalSocket()
        socket.connectToServer(self.app_settings.app_name)
        if socket.waitForConnected(500):
            sys.exit(0)
        self.server: QLocalServer = QLocalServer()
        self.server.removeServer(self.app_settings.app_name)
        self.server.listen(self.app_settings.app_name)

    def _set_dns(self, ipv4: IpPair, ipv6: IpPair) -> None:
        self.backend.set_dns(ipv4, ipv6)
        QTimer.singleShot(500, UiContext.safe_callback(self._update_state))

    def _update_state(self) -> None:
        network_state: NetworkState = self.network_state_provider.retrieve()
        if self.network_state and self.network_state.matches_state(network_state):
            return
        dns_interpretation: DnsInterpretation = self.dns_interpreter.resolve(network_state)
        dns_view: DnsView = DnsView.from_dns_interpretation(dns_interpretation)
        self.tray.update(dns_view)
        self._send_notification(dns_view)
        self.network_state: NetworkState = network_state

    def _on_network_event(self) -> None:
        self.debouncer.trigger()

    def _send_notification(self, view: DnsView) -> None:
        icon: AppIcon = self.tray.get_icon(view.icon_key)
        title: str = f"{view.display_name} DNS" if view.mode != DnsMode.DISCONNECTED else view.display_name
        self.notifier.notify(title, "\n".join(view.body), icon)

    def _open_config(self) -> None:
        CommandExecutor.execute_async(["xdg-open", str(self.app_settings.dns_providers_file)])

    @staticmethod
    def _restart_app() -> None:
        QApplication.quit()
        CommandExecutor.execute_async([sys.executable, "-m", "qds.main"] + sys.argv[1:])

    def _quit_app(self) -> None:
        self.app.quit()
