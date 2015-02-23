from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name='ckanext-tags',
    version=version,
    description="dataset tags",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Janos Farkas',
    author_email='farkas48@uniba.sk',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.tags'],
    package_data={'': [
        'i18n/*/LC_MESSAGES/*.po',
        'templates/*.html',\
        'templates/admin/*.html',\
        'templates/package/*.html']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    #entry_points='''
    #    [ckan.plugins]
    #    tags=ckanext.tags.plugin:TagsPlugin
    #''',
    entry_points={
        'babel.extractors': [
                    'ckan = ckan.lib.extract:extract_ckan',
                    ],
        'ckan.plugins' : [
                    'tags =ckanext.tags.plugin:TagsPlugin',
                    ]
        }
)
