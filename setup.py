#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='healthcheck',
      version='1.1.0',
      description='Adds healthcheck endpoints to Flask apps',
      author='Frank Stratton',
      author_email='frank@runscope.com',
      url='https://github.com/Runscope/healthcheck',
      download_url='https://github.com/Runscope/healthcheck/tarball/1.1.0',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[],
      classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Flask',
                   'Programming Language :: Python'))
