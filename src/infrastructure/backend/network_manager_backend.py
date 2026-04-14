#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from subprocess import CompletedProcess
from typing import List, Optional
from src.domain.enums.network_device_type import NetworkDeviceType
from src.infrastructure.backend.network_backend_base import NetworkBackendBase
from src.domain.models.network.ip_pair import IpPair
from src.domain.models.network.network_connection import NetworkConnection
from src.infrastructure.system.command_executor import CommandExecutor


class NetworkManagerBackend(NetworkBackendBase):
    IGNORE_AUTO_DNS_TRUE: str = "yes"
    IGNORE_AUTO_DNS_FALSE: str = "no"
    PROTOCOL_METHOD_DISABLED: str = "disabled"

    def __init__(self) -> None:
        self.connections: List[NetworkConnection] = []

    def get_active_connections(self) -> List[NetworkConnection]:
        self.connections: List[NetworkConnection] = []
        self._retrieve_active_connections_info()
        self._fill_auto_ignore_dns_field()
        return self.connections

    def _retrieve_active_connections_info(self) -> None:
        name: Optional[str] = None
        device: Optional[str] = None
        device_type: Optional[str] = None
        ipv4_list: List[str] = []
        ipv6_list: List[str] = []
        connected: bool = False
        result: CompletedProcess = CommandExecutor.execute(
            [
                "nmcli",
                "-t", "-f",
                "GENERAL.CONNECTION,GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE,IP4.DNS,IP6.DNS",
                "device", "show"
            ],
            check=True
        )
        for line in [l.strip() for l in result.stdout.splitlines()]:
            if not line: continue
            if ":" not in line: continue
            key: str
            value: str
            key, value = [l.strip() for l in line.split(":", 1)]
            if key == "GENERAL.CONNECTION":
                self._add_network_connection(name, device, device_type, connected, ipv4_list, ipv6_list)
                name: Optional[str] = value
                device: Optional[str] = None
                device_type: Optional[str] = None
                connected: bool = False
                ipv4_list: List[str] = []
                ipv6_list: List[str] = []
            elif key == "GENERAL.DEVICE":
                device: Optional[str] = value
            elif key == "GENERAL.TYPE":
                device_type: Optional[str] = value
            elif key == "GENERAL.STATE":
                connected: bool = value.startswith("100")
            elif key.startswith("IP4.DNS"):
                if value:
                    ipv4_list.append(value)
            elif key.startswith("IP6.DNS"):
                if value:
                    ipv6_list.append(value)
        self._add_network_connection(name, device, device_type, connected, ipv4_list, ipv6_list)

    def _add_network_connection(self,
        name: str,
        device: str,
        type_str: str,
        connected: bool,
        ipv4_list: List[str],
        ipv6_list: List[str]
    ) -> None:
        if not all([name, device, connected]):
            return
        try:
            device_type: NetworkDeviceType = NetworkDeviceType[type_str.upper()]
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
            result: CompletedProcess = CommandExecutor.execute(
                ["nmcli", "-g", "ipv4.ignore-auto-dns,ipv6.ignore-auto-dns,ipv4.method,ipv6.method", "connection", "show", conn.name],
                check=True
            )
            ipv4_ignore_auto_dns, ipv6_ignore_auto_dns, ipv4_method, ipv6_method = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            conn.ipv4_ignore_auto_dns = ipv4_ignore_auto_dns == NetworkManagerBackend.IGNORE_AUTO_DNS_TRUE
            conn.ipv6_ignore_auto_dns = ipv6_ignore_auto_dns == NetworkManagerBackend.IGNORE_AUTO_DNS_TRUE
            conn.ipv4_enabled = ipv4_method != NetworkManagerBackend.PROTOCOL_METHOD_DISABLED
            conn.ipv6_enabled = ipv6_method != NetworkManagerBackend.PROTOCOL_METHOD_DISABLED

    def set_dns(self, ipv4: IpPair, ipv6: IpPair) -> None:
        v4_ips: List[str] = ipv4.get_ip_list()
        v6_ips: List[str] = ipv6.get_ip_list()
        v4_ignore_auto: str = NetworkManagerBackend.IGNORE_AUTO_DNS_TRUE if v4_ips else NetworkManagerBackend.IGNORE_AUTO_DNS_FALSE
        v6_ignore_auto: str = NetworkManagerBackend.IGNORE_AUTO_DNS_TRUE if v6_ips else NetworkManagerBackend.IGNORE_AUTO_DNS_FALSE
        for conn in self.get_active_connections():
            CommandExecutor.execute(
                [
                    "nmcli",
                    "connection",
                    "modify", conn.name,
                    "ipv4.ignore-auto-dns", v4_ignore_auto,
                    "ipv6.ignore-auto-dns", v6_ignore_auto,
                    "ipv4.dns", ",".join(v4_ips),
                    "ipv6.dns", ",".join(v6_ips),
                    "ipv4.dns-priority", "-1",
                    "ipv6.dns-priority", "-1",
                    "ipv4.dns-search", "~.",
                    "ipv6.dns-search", "~."
                ],
                check=True
            )
            result_reapply: CompletedProcess = CommandExecutor.execute(["nmcli", "device", "reapply", conn.device], check=False)
            if result_reapply.returncode != 0:
                logging.warning("Error resetting infrastructure, trying aggressive method...", stack_info=True)
                CommandExecutor.execute(["nmcli", "connection", "up", conn.name], check=True)
