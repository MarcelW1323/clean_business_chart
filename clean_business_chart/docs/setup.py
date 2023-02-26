from setuptools import setup

requirements = ['matplotlib>=3.5.1']

setup(name='Clean Business Chart',
      version='0.1.0',
      description="Clean Business Chart is a Python package for IBCS-like charts based on matplotlib.",
      long_description=readme + '\n\n' + history,
      author="Marcel Wuijtenburg",
      author_email='marcelw1323@gmail.com',
      license="MIT license",
      packages=find_packages(include=['clean_business_chart', 'clean_business_chart.*']),
      zip_safe=False,
      install_requires=requirements,
      )
