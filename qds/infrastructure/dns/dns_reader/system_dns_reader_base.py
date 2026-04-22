#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional
from qds.domain.models.dns.resolved_dns import ResolvedDns


class SystemDnsReaderBase(ABC):
    @abstractmethod
    def read(self, ipv4_enabled: bool = True, ipv6_enabled: bool = True) -> Optional[ResolvedDns]:
        pass
