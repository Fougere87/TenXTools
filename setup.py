from setuptools import setup

setup(name='10xTools',
      version='0.1',
      description='Tools to reads metrics from molecule_info.h5 file from cellranger',
      url='http://github.com/fougere87/10xTools',
      author='C MAYERE',
      author_email='chloe.mayere@unige.ch',
      license='MIT',
      packages=['10xTools'],
      install_requires=[
          'h5py',
          'time',
          'numpy',
          'pandas',
          'gc'
      ],
      zip_safe=False)
