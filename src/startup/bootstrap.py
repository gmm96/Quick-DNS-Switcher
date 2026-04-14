#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from PyQt6.QtWidgets import QApplication
from src.app.quick_dns_switcher import QuickDnsSwitcher
from src.config.paths import Paths
from src.domain.services.dns_interpreter import DnsInterpreter
from src.infrastructure.backend.network_backend_base import NetworkBackendBase
from src.infrastructure.dns.dns_provider_loader import DnsProviderLoader
from src.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from src.infrastructure.network.network_state_provider import NetworkStateProvider
from src.infrastructure.notifications.notifier_base import NotifierBase
from src.infrastructure.dns.dns_reader.system_dns_reader_base import SystemDnsReaderBase
from src.startup.linux_factory import LinuxFactory
from src.startup.platform_factory import PlatformFactory
from src.startup.windows_factory import WindowsFactory


class Bootstrap:
    @staticmethod
    def create_app(qt_app: QApplication) -> QuickDnsSwitcher:
        platform_factory: PlatformFactory = Bootstrap._get_platform_factory()
        backend: NetworkBackendBase = platform_factory.create_backend()
        system_dns_reader: SystemDnsReaderBase = platform_factory.create_system_dns_reader()
        network_state_provider: NetworkStateProvider = NetworkStateProvider(backend, system_dns_reader)
        dns_provider_loader: DnsProviderLoader = DnsProviderLoader(Paths.DNS_PROVIDERS_FILE)
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
            dns_providers=dns_provider_loader.providers
        )

    @staticmethod
    def _get_platform_factory() -> PlatformFactory:
        platform_system: str = platform.system().lower()
        if platform_system == "linux":
            return LinuxFactory()
        elif platform_system == "windows":
            return WindowsFactory()
        raise Exception(f"Unsupported system: {platform.system()}")
