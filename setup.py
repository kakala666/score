from distutils.core import setup
from Cython.Build import cythonize
setup(
    name='',
    ext_modules=cythonize(module_list="*.py"),
)
