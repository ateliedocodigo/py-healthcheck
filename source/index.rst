Healthcheck Python library
==========================

.. image:: _static/py-healthcheck.jpg
    :alt: Python Healthcheck library

Healthcheck is a library to write simple healthcheck functions that can
be used to monitor your application. It is possible to use in a `Flask`
app or `Tornado` app. It's useful for asserting that your dependencies
are up and running and your application can respond to HTTP requests.
The Healthcheck functions can be exposed via a user defined `Flask`
route so you can use an external monitoring application (`monit`,
`nagios`, `Runscope`, etc.) to check the status and uptime of your
application.


Quickstart Flask
----------------

After :ref:`installation<installing>`, you can setup your Flask application.

.. code-block:: python

    from flask import Flask
    from healthcheck import HealthCheck

    app = Flask(__name__)

    health = HealthCheck()

    # Add a flask route to expose information
    app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())


To run all of your check functions, make a request to the healthcheck
URL you specified, like this:

    curl http://localhost:5000/healthcheck

Quickstart Tornado
------------------

After :ref:`installation<installing>`, you can setup your Tornado application using `TornadoHandler`.

.. code-block:: python

    import tornado.web
    from healthcheck import TornadoHandler

    app = tornado.web.Application([
        ('/healthcheck', TornadoHandler)
    ])

To run all of your check functions, make a request to the healthcheck
URL you specified, like this:

    curl http://localhost:8080/healthcheck

.. toctree::
   :titlesonly:

   installing
   api
   healthcheck_functions
   environment_dump
   flask
   tornado
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
