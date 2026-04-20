#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qds.startup.platform_factory import PlatformFactory


class WindowsFactory(PlatformFactory):
    def create_backend(self):
        raise Exception

    def create_notifier(self):
        raise Exception

    def create_monitor(self):
        raise Exception

    def create_system_dns_reader(self):
        pass
