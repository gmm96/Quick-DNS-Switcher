#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from PyQt6.QtGui import QIcon


@dataclass(frozen=True)
class AppIcon:
    name: str
    qicon: QIcon
