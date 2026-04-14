#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Optional
from PyQt6.QtCore import QFileSystemWatcher, QObject
from src.infrastructure.errors.infrastructure_error import InfrastructureError
from src.infrastructure.system.file_system_helper import FileSystemHelper
from src.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase


class NetworkManagerMonitor(QObject, NetworkMonitorBase):
    PATH: str = "/etc/resolv.conf"

    def __init__(self, path: Optional[str] = PATH) -> None:
        QObject.__init__(self)
        NetworkMonitorBase.__init__(self)
        self.file_path: str = FileSystemHelper.resolve_file(path if path else NetworkManagerMonitor.PATH)
        self.dir_path: str = os.path.dirname(self.file_path)
        self.watcher: QFileSystemWatcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self.on_change)
        self.watcher.directoryChanged.connect(self.on_change)
        self._setup_watch()

    def _setup_watch(self) -> None:
        new_file: str = FileSystemHelper.resolve_file(self.file_path)
        new_dir: str = os.path.dirname(self.file_path)
        if new_file == self.file_path and new_dir == self.dir_path:
            return
        self.file_path = new_file
        self.dir_path = new_dir
        self.watcher.removePaths(self.watcher.files())
        self.watcher.removePaths(self.watcher.directories())
        if not os.path.exists(self.file_path):
            raise InfrastructureError("DNS file resolv.conf could not be found in system.")
        self.watcher.addPath(self.file_path)
        if not os.path.exists(self.dir_path):
            raise InfrastructureError("Directory of DNS file resolv.conf could not be found in system.")
        self.watcher.addPath(self.dir_path)

    def on_change(self, path: str) -> None:
        #self._setup_watch()
        self._emit()
