import time

from flask import Flask

from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)

health = HealthCheck()
envdump = EnvironmentDump()


# add your own check function to the healthcheck
def redis_available():
    time.sleep(3)
    return True, "redis ok"


def rest_available():
    time.sleep(2)
    raise Exception("NO")
    # return True, "rest ok"


health.add_check(redis_available)
health.add_check(rest_available)


# add your own data to the environment dump
def application_data():
    return {"maintainer": "Luis Fernando Gomes",
            "git_repo": "https://github.com/ateliedocodigo/py-healthcheck"}


envdump.add_section("application", application_data)

# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
