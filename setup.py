from distutils.core import setup
from setuptools import find_packages

import versioneer
"""
To upload a new version:
0. rm -rf *.egg-info
1. Git tag a new version
2. python setup.py sdist register upload
"""

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='remote-pip',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Remote pip',
      long_description='Execute pip commands in remote nodes',
      author='Daniel Rodriguez',
      author_email='df.rodriguez@gmail.com',
      url='https://github.com/danielfrg/remote-pip',
      license='Apache 2.0',
      packages=find_packages(),
      include_package_data=True,
      entry_points="""
        [console_scripts]
        rpip=rpip.cli.main:start
      """,
      install_requires=required)
