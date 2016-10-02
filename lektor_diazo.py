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
import re

import click
from diazo.compiler import compile_theme
from diazo.utils import quote_param
from lektor.pluginsystem import Plugin
from lxml import etree, html

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

doctype_re = re.compile(b"^<!DOCTYPE\\s[^>]+>\\s*", re.MULTILINE)


class DiazoThemePlugin(Plugin):
    name = 'Diazo themes for Lektor'
    description = README

    charset = 'UTF-8'
    doctype = '<!DOCTYPE html>'
    file_encoding = 'utf-8'
    valid_extensions = (
        'html',
    )
    ignored_extensions = (
        'js', 'css', 'gif', 'jpg', 'jpeg', 'pdf', 'ps', 'doc',
        'png', 'ico', 'mov', 'mpg', 'mpeg', 'mp3', 'm4a', 'txt',
        'rtf', 'swf', 'wav', 'zip', 'wmv', 'ppt', 'gz', 'tgz',
        'jar', 'xls', 'bmp', 'tif', 'tga', 'hqx', 'avi')
    transform_permissions = {
        'read_file': True,
        'write_file': False,
        'create_dir': False,
        'read_network': False,
        'write_network': False
    }

    def _parse_file(self, file_, base_url=None):
        """Parse a file given a file/filename and returns an etree."""
        return html.parse(file_, base_url=base_url)

    def _serialize_etree(self, tree, fname):
        """Save an etree into a file."""
        assert isinstance(tree, etree._XSLTResultTree)
        res = bytes(tree)

        if self.doctype is not None:
            doc_encoded = self.doctype.encode()
            res, subs = doctype_re.subn(doc_encoded, res, 1)
            if not subs:
                res = doc_encoded + res
        with open(fname, 'w') as f:
            f.write(res)

    def on_setup_env(self, **extra):
        self.access_control = etree.XSLTAccessControl(**self.transform_permissions)
        rules_path = os.path.join(self.env.root_path, 'theme', 'rules.xml')

        if os.path.exists(rules_path):
            tree = compile_theme(rules_path, access_control=self.access_control)
            self.transform = etree.XSLT(tree,
                                        access_control=self.access_control)
        else:
            self.transform = None # disabled

        self.valid_pattern = re.compile(
            "^.*\.(%s)$" % '|'.join(self.valid_extensions))
        self.ignored_pattern = re.compile(
            "^.*\.(%s)$" % '|'.join(self.ignored_extensions))


    def on_after_build(self, builder, build_state, source, prog, **extra):
        if not self.transform:
            return
        sign = click.style('T', fg='blue')
        for art in build_state.updated_artifacts:
            if self.valid_pattern.search(art.dst_filename) is not None:
                with open(art.dst_filename, encoding=self.file_encoding) as f:
                    src_tree = self._parse_file(f)
                res_tree = self.transform(src_tree,
                    path=quote_param(art.artifact_name)
                )
                self._serialize_etree(res_tree, art.dst_filename)
                text = '%s %s' % (sign, art.artifact_name)
                click.echo(text)
