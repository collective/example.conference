from setuptools import setup, find_packages
import os
import sys

version = '1.0a1'

install_requires = [
    'setuptools',
    'plone.app.dexterity',
    'plone.principalsource',
    'plone.namedfile',
    'plone.formwidget.namedfile',
    'collective.wtf',
    ]


setup(name='example.conference',
      version=version,
      description="Example accompanying http://developer.plone.org/reference_manuals/external/plone.app.dexterity/",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
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
      install_requires=install_requires,
      extras_require={
          'test':  ['plone.app.testing', 'plone.mocktestcase'],
          # Test relations within datagrid fields.  Some of these do
          # not yet have releases with the changes we need.
          'datagrid': [
              'collective.z3cform.datagridfield>0.5',
              'plone.app.referenceablebehavior',
              'plone.formwidget.contenttree>1.0',
              ],
          },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
