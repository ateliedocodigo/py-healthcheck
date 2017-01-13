#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from healthcheck import HealthCheck


class BasicHealthCheckTest(unittest.TestCase):

    def test_basic_check(self):
        def hc():
            return HealthCheck().run()

        message, status, headers = hc()

        self.assertEqual(200, status)

    def test_failing_check(self):

        def throws_exception():
            bad_var = None
            bad_var['explode']

        def hc():
            return HealthCheck(checkers=[throws_exception]).run()

        message, status, headers = hc()

        self.assertEqual(500, status)

        jr = json.loads(message)
        self.assertEqual("failure", jr["status"])

    def test_success_check(self):

        def addition_works():
            if 1 + 1 == 2:
                return True, "addition works"
            else:
                return False, "the universe is broken"

        def hc():
            return HealthCheck(checkers=[addition_works]).run()

        message, status, headers = hc()

        self.assertEqual(200, status)

        jr = json.loads(message)
        self.assertEqual("success", jr["status"])


if __name__ == '__main__':
    unittest.main()
