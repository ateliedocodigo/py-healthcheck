#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import socket
import time
try:
    from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union
except ImportError:
    # for python2
    pass

import six

from .timeout import timeout

logger = logging.getLogger(__name__)

try:
    from functools import reduce
except Exception:
    pass


def basic_exception_handler(_, exc):  # type: (Any, Exception) -> Tuple[bool, str]
    return False, str(exc)


def json_success_handler(results, *args, **kw):  # type: (dict,*Any,**Any) -> str
    data = {
        'hostname': socket.gethostname(),
        'status': 'success',
        'timestamp': time.time(),
        'results': results,
    }
    data.update(kw)
    return json.dumps(data)


def json_failed_handler(results, *args, **kw):  # type: (dict, *Any, **Any) -> str
    data = {
        'hostname': socket.gethostname(),
        'status': 'failure',
        'timestamp': time.time(),
        'results': results,
    }
    data.update(kw)
    return json.dumps(data)


def check_reduce(passed, result):  # type: (bool, Mapping[str,bool]) -> bool
    return passed and result.get('passed')  # type: ignore[return-value]


class HealthCheck:
    def __init__(self, success_status=200,
                 success_headers=None, success_handler=json_success_handler,
                 success_ttl=27, failed_status=500, failed_headers=None,
                 failed_handler=json_failed_handler, failed_ttl=9,
                 error_timeout=0,
                 exception_handler=basic_exception_handler, checkers=None,
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
        for k, v in kwargs.items():
            if k not in self.functions:
                self.add_section(k, v)

    def add_section(self, name, func):  # type:(str, Callable[..., Tuple[bool,str]]) -> None
        if name in self.functions:
            raise Exception('The name "{}" is already taken.'.format(name))
        self.functions[name] = func

    def add_check(self, func):  # type:(Callable[..., Tuple[bool,str]]) -> None
        self.checkers.append(func)

    def run(self, check=None):  # type:(Optional[Callable[..., Tuple[bool,str]]]) -> Tuple[str, int, Dict[str, str]]
        results = []
        filtered = [c for c in self.checkers if check is None or c.__name__ == check]
        for checker in filtered:
            if checker in self.cache and self.cache[checker].get('expires') >= time.time():
                result = self.cache[checker]
            else:
                result = self.run_check(checker)
                self.cache[checker] = result
            results.append(result)

        custom_section = dict()
        for (name, func) in six.iteritems(self.functions):
            try:
                custom_section[name] = func() if callable(func) else func
            except Exception:
                pass

        passed = reduce(check_reduce, results, True)

        if passed:
            message = 'OK'
            if self.success_handler:
                message = self.success_handler(results, **custom_section)

            return message, self.success_status, self.success_headers
        message = 'NOT OK'
        if self.failed_handler:
            message = self.failed_handler(results, **custom_section)
        return message, self.failed_status, self.failed_headers

    def run_check(self, checker):  # type:(Callable) -> Dict[str, Union[str, float, bool]]
        start_time = time.time()

        try:
            if self.error_timeout > 0:
                passed, output = timeout(self.error_timeout, 'Timeout error!')(checker)()
            else:
                passed, output = checker()
        except Exception as exc:
            logger.error(exc)
            passed, output = self.exception_handler(checker, exc)

        end_time = time.time()
        elapsed_time = end_time - start_time
        # Reduce to 6 decimal points to have consistency with timestamp
        elapsed_time = float('{:.6f}'.format(elapsed_time))

        if passed:
            msg = 'Health check "{}" passed'.format(checker.__name__)
            logger.debug(msg)
        else:
            msg = 'Health check "{}" failed with output "{}"'.format(checker.__name__, output)
            logger.error(msg)

        timestamp = time.time()
        if passed:
            expires = timestamp + self.success_ttl
        else:
            expires = timestamp + self.failed_ttl

        result = {'checker': checker.__name__,
                  'output': output,
                  'passed': passed,
                  'timestamp': timestamp,
                  'expires': expires,
                  'response_time': elapsed_time}
        return result
