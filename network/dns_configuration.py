#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import sys
from typing import List, Optional
from network.dns_provider import DnsProvider
from utils.tools import display_error_dialog


class DnsConfiguration:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.providers: List[DnsProvider]= []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.file_path):
            display_error_dialog(f"DNS configuration file not found:\n\n{self.file_path}")
            sys.exit(1)
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            display_error_dialog(f"Invalid JSON format in DNS configuration file:\n\n{self.file_path}\n\n{e}")
            sys.exit(1)
        except Exception as e:
            display_error_dialog(f"Unexpected error loading DNS configuration file:\n\n{self.file_path}\n\n{e}")
            sys.exit(1)
        self.providers = [DnsProvider.from_dict(name, details) for name, details in data.items()]

    def get_all(self) -> List[DnsProvider]:
        return self.providers

    def get_by_name(self, name: str) -> Optional[DnsProvider]:
        return next((dns for dns in self.providers if dns.name == name), None)
