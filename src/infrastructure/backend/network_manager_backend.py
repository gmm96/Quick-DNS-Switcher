#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List, Optional, Set
from src.domain.models.device_type import DeviceType
from src.infrastructure.backend.network_backend_base import NetworkBackendBase
from src.domain.models.dns_snapshot import DnsSnapshot
from src.domain.models.ip_pair import IpPair
from src.domain.models.network_connection import NetworkConnection
from src.utils.tools import execute_command


class NetworkManagerBackend(NetworkBackendBase):
    def __init__(self) -> None:
        self.connections: List[NetworkConnection] = []

    def get_dns_snapshot(self) -> DnsSnapshot:
        self.connections = []
        self._retrieve_active_connections_info()
        self._fill_auto_ignore_dns_field()
        return DnsSnapshot(self.connections)

    def _retrieve_active_connections_info(self) -> None:
        name: Optional[str] = None
        device: Optional[str] = None
        device_type: Optional[str] = None
        ipv4_list: List[str] = []
        ipv6_list: List[str] = []
        connected: bool = False
        result = execute_command([
            "nmcli", "-t", "-f", "GENERAL.CONNECTION,GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE,IP4.DNS,IP6.DNS", "device", "show"
        ])
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line: continue
            if ":" not in line: continue
            key, value = line.split(":", 1)
            value = value.strip()
            if key == "GENERAL.CONNECTION":
                self._add_network_connection(name, device, device_type, connected, ipv4_list, ipv6_list)
                name = value
                device = None
                device_type = None
                connected = False
                ipv4_list = []
                ipv6_list = []
            elif key == "GENERAL.DEVICE":
                device = value
            elif key == "GENERAL.TYPE":
                device_type = value
            elif key == "GENERAL.STATE":
                connected = value.startswith("100")
            elif key.startswith("IP4.DNS"):
                if value:
                    ipv4_list.append(value)
            elif key.startswith("IP6.DNS"):
                if value:
                    ipv6_list.append(value)
        self._add_network_connection(name, device, device_type, connected, ipv4_list, ipv6_list)

    def _add_network_connection(self, name: str, device: str, type_str: str, connected: bool, ipv4_list: List[str], ipv6_list: List[str]) -> None:
        if not all([name, device, connected]):
            return
        try:
            device_type: DeviceType = DeviceType[type_str.upper()]
            self.connections.append(
                NetworkConnection(
                    name,
                    device,
                    device_type,
                    IpPair.from_list(4, ipv4_list),
                    IpPair.from_list(6, ipv6_list)
                )
            )
        except KeyError:
            pass

    def _fill_auto_ignore_dns_field(self) -> None:
        for conn in self.connections:
            result = execute_command(
                ["nmcli", "-g", "ipv4.ignore-auto-dns,ipv6.ignore-auto-dns", "connection", "show", conn.name]
            )
            ipv4_ignore_auto_dns, ipv6_ignore_auto_dns = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            conn.parse_ignore_auto_dns(ipv4_ignore_auto_dns, ipv6_ignore_auto_dns)

    def set_dns(self, ipv4: IpPair, ipv6: IpPair) -> None:
        v4_ips: List[str] = ipv4.get_ip_list()
        v6_ips: List[str] = ipv6.get_ip_list()
        v4_ignore_auto: str = "yes" if v4_ips else "no"
        v6_ignore_auto: str = "yes" if v6_ips else "no"
        for conn in self.get_dns_snapshot().connections:
            execute_command([
                "nmcli",
                "connection",
                "modify", conn.name,
                "ipv4.ignore-auto-dns", v4_ignore_auto,
                "ipv6.ignore-auto-dns", v6_ignore_auto,
                "ipv4.dns", ",".join(v4_ips),
                "ipv6.dns", ",".join(v6_ips)
            ])
            result_reapply = execute_command(["nmcli", "device", "reapply", conn.device], True, False)
            if result_reapply.returncode != 0:
                logging.warning("Error resetting infrastructure, trying aggressive method...", stack_info=True)
                execute_command(["nmcli", "connection", "up", conn.name], True, True)
