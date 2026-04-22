#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, Set, List
from qds.domain.models.dns.dns_interpretation import DnsInterpretation
from qds.domain.enums.dns_mode import DnsMode
from qds.domain.models.dns.dns_provider import DnsProvider
from qds.domain.models.network_state import NetworkState


class DnsInterpreter:
    def __init__(self, providers: List[DnsProvider]) -> None:
        self.providers: List[DnsProvider] = providers

    def resolve(self, network_state: NetworkState) -> DnsInterpretation:
        if not network_state.network_configuration.connections:
            return DnsInterpretation(DnsMode.DISCONNECTED, network_state, None)
        if network_state.network_configuration.is_auto:
            return DnsInterpretation(DnsMode.AUTO, network_state, None)
        provider: Optional[DnsProvider] = self._find_provider(network_state)
        if provider:
            return DnsInterpretation(DnsMode.PROVIDER, network_state, provider)
        return DnsInterpretation(DnsMode.UNKNOWN, network_state, None)

    def _find_provider(self, network_state: NetworkState) -> Optional[DnsProvider]:
        if not network_state.resolved_dns.top:
            return None
        system_top: Set[str] = set(network_state.resolved_dns.top)
        system_all: Set[str] = network_state.resolved_dns.identity()
        for provider in self.providers:
            provider_ips: Set[str] = set()
            if network_state.network_configuration.ipv4_enabled:
                provider_ips |= set(provider.ipv4.get_ip_list())
            if network_state.network_configuration.ipv6_enabled:
                provider_ips |= set(provider.ipv6.get_ip_list())
            if not provider_ips:
                continue
            if not provider_ips.issubset(system_all):
                continue
            top_matches: Set[str] = system_top.intersection(provider_ips)
            if len(top_matches) >= min(len(system_top), len(provider_ips)):
                return provider
        return None
