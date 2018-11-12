# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

"""
Sparql generation code.
"""

from builtins import str

from . import settings
from .dsl import IsRelatedTo
from .expression import isnode

_indent = "  "


def escape(string):
    # type: (str, ) -> str

    string = str(string)
    string = string.replace("\n", "")
    string = string.replace("\r", "")
    string = string.replace("\t", "")
    string = string.replace("\x0b", "")
    if not string or any([x for x in string if 0 < ord(x) < 31]) or \
            string.startswith(":") or string.endswith(":"):
        raise ValueError("Unable to generate sparql: invalid nodes or relation")
    return string


def adapt(x):
    if isnode(x):
        x = "?x{}".format(x)
        return x
    if isinstance(x, str):
        if x.startswith("\"") or ":" in x:
            return x
        return '"{}"'.format(x)
    if isinstance(x, bytes):
        raise ValueError("Argument must be unicode")
    return str(x)


def expression_to_sparql(e, full=False):
    template = "{preamble}\n" +\
               "SELECT DISTINCT {select} WHERE {{\n" +\
               "{expression}\n" +\
               "}}\n"
    head = adapt(e.get_head())
    if full:
        select = "*"
    else:
        select = head
    y = 0
    xs = []
    for node in e.iter_nodes():
        for relation, dest in e.iter_edges(node):
            if relation is IsRelatedTo:
                relation = "?y{}".format(y)
                y += 1
            xs.append(triple(adapt(node), relation, adapt(dest),
                      indentation=1))
    sparql = template.format(preamble=settings.SPARQL_PREAMBLE,
                             select=select,
                             expression="\n".join(xs))
    return select, sparql


def triple(a, p, b, indentation=0):
    a = escape(a)
    b = escape(b)
    p = escape(p)
    s = _indent * indentation + "{0} {1} {2}."
    return s.format(a, p, b)
