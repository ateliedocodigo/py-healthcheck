import json
import socket
import sys
import traceback

from flask import request


def basic_exception_handler(checker, e):
    return False, str(e)


def json_success_handler(results):
    data = {
        'hostname': socket.gethostname(),
        'status': 'success',
        'results': results,
    }

    return json.dumps(data)


def json_failed_handler(results):
    data = {
        'hostname': socket.gethostname(),
        'status': 'failure',
        'results': results,
    }

    return json.dumps(data)


class HealthCheck(object):
    def __init__(self, app=None, path=None, success_status=200,
                 success_headers=None, success_handler=json_success_handler,
                 failed_status=500, failed_headers=None,
                 failed_handler=json_failed_handler,
                 exception_handler=basic_exception_handler, checkers=None,
                 **options):

        self.app = app
        self.path = path

        self.success_status = success_status
        # XXX this default should be somewhere else, maybe returned by the handler
        self.success_headers = success_headers or {'Content-Type': 'application/json'}
        self.success_handler = success_handler

        self.failed_status = failed_status
        # XXX this default should be somewhere else, maybe returned by the handler
        self.failed_headers = failed_headers or {'Content-Type': 'application/json'}
        self.failed_handler = failed_handler

        self.exception_handler = exception_handler

        self.options = options
        self.checkers = checkers or []

        if self.app and self.path:
            app.add_url_rule(self.path, view_func=self.check, **options)

    def add_check(self, func):
        self.checkers.append(func)

    def check(self):
        skip_checks = request.args.get('simple', 'false') == 'true'
    
        results = []
        current_checker = None
        for checker in self.checkers:
            current_checker = checker
            if skip_checks:
                result = {
                    'checker': checker.func_name,
                    'skipped': True
                }
            else:
                try:
                    passed, output = checker()
                except:
                    traceback.print_exc()
                    e = sys.exc_info()[0]
                    self.app.logger.exception(e)
                    passed, output = self.exception_handler(current_checker, e)

                if not passed:
                    msg = 'Health check "{}" failed with output "{}"'.format(checker.func_name, output)
                    self.app.logger.error(msg)

                result = {
                    'checker': checker.func_name,
                    'output': output,
                    'passed': passed
                }
                
            results.append(result)

        fn = lambda result, passed: passed and (result.get('passed') or result.get('skipped'))
        passed = reduce(fn, results)

        if passed:
            message = "OK"
            if self.success_handler:
                message = self.success_handler(results)

            return message, self.success_status, self.success_headers
        else:
            message = "NOT OK"
            if self.failed_handler:
                message = self.failed_handler(results)

            return message, self.failed_status, self.failed_headers
