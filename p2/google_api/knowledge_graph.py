# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import warnings
import urllib
import requests

from . import API_KEY


warnings.warn('The Knowledge Graph API Search API allows developers a free quota of up to 100,000 (one hundred thousand) read calls per day per project. We believe this meets the needs of the vast majority of developers.')


SEARCH_URL = 'https://kgsearch.googleapis.com/v1/entities:search?query={query}&key={api_key}{params}'


def search_full(query, params=None, timeout=(10, 50)):

    params = '&'+urllib.urlencode(params) if params else ''
    req = requests.get(SEARCH_URL.format(query=query, api_key=API_KEY, params=params), timeout=timeout)
    return req.json() if req.status_code == 200 else None


def search(query, lang=None, limit=30):

    params = dict()
    params['limit'] = limit
    if lang: params['languages'] = lang
    data = search_full(query, params)
    if not data: return None

    elements = data.get('itemListElement', [])
    elements_clean = [{'result': el.get('result', {}), 'score': el.get('resultScore', None)} for el in elements]
    return elements_clean