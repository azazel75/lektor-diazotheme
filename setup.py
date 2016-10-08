# -*- coding: utf-8 -*-
# :Project:   lektor_diazo -- A package to postprocess html artifacts with diazo
# :Created:   gio 11 ago 2016 12:19:27 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU Lesser General Public License version 3 or later
# :Copyright: Copyright © 2016 Alberto Berti
#

from codecs import open
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()


setup(
    name='lektor-diazotheme',
    version=VERSION,
    url="https://github.com/azazel75/lektor-diazotheme",

    description="A package to postprocess html artifacts with diazo",
    long_description=README + u'\n\n' + CHANGES,
    author=u'Alberto Berti',
    author_email='alberto@metapensiero.it',
    license='LGPL3+',
    py_modules=['lektor_diazo'],
    install_requires=['diazo'],
    extras_require={'dev': ['metapensiero.tool.bump_version']},
    entry_points={
        'lektor.plugins': [
            'diazotheme = lektor_diazo:DiazoThemePlugin',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ]
)
