from setuptools import setup, find_packages

setup(name='TenXTools',
      version='0.1',
      description='Tools to reads metrics from molecule_info.h5 file from cellranger',
      url='http://github.com/fougere87/10xTools',
      author='Chloe MAYERE',
      author_email='chloe.mayere@unige.ch',
      license='MIT',
      packages=find_packages('TenXTools'),
      package_dir =   {'':'TenXTools'},
      entry_points = {
        'console_scripts': ['GetMetrics=TenXTools.GetMetrics:main']},
      #scripts=['bin/GetMetrics'],
      install_requires=[
          'h5py',
          'numpy',
          'pandas'
      ],
      zip_safe=False)
