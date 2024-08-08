from setuptools import setup, find_packages
from subprocess import check_output

# get the version of gdal-config to use as a requirement (from bash)
gdalconfig_version = check_output('gdal-config --version', shell=True).decode('utf-8').strip()

setup(
    name='hmc',
    version='0.1',
    packages=find_packages(),
    description='Hydrological Model Continuum Package',
    author='Fabio Delogu',
    author_email='fabio.delogu@cimafoundation.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPL 1.2 License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    keywords='hydrological modelling',
    install_requires=[
        f'gdal[numpy]=={gdalconfig_version}',
        'xarray>=2023.9.0',
        'dask',
        'scipy',
        'pandas',
    ],
    python_requires='>=3.10',
    test_suite='tests',
)
