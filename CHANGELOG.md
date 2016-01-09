# Healthcheck Changelog

### 1.3.1
- Fix for 'Inappropriate ioctl for device' error on posix systems.

### 1.3.0
- Adds support for init_app construction of healthcheck objects. Thanks to
  Iuri de Silvio for the pull request.


### 1.2.0
- Adds support for Python 3.x. Thanks to Guilherme D'Amoreira for the pull
request.

### 1.1.0
- Added the `EnvironmentDump` class which provides a second endpoint for
details about your application's environment.

### 1.0.0
- Incremented the version number to indicate that this is a stable release.

### 0.2
- Added caching to health check responses. Successful checks are cached for 27
seconds; failures are cached for 9 seconds.
- Removed the "simple" view of the health check, which had been available with
the query string `?simple=true`. This isn't necessary now that we cache the
results of the checks.
- Added `timestamp` field to the outer level of the JSON response, and
`timestamp` and `expires` to each check result.
