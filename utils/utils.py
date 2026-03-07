# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from typing import List


def display_error_dialog(content) -> None:
    QMessageBox.critical(None, "ERROR - Quick DNS switcher", content)


def execute_command(args: List[str], output: bool = True, raise_error: bool = True) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, capture_output=output, text=True, check=raise_error)
    except subprocess.CalledProcessError as e:
        display_error_dialog(f"Error executing command:\n\n{' '.join(args)}\n\n{e}")
        sys.exit(1)


def ensure_single_instance() -> QLocalServer:
    socket = QLocalSocket()
    socket.connectToServer(APP_ID)
    if socket.waitForConnected(500):
        socket.close()
        pid_file = "/tmp/kde_quick_dns_switcher.pid"
        if os.path.exists(pid_file):
            try:
                with open(pid_file, "r") as f:
                    old_pid = int(f.read().strip())
                os.kill(old_pid, signal.SIGTERM)
            except Exception:
                pass
    server = QLocalServer()
    try:
        server.removeServer(APP_ID)
    except Exception:
        pass
    server.listen(APP_ID)
    with open("/tmp/kde_quick_dns_switcher.pid", "w") as f:
        f.write(str(os.getpid()))
    return server
