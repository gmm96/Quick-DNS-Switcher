#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABC
from src.network.dns_state import DnsState
from src.network.ip_pair import IpPair


class NetworkBackendBase(ABC):
    @abstractmethod
    def get_dns_state(self) -> DnsState:
        pass

    @abstractmethod
    def set_dns(self, ipv4: IpPair, ipv6: IpPair) -> None:
        pass
