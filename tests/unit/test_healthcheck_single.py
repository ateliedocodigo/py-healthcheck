#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from healthcheck import HealthCheck, HealthCheckMonitor


class HealthCheckSingleRunTest(unittest.TestCase):

    def setUp(self):
        HealthCheckMonitor.unregister_all()

    @staticmethod
    def check_that_works():
        """Check that always return true."""
        return True, 'it works'

    @staticmethod
    def check_throws_exception():
        raise Exception('My exception')

    def test_should_run_only_filtered_checks(self):
        check = 'check_that_works'
        hc = HealthCheck(checkers=[self.check_that_works, self.check_throws_exception])

        message, status, headers = hc.run(check)
        self.assertEqual(200, status)

        jr = json.loads(message)
        self.assertEqual('success', jr['status'])
        self.assertEqual(len(jr['results']), 1)


if __name__ == '__main__':
    unittest.main()
