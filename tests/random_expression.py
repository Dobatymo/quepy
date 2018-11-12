# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals

from builtins import chr
from future.utils import python_2_unicode_compatible

import random
from quepy.expression import Expression


def get_random_unichar():
    # returns only encodable unicode chars
    while True:
        x = random.random()
        if 0.1 > x:
            c = random.choice(" ./\n")
        elif 0.50 > x:
            c = chr(random.randint(65, 122))
        elif 0.85 > x:
            c = chr(random.randint(0, 127))
        else:
            c = chr(random.randint(0, 65535))

        try:
            c.encode("utf-8")
            return c
        except UnicodeEncodeError:
            pass

def random_data(only_ascii=False):
    data = []
    first = True
    while first or 1 / 20 < random.random():
        first = False
        if only_ascii:
            c = chr(random.randint(33, 126))
            data.append(c)
        else:
            c = get_random_unichar()

        data.append(c)
    return "".join(data)


def random_relation(only_ascii=False):
    data = random_data(only_ascii)
    data = data.replace(" ", "")
    if random.random() > 0.05:
        return data

    @python_2_unicode_compatible
    class UnicodeableDummy(object):
        def __str__(self):
            return data
    return UnicodeableDummy()


def random_expression(only_ascii=False):
    """
    operations: new node, add data, decapitate, merge
    """
    mean_size = 20
    xs = [40, 30, 50, 20]
    xs = [x * (1 - random.random()) for x in xs]
    assert all(x != 0. for x in xs)
    new_node, add_data, decapitate, _ = [x / sum(xs) for x in xs]
    expressions = [Expression(), Expression(), Expression(), Expression()]
    while len(expressions) != 1:
        if (1 / mean_size) < random.random():
            # Will start to merge more and will not create new nodes
            new_node = 0.
        # Choose action
        r = random.random()
        if r < new_node:
            # New expression
            expressions.append(Expression())
        elif r < add_data + new_node:
            # Add data
            e = random.choice(expressions)
            e.add_data(random_relation(only_ascii), random_data(only_ascii))
        elif r < decapitate + add_data + new_node:
            # Decapitate
            e = random.choice(expressions)
            e.decapitate(random_relation(only_ascii),
                         reverse=(0.25 < random.random()))
        elif len(expressions) != 1:
            # Merge
            random.shuffle(expressions)
            e2 = expressions.pop()
            e1 = expressions[-1]
            e1 += e2
    return expressions[0]
