#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List, Optional
from qds.domain.models.dns.resolved_dns import ResolvedDns
from qds.infrastructure.dns.dns_reader.system_dns_reader_base import SystemDnsReaderBase
from qds.infrastructure.system.file_system_helper import FileSystemHelper


class LinuxDnsReader(SystemDnsReaderBase):
    PATH: str = "/etc/resolv.conf"
    GLIBC_MAX_LIMIT: int = 3
    GLIBC_LIMIT_PER_INTERFACE: int = 2

    def __init__(self, path: str = PATH):
        self.path: str = path

    def read(self, ipv4_enabled: bool = True, ipv6_enabled: bool = True) -> Optional[ResolvedDns]:
        top: List[str] = []
        fallback: List[str] = []
        if ipv4_enabled and ipv6_enabled:
            dynamic_limit: int = LinuxDnsReader.GLIBC_MAX_LIMIT
        elif ipv4_enabled or ipv6_enabled:
            dynamic_limit: int = LinuxDnsReader.GLIBC_LIMIT_PER_INTERFACE
        else:
            return None
        path: str = FileSystemHelper.resolve_file(self.path)
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line.startswith('nameserver'):
                        continue
                    try:
                        ip: str = line.split()[1].split('%')[0]
                    except IndexError:
                        continue
                    top.append(ip) if len(top) < dynamic_limit else fallback.append(ip)
        except IOError as e:
            logging.error(f"Error while reading DNS from {self.path}: {e}", stack_info=True)
        return ResolvedDns(top, fallback)
