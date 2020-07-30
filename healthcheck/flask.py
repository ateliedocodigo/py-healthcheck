from functools import wraps

from .healthcheck import HealthCheck


class FlaskHealthCheck(HealthCheck):

    def __init__(self, app, checkers=None, *args, **kwargs):
        self.app = app
        super(FlaskHealthCheck, self).__init__(*args, **kwargs)

        self.checkers = [self._flask_context(c) for c in checkers]

    def add_check(self, func):
        self.checkers.append(self._flask_context(func))

    def _flask_context(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            with self.app.app_context():
                return f(*args, **kwargs)

        return inner
