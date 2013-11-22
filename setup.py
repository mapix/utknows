# -*- coding:utf-8 -*-

import os

from setuptools import find_packages, setup

from utknows import __version__
BASE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE, 'README.rst')).read()

setup(
    name='utknows',
    version=__version__,
    classifiers=['License :: OSI Approved :: BSD License'],
    long_description=find_packages(),
    url='http://mapix.me/utknows/',
    license='BSD',
    packages=['utknows'],
    include_package_data=True,
    zip_safe=True,
)
