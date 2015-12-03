from __future__ import with_statement

import unittest
import flask
from healthcheck import HealthCheck, EnvironmentDump


class BasicHealthCheckTest(unittest.TestCase):

    def setUp(self):
        self.path = '/h'
        self.app = flask.Flask(__name__)
        self.hc = self._hc()
        self.client = self.app.test_client()

    def _hc(self):
        return HealthCheck(self.app, self.path)

    def test_basic_check(self):
        response = self.client.get(self.path)
        self.assertEqual(200, response.status_code)

    def test_failing_check(self):
        def fail_check():
            return False, "FAIL"

        self.hc.add_check(fail_check)
        response = self.client.get(self.path)
        self.assertEqual(500, response.status_code)


class BasicEnvironmentDumpTest(unittest.TestCase):

    def setUp(self):
        self.path = '/e'
        self.app = flask.Flask(__name__)
        self.hc = self._hc()
        self.client = self.app.test_client()

    def _hc(self):
        return EnvironmentDump(self.app, self.path)

    def test_basic_check(self):
        def test_ok():
            return "OK"

        self.hc.add_section("test_func", test_ok)

        response = self.client.get(self.path)
        self.assertEqual(200, response.status_code)
        jr = flask.json.loads(response.data)
        self.assertEqual("OK", jr["test_func"])


class LazyHealthCheckTest(BasicHealthCheckTest):

    def setUp(self):
        super(LazyHealthCheckTest, self).setUp()
        self.hc.init_app(self.app, self.path)

    def _hc(self):
        return HealthCheck()


class LazyEnvironmentDumpTest(unittest.TestCase):

    def setUp(self):
        super(LazyEnvironmentDumpTest, self).setUp()
        self.hc.init_app(self.app, self.path)

    def _hc(self):
        return EnvironmentDump()

if __name__ == '__main__':
    unittest.main()
