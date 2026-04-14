#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional
from src.domain.enums.dns_mode import DnsMode
from src.domain.models.dns.dns_provider import DnsProvider
from src.domain.models.network_state import NetworkState


@dataclass(frozen=True)
class DnsInterpretation:
    network_state: NetworkState
    dns_mode: DnsMode
    provider: Optional[DnsProvider] = None
