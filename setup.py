from setuptools import setup, find_packages
import os

version = '0.68'

setup(name='Products.CNXPloneSite',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rhaptos developers',
      author_email='rhaptos@cnx.rice.edu',
      url='http://rhaptos.org',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.RhaptosSite',
          'Products.RhaptosBugTrackingTool',
          'Products.CNXContent',
          'Products.CNXPloneSite',
          'Products.FeatureArticle',
          'Products.RisaCollection',
          'Products.RisaHitCountTool',
          'Products.RisaModuleEditor',
          'Products.RisaModuleStorage',
          'Products.RisaPatchTool',
          'Products.RisaPDFLatexTool',
          'Products.RisaRepository',
          'Products.RisaSimilarityTool',
          'Products.RisaSite',
          'Products.RisaWorkgroup',
          'Products.Siyavula',
      ],
      tests_require = [
           'zope.testing>=3.5',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

