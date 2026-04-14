#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path


class Paths:
    SRC_DIR: Path = Path(__file__).resolve().parent.parent
    RESOURCES_DIR: Path = SRC_DIR / "resources"
    ICONS_DIR: Path = RESOURCES_DIR / "assets" / "icons"
    DNS_PROVIDERS_FILE: Path = RESOURCES_DIR / "config" / "dns_providers.json"
