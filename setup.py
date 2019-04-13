#!/usr/bin/env python
from distutils.core import setup
from pyamex.version import __version__

setup(name='pyamex',
      version=__version__,
      license='MIT',
      description='Python Library for accessing American Express account data',
      author='Niall McConville',
      author_email='niall.mcconville@cantab.net',
      url='https://github.com/nm523/pyamex',
      python_requires='>3.4.0',
      packages=['pyamex'],
      package_data={'pyamex': ['data/*.xml']}
      )
