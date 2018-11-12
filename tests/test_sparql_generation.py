# -*- coding: utf-8 -*-

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

from builtins import str, range

import re
import unittest
from random_expression import random_expression
from random import seed
from quepy.sparql_generation import expression_to_sparql
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


class TestSparqlGeneration(unittest.TestCase):

    _sparql_line = re.compile("\?x\d+ \S+ (?:\?x\d+|\".*\"|\S+?:\S+?)"
                              "(?:@\w+)?.", re.DOTALL)
    _sparql_query_start = re.compile("SELECT DISTINCT .+ WHERE {(.+)}", re.DOTALL)

    def _standard_check(self, s, e):
        self.assertIsInstance(s, str)
        vs = ["x{}".format(i) for i in range(len(e))]
        for var in vs:
            self.assertIn(var, s)

    def _sparql_check(self, s):
        m = self._sparql_query_start.search(s)
        self.assertNotEqual(m, None, "Could not find query start ")
        lines = m.group(1).split("\n")
        for line in lines:
            line = line.strip()
            if line:
                s = "Line out of format: {!r}\n".format(line)
                self.assertNotEqual(self._sparql_line.match(line), None, s)

    def test_sparql_takes_unicode(self):
        e = gen_fixedtype("·̣─@łæßð~¶½")
        e += gen_datarel("tµŧurułej€", "←ðßðæßđæßæđßŋŋæ @~~·ŋŋ·¶·ŋ“¶¬@@")
        _, s = expression_to_sparql(e)
        self._standard_check(s, e)
        self._sparql_check(s)

    @unittest.skip("should be fixed")
    def test_sparql_ascii_stress(self):
        seed(b"sacala dunga dunga dunga")
        for _ in range(100):
            expression = random_expression(only_ascii=True)
            _, s = expression_to_sparql(expression)
            self._standard_check(s, expression)
            self._sparql_check(s)

    def test_sparql_stress(self):
        seed(b"sacala dunga dunga dunga")
        for _ in range(100):
            expression = random_expression()
            try:
                _, s = expression_to_sparql(expression)
            except ValueError as error:
                if "Unable to generate sparql" in str(error):
                    continue

            self._standard_check(s, expression)
            self._sparql_check(s)

    def test_sparql_takes_fails_ascii1(self):
        e = gen_fixedtype(b"a")
        e += gen_datarel(b"b", b"c")
        e = gen_fixedrelation(b"d", e)
        self.assertRaises(ValueError, expression_to_sparql, e)

    def test_sparql_takes_fails_ascii2(self):
        e = gen_fixedtype(b"\xc2\xb7\xcc\xa3\xe2\x94\x80@\xc5\x82\xc3\xa6\xc3\x9f\xc3\xb0~\xc2\xb6\xc2\xbd")
        e += gen_datarel(b"t\xc2\xb5\xc5\xa7uru\xc5\x82ej\xe2\x82\xac", b"\xe2\x86\x90\xc3\xb0\xc3\x9f\xc3\xb0\xc3\xa6\xc3\x9f\xc4\x91\xc3\xa6\xc3\x9f\xc3\xa6\xc4\x91\xc3\x9f\xc5\x8b\xc5\x8b\xc3\xa6 @~~\xc2\xb7\xc5\x8b\xc5\x8b\xc2\xb7\xc2\xb6\xc2\xb7\xc5\x8b\xe2\x80\x9c\xc2\xb6\xc2\xac@@")
        self.assertRaises(ValueError, expression_to_sparql, e)


if __name__ == "__main__":
    unittest.main()
