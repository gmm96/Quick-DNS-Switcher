#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from src.domain.enums.network_device_type import NetworkDeviceType
from src.domain.models.network.ip_pair import IpPair


class NetworkConnection:
    def __init__(self,
        name: str,
        device: str,
        device_type: NetworkDeviceType,
        ipv4: IpPair,
        ipv6: IpPair,
        ipv4_ignore_auto_dns: bool = False,
        ipv6_ignore_auto_dns: bool = False,
        ipv4_enabled: bool = True,
        ipv6_enabled: bool = True
    ) -> None:
        self.name: str = name
        self.device: str = device
        self.type: NetworkDeviceType = device_type
        self.ipv4: IpPair = ipv4
        self.ipv6: IpPair = ipv6
        self.ipv4_ignore_auto_dns: bool = ipv4_ignore_auto_dns
        self.ipv6_ignore_auto_dns: bool = ipv6_ignore_auto_dns
        self.ipv4_enabled: bool = ipv4_enabled
        self.ipv6_enabled: bool = ipv6_enabled

    def identity(self) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], bool, bool, bool, bool]:
        return (
            self.ipv4.main,
            self.ipv4.alternative,
            self.ipv6.main,
            self.ipv6.alternative,
            self.ipv4_ignore_auto_dns,
            self.ipv6_ignore_auto_dns,
            self.ipv4_enabled,
            self.ipv6_enabled
        )

    def __eq__(self, other: Optional[object]) -> bool:
        if not isinstance(other, NetworkConnection): return False
        return self.ipv4 == other.ipv4 and \
            self.ipv6 == other.ipv6 and \
            self.ipv4_ignore_auto_dns == other.ipv4_ignore_auto_dns and \
            self.ipv6_ignore_auto_dns == other.ipv6_ignore_auto_dns
