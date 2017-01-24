#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from functools import reduce
except Exception:
    pass

try:
    from .tornado_handler import TornadoHandler
except ImportError:
    pass

from .environmentdump import EnvironmentDump
from .healthcheck import HealthCheck
