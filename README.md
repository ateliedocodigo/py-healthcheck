Healthcheck
----------

Healthcheck wraps a Flask app object and adds a way to write simple heathcheck functions that can be use to monitor your application.  It's useful for asserting that your dependencies are up and running and your application can respond to HTTP requests.  The Healthcheck functions are exposed via a user defined flask route so you can use an external monitoring application (monit, nagios, Runscope, etc.) to check the status and uptime of your application.

Installing
----------

```
pip install healthcheck

```

Usage
-----

Here's an example of basic usage

```python
from flask import Flask
from healthcheck import HealthCheck

app = Flask(__name__)

# wrap the flask app and give a heathcheck url
health = HealthCheck(app, "/healthcheck")


# add check functions
def redis_available():
    client = _redis_client()
    info = client.info()
    return True, "redis ok"

health.add_check(redis_available)
```

To run all of your check functions, make a request to the healthcheck URL
you specified, like this:

```
curl "http://localhost:5000/healthcheck"
```

Check Functions
---------------

Check functions take no arguments and should return a tuple of (bool, str).
The boolean is whether or not the check passed.  The message is any string or
output that should be rendered for this check.  Useful for error
messages/debugging.

```python
# add check functions
def addition_works():

	if 1 + 1 == 2:
		return True, "addition works"
	else:
		return False, "the universe is broken"
```

Any exceptions that get thrown by your code will be caught and handled as
errors in the healthcheck:

```python
# add check functions
def throws_exception():
	bad_var = None
	bad_var['explode']

```

Will output:

```json
{
	"status": "failure",
		"results": [
		{
			"output": "'NoneType' object has no attribute '__getitem__'",
			"checker": "throws_exception",
			"passed": false
		}
	]
}
```

Note, all checkers will get run and all failures will be reported.  It's
intended that they are all separate checks and if any one fails the
healthcheck overall is failed.

Caching
-------

In Runscope's infrastructure, the /healthcheck endpoint is hit surprisingly
often. haproxy runs on every server, and each haproxy hits every healthcheck
twice a minute. (So if we have 30 servers in our infrastructure, that's 60
healthchecks per minute to every Flask service.) Plus, monit hits every
healthcheck 6 times a minute. 

To avoid putting too much strain on backend services, health check results can
be cached in process memory. By default, health checks that succeed are cached
for 27 seconds, and failures are cached for 9 seconds. These can be overridden
with the `success_ttl` and `failed_ttl` parameters. If you don't want to use
the cache at all, initialize the Healthcheck object with `success_ttl=None,
failed_ttl=None`.

Customizing
-----------

You can customize the status codes, headers, and output format for success and
failure responses.  
