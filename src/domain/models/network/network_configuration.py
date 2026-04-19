#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
from src.domain.models.network.network_connection import NetworkConnection


@dataclass(frozen=True)
class NetworkConfiguration:
    connections: List[NetworkConnection]
    ipv4_enabled: bool = False
    ipv6_enabled: bool = False
    is_auto: bool = False

    def identity(self) -> Set[Tuple[Optional[str], Optional[str], Optional[str], Optional[str], bool, bool, bool, bool]]:
        return {conn.identity() for conn in self.connections}
