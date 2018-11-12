# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

"""
Tests for tagger.
"""

from builtins import str

import unittest
from quepy import tagger

au = "æßđħłłþłłł@æµß"
bu = "ŧłþłßæ#¶ŋħ~#~@"
cu = "øĸŋøħþ€ĸłþ€øæ«»¢"

ab = au.encode("utf-8")
bb = bu.encode("utf-8")
cb = cu.encode("utf-8")

class TestTagger(unittest.TestCase):
    def test_tagset_unicode(self):
        for tag in tagger.PENN_TAGSET:
            self.assertIsInstance(tag, str)

    def test_word_encoding(self):
        word = tagger.Word(token=au, lemma=bu, pos=cu)

        self.assertIsInstance(word.token, str)
        self.assertEqual(word.token, au)
        self.assertIsInstance(word.lemma, str)
        self.assertEqual(word.lemma, bu)
        self.assertIsInstance(word.pos, str)
        self.assertEqual(word.pos, cu)

    def test_word_wrong_encoding(self):

        # Token not unicode
        self.assertRaises(TypeError, tagger.Word, ab, bu, cu)
        # Lemma not unicode
        self.assertRaises(TypeError, tagger.Word, au, bb, cu)
        # Pos not unicode
        self.assertRaises(TypeError, tagger.Word, au, bu, cb)

    def test_word_attrib_set(self):
        word = tagger.Word(au)
        word.lemma = bu
        word.pos = cu

        self.assertIsInstance(word.token, str)
        self.assertEqual(word.token, au)
        self.assertIsInstance(word.lemma, str)
        self.assertEqual(word.lemma, bu)
        self.assertIsInstance(word.pos, str)
        self.assertEqual(word.pos, cu)

    def test_word_wrong_attrib_set(self):
        word = tagger.Word(au)

        # Token not unicode
        self.assertRaises(TypeError, setattr, word, "token", ab)
        # Lemma not unicode
        self.assertRaises(TypeError, setattr, word, "lemma", bb)
        # Pos not unicode
        self.assertRaises(TypeError, setattr, word, "pos", cb)


if __name__ == "__main__":
    unittest.main()
