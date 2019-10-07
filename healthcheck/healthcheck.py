#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import socket
import threading

import six
import time

logger = logging.getLogger(__name__)

try:
    from functools import reduce
except Exception:
    pass


def basic_exception_handler(_, e):
    return False, str(e)


def json_success_handler(results, *args, **kw):
    data = {
        'hostname': socket.gethostname(),
        'status': 'success',
        'timestamp': time.time(),
        'results': results,
    }
    [data.update({k: v}) for k, v in kw.items()]
    return json.dumps(data)


def json_failed_handler(results, *args, **kw):
    data = {
        'hostname': socket.gethostname(),
        'status': 'failure',
        'timestamp': time.time(),
        'results': results,
    }
    [data.update({k: v}) for k, v in kw.items()]
    return json.dumps(data)


def check_reduce(passed, result):
    return passed and result.get('passed')


class _ThreadedChecker(threading.Thread):
    def __init__(self,
                 checker,
                 success_ttl,
                 failed_ttl,
                 exception_handler):
        threading.Thread.__init__(self, name='checker-' + checker.__name__)
        self.result = {'checker': checker.__name__,
                       'output': None,
                       'passed': None,
                       'timestamp': None,
                       'expires': None,
                       'response_time': None}
        self.checker = checker
        self.success_ttl = success_ttl
        self.failed_ttl = failed_ttl
        self.exception_handler = exception_handler

    def run(self):
        start_time = time.time()

        try:
            passed, output = self.checker()
        except Exception as e:
            logger.exception(e)
            passed, output = self.exception_handler(self.checker, e)

        end_time = time.time()
        elapsed_time = end_time - start_time
        # Reduce to 6 decimal points to have consistency with timestamp
        elapsed_time = float('{:.6f}'.format(elapsed_time))

        if not passed:
            msg = 'Health check "{}" failed with output "{}"'.format(self.checker.__name__, output)
            logger.error(msg)

        timestamp = time.time()
        if passed:
            expires = timestamp + self.success_ttl
        else:
            expires = timestamp + self.failed_ttl

        self.result['output'] = output
        self.result['passed'] = passed
        self.result['timestamp'] = timestamp
        self.result['expires'] = expires
        self.result['response_time'] = elapsed_time
        return

    def get_result(self):
        return self.result

    def get_timeout_result(self, timeout):
        self.result['passed'] = False
        self.result['output'] = 'Timeout'
        self.result['timestamp'] = time.time()
        self.result['expires'] = time.time() + self.failed_ttl
        self.result['response_time'] = timeout
        return self.get_result()


class HealthCheck(object):
    def __init__(self,
                 success_status=200,
                 success_headers=None,
                 success_handler=json_success_handler,
                 success_ttl=27,
                 failed_status=500,
                 failed_headers=None,
                 failed_handler=json_failed_handler,
                 failed_ttl=9,
                 error_timeout=None,
                 exception_handler=basic_exception_handler,
                 checkers=None,
                 **kwargs):
        self.cache = dict()

        self.success_status = success_status
        self.success_headers = success_headers or {'Content-Type': 'application/json'}
        self.success_handler = success_handler
        self.success_ttl = float(success_ttl or 0)

        self.failed_status = failed_status
        self.failed_headers = failed_headers or {'Content-Type': 'application/json'}
        self.failed_handler = failed_handler
        self.failed_ttl = float(failed_ttl or 0)

        self.error_timeout = error_timeout

        self.exception_handler = exception_handler

        self.checkers = checkers or []

        self.functions = dict()
        # ads custom_sections on signature
        [self.add_section(k, v) for k, v in kwargs.items() if k not in self.functions]

    def add_section(self, name, func):
        if name in self.functions:
            raise Exception('The name "{}" is already taken.'.format(name))
        self.functions[name] = func

    def add_check(self, func):
        self.checkers.append(func)

    def run(self, check=None):
        filtered = [c for c in self.checkers if check is None or c.__name__ == check]
        threads = []
        results = []
        for checker in filtered:
            if checker in self.cache and self.cache[checker].get('expires') >= time.time():
                result = self.cache[checker]
                results.append(result)
            else:
                threaded_checker = _ThreadedChecker(checker,
                                                    self.success_ttl,
                                                    self.failed_ttl,
                                                    self.exception_handler)
                threaded_checker.start()
                threads.append(threaded_checker)

        for thread in threads:
            thread.join(timeout=self.error_timeout
                        if self.error_timeout
                        else None)

        for thread in threads:
            checker_result = thread.get_result()
            if thread.is_alive():       # check failed due call timeout
                checker_result = thread.get_timeout_result(self.error_timeout)
            results.append(checker_result)

        custom_section = dict()
        for (name, func) in six.iteritems(self.functions):
            try:
                custom_section[name] = func() if callable(func) else func
            except Exception:
                pass

        passed = reduce(check_reduce, results, True)

        if passed:
            message = "OK"
            if self.success_handler:
                message = self.success_handler(results, **custom_section)

            return message, self.success_status, self.success_headers
        else:
            message = "NOT OK"
            if self.failed_handler:
                message = self.failed_handler(results, **custom_section)

            return message, self.failed_status, self.failed_headers
