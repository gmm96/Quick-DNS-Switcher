#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from typing import Optional, List


class IpPair:
    def __init__(self, version: int = 4, main: Optional[str] = None, alternative: Optional[str] = None) -> None:
        self._validate_version(version)
        self.version: int = version
        self._validate_ip(main)
        self._validate_ip(alternative)
        self.main: Optional[str] = main
        self.alternative: Optional[str] = alternative
    
    @classmethod
    def from_list(cls, version: int, ip_list: List[str]) -> IpPair:
        main = ip_list[0] if len(ip_list) > 0 else None
        alt = ip_list[1] if len(ip_list) > 1 else None
        return cls(version, main, alt)

    def _validate_version(self, version: int) -> None:
        if version not in (4, 6):
            raise ValueError("Ip version should be 4 or 6.")

    def _validate_ip(self, ip: Optional[str]) -> None:
        if not ip:
            return
        ip_address = ipaddress.ip_address(ip)
        if ip_address.version != self.version:
            raise ValueError(f"IP address {ip} does not match version {self.version}")

    def get_ip_list(self) -> List[str]:
        return [ip for ip in (self.main, self.alternative) if ip]

    def __eq__(self, other: Optional[object]):
        if not other: return False
        if not isinstance(other, IpPair): return False
        if self is other: return True
        return self.version == other.version and \
                self.main == other.main and \
                self.alternative == other.alternative
