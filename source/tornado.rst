Tornado
=======

To use with ``Tornado`` you can import the ``TornadoHandler``:

.. code:: python

    import tornado.web
    from healthcheck import TornadoHandler, HealthCheck, EnvironmentDump

    app = tornado.web.Application()

    health = HealthCheck()
    envdump = EnvironmentDump()

    # add your own check function to the healthcheck
    def redis_available():
        client = _redis_client()
        info = client.info()
        return True, "redis ok"

    health.add_check(redis_available)

    # add your own data to the environment dump or healthcheck
    def application_data():
        return {"maintainer": "Luis Fernando Gomes",
                "git_repo": "https://github.com/ateliedocodigo/py-healthcheck"}

    # ou choose where you want to output this information
    health.add_section("application", application_data)
    health.add_section("version", __version__)
    envdump.add_section("application", application_data)

    # Add a tornado handler to expose information
    app.add_handlers(
        r".*",
        [
            (
                "/healthcheck",
                TornadoHandler, dict(checker=health)
            ),
            (
                "/environment",
                TornadoHandler, dict(checker=envdump)
            ),
        ]
    )

Alternatively you can set all together:

.. code:: python

    import tornado.web
    from healthcheck import TornadoHandler, HealthCheck, EnvironmentDump

    # add your own check function to the healthcheck
    def redis_available():
        client = _redis_client()
        info = client.info()
        return True, "redis ok"

    health = HealthCheck(checkers=[redis_available])

    # add your own data to the environment dump
    def application_data():
        return {"maintainer": "Luis Fernando Gomes",
                "git_repo": "https://github.com/ateliedocodigo/py-healthcheck"}

    envdump = EnvironmentDump(application=application_data)

    app = tornado.web.Application([
        ("/healthcheck", TornadoHandler, dict(checker=health)),
        ("/environment", TornadoHandler, dict(checker=envdump)),
    ])
