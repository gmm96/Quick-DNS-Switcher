#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, auto
from typing import List, Optional, Set, Literal
from src.network.dns_provider import DnsProvider
from src.network.network_connection import NetworkConnection


class DnsState():
    def __init__(self, connections: List[NetworkConnection]) -> None:
        self.connections: List[NetworkConnection] = connections

    def matches_provider(self, provider: DnsProvider) -> bool:
        return all(
            conn.ipv4 == provider.ipv4 and \
            conn.ipv6 == provider.ipv6 and \
            conn.ipv4_ignore_auto_dns and \
            conn.ipv6_ignore_auto_dns \
            for conn in self.connections
        )

    def matches_state(self, other: Optional[DnsState]) -> bool:
        if not isinstance(other, DnsState): return False
        self_set = {conn.get_dns_identity() for conn in self.connections}
        other_set = {conn.get_dns_identity() for conn in other.connections}
        return self_set == other_set

    def is_auto(self) -> bool:
        return all(not conn.ipv4_ignore_auto_dns and not conn.ipv6_ignore_auto_dns for conn in self.connections)

    @property
    def all_ips(self) -> List[str]:
        ips: Set = set()
        for conn in self.connections:
            ips.update(conn.ipv4.get_ip_list())
            ips.update(conn.ipv6.get_ip_list())
        return list(ips)
