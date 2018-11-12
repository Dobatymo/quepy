# -*- coding: utf-8 -*-

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

from builtins import str, range

import unittest
import tempfile
import subprocess
from random_expression import random_expression
from random import seed
from quepy.dot_generation import expression_to_dot
from quepy.dsl import FixedRelation, FixedType, FixedDataRelation


def gen_datarel(rel, data):
    class X(FixedDataRelation):
        relation = rel
    return X(data)


def gen_fixedtype(type_):
    class X(FixedType):
        fixedtype = type_
    return X()


def gen_fixedrelation(rel, e):
    class X(FixedRelation):
        relation = rel
    return X(e)


class TestDotGeneration(unittest.TestCase):

    def _standard_check(self, s, e):
        self.assertIsInstance(s, str)
        vs = ["x{}".format(i) for i in range(len(e))]
        for var in vs:
            self.assertIn(var, s)

    def test_dot_takes_unicode(self):
        e = gen_fixedtype("·̣─@łæßð~¶½")
        e += gen_datarel("tµŧurułej€", "←ðßðæßđæßæđßŋŋæ @~~·ŋŋ·¶·ŋ“¶¬@@")
        _, s = expression_to_dot(e)
        self._standard_check(s, e)

    def test_dot_takes_fails_ascii1(self):
        e = gen_fixedtype(b"a")
        e += gen_datarel(b"b", b"c")
        e = gen_fixedrelation(b"d", e)
        self.assertRaises(ValueError, expression_to_dot, e)

    #@unittest.skip("SyntaxError: bytes can only contain ASCII literal characters.")
    def test_dot_takes_fails_ascii2(self):
        e = gen_fixedtype(b"\xc2\xb7\xcc\xa3\xe2\x94\x80@\xc5\x82\xc3\xa6\xc3\x9f\xc3\xb0~\xc2\xb6\xc2\xbd")
        e += gen_datarel(b"t\xc2\xb5\xc5\xa7uru\xc5\x82ej\xe2\x82\xac", b"\xe2\x86\x90\xc3\xb0\xc3\x9f\xc3\xb0\xc3\xa6\xc3\x9f\xc4\x91\xc3\xa6\xc3\x9f\xc3\xa6\xc4\x91\xc3\x9f\xc5\x8b\xc5\x8b\xc3\xa6 @~~\xc2\xb7\xc5\x8b\xc5\x8b\xc2\xb7\xc2\xb6\xc2\xb7\xc5\x8b\xe2\x80\x9c\xc2\xb6\xc2\xac@@")
        self.assertRaises(ValueError, expression_to_dot, e)

    def test_dot_stress(self):
        seed(b"I have come here to chew bubblegum and kick ass... and I'm all out of bubblegum.")
        with tempfile.NamedTemporaryFile() as dot_file:
            cmdline = "dot %s" % dot_file.name
            msg = "dot returned error code {}, check {} input file."
            for _ in range(100):
                expression = random_expression()
                _, dot_string = expression_to_dot(expression)
                dot_file.write(dot_string.encode("utf-8"))

                try:
                    with tempfile.TemporaryFile() as temp:
                        retcode = subprocess.call(cmdline.split(), stdout=temp)
                except OSError:
                    print("Warning: the program 'dot' was not found, tests skipped")
                    return
                if retcode != 0:
                    dot_file.delete = False
                self.assertEqual(retcode, 0, msg.format(retcode, dot_file.name))


if __name__ == "__main__":
    unittest.main()
