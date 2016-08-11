# -*- coding: utf-8 -*-
# :Project:   lektor_diazo -- A package to postprocess html artifacts with diazo
# :Created:   gio 11 ago 2016 12:19:27 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU Lesser General Public License version 3 or later
# :Copyright: Copyright © 2016 Alberto Berti
#

from lektor.pluginsystem import Plugin


class DiazoThemePlugin(Plugin):
    name = u'Diazo themes for Lektor'
    description = u'Add your description here.'

    def on_process_template_context(self, context, **extra):
        def test_function():
            return 'Value from plugin %s' % self.name
        context['test_function'] = test_function
