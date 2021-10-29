# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import warnings
import urllib
import requests
from bs4 import BeautifulSoup

from .net import DEF_HEADERS, rand_proxy
from .utils import find, norm


warnings.warn('Using proxies!')


def google_sites(query, timeout=(10, 50)):

    query = norm(query, to='str')
    url = 'https://www.google.com/search?q={}&sourceid=chrome&ie=UTF-8'.format(urllib.pathname2url(query).replace('%20', '+'))
    req = requests.get(url, proxies=rand_proxy(), headers=DEF_HEADERS, timeout=timeout)
    result = BeautifulSoup(req.content, 'html.parser') if req.status_code == 200 else None

    query = norm(query, to='unicode')
    if result == None or query not in result.title.text: return None
    
    data = []
    for item in result.find_all('div', class_='yuRUbf'):
        data.append({
            'name' : item.find('span').text,
            'link' : item.find('a').get('href')
        })

    return data


def google_images(query, timeout=(10, 50)):

    url = 'https://www.google.com/search?q={}&tbm=isch&sourceid=chrome&ie=UTF-8'.format(urllib.pathname2url(query).replace('%20', '+'))
    req = requests.get(url, proxies=rand_proxy(), headers=DEF_HEADERS, timeout=timeout)
    result = BeautifulSoup(req.content, 'html.parser') if req.status_code == 200 else None

    if result == None or query not in result.title.text: return None
    page = req.text
    
    data = []
    for item in result.find_all('div', class_='isv-r'):

        if len(item.contents) != 2: continue

        data_id = item.get('data-id')
        p0 = page.find(',"{}",'.format(data_id))
        p1 = find(page, '["http', start=p0, nth_occurrence=2)
        url = page[p1+2: page.find('",', p1)]

        data.append({
            'name' : item.contents[1].get('title'),
            'link' : item.contents[1].get('href'),
            'url' : url if url.startswith('http') else None
        })

    return data


def wikipedia(concept):

    results = google_sites(concept)
    if not results: return []

    urls = []
    for site in results:
        url = site.get('link', '')
        if 'wikipedia' in url:
            urls.append(url)

    return urls


def get_synonyms_wikipedia(url, recursivity_langs=False, langs=None, only_title=False, timeout=(10, 50)):

    url = url.replace('.m.wikipedia.org', '.wikipedia.org')
    current_lang = url[len('https://'):url.find('.wikipedia.org')]

    req = requests.get(url, proxies=rand_proxy(), headers=DEF_HEADERS, timeout=timeout)
    if req.status_code != 200: return {}
    wiki = BeautifulSoup(req.content, 'html.parser')

    title = wiki.find(id='firstHeading')
    title = title.string if title else None
    wiki_concepts = {current_lang: [title.lower()]} if title else {current_lang: []}

    cont = wiki.find('div', class_='mw-parser-output')
    if not only_title and cont:
        for ch in cont.children:

            if ch.name == 'p' and 'mw-empty-elt' not in ch.get('class', ['']):

                bold_concepts = [b.string.lower() if b.string else None for b in ch.find_all('b')]
                bold_concepts = [bc for bc in bold_concepts if bc]
                
                if len(bold_concepts) > 0:
                    wiki_concepts[current_lang].extend(bold_concepts)
                    wiki_concepts[current_lang] = list(set(wiki_concepts[current_lang]))
                    break

    if recursivity_langs:
        for lang in wiki.find_all('a', class_='interlanguage-link-target'):

            if not langs or lang.get('lang', '') in langs:

                wiki_concepts.update(
                    get_synonyms_wikipedia(
                        lang.get('href'),
                        recursivity_langs=False,
                        only_title=only_title
                    )
                )

    return wiki_concepts