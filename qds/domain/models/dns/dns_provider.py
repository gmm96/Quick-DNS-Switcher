#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, Dict
from qds.domain.models.network.ip_pair import IpPair


class DnsProvider:
    def __init__(self, name: str, ipv4: IpPair, ipv6: IpPair, icon_name: Optional[str] = None) -> None:
        self.name: str = name
        self.ipv4: IpPair = ipv4
        self.ipv6: IpPair = ipv6
        self.icon_name: Optional[str] = icon_name

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> DnsProvider:
        return cls(
            name=name,
            ipv4=IpPair(4, data.get("ipv4_1"), data.get("ipv4_2")),
            ipv6=IpPair(6, data.get("ipv6_1"), data.get("ipv6_2")),
            icon_name=data.get("icon")
        )
