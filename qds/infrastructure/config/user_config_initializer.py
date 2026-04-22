#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from qds.config.app_settings import AppSettings


class UserConfigInitializer:
    def __init__(self, app_settings: AppSettings) -> None:
        self.app_settings: AppSettings = app_settings

    def ensure_dns_providers_file(self) -> None:
        if self.app_settings.is_dev: return
        user_file: Path = self.app_settings.dns_providers_file
        if user_file.exists(): return
        user_file.parent.mkdir(parents=True, exist_ok=True)
        system_file: Path = self.app_settings.system_config_dir / self.app_settings.config_filename
        if system_file.exists():
            shutil.copy2(system_file, user_file)
        else:
            raise Exception(f"System config file {system_file} does not exist")
