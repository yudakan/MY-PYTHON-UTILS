# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division


def _diff(a, b, give_me_dic_a_in_b, ignore_key=None):

    if not ignore_key:

        for dic_a in a:
            if (dic_a not in b) ^ give_me_dic_a_in_b:
                yield dic_a

    else:

        ignore_key = set(ignore_key)

        for dic_a in a:
            dic_a_in_b = False
            for dic_b in b:
                
                dica_equal_dicb = True
                for dic_a_k in dic_a:
                    if dic_a_k in ignore_key: continue
                    if dic_a_k not in dic_b or dic_a[dic_a_k] != dic_b[dic_a_k]:
                        dica_equal_dicb = False
                        break

                if dica_equal_dicb:
                    for dic_b_k in dic_b:
                        if dic_b_k in ignore_key: continue
                        if dic_b_k not in dic_a or dic_b[dic_b_k] != dic_a[dic_b_k]:
                            dica_equal_dicb = False
                            break
                
                if dica_equal_dicb:
                    dic_a_in_b = True
                    break

            if (not dic_a_in_b) ^ give_me_dic_a_in_b: yield dic_a


def subtraction(a, b, ignore_key=None):
    ''' It gives the items in a but not in b.

        Args:
            a (list of dicts): A list (where each item is a dictionary if ignore_key is set).
            b (list of dicts): A list (where each item is a dictionary if ignore_key is set).
            ignore_key (list of str): A list containing those keys (shared among all items)
                that will not be compared.

        Returns:
            items in a but not in b (generator)
    '''

    return _diff(a, b, False, ignore_key=ignore_key)


def intersection(a, b, ignore_key=None):
    ''' It gives the items in both a and b.

        Args:
            a (list of dicts): A list (where each item is a dictionary if ignore_key is set).
            b (list of dicts): A list (where each item is a dictionary if ignore_key is set).
            ignore_key (list of str): A list containing those keys (shared among all items)
                that will not be compared.

        Returns:
            items in both (generator)
    '''

    return _diff(a, b, True, ignore_key=ignore_key)


def clean(data, ignore_key=None):
    ''' It removes duplicate dictionaries in a list.

        Args:
            data (list of dicts): A list where each item is a dictionary.
            ignore_key (list of str): A list containing those keys that will not be
                compared to remove or pass duplicate elements.

        Returns:
            Clean list.
    '''

    ignored_ones = []
    clean_data = []

    for reg in data:

        if ignore_key != None:
            ignored_keys = []
            for ig_k_k in ignore_key: ignored_keys.append([ig_k_k, reg.pop(ig_k_k, None)])
        
        if reg not in clean_data:

            if ignore_key != None:
                ignored_ones.append([[len(clean_data)]+ig_k for ig_k in ignored_keys if ig_k[1] != None])

            clean_data.append(reg)

    if ignore_key != None:
        for ig in ignored_ones:
            for ig_k in ig: clean_data[ig_k[0]][ig_k[1]] = ig_k[2]

    return clean_data


def group_by_key(key, data, clean_redundancy=False, redundancy_ignore_key=None):
    ''' Groups items in a dictionary by key, but we can customize the process

        Args:
            key (str): Comparative key.
            data (list of dicts): A list where each item is a dictionary (these dicts must have the key).
            clean_redundancy (bool): Indicates whether duplicate items are removed or not.
            redundancy_ignore_key (list of str): If clean_redundancy is set to True, a list containing
                those keys that will not be compared to remove or pass duplicate elements.

        Returns:
            Dictionary {key0: [items], ...}
    '''

    if clean_redundancy: data = clean(data, ignore_key=redundancy_ignore_key)

    unique_keys = list(set(reg[key] for reg in data))
    return {current_key: [{k: reg[k] for k in reg if k != key} for reg in data if reg[key] == current_key] for current_key in unique_keys}


def get_in_deep(dic, keys, value=None):
    ''' Navigate through nested dictionaries, key by key, until the end value (the deepest) is returned.

        Args:
            dic (dict): Nested dictionaries.
            keys (list): Keys list.
            value (): Value to be returned if some key is not found.
    '''

    if type(keys) is not list: return dic.get(keys, value)

    last = dic
    for k in keys:
        last = last.get(k, value)
        if last == None:
            break

    return last