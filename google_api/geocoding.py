# -*- coding: utf-8 -*-
import os
import warnings
import urllib
import requests

from . import API_KEY
from .. import utils


warnings.warn('Current API KEY --> ???')


URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'


def geocoding(location, timeout=(10, 50)):

    location = utils.norm(location, to='str')
    location = utils.normalize(location.lower())
    try: address = urllib.parse.quote_plus(location).replace('+', '%20')
    except: return None
    url = URL.format(address, API_KEY)
    req = requests.get(url, timeout=timeout)
    return req.json() if req.status_code == 200 else None


def get_lat_lng(location, single=True):

    res = geocoding(location)
    if not res: return res

    res = res.get('results', None)
    if not res: return {} if single else []
    if single: return res[0].get('geometry', {}).get('location', {})
    return [r.get('geometry', {}).get('location', {}) for r in res]