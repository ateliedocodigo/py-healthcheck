#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from healthcheck import HealthCheck


class BasicHealthCheckTest(unittest.TestCase):

    @staticmethod
    def check_adition_works():
        """Check that always return true."""
        if 1 + 1 == 2:
            return True, "addition works"
        else:
            return False, "the universe is broken"

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
        self.assertEqual("failure", jr["status"])

    def test_success_check(self):
        hc = HealthCheck(checkers=[self.check_adition_works])
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual("success", jr["status"])

    def test_custom_section_success_check(self):
        def custom_section():
            return "My custom section"
        hc = HealthCheck(checkers=[self.check_adition_works])
        hc.add_section("custom_section", custom_section)
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])

    def test_custom_section_signature_success_check(self):
        def custom_section():
            return "My custom section"
        hc = HealthCheck(checkers=[self.check_adition_works], custom_section=custom_section)
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])

    def test_custom_section_prevent_duplication(self):
        def broke_section():
            raise Exception("My broke section")
        hc = HealthCheck(checkers=[self.check_adition_works], custom_section=broke_section)
        message, status, headers = hc.run()
        self.assertEqual(200, status)
        jr = json.loads(message)
        self.assertNotIn("custom_section", jr)

    def test_custom_section_failing_check(self):
        def custom_section():
            return "My custom section"
        hc = HealthCheck(checkers=[self.check_throws_exception])
        hc.add_section("custom_section", custom_section)
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])

    def test_custom_section_signature_failure_check(self):
        def custom_section():
            return "My custom section"
        hc = HealthCheck(checkers=[self.check_throws_exception], custom_section=custom_section)
        message, status, headers = hc.run()
        self.assertEqual(500, status)
        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])

if __name__ == '__main__':
    unittest.main()
