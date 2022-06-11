#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

import tornado.testing
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from healthcheck import TornadoHandler, HealthCheck, EnvironmentDump


class BasicHealthCheckTest(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application()

    def setUp(self):
        super(BasicHealthCheckTest, self).setUp()
        self.path = '/h'
        self.hc = self._hc()
        self._set_handler()

    def _hc(self):
        return HealthCheck()

    def _set_handler(self):

        handler_args = dict(checker=self.hc)
        self._app.add_handlers(
            r'.*',
            [
                (
                    self.path,
                    TornadoHandler, handler_args
                ),
            ]
        )

    def test_basic_check(self):

        response = self.fetch(self.path)
        self.assertEqual(response.code, 200)

    def test_failing_check(self):
        def fail_check():
            return False, 'FAIL'

        self.hc.add_check(fail_check)
        response = self.fetch(self.path)
        self.assertEqual(response.code, 500)

        jr = json.loads(response.body.decode('ascii'))
        self.assertEqual('failure', jr['status'])


class BasicEnvironmentDumpTest(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application()

    def setUp(self):
        super(BasicEnvironmentDumpTest, self).setUp()
        self.path = '/e'
        self.hc = self._hc()

    def _hc(self):
        return EnvironmentDump()

    def _set_handler(self):

        handler_args = dict(checker=self.hc)
        self._app.add_handlers(
            r'.*',
            [
                (
                    self.path,
                    TornadoHandler, handler_args
                ),
            ]
        )

    def test_basic_check(self):
        def test_ok():
            return 'OK'

        self.hc.add_section('test_func', test_ok)
        self._set_handler()

        response = self.fetch(self.path)
        self.assertEqual(response.code, 200)
        jr = json.loads(response.body.decode('ascii'))
        self.assertEqual('OK', jr['test_func'])


if __name__ == '__main__':
    unittest.main()
