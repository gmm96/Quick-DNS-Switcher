#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from src.infrastructure.backend.network_backend_base import NetworkBackendBase
from src.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from src.infrastructure.notifications.notifier_base import NotifierBase
from src.infrastructure.dns.dns_reader.system_dns_reader_base import SystemDnsReaderBase


class PlatformFactory(ABC):
    @abstractmethod
    def create_backend(self) -> NetworkBackendBase:
        pass

    @abstractmethod
    def create_notifier(self) -> NotifierBase:
        pass

    @abstractmethod
    def create_monitor(self) -> NetworkMonitorBase:
        pass

    @abstractmethod
    def create_system_dns_reader(self) -> SystemDnsReaderBase:
        pass
