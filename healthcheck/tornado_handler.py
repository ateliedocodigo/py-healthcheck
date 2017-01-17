#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web


class TornadoHandler(tornado.web.RequestHandler):

    def initialize(self, checker):
        self.checker = checker

    def get(self, *args, **kwargs):
        message, status_code, headers = self.checker.run()
        self.set_status(status_code)
        [self.set_header(k, v) for k, v in headers.items()]
        self.write(message)
