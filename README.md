Installing
----------

Add the following to your requirements.txt

```
-e git+git@github.com:Runscope/healthcheck.git#egg=healthcheck
```

Usage
-----

Here's an example of basic usage

```
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

Check Functions
---------------

Check functions take no arguments and should return a tuple of (bool, str).
The boolean is whether or not the check passed.  The message is any string or
output that should be rendered for this check.  Useful for error
messages/debugging.

```
# add check functions
def addition_works():

	if 1 + 1 == 2:
		return True, "addition works"
	else:
		return False, "the universe is broken"
```

Any exceptions that get thrown by your code will be caught and handled as
errors in the healthcheck:

```
# add check functions
def throws_exception():
	bad_var = None
	bad_var['explode']

```

Will output:

```
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

Note, all checkers will get run and all failures will be reported.  It's
intended that they are all separate checks and if any one fails the
healthcheck overall is failed.

```

Customizing
-----------

You can customize the status codes, headers, and output format for success and
failure responses.  
