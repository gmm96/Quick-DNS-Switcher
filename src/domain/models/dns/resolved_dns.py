#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Set, List


@dataclass(frozen=True)
class ResolvedDns:
    top: List[str] = field(default_factory=list)
    fallback: List[str] = field(default_factory=list)

    @property
    def all_ips(self) -> List[str]:
        return self.top + self.fallback

    def identity(self) -> Set[str]:
        return set(self.all_ips)
