#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABC
from typing import List
from src.domain.models.network.ip_pair import IpPair
from src.domain.models.network.network_connection import NetworkConnection


class NetworkBackendBase(ABC):
    @abstractmethod
    def get_active_connections(self) -> List[NetworkConnection]:
        pass

    @abstractmethod
    def set_dns(self, ipv4: IpPair, ipv6: IpPair) -> None:
        pass
