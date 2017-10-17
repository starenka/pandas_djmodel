#!/usr/bin/env python
from setuptools import setup, find_packages

setup_requires = ('setuptools',)
dependency_links, install_requires = [], []


def parse_reqs(f):
    reqs, deps = [], []
    for l in f.readlines():
        l = l.strip()
        if l and not l.startswith("#"):
            reqs.append(l)

    return reqs, deps


with open('requirements.pip') as f:
    install_requires, dependency_links = parse_reqs(f)

with open('requirements_test.pip') as f:
    tests_require, tdeps = parse_reqs(f)
    dependency_links += tdeps

setup(name='pandas_djmodel',
      version='0.1.0',
      author='starenka',
      author_email='starenka0@gmail.com',
      url='https://github.com/starenka/pandas_djmodel',
      packages=find_packages(),
      include_package_data=True,
      scripts=[],
      install_requires=install_requires,
      dependency_links=dependency_links,
      setup_requires=setup_requires,
      tests_require=tests_require,
      )
