#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from src.network.backend.backend_factory import BackendFactory
from src.network.backend.network_backend_base import NetworkBackendBase
from src.utils.tools import display_error_dialog
from src.quick_dns_switcher import QuickDnsSwitcher

try:
    backend: NetworkBackendBase = BackendFactory.create()
    switcher: QuickDnsSwitcher = QuickDnsSwitcher(backend)
    switcher.run()
except Exception as e:
    logging.exception(e)
    display_error_dialog(str(e))
