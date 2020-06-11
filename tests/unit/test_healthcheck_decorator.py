import unittest

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from healthcheck.healthcheck import Checker, HealthCheckMonitor, HealthCheck
from healthcheck.wrappers import checker


class HealthCheckCheckerDecoratorTest(unittest.TestCase):

    def setUp(self):
        HealthCheckMonitor.unregister_all()

    @patch.object(Checker, 'decorate')
    def test_should_decorate_without_args(self, checker_mock):
        def foo():
            pass

        checker(foo)
        checker_mock.assert_called_once_with(foo)

    # @patch.object(Checker, '__init__')
    # def test_should_decorate_with_args(self, checker_mock):
    #     checker_mock.return_value = None
    #     checker(name='foobar')
    #     checker_mock.assert_called_once_with(name='foobar')

    def test_should_call_decorated_function_without_args(self):
        foo = Mock(__name__='bar', return_value=(True, 'It works!'))
        bar = Mock(__name__='bar', return_value=(True, 'It works!'))

        @checker
        def foo_decorated():
            return foo()

        checker(bar)

        message, status, headers = HealthCheck().run()
        self.assertEqual(200, status)

        if hasattr(foo, 'assert_called_once'):
            foo.assert_called_once()
        self.assertEqual(1, foo.call_count)
        if hasattr(bar, 'assert_called_once'):
            bar.assert_called_once()
        self.assertEqual(1, bar.call_count)

    def test_should_call_decorated_function_with_args(self):
        foo = Mock(__name__='bar', return_value=(True, 'It works!'))
        bar = Mock(__name__='bar', return_value=(True, 'It works!'))

        @checker(name='foofoo')
        def foo_decorated():
            return foo()

        checker(name='barbar')(bar)

        message, status, headers = HealthCheck().run()
        self.assertEqual(200, status)

        if hasattr(foo, 'assert_called_once'):
            foo.assert_called_once()
        self.assertEqual(1, foo.call_count)
        if hasattr(bar, 'assert_called_once'):
            bar.assert_called_once()
        self.assertEqual(1, bar.call_count)

    def test_should_call_decorated_method_without_args(self):
        foo = Mock(__name__='bar', return_value=(True, 'It works!'))

        class Foo:
            def __init__(self):
                checker(self.foo_decorated)

            def foo_decorated(self):
                return foo()

        Foo()

        message, status, headers = HealthCheck().run()
        self.assertEqual(200, status)

        if hasattr(foo, 'assert_called_once'):
            foo.assert_called_once()
        self.assertEqual(1, foo.call_count)

    def test_should_call_decorated_method_with_args(self):
        foo = Mock(__name__='bar', return_value=(True, 'It works!'))

        class Foo:
            def __init__(self):
                checker('foo')(self.foo_decorated)

            def foo_decorated(self):
                return foo()

        Foo()

        message, status, headers = HealthCheck().run()
        self.assertEqual(200, status)

        if hasattr(foo, 'assert_called_once'):
            foo.assert_called_once()
        self.assertEqual(1, foo.call_count)


if __name__ == '__main__':
    unittest.main()
