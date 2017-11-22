#!/usr/bin/env python
from distutils.core import setup

VERSIONFILE = 'pyamex/version.py'

setup(name='pyamex',
	  version='0.2.1',
      license='MIT',
	  description='Python Library for accessing American Express account data',
	  author='Niall McConville',
	  author_email='niall.mcconville@cantab.net',
	  url='https://github.com/nm523/pyamex',
	  python_requires='>3.4.0',
	  packages=['pyamex'],
          package_data = { 'pyamex' : ['data/*.xml'] }
     )
