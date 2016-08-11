# -*- coding: utf-8 -*-
# :Project:   lektor_diazo -- A package to postprocess html artifacts with diazo
# :Created:   gio 11 ago 2016 12:19:27 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU Lesser General Public License version 3 or later
# :Copyright: Copyright © 2016 Alberto Berti
#

from __future__ import unicode_literals, absolute_import, print_function

from codecs import open
import os

from lektor.pluginsystem import Plugin

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()


class DiazoThemePlugin(Plugin):
    name = 'Diazo themes for Lektor'
    description = README

    def on_after_build(self, builder, build_state, source, prog, **extra):
        print('after-build called')
