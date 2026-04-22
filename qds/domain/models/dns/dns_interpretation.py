#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional
from qds.domain.enums.dns_mode import DnsMode
from qds.domain.models.dns.dns_provider import DnsProvider
from qds.domain.models.network_state import NetworkState


@dataclass(frozen=True)
class DnsInterpretation:
    dns_mode: DnsMode
    network_state: NetworkState
    provider: Optional[DnsProvider] = None
