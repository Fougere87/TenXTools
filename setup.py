from setuptools import setup

setup(name='TenXTools',
      version='0.1',
      description='Tools to reads metrics from molecule_info.h5 file from cellranger',
      url='http://github.com/fougere87/10xTools',
      author='Chloe MAYERE',
      author_email='chloe.mayere@unige.ch',
      license='MIT',
      packages=['TenXTools'],
      scripts=['bin/GetMetrics'],
      install_requires=[
          'h5py',
          'numpy',
          'pandas'
      ],
      zip_safe=False)
