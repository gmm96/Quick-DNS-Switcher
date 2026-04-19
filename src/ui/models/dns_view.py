#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional
from src.domain.enums.dns_mode import DnsMode
from src.domain.models.network_state import NetworkState
from src.domain.models.dns.dns_interpretation import DnsInterpretation
from src.ui.ui_constants import UiConstants


@dataclass(frozen=True)
class DnsView:
    display_name: str
    icon_key: Optional[str]
    body: List[str]
    network_state: NetworkState
    mode: DnsMode

    @staticmethod
    def from_dns_interpretation(dns_interpretation: DnsInterpretation) -> DnsView:
        if dns_interpretation.dns_mode == DnsMode.DISCONNECTED:
            display_name: str = UiConstants.DISCONNECTED_NAME
            icon_key: Optional[str] = UiConstants.DISCONNECTED_ICON
        elif dns_interpretation.dns_mode == DnsMode.AUTO:
            display_name: str = UiConstants.AUTO_NAME
            icon_key: Optional[str] = UiConstants.AUTO_ICON
        elif dns_interpretation.provider:
            display_name: str = dns_interpretation.provider.name
            icon_key: Optional[str] = dns_interpretation.provider.icon_name
        else:
            display_name: str = UiConstants.UNKNOWN_NAME
            icon_key: str = UiConstants.UNKNOWN_ICON
        body: List[str] = dns_interpretation.network_state.all_ips if dns_interpretation.network_state.all_ips else [UiConstants.DEFAULT_BODY]
        return DnsView(
            display_name=display_name,
            icon_key=icon_key,
            body=body,
            network_state=dns_interpretation.network_state,
            mode=dns_interpretation.dns_mode
        )
