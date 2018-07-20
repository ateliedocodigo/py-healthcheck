#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import json
import os
import platform
import six


class EnvironmentDump(object):
    def __init__(self,
                 include_os=True,
                 include_python=True,
                 include_process=True,
                 **kwargs):
        self.functions = {}
        if include_os:
            self.functions['os'] = self.get_os
        if include_python:
            self.functions['python'] = self.get_python
        if include_process:
            self.functions['process'] = self.get_process

        # ads custom_sections on signature
        [self.add_section(k, v) for k, v in kwargs.items() if k not in self.functions]

    def add_section(self, name, func):
        if name in self.functions:
            raise Exception('The name "{}" is already taken.'.format(name))
        if not hasattr(func, '__call__'):
            self.functions[name] = lambda: func
            return
        self.functions[name] = func

    def run(self):
        data = {}
        for (name, func) in six.iteritems(self.functions):
            data[name] = func()

        return json.dumps(data, default=str), 200, {'Content-Type': 'application/json'}

    def get_os(self):
        return {'platform': sys.platform,
                'name': os.name,
                'uname': platform.uname()}

    def get_python(self):
        result = {'version': sys.version,
                  'executable': sys.executable,
                  'pythonpath': sys.path,
                  'version_info': {'major': sys.version_info.major,
                                   'minor': sys.version_info.minor,
                                   'micro': sys.version_info.micro,
                                   'releaselevel': sys.version_info.releaselevel,
                                   'serial': sys.version_info.serial}}
        try:
            import pip
            packages = dict([(p.project_name, p.version) for p in pip.get_installed_distributions()])
            result['packages'] = packages
        except Exception:
            pass

        return result

    def get_login(self):
        # Based on https://github.com/gitpython-developers/GitPython/pull/43/
        # Fix for 'Inappopropirate ioctl for device' on posix systems.
        if os.name == "posix":
            import pwd
            username = pwd.getpwuid(os.geteuid()).pw_name
        else:
            username = os.environ.get('USER', os.environ.get('USERNAME', 'UNKNOWN'))
            if username == 'UNKNOWN' and hasattr(os, 'getlogin'):
                username = os.getlogin()
        return username

    def get_process(self):
        return {'argv': sys.argv,
                'cwd': os.getcwd(),
                'user': self.get_login(),
                'pid': os.getpid(),
                'environ': self.safe_dump(os.environ)}

    def safe_dump(self, dictionary):
        result = {}
        for key in dictionary.keys():
            if 'key' in key.lower() or 'token' in key.lower() or 'pass' in key.lower():
                # Try to avoid listing passwords and access tokens or keys in the output
                result[key] = "********"
            else:
                try:
                    json.dumps(dictionary[key], default=str)
                    result[key] = dictionary[key]
                except TypeError:
                    pass
        return result
