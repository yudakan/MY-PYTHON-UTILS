# -*- coding: utf-8 -*-
import os
import warnings
import io
import base64
import json
import requests

from . import API_KEY


warnings.warn('Current API KEY --> Free first 1000 units/month.')


LABELS_URL = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)


def labels_full(img_content, max_results=1, timeout=(10, 50)):

    req_json = {
        'requests': [
            {
                'image': {
                    'content': base64.b64encode(img_content).decode('utf-8')
                },
                'features': [
                    {
                        'type': 'LABEL_DETECTION',
                        'maxResults': max_results
                    }
                ]
            }
        ]
    }
    req = requests.post(
        LABELS_URL,
        data=json.dumps(req_json),
        headers={'Content-type': 'application/json; charset=utf-8'},
        timeout=timeout
    )
    return req.json() if req.status_code == 200 else None


def labels(img, max_results=1):

    if isinstance(img, io.IOBase): img_content = img.read()
    elif type(img) is str and os.path.exists(img): img_content = open(img, 'rb').read()
    else: img_content = img

    res = labels_full(img_content, max_results=max_results)
    if not res: return res

    return res.get('responses', [{}])[0].get('labelAnnotations', [])