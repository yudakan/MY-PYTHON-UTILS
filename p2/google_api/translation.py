# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import warnings
import requests

from . import API_KEY


warnings.warn('Current API KEY --> 500.000 free characters per month.')


LANG_CODES = {
    'amharic': 'am',
    'arabic': 'ar',
    'basque': 'eu',
    'bengali': 'bn',
    'english': 'en',
    'portuguese': 'pt',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'estonian': 'et',
    'finnish': 'fi',
    'french': 'fr',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'hebrew': 'iw',
    'hindi': 'hi',
    'hungarian': 'hu',
    'icelandic': 'is',
    'indonesian': 'id',
    'italian': 'it',
    'japanese': 'ja',
    'kannada': 'kn',
    'korean': 'ko',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'malay': 'ms',
    'malayalam': 'ml',
    'marathi': 'mr',
    'norwegian': 'no',
    'polish': 'pl',
    'romanian': 'ro',
    'russian': 'ru',
    'serbian': 'sr',
    'chinese(prc)': 'zh-cn',
    'slovak': 'sk',
    'slovenian': 'sl',
    'spanish': 'es',
    'swahili': 'sw',
    'swedish': 'sv',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'chinese(taiwan)': 'zh-tw',
    'turkish': 'tr',
    'urdu': 'ur',
    'ukrainian': 'uk',
    'vietnamese': 'vi',
    'welsh': 'cy',
}
TRANSLATE_URL = 'https://translation.googleapis.com/language/translate/v2?key={}'.format(API_KEY)
DETECT_LANG_URL = 'https://translation.googleapis.com/language/translate/v2/detect?key={}'.format(API_KEY)


def detect_lang_full(text, timeout=(10, 50)):
    
    req = requests.post(DETECT_LANG_URL, data={'q': text}, timeout=timeout)
    return req.json() if req.status_code == 200 else None


def translate_full(text, target, source, _format='text', timeout=(10, 50)):

    req_json = {'q': text, 'source': source, 'target': target, 'format': _format}
    req = requests.post(TRANSLATE_URL, data=req_json, timeout=timeout)
    
    return req.json() if req.status_code == 200 else None


def detect_lang(text):
    
    res = detect_lang_full(text)
    if not res: return res
    return res.get('data', {}).get('detections', [[{}]])[0][0].get('language', '')


def translate(text, target, source=None):

    if not source: source = detect_lang(text)
    if not source: return source
    if source == target: return text
    
    res = translate_full(text, target, source)
    if not res: return res
    return res.get('data', {}).get('translations', [{}])[0].get('translatedText', '')
