#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web


class TornadoHandler(tornado.web.RequestHandler):

    def initialize(self, checker, **options):
        self.checker = checker

    def get(self):
        message, status_code, headers = self.checker.run()
        self.set_status(status_code)
        self.write(message)
