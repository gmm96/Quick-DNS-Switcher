# !/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Optional, Dict
from ip_pair import IpPair


class DnsProvider:
    def __init__(self, name: str, ipv4: Optional[IpPair], ipv6: Optional[IpPair], icon: Optional[str]) -> None:
        self.name = name
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.icon = icon

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> DnsProvider:
        return cls(
            name=name,
            ipv4=IpPair(4, data.get("ipv4_1"), data.get("ipv4_2")),
            ipv6=IpPair(6, data.get("ipv6_1"), data.get("ipv6_2")),
            icon=data.get("icon")
        )
