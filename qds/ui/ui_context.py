#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, Callable, Any

from PyQt6.QtCore import QEventLoop, QTimer

from qds.app.error_handler import ErrorHandler


class UiContext:
    error_handler: Optional[ErrorHandler] = None

    @staticmethod
    def safe_callback(function: Callable[[], Any]) -> Callable[..., None]:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            try:
                function()
            except Exception as e:
                if UiContext.error_handler is None:
                    raise
                UiContext.error_handler.handle(e)
        return wrapper

    @staticmethod
    def qt_sleep(milliseconds: int) -> None:
        loop: QEventLoop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec()
