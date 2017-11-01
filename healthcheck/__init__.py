#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from functools import reduce  # noqa
except Exception:
    pass

try:
    from .tornado_handler import TornadoHandler  # noqa
except ImportError:
    pass

from .environmentdump import EnvironmentDump  # noqa
from .healthcheck import HealthCheck  # noqa
