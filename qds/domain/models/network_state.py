#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from qds.domain.models.network.network_configuration import NetworkConfiguration
from qds.domain.models.dns.resolved_dns import ResolvedDns


class NetworkState:
    def __init__(self, network_configuration: NetworkConfiguration, resolved_dns: ResolvedDns) -> None:
        self.network_configuration: NetworkConfiguration = network_configuration
        self.resolved_dns: ResolvedDns = resolved_dns

    def matches_state(self, other: Optional[NetworkState]) -> bool:
        if not isinstance(other, NetworkState): return False
        return (
                self.network_configuration.identity() == other.network_configuration.identity() and
                self.resolved_dns.identity() == other.resolved_dns.identity()
        )

    @property
    def all_ips(self) -> List[str]:
        return self.resolved_dns.all_ips if self.resolved_dns else []
