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
if sys.version_info < (2, 6):
    # collective.autopermission is not needed on Zope 2.12, but hard
    # to add as an extra for Plone 3, given our current buildout
    # configs where an 'eggs += example.conference [plone3]' would
    # conflict with the 'eggs -=' that is already there.  As long as
    # we don't actually release to PyPI (giving different results when
    # creating an sdist with python2.4 or python2.6) this setup should
    # be fine too.
    install_requires.append('collective.autopermission')


setup(name='example.conference',
      version=version,
      description="Example accompanying http://dexterity-developer-manual.readthedocs.org",
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
          'plone3': ['collective.autopermission'],
          },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
