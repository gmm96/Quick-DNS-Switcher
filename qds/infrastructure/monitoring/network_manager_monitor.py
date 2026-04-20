#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Optional
from PyQt6.QtCore import QObject, QFileSystemWatcher
from qds.infrastructure.errors.infrastructure_error import InfrastructureError
from qds.infrastructure.monitoring.network_monitor_base import NetworkMonitorBase
from qds.infrastructure.system.file_system_helper import FileSystemHelper


class NetworkManagerMonitor(QObject, NetworkMonitorBase):
    FILE_PATH: str = "/etc/resolv.conf"

    def __init__(self, file_path: Optional[str] = FILE_PATH) -> None:
        QObject.__init__(self)
        NetworkMonitorBase.__init__(self)
        self.file_path: str = FileSystemHelper.resolve_file(file_path if file_path else NetworkManagerMonitor.FILE_PATH)
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

    def on_change(self, file_path: str) -> None:
        #self._setup_watch()
        self._emit()
