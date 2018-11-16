# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

"""
Tagging using NLTK.
"""

# Required data files are:
#   - "averaged_perceptron_tagger" in Models
#   - "wordnet" in Corpora

from builtins import str
from future.utils import iteritems

import nltk
from nltk.corpus import wordnet

from .tagger import Word


class run_nltktagger(object):

	_penn_to_morphy_tag = {
		'NN': wordnet.NOUN,
		'JJ': wordnet.ADJ,
		'VB': wordnet.VERB,
		'RB': wordnet.ADV,
	}

	def __init__(self, nltk_data_path=None):
		if nltk_data_path:
			nltk.data.path = nltk_data_path

	def penn_to_morphy_tag(self, tag):
		# type: (str, ) -> Optional[str]

		for penn, morphy in iteritems(self._penn_to_morphy_tag):
			if tag.startswith(penn):
				return morphy
		return None

	def __call__(self, string):
		# type: (str) -> List[str]

		"""
		Runs nltk tagger on `string` and returns a list of
		:class:`quepy.tagger.Word` objects.
		"""

		if not isinstance(string, str):
			raise TypeError("Input must be a unicode string")

		# Recommended tokenizer doesn't handle non-ascii characters very well
		#tokens = nltk.word_tokenize(string)
		tokens = nltk.wordpunct_tokenize(string)
		tags = nltk.pos_tag(tokens)

		words = []
		for token, pos in tags:
			word = Word(token)
			# Eliminates stuff like JJ|CC
			word.pos = pos.split("|")[0]

			mtag = self.penn_to_morphy_tag(word.pos)
			# Nice shooting, son. What's your name?
			word.lemma = wordnet.morphy(word.token, pos=mtag)
			if not word.lemma:
				word.lemma = word.token.lower()

			words.append(word)

		return words
