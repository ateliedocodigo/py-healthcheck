#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import flask

from healthcheck import HealthCheck, EnvironmentDump


class BasicHealthCheckTest(unittest.TestCase):

    def setUp(self):
        self.path = '/h'
        self.app = flask.Flask(__name__)
        self.hc = self._hc()
        self.client = self.app.test_client()

        self.app.add_url_rule(self.path, view_func=lambda: self.hc.run())

    def _hc(self):
        return HealthCheck()

    def test_basic_check(self):
        response = self.client.get(self.path)
        self.assertEqual(200, response.status_code)

    def test_failing_check(self):
        def fail_check():
            return False, "FAIL"

        self.hc.add_check(fail_check)
        response = self.client.get(self.path)
        self.assertEqual(500, response.status_code)

        jr = flask.json.loads(response.data)
        self.assertEqual("failure", jr["status"])


class BasicEnvironmentDumpTest(unittest.TestCase):

    def setUp(self):
        self.path = '/e'
        self.app = flask.Flask(__name__)
        self.hc = self._hc()
        self.client = self.app.test_client()

        self.app.add_url_rule(self.path, view_func=lambda: self.hc.run())

    def _hc(self):
        return EnvironmentDump()

    def test_basic_check(self):
        def test_ok():
            return "OK"

        self.hc.add_section("test_func", test_ok)
        self.hc.add_section("config", self.app.config)

        response = self.client.get(self.path)
        self.assertEqual(200, response.status_code)
        jr = flask.json.loads(response.data)
        self.assertEqual("OK", jr["test_func"])


if __name__ == '__main__':
    unittest.main()
