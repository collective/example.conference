from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='example.conference',
      version=version,
      description="Example accompanying http://plone.org/products/dexterity/documentation/manual/developers-manual/",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity example',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://plone.org/products/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['example'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'collective.autopermission',
          'plone.principalsource',
          'plone.namedfile',
          'plone.formwidget.namedfile',
          'collective.testcaselayer',
          'collective.wtf',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
