# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import os
import requests

import dictionaries

''' Slack API shortcut :P
    O3O App --> https://api.slack.com/apps/oooO3Oooooo/
'''

API_TOKEN = '¿ owo ?'


def get_channels_full(timeout=(10, 50)):

    req = requests.get(
        'https://slack.com/api/conversations.list',
        headers={'Authorization': 'Bearer ' + API_TOKEN},
        timeout=timeout
    )
    return req.json() if req.status_code == 200 else None


def get_users_full(timeout=(10, 50)):

    req = requests.get(
        'https://slack.com/api/users.list',
        headers={'Authorization': 'Bearer ' + API_TOKEN},
        timeout=timeout
    )
    return req.json() if req.status_code == 200 else None


def send_msg_full(msg, to, data=None, timeout=(10, 50)):

    if not data: data = dict()
    data['channel'] = to
    data['text'] = msg
    req = requests.post(
        'https://slack.com/api/chat.postMessage',
        data=data,
        headers={'Authorization': 'Bearer ' + API_TOKEN},
        timeout=timeout
    )

    return req.json() if req.status_code == 200 else None


def send_file_full(file_content, to, data=None, timeout=(10, 50)):

    if not data: data = dict()

    data['channels'] = ','.join(to) if type(to) is list else to
    if isinstance(file_content, file):
        the_file = {'file': file_content.read()}
        req = requests.post(
            'https://slack.com/api/files.upload',
            data=data,
            files=the_file,
            headers={'Authorization': 'Bearer ' + API_TOKEN},
            timeout=timeout
        )
    else:
        data['content'] = file_content
        req = requests.post(
            'https://slack.com/api/files.upload',
            data=data,
            headers={'Authorization': 'Bearer ' + API_TOKEN},
            timeout=timeout
        )

    return req.json() if req.status_code == 200 else None


def get_channels(keys=None):

    if not keys: keys = ['id', 'name']
    chs = get_channels_full().get('channels', [])
    return [{k[-1] if type(k) is list else k: dictionaries.get_in_deep(ch, k, None) for k in keys} for ch in chs]


def get_users(keys=None):

    if not keys: keys = ['id', 'name', 'real_name', ['profile', 'display_name']]
    users = get_users_full().get('members', [])
    return [{k[-1] if type(k) is list else k: dictionaries.get_in_deep(user, k, None) for k in keys} for user in users]


def send_msg(msg, to):

    if not send_msg_full(msg, to).get('ok', None):
        raise Exception('Error trying to send message.')


def send_file(f, to, title=None, msg=None):

    data = dict()
    data['filename'] = os.path.basename(f.name)
    data['title'] = title if title else data['filename'].upper()
    if msg: data['initial_comment'] = msg

    if not send_file_full(f, to, data=data).get('ok', None):
        raise Exception('Error trying to send file.')
