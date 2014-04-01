#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='healthcheck',
      version='0.1.2',
      description='Adds healthcheck endpoints to Flask apps',
      author='Frank Stratton',
      author_email='frank@runscope.com',
      url='http://runscope.com',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[
      ],
)
