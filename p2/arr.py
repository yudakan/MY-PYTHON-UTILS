# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division


def flat_sm(arr, value=None, only_first=False):

    if len(arr) == 0:
        return value
    
    if len(arr) == 1 or only_first:
        _id = 0 if type(arr) is list else arr.keys()[0]
        return arr[_id]

    return arr