#!/usr/bin/env python
"""
Some docs
"""
# -*- coding: utf-8 -*-
import json
import os
import platform
import sys

import six

from .security import safe_dict


class EnvironmentDump(object):
    def __init__(self,
                 include_os=True,
                 include_python=True,
                 include_process=True,
                 **kwargs):
        """
        Class to view information about your application's environment

        :param include_os: Include information about your operating system
        :param include_python: Include information about your Python executable, Python path, and installed packages.
        :param include_process: Include information about the currently running Python process, including the PID,
                                command line arguments, and all environment variables.
        """
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
        """ Add custom section

        :param name: Name of section
        :param func: Value to of section, it can be dynamic value like a function
        :return: None
        """
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
                'environ': safe_dict(os.environ)}
