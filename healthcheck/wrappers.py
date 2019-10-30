from .environmentdump import EnvironmentDump
from .healthcheck import HealthCheck


def add_check_to(health_check):
    """
    Adds the decorated function to the given class.

    :param our_class:
        An instance of :code:`HealthCheck`.
    """

    def real_add_check(func):

        if not isinstance(health_check, HealthCheck):
            raise Exception(
                "{0} given, {1} expected.".format(health_check, HealthCheck)
            )

        health_check.add_check(func)
        return func

    return real_add_check


def add_section_to(our_class, name):
    """
    Adds the decoraten section method/function to
    the given class.

    :param our_class:
        An instance of :code:`HealthCheck`
        or :code:`HealthCheck`.
    :param str name:
        The name to use to index the given section
        data.

    :raise Exception:
        When :code:`our_class` is not an instance of
        :code:`HealthCheck` or :code:`HealthCheck`.
    """

    def real_add_section(func):

        if not isinstance(our_class, (HealthCheck, EnvironmentDump)):
            raise Exception(
                "{0} given, {1} or {2} expected.".format(
                    our_class, HealthCheck, EnvironmentDump
                )
            )

        our_class.add_section(name, func)
        return func

    return real_add_section
