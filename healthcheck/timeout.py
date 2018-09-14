#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
import errno
import os
import signal


class TimeoutError(Exception):
    pass


try:
    err_msg = os.strerror(errno.ETIME)
except AttributeError:
    # errno.ETIME does not exist on FreeBSD
    err_msg = "Timer expired"


def timeout(seconds=2, error_message=err_msg):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
