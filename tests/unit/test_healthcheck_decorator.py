import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from healthcheck.healthcheck import Checker, checker, HealthCheckMonitor


class HealthCheckCheckerDecoratorTest(unittest.TestCase):

    def setUp(self):
        HealthCheckMonitor.unregister_all()

    @patch.object(Checker, 'decorate')
    def test_should_decorate_without_args(self, checker_mock):
        def foo():
            pass
        checker(foo)
        checker_mock.assert_called_once_with(foo)

    @patch.object(Checker, '__init__')
    def test_should_decorate_with_args(self, checker_mock):
        checker_mock.return_value = None
        checker(name='foobar')
        checker_mock.assert_called_once_with(name='foobar')


if __name__ == '__main__':
    unittest.main()
