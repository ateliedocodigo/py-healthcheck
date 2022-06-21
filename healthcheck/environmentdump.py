#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import platform
import sys
from typing import Dict, Any, Tuple

import six

from .security import safe_dict


class EnvironmentDump:
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
        for k, v in kwargs.items():
            if k not in self.functions:
                self.add_section(k, v)

    def add_section(self, name, func) -> None:
        if name in self.functions:
            raise Exception('The name "{}" is already taken.'.format(name))
        if not hasattr(func, '__call__'):
            self.functions[name] = lambda: func
            return
        self.functions[name] = func

    def run(self) -> Tuple[str, int, Dict[str, str]]:
        data = {}
        for (name, func) in six.iteritems(self.functions):
            data[name] = func()

        return json.dumps(data, default=str), 200, {'Content-Type': 'application/json'}

    def get_os(self) -> Dict[str, Any]:
        return {'platform': sys.platform,
                'name': os.name,
                'uname': platform.uname()}

    def get_python(self) -> Dict[str, Any]:
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
            packages = {p.project_name: p.version for p in pip.get_installed_distributions()}
            result['packages'] = packages
        except Exception:
            pass

        return result

    def get_login(self) -> str:
        # Based on https://github.com/gitpython-developers/GitPython/pull/43/
        # Fix for 'Inappopropirate ioctl for device' on posix systems.
        if os.name == 'posix':
            import pwd
            username = pwd.getpwuid(os.geteuid()).pw_name
        else:
            username = os.environ.get('USER', os.environ.get('USERNAME', 'UNKNOWN'))
            if username == 'UNKNOWN' and hasattr(os, 'getlogin'):
                username = os.getlogin()
        return username

    def get_process(self) -> Dict[str, Any]:
        return {'argv': sys.argv,
                'cwd': os.getcwd(),
                'user': self.get_login(),
                'pid': os.getpid(),
                'environ': safe_dict(os.environ)}
