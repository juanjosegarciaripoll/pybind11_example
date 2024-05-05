from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import glob
import numpy as np
import sys

# The main interface is through Pybind11Extension.
# * You can add cxx_std = 11 / 14 / 17, and then build_ext can be removed.
# * You can set include_pybind11 = false to add the include directory yourself,
# say from a submodule.
#
# Note:
# Sort input source files if you glob sources to ensure bit - for - bit
# reproducible builds(https: // github.com/pybind/python_example/pull/53)
from pybind11.setup_helpers import Pybind11Extension

if sys.platform == "linux":
    # We assume GCC or other compilers with compatible command line
    extra_compile_args = ["-O3", "-ffast-math", "-Wno-sign-compare"]
else:
    # We assume Microsoft Visual C / C++ compiler
    extra_compile_args = ["/Ox", "/fp:fast"]
extra_dependencies = [
    s.replace("\\", "/") for s in glob.glob("src/**/*.h", recursive=True)
] + [s.replace("\\", "/") for s in glob.glob("src/**/*.cc", recursive=True)]
pybind11_modules = [
    Pybind11Extension(
        "example.pybind",
        [
            "src/example/pybind.cc",
        ],
        extra_compile_args=extra_compile_args,
        include_dirs=[np.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        depends=extra_dependencies,
        cxx_std=17,
    ),
]


# This flag controls whether we build the library with bounds checks and
# other safety measures. Useful when testing where a code breaks down;
# but bad for production performance
debug_library = False
extra_compile_args = []
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.error_on_uninitialized = True
directives = {
    "language_level": "3",  # We assume Python 3 code
    "boundscheck": False,  # Do not check array access
    "wraparound": False,  # a[-1] does not work
    "always_allow_keywords": False,  # Faster calling conventions
    "cdivision": True,  # No exception on zero denominator
    "initializedcheck": False,  # We take care of initializing cdef classes and memory views
    "overflowcheck": False,
    "binding": False,
}
if sys.platform == "linux":
    # We assume GCC or other compilers with compatible command line
    extra_compile_args = ["-O3", "-ffast-math"]
else:
    # We assume Microsoft Visual C/C++ compiler
    extra_compile_args = ["/Ox", "/fp:fast"]
# All Cython files with unix pathnames
cython_files = [s.replace("\\", "/") for s in glob.glob("src/**/*.pyx", recursive=True)]
include_files = [
    s.replace("\\", "/") for s in glob.glob("src/**/*.pxi", recursive=True)
]
extension_names = [".".join(f[4:-4].split("/")) for f in cython_files]
cython_modules = [
    Extension(
        name,
        [file],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        extra_compile_args=extra_compile_args,
        include_dirs=[np.get_include()],
        depends=include_files,
    )
    for name, file in zip(extension_names, cython_files)
]


setup(ext_modules=cython_modules + pybind11_modules)
