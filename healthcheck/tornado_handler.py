#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from typing import Any
except ImportError:
    # for python2
    pass

import tornado.web

from healthcheck import HealthCheck


class TornadoHandler(tornado.web.RequestHandler):

    def initialize(self, checker):  # type: (HealthCheck) -> None
        self.checker = checker

    def get(self, *args, **kwargs):  # type: (*Any, **Any) -> None
        message, status_code, headers = self.checker.run(*args, **kwargs)
        self.set_status(status_code)
        for k, v in headers.items():
            self.set_header(k, v)
        self.write(message)
