# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

from __future__ import absolute_import, unicode_literals

from future.utils import python_2_unicode_compatible
from builtins import str

import logging

from . import settings

logger = logging.getLogger("quepy.tagger")
PENN_TAGSET = set("$ `` '' ( ) , -- . : CC CD DT EX FW IN JJ JJR JJS LS MD "
    "NN NNP NNPS NNS PDT POS PRP PRP$ RB RBR RBS RP SYM TO UH "
    "VB VBD VBG VBN VBP VBZ WDT WP WP$ WRB".split())


class TaggingError(Exception):
    """
    Error parsing tagger's output.
    """
    pass

class run_spacytagger(object):

	def __init__(self):
		import spacy
		self.nlp = spacy.load("en")

	@staticmethod
	def convert_to_quepy(doc):
		for ent in doc:
			w = Word(ent.text)
			w.pos = ent.tag_
			w.lemma = ent.lemma_
			yield w

	def __call__(self, string):
		return list(self.convert_to_quepy(self.nlp(string)))

@python_2_unicode_compatible
class Word(object):
    """
    Representation of a tagged word.
    Contains *token*, *lemma*, *pos tag* and optionally a *probability* of
    that tag.
    """

    __slots__ = ("_token", "_lemma", "_pos", "prob")

    def __init__(self, token, lemma=None, pos=None, prob=None):

        self.token = token
        self.lemma = lemma
        self.pos = pos
        self.prob = prob

    def __str__(self):
        return "|".join([self._token, self._lemma, self._pos, self.prob])

    def __repr__(self):
        return str(self)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        if not isinstance(value, str):
            raise TypeError("Input must be str, not {}".format(type(value)))

        self._token = value

    @property
    def lemma(self):
        return self._lemma

    @lemma.setter
    def lemma(self, value):
        if value and not isinstance(value, str):
            raise TypeError("Input must be str, not {}".format(type(value)))

        self._lemma = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if value and not isinstance(value, str):
            raise TypeError("Input must be str, not {}".format(type(value)))

        self._pos = value

def get_tagger():
    # type: () -> Callable

    """
    Return a tagging function given some app settings.
    `Settings` is the settings module of an app.
    The returned value is a function that receives a string and returns
    a list of `Word` instances.
    """

    from quepy.nltktagger import run_nltktagger as pos_tagger
    # pos_tagger = run_spacytagger

    tagger_function = pos_tagger(settings.NLTK_DATA_PATH)

    def wrapper(string):
        # type: (str, ) -> List[str]

        words = tagger_function(string)
        for word in words:
            if word.pos not in PENN_TAGSET:
                logger.warning("Tagger emitted a non-penn POS tag {!r}".format(word.pos))
        return words
    return wrapper
