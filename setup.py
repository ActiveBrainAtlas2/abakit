# This is just a shim for `pip install -e` to work. See
#   https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#development-mode

import setuptools
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('mymodule/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(version=main_ns['__version__'])