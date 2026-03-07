# !/usr/bin/python3
# -*- coding: utf-8 -*-

import ipaddress
from typing import Optional


class IpPair:
    def __init__(self, version: int = 4, main: Optional[str] = None, alternative: Optional[str] = None) -> None:
        self._validate_version(version)
        self.version = version
        self._validate_ip(main)
        self._validate_ip(alternative)
        self.main = main
        self.alternative = alternative

    def _validate_version(self, version: int) -> None:
        if version not in (4, 6):
            raise ValueError("Ip version should be 4 or 6.")

    def _validate_ip(self, ip: Optional[str]) -> None:
        if not ip:
            return
        ip_address = ipaddress.ip_address(ip)
        if ip_address.version != self.version:
            raise ValueError
