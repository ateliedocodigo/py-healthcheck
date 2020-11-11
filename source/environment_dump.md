Environment Dump
================

Healthcheck also gives you the `EnvironmentDump` class to view information about your application's environment.
By default, this includes data about the operating system, the Python environment, the current process,
and the application config.
You can customize which sections are included, or add your own sections to the output.

Built-in data sections
----------------------

By default, EnvironmentDump data includes these 4 sections:

-   `os`: information about your operating system.
-   `python`: information about your Python executable, Python path, and
    installed packages.
-   `process`: information about the currently running Python process,
    including the PID, command line arguments, and all environment
    variables.

Some of the data is scrubbed to avoid accidentally exposing passwords or
access keys/tokens. Config keys and environment variable names are
scanned for `key`, `token`, or `pass`. If those strings are present in
the name of the variable, the value is not included.

Disabling built-in data sections
--------------------------------

For security reasons, you may want to disable an entire section. You can
disable sections when you instantiate the `EnvironmentDump` object, like
this:

```python
envdump = EnvironmentDump(include_python=False,
                          include_os=False,
                          include_process=False)
```

Adding custom data sections
---------------------------

You can add a new section to the output by registering a function of
your own. Here's an example of how this would be used:

```python
def application_data():
    return {
        'maintainer': 'Atelie do Codigo',
        'git_repo': 'https://github.com/ateliedocodigo/py-healthcheck',
    }

envdump = EnvironmentDump()
envdump.add_section('application', application_data)
```

You can also add custom section on `constructor`

```python
from healthcheck import  EnvironmentDump
def application_data():
    return {
        'maintainer': 'Atelie do Codigo',
        'git_repo': 'https://github.com/ateliedocodigo/py-healthcheck',
    }

envdump = EnvironmentDump(application_data=application_data)
```

Usage in Flask applications
---------------------------

```python
from flask import Flask
from healthcheck import EnvironmentDump

app = Flask(__name__)

@app.route('/environment')
def environment():
    return EnvironmentDump().run()
```

Usage in Tornado applications
-----------------------------

```python
import tornado.web
from healthcheck import TornadoHandler, EnvironmentDump

envdump = EnvironmentDump()

app = tornado.web.Application([
    ('/environment', TornadoHandler, dict(checker=envdump)),
])
```
