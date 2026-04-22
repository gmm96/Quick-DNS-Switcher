#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from PyQt6.QtWidgets import QApplication
from qds.app.quick_dns_switcher import QuickDnsSwitcher
from qds.config.app_settings import AppSettings
from qds.domain.services.dns_interpreter import DnsInterpreter
from qds.infrastructure.backend.network_backend_base import NetworkBackendBase
from qds.infrastructure.config.user_config_initializer import UserConfigInitializer
from qds.infrastructure.dns.dns_provider_loader import DnsProviderLoader
from qds.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from qds.infrastructure.network.network_state_provider import NetworkStateProvider
from qds.infrastructure.notifications.notifier_base import NotifierBase
from qds.infrastructure.dns.dns_reader.system_dns_reader_base import SystemDnsReaderBase
from qds.startup.linux_factory import LinuxFactory
from qds.startup.platform_factory import PlatformFactory
from qds.startup.windows_factory import WindowsFactory


class Bootstrap:
    @staticmethod
    def create_app(qt_app: QApplication) -> QuickDnsSwitcher:
        app_settings: AppSettings = AppSettings()
        user_config_initializer: UserConfigInitializer = UserConfigInitializer(app_settings)
        user_config_initializer.ensure_dns_providers_file()
        platform_factory: PlatformFactory = Bootstrap._get_platform_factory()
        backend: NetworkBackendBase = platform_factory.create_backend()
        system_dns_reader: SystemDnsReaderBase = platform_factory.create_system_dns_reader()
        network_state_provider: NetworkStateProvider = NetworkStateProvider(backend, system_dns_reader)
        dns_provider_loader: DnsProviderLoader = DnsProviderLoader(app_settings.dns_providers_file)
        dns_interpreter: DnsInterpreter = DnsInterpreter(dns_provider_loader.providers)
        notifier: NotifierBase = platform_factory.create_notifier()
        monitor: NetworkMonitorBase = platform_factory.create_monitor()
        return QuickDnsSwitcher(
            app=qt_app,
            backend=backend,
            network_state_provider=network_state_provider,
            dns_interpreter=dns_interpreter,
            notifier=notifier,
            monitor=monitor,
            dns_providers=dns_provider_loader.providers,
            app_settings=app_settings
        )

    @staticmethod
    def _get_platform_factory() -> PlatformFactory:
        platform_system: str = platform.system().lower()
        if platform_system == "linux":
            return LinuxFactory()
        elif platform_system == "windows":
            return WindowsFactory()
        raise Exception(f"Unsupported system: {platform.system()}")
