#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['matplotlib>=3.5.1',
                'pandas>=1.3']

test_requirements = ['pytest>=3', ]

setup(
    author="Marcel Wuijtenburg",
    author_email='marcelw1323@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    description="Clean Business Chart is a Python package for IBCS-like charts based on matplotlib.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['clean business chart', 'IBCS', 'business chart', 'clean business charts', 'business charts', 'chart', 'charts'],
    name='Clean Business Chart',
    packages=find_packages(include=['clean_business_chart', 'clean_business_chart.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcelw1323/clean_business_chart',
    version='0.1.2',
    zip_safe=False,
)

