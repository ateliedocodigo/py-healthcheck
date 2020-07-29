#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import unittest

from healthcheck import EnvironmentDump

try:
    from collections.abc import Mapping  # only works on python 3.3+
except ImportError:
    from collections import Mapping


class BasicEnvironmentDumpTest(unittest.TestCase):

    def test_basic_check(self):
        def custom_section():
            return "My custom section"

        ed = EnvironmentDump()

        ed.add_section("custom_section", custom_section)

        message, status, headers = ed.run()

        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])

    def test_custom_section_signature(self):
        def custom_section():
            return "My custom section"

        ed = EnvironmentDump(custom_section=custom_section)

        message, status, headers = ed.run()

        jr = json.loads(message)
        self.assertEqual("My custom section", jr["custom_section"])


class TestEnvironmentDumpSafeDump(unittest.TestCase):

    def test_should_return_safe_environment_vars(self):
        os.environ['SOME_KEY'] = 'fake-key'

        ed = EnvironmentDump()
        message, status, headers = ed.run()

        jr = json.loads(message)
        self.assertIsInstance(jr["process"]["environ"], Mapping)
        self.assertEqual("********", jr["process"]["environ"]["SOME_KEY"])


if __name__ == '__main__':
    unittest.main()
