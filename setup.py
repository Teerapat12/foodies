from setuptools import setup

setup(name='foodies',
      version='0.1',
      description='Repository for Foodies Recommender System',
      url='https://github.com/Teerapat12/foodies',
      author='Teerapat (Time)',
      author_email='teerapat.time12@gmail.com',
      license='MIT',
      packages=[
          'foodies'
      ],
      install_requires=[
          'pandas'
      ],  # Optional
      zip_safe=False)