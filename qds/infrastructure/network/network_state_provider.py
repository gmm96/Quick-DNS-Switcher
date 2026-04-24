#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from qds.domain.models.dns.resolved_dns import ResolvedDns
from qds.domain.models.network.network_configuration import NetworkConfiguration
from qds.domain.models.network.network_connection import NetworkConnection
from qds.domain.models.network_state import NetworkState
from qds.infrastructure.backend.network_backend_base import NetworkBackendBase
from qds.infrastructure.dns.dns_reader.system_dns_reader_base import SystemDnsReaderBase


class NetworkStateProvider:
    def __init__(self, backend: NetworkBackendBase, system_dns_reader: SystemDnsReaderBase) -> None:
        self.backend: NetworkBackendBase = backend
        self.system_dns_reader: SystemDnsReaderBase = system_dns_reader

    def retrieve(self) -> Optional[NetworkState]:
        connections: List[NetworkConnection] = self.backend.get_active_connections()
        network_config: NetworkConfiguration = self._get_network_config_from_connections(connections)
        system_dns_config: Optional[ResolvedDns] = self.system_dns_reader.read(network_config.ipv4_enabled, network_config.ipv6_enabled)
        if not system_dns_config:
            return None
        return NetworkState(network_config, system_dns_config)

    @staticmethod
    def _get_network_config_from_connections(connections: List[NetworkConnection]) -> NetworkConfiguration:
        ipv4_enabled: bool = any(conn.ipv4_enabled for conn in connections)
        ipv6_enabled: bool = any(conn.ipv6_enabled for conn in connections)
        is_auto: bool = all(not conn.ipv4_ignore_auto_dns and not conn.ipv6_ignore_auto_dns for conn in connections)
        return NetworkConfiguration(
            connections=connections,
            ipv4_enabled=ipv4_enabled,
            ipv6_enabled=ipv6_enabled,
            is_auto=is_auto
        )
