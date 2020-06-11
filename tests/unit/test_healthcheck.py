#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from healthcheck import HealthCheck


class BasicHealthCheckTest(unittest.TestCase):

    def setUp(self):
        HealthCheck.unregister_all()

    @staticmethod
    def check_that_works():
        """Check that always return true."""
        return True, 'it works'

    @staticmethod
    def check_throws_exception():
        bad_var = None
        bad_var['explode']

    def test_basic_check(self):
        message, status, headers = HealthCheck().run()
        self.assertEqual(200, status)

    def test_failing_check(self):
        hc = HealthCheck(checkers=[self.check_throws_exception])
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('failure', jr['status'])

    def test_success_check(self):
        hc = HealthCheck(checkers=[self.check_that_works])
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('success', jr['status'])

    def test_custom_section_function_success_check(self):
        hc = HealthCheck(checkers=[self.check_that_works])
        hc.add_section('custom_section', lambda: 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_signature_function_success_check(self):
        hc = HealthCheck(checkers=[self.check_that_works], custom_section=lambda: 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_value_success_check(self):
        hc = HealthCheck(checkers=[self.check_that_works])
        hc.add_section('custom_section', 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_signature_value_success_check(self):
        hc = HealthCheck(checkers=[self.check_that_works], custom_section='My custom section')
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_function_failing_check(self):
        hc = HealthCheck(checkers=[self.check_throws_exception])
        hc.add_section('custom_section', lambda: 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_signature_function_failure_check(self):
        hc = HealthCheck(checkers=[self.check_throws_exception], custom_section=lambda: 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_value_failing_check(self):
        hc = HealthCheck(checkers=[self.check_throws_exception])
        hc.add_section('custom_section', 'My custom section')
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_signature_value_failing_check(self):
        hc = HealthCheck(checkers=[self.check_throws_exception], custom_section='My custom section')
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('My custom section', jr['custom_section'])

    def test_custom_section_prevent_duplication(self):
        hc = HealthCheck(checkers=[self.check_that_works], custom_section='My custom section')
        self.assertRaises(Exception, 'The name "custom_section" is already taken.',
                          hc.add_section, 'custom_section', 'My custom section')


@unittest.skip
class TimeoutHealthCheckTest(unittest.TestCase):

    def setUp(self):
        HealthCheck.unregister_all()

    def test_default_timeout_should_success_check(self):
        def timeout_check():
            import time
            time.sleep(10)
            return True, 'Waited for 10 seconds'

        hc = HealthCheck(checkers=[timeout_check])
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual('success', jr['status'])

    def test_error_timeout_function_should_failing_check(self):
        def timeout_check():
            import time
            time.sleep(5)
            return True, 'Waited for 10 seconds'

        hc = HealthCheck(checkers=[timeout_check], error_timeout=2)
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual('failure', jr['status'])


if __name__ == '__main__':
    unittest.main()
