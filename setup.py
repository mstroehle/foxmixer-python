#!/usr/bin/env python

from setuptools import setup

VERSION = None
with open('foxmixer/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            VERSION = line.replace("'", '').split('=')[1].strip()
            break
if VERSION is None:
    raise ValueError('__version__ not found in __init__.py')

DOWNLOAD_URL = 'https://github.com/teran-mckinney/foxmixer-python/tarball/{}'

DESCRIPTION = 'foxmixer.com Bitcoin Mixer Library'

setup(
    python_requires='>=3.3',
    name='foxmixer',
    version=VERSION,
    author='Teran McKinney',
    author_email='sega01@go-beyond.org',
    description=DESCRIPTION,
    keywords=['bitcoin', 'mixer', 'mixing', 'tumbler'],
    license='Unlicense',
    url='https://github.com/teran-mckinney/foxmixer-python',
    download_url=DOWNLOAD_URL.format(VERSION),
    packages=['foxmixer'],
    install_requires=[
        'aaargh',
        'requests[socks]>=2.22.0',
        'pyqrcode'
    ],
    entry_points={
        'console_scripts': [
            'foxmixer = foxmixer:main'
        ]
    }
)
