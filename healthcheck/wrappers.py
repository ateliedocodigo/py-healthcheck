#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .healthcheck import Checker


def checker(name=None):
    if callable(name):
        return Checker().decorate(name)
    return Checker(name=name).decorate
