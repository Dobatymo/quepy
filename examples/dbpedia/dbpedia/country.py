# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Country related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle, Lemmas
from .dsl import IsCountry, IncumbentOf, IncumbentSinceOf, CapitalOf, LeaderOf, LabelOf, LanguageOf, OfficialLanguageOf, PopulationOf, AreaOf


class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)


class LeaderOfQuestion(QuestionTemplate):
    """
    Regex for questions about the leader of a country.
    Ex: "Who is the leader of Argentina?"
    """

    regex = Pos("WP") + Token("is") + Question(Pos("DT")) + \
        (Lemma("leader")|Lemma("president")) + Pos("IN") + Country() + Question(Pos("."))

    def interpret(self, match):
        office = LeaderOf(match.country)
        incumbent = IncumbentOf(office)
        name = LabelOf(incumbent)

        return name, "enum"

class LeaderSinceQuestion(QuestionTemplate):
    regex = Lemmas("Since when is the current leader of") + Country() + Lemmas("in office") + Question(Pos("."))

    def interpret(self, match):
        office = LeaderOf(match.country)
        incumbentsince = IncumbentSinceOf(office)
        since = LabelOf(incumbentsince)

        return since, "literal"


class CapitalOfQuestion(QuestionTemplate):
    """
    Regex for questions about the capital of a country.
    Ex: "What is the capital of Bolivia?"
    """

    opening = Lemma("what") + Token("is")
    regex = opening + Pos("DT") + Lemma("capital") + Pos("IN") + \
        Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        capital = CapitalOf(match.country)
        label = LabelOf(capital)
        return label, "enum"


class OfficialLanguageOfQuestion(QuestionTemplate):
    """
    Regex for questions about the language spoken in a country.
    Ex: "What is the language of Argentina?"
        "what language is spoken in Argentina?"
    """

    openings = (Lemma("what") + Token("is") + Pos("DT") + Lemma("official") + Lemma("language")) | \
               (Lemma("what") + Lemma("language") + Token("is") + Lemma("speak"))

    regex = openings + Pos("IN") + Question(Pos("DT")) + Country() + \
        Question(Pos("."))

    def interpret(self, match):
        language = OfficialLanguageOf(match.country)
        label = LabelOf(language)
        return label, "enum"


class LanguageOfQuestion(QuestionTemplate):
    """
    Regex for questions about the language spoken in a country.
    Ex: "What is the language of Argentina?"
        "what language is spoken in Argentina?"
    """

    openings = (Lemma("what") + Token("is") + Pos("DT") + Lemma("language")) | \
               (Lemma("what") + Lemma("language") + Token("is") + Lemma("speak"))

    regex = openings + Pos("IN") + Question(Pos("DT")) + Country() + \
        Question(Pos("."))

    def interpret(self, match):
        language = LanguageOf(match.country)
        label = LabelOf(language)
        return label, "enum"


class PopulationOfQuestion(QuestionTemplate):
    """
    Regex for questions about the population of a country.
    Ex: "What is the population of China?"
        "How many people live in China?"
    """

    openings = (Pos("WP") + Token("is") + Pos("DT") +
                Lemma("population") + Pos("IN")) | \
               (Pos("WRB") + Lemma("many") + Lemma("people") +
                Token("live") + Pos("IN"))
    regex = openings + Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        population = PopulationOf(match.country)
        return population, "literal"

class AreaOfQuestion(QuestionTemplate):
    regex = Pos("WP") + Token("is") + Pos("DT") + Lemma("area") + Pos("IN") + Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        area = AreaOf(match.country)
        return area, "area"
