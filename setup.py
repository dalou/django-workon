#from __future__ import print_function
import ast
import os
import sys
import codecs
import subprocess
from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages


def find_version(*parts):
    try:
        version_py = os.path.join(os.path.dirname(__file__), 'workon/version.py')
        version_git = subprocess.check_output(["git", "tag"]).rstrip().splitlines()[-1]
        version_msg = "# Do not edit this file, pipeline versioning is governed by git tags" + os.linesep + "# following PEP 386"
        open(version_py, 'wb').write(version_msg + os.linesep + '__version__ = "%s"' % version_git)

    except:
        # NOT RAN LOCALY
        pass

    from workon.version import __version__
    return "{ver}".format(ver=__version__)

def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()



# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

setup(
    name='django-workon',
    version=find_version(),
    description='Django extensions packages',
    long_description=read('README.rst'),
    author='Autrusseau Damien',
    author_email='autrusseau.damien@gmail.com',
    url='http://github.com/dalou/django-workon',
    packages=find_packages(exclude=('tests*',)),
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # test_suite='runtests.runtests',
    install_requires=[
        'django>=1.8.4,<=1.9.2',

        'django_select2==5.8.4',

        # Crypto
        "cryptography==1.0.2",
        "cffi==1.2.1",
        "pycrypto==2.6.1",
        "pyopenssl==0.15.1",
        "requests[security]==2.9.1",
        "oauth2client==2.0.1",
        "requests_oauthlib==0.6.1",

        # Fields / models
        "jsonfield==1.0.3",
        "babel==1.3",
        "django-mptt==0.8.0",

        # payments
        "stripe==1.29.1",

        # Emailing
        "premailer==2.9.6",
        "cssutils==1.0.1",
        "cssselect==0.9.1",

        # Flow
        "django-redis-sessions==0.5.0",

        # Storage
        "boto==2.38.0",
        "django-storages==1.1.8",

        # Watcher
        "watchdog==0.8.3",

        # Geolocation
        "geopy==1.11.0",
        "python-gmaps==0.1.1",
        "google-api-python-client==1.5.0",

        "colour==0.1.2",
        "bleach==1.4.2",
        "django-classy-tags==0.4",

    ],
)
