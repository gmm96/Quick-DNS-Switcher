#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path


class AppSettings:
    PROD_ENV: str = "prod"
    DEV_ENV: str = "dev"

    def __init__(self) -> None:
        self.env: str = os.getenv("QDS_ENV", AppSettings.PROD_ENV)
        self.is_dev: bool = self.env == AppSettings.DEV_ENV
        self.app_name: str = "quick-dns-switcher"
        self.config_filename: str = "dns_providers.json"
        self.user_config_dir: Path = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / self.app_name
        self.system_config_dir: Path = Path("/usr/share") / self.app_name

    @property
    def dns_providers_file(self) -> Path:
        file_path: Path = self.user_config_dir / self.config_filename
        if self.is_dev:
            file_path: Path = Path(__file__).resolve().parent.parent / "resources" / "config" / self.config_filename
        return file_path.resolve()
