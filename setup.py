# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''


setup(
    name='icon_font_to_png',
    url='https://github.com/Pythonity/icon-font-to-png',
    download_url='https://github.com/Pythonity/icon-font-to-png/releases/latest',
    bugtrack_url='https://github.com/Pythonity/icon-font-to-png/issues',
    version='0.3.5',
    license='MIT License',
    author='Pythonity',
    author_email='pythonity@pythonity.com',
    maintainer='Paweł Adamczak',
    maintainer_email='pawel.adamczak@sidnet.info',
    description='Python script (and library) for exporting icons from '
                'icon fonts (e.g. Font Awesome, Octicons) as PNG images.',
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[
        'pillow>=3.0.0',
        'tinycss>=0.3',
        'six>=1.10.0',
        'requests>=2.10.0',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    scripts=['bin/font-awesome-to-png', 'bin/icon-font-to-png'],
    keywords='icon font export font awesome octicons',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
)
