# Healthcheck Changelog

### 0.2
- Added caching to health check responses. Successful checks are cached for 27
seconds; failures are cached for 9 seconds.
- Removed the "simple" view of the health check, which had been available with
the query string `?simple=true`. This isn't necessary now that we cache the
results of the checks.
- Added `timestamp` field to the outer level of the JSON response, and
`timestamp` and `expires` to each check result.
