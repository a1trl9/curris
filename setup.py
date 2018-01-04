""" setup for curris
"""

import sys
from setuptools import setup
from setuptools.command.test import test as Test

from curris import __version__

class PyTest(Test):
    """ pytest class
    """
    def finalize_options(self):
        Test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='curris',
    version=__version__,
    url='https://github.com/a1trl9/curris',
    license='MIT License',
    author='a1trl9',
    tests_require=['pytest'],
    install_requires=[],
    packages=['curris', 'curris.render'],
    cmdclass={'test': PyTest},
    author_email='adavindes@gmail.com',
    description='Minimal Markdown Parser in Python3',
    include_package_data=True,
    platforms='any',
    test_suite='curris.test.test_curris',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 0 - Alpha',
        'Natural Language :: English',
        'Environment :: Local Environment',
        'Intended Audience :: Markdown Users',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Markdown'
    ],
    extras_require={
        'testing': ['pytest']
        },
    entry_points='''
        [console_scripts]
        curris=curris.cli:main
    '''
    )
