Healthcheck Functions
=====================

All healthcheck functions should return a `tuple` containing result and message.


Return status `True` for a success check and an arbitrary message
```python
def check_that_works():
    return True, 'it works'
```

Return status `False` for a failed check and an arbitrary message
```python
def check_that_fails():
    return False, 'check was failed!'
```

All functions are wrapped to prevent exceptions, it will be a failed check with the `Exception` as message.

```python
def check_throws_exception():
    bad_var = None
    bad_var['key-does-not-exists']
```

Rich message
------------

Message can be a dict too, if you want to expose extra info.

```python
def some_check():
    extra_info = {
        'hello': 'world',
    }
    return True, extra_info
```


Add healthcheck functions
-------------------------

You can set up your functions on healthcheck's constructor.

```python
health = HealthCheck(checkers=[your_check])
```

Also, you can set up your functions using healthcheck's `add_check` method.

```python
health = HealthCheck()
health.add_check(your_check)
```
