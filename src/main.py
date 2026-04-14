#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from src.app.quick_dns_switcher import QuickDnsSwitcher
from src.startup.bootstrap import Bootstrap
from src.ui.qt_error_handler import QtErrorHandler
from src.ui.ui_context import UiContext


if __name__ == "__main__":
    error_handler: QtErrorHandler = QtErrorHandler()
    UiContext.error_handler = error_handler
    try:
        qt_app: QApplication = QApplication(sys.argv)
        app: QuickDnsSwitcher = Bootstrap.create_app(qt_app)
        app.run()
    except Exception as e:
        error_handler.handle(e)
