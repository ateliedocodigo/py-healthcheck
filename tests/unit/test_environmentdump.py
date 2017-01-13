#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from healthcheck import EnvironmentDump


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


if __name__ == '__main__':
    unittest.main()
