#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

"""
Tests for nltktagger.
"""

import unittest
from quepy import nltktagger
from quepy.tagger import Word


class TestNLTKTagger(unittest.TestCase):
    def test_word_output(self):
        output = nltktagger.run_nltktagger("this is a test case «¢ðßæŋħħ")

        self.assertIsInstance(output, list)
        for word in output:
            self.assertIsInstance(word, Word)

    def tests_wrong_input(self):
        self.assertRaises(TypeError, nltktagger.run_nltktagger, b"this is not unicode")


if __name__ == "__main__":
    unittest.main()
