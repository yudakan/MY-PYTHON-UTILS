# -*- coding: utf-8 -*-
import os
import subprocess
import unicodedata
from urllib import parse


##################################################
##########             TEXT             ##########
##################################################

def norm_json(data, to='str'):
    ''' It normalizes strings recursively in json (list/dict).
        
        Note:
            Other objects than str/bytes/list/dict will be copied only by reference.

        Returns:
            New normalized json.
    '''

    if type(data) is list:
    
        new_data = []

        for val in data:
            if type(val) is str or type(val) is bytes:
                new_data.append(norm(val, to=to))
            elif type(val) is list or type(val) is dict:
                new_data.append(norm_json(val, to=to))
            else:
                new_data.append(val)

    elif type(data) is dict:
    
        new_data = {}

        for key, val in data.items():
            if type(val) is str or type(val) is bytes:
                new_data[norm(key, to=to)] = norm(val, to=to)
            elif type(val) is list or type(val) is dict:
                new_data[norm(key, to=to)] = norm_json(val, to=to)
            else:
                new_data[norm(key, to=to)] = val

    else: raise Exception('Not a JSON (`{}` found instead) -.-"'.format(type(data)))

    return new_data


def norm(string, to='str'):

    if to == 'bytes':
        return string.encode('utf-8') if type(string) is str else string
    elif to == 'str':
        return string if type(string) is str else string.decode('utf-8')
    else:
        return string


def normalize(s):
    
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_url_params(url, unique_keys=False, filter_key=lambda k, v: True):

    # Prepare
    parsed = parse.urlparse(norm(url))
    params = []

    # Get each parameter
    for k, v in parse.parse_qs(parsed.query).items():
        if unique_keys:
            if filter_key(k, v): params.append((k, v))
        else:
            for vv in v:
                if filter_key(k, vv): params.append((k, vv))

    return tuple(params)


def json_quick_look(data, indent=4):

    if type(data) == dict:
        arr = ['"{}": {}'.format(norm(k), '{...}' if type(v) == dict else '[...]' if type(v) == list else '...') for k, v in data.items()]
        tab = '\n'+' '*indent
        arr_joined = tab + tab.join(arr)
        return '{{\n{}\n}}'.format(arr_joined)

    elif type(data) == list: return '[...]'
    else: return '...'


def find(haystack, needle, start=None, end=None, nth_occurrence=1):

    end = len(haystack) if end == None else end
    pos = -1 if start == None else start-1
    for _ in range(nth_occurrence): pos = haystack.find(needle, pos+1, end)
    return pos


def rfind(haystack, needle, start=None, end=None, nth_occurrence=1):

    pos = (len(haystack) if end == None else end) + 1
    start = 0 if start == None else start
    for _ in range(nth_occurrence): pos = haystack.rfind(needle, start, pos-1)
    return pos


##################################################
##########              OS              ##########
##################################################


def realpath_dir(dir_name):

    return os.path.realpath(os.path.dirname(dir_name))


def mkdir(path, mode=0o0777, exist_ok=False):
    
    if exist_ok and os.path.exists(path): return
    os.mkdir(path, mode=mode)


def makedirs(path, mode=0o0777, exist_ok=False):
    
    os.makedirs(path, mode=mode, exist_ok=exist_ok)


def run(cmd, stdin=None, shell=True):

    proc = subprocess.Popen(
        cmd,
        shell=shell,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate(stdin if stdin else b'')
 
    return proc.returncode, stdout, stderr


def interactive_run(cmd, shell=True):

    proc = subprocess.Popen(
        cmd,
        shell=shell,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
 
    return proc.stdin, proc.stdout, proc.stderr


def add_this_arg(method):
    
    def wrapped(self, *args, **kwargs):
        return method(self, wrapped, *args, **kwargs)
    return wrapped
