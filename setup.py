# coding=utf-8

import os

from setuptools import find_packages, setup

requirements = [
    'sarge',
]
test_requirements = [
    'epab',
]

# TODO: fix trove classifiers
CLASSIFIERS = filter(None, map(str.strip,
                               """
Development Status :: 3 - Alpha
License :: OSI Approved :: MIT License
Environment :: Win32 (MS Windows)
Natural Language :: English
Operating System :: Microsoft :: Windows
Operating System :: Microsoft :: Windows :: Windows 7
Operating System :: Microsoft :: Windows :: Windows 8
Operating System :: Microsoft :: Windows :: Windows 8.1
Operating System :: Microsoft :: Windows :: Windows 10
Programming Language :: Cython
Programming Language :: Python
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
""".splitlines()))


def read_local_files(*file_paths: str) -> str:
    """
    Reads one or more text files and returns them joined together.
    A title is automatically created based on the file name.

    Args:
        *file_paths: list of files to aggregate

    Returns: content of files
    """

    def _read_single_file(file_path):
        with open(file_path) as f:
            filename = os.path.splitext(file_path)[0]
            title = f'{filename}\n{"=" * len(filename)}'
            return '\n\n'.join((title, f.read()))

    return '\n' + '\n\n'.join(map(_read_single_file, file_paths))


setup(
    name='elib_run',
    author='etcher',
    zip_safe=False,
    author_email='etcher@daribouca.net',
    platforms=['win32'],
    url=r'https://github.com/etcher-be/elib_run',
    download_url=r'https://github.com/etcher-be/elib_run/releases',
    description="Simple wrapper around the Sarge library to run sub-processes",
    license='MIT',
    long_description=read_local_files('README.md'),
    packages=find_packages(),
    package_data={
        'elib_run': 'test'
    },
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    python_requires='>=3.6',
    classifiers=CLASSIFIERS,
)
