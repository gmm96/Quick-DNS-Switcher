#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class FileSystemHelper:
    @staticmethod
    def resolve_file(path: str) -> str:
        try:
            if os.path.islink(path):
                real_path: str = os.path.realpath(path)
                if os.path.exists(real_path):
                    return real_path
        except (OSError, PermissionError):
            pass
        return path
