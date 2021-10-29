# -*- coding: utf-8 -*-
import sys
import inspect
# import random


# KAOMOJI_GOOD = ('^^', 'n.n', 'nwn', '^-^', 'n_n', '^_^', '^w^')
# KAOMOJI_BAD = ('>_<', '>o<', '>.<', '>~<', '>-<', 'ò.ó', 'ò_ó', 'o.ó', 'o_ó', 'è_é', 'e_e', 'e.e', 'è.é')
TPUT = {
    'reset': '\x1b[0m',
    'bright': '\x1b[1m',
    'dim': '\x1b[2m',
    'underscore': '\x1b[4m',
    'blink': '\x1b[5m',
    'reverse': '\x1b[7m',
    'hidden': '\x1b[8m',
    'fg_black': '\x1b[30m',
    'fg_red': '\x1b[31m',
    'fg_green': '\x1b[32m',
    'fg_yellow': '\x1b[33m',
    'fg_blue': '\x1b[34m',
    'fg_magenta': '\x1b[35m',
    'fg_cyan': '\x1b[36m',
    'fg_white': '\x1b[37m',
    'bg_black': '\x1b[40m',
    'bg_red': '\x1b[41m',
    'bg_green': '\x1b[42m',
    'bg_yellow': '\x1b[43m',
    'bg_blue': '\x1b[44m',
    'bg_magenta': '\x1b[45m',
    'bg_cyan': '\x1b[46m',
    'bg_white': '\x1b[47m'
}


# def get_kaomoji(type):

#     return KAOMOJI_GOOD[random.randint(1, len(KAOMOJI_GOOD)) - 1]


def context_print(tell_me, end='\n', file=sys.stderr):

    itself = inspect.stack()[1][0].f_locals.get('self', None)
    class_name = itself.__class__.__name__ + '.' if itself != None else ''
    function_name = inspect.stack()[1][3]

    msg = '{}{} --> {}'.format(class_name, function_name, tell_me)
    if file == 'str': return '{}{}'.format(msg, end)
    print(msg, end=end, file=file)


def stylized_print(mode, tell_me, end='\n', file=sys.stderr):
    ''' Note: Use TPUT keys to reference a mode
            Mode can be a list
    '''

    if type(mode) is list: _mode = ''.join(TPUT.get(m, '') for m in mode)
    else: _mode = TPUT.get(mode, '')
    _reset = TPUT['reset']

    msg = '{}{}{}'.format(_mode, tell_me, _reset)
    if file == 'str': return '{}{}'.format(msg, end)
    print(msg, end=end, file=file)

    
def info_print(tell_me, context=True, deep=0, ch='-', file=sys.stderr):

    msg = context_print(tell_me, end='', file='str') if context else tell_me
    msg = '{}{} {}'.format(deep*'   ', '[{}]'.format(ch) if ch else '', msg)
    
    if file == 'str': return msg
    print(msg, file=file)


def ok_print(tell_me, context=False, deep=0, ch='-', file=sys.stderr):

    msg = info_print(tell_me, context=context, deep=deep, ch=ch, file='str')
    stylized_print('fg_white', msg, file=file)


def sub_print(tell_me, context=False, deep=0, ch='', file=sys.stderr):

    msg = info_print('↳ {}'.format(tell_me), context=context, deep=deep, ch=ch, file='str')
    stylized_print('fg_white', msg, file=file)


def warning_print(tell_me, context=False, deep=0, ch='!', file=sys.stderr):

    msg = info_print(tell_me, context=context, deep=deep, ch=ch, file='str')
    stylized_print('fg_yellow', msg, file=file)


def fine_print(tell_me, context=False, deep=0, ch='#', file=sys.stderr):

    msg = info_print(tell_me, context=context, deep=deep, ch=ch, file='str')
    stylized_print('fg_green', msg, file=file)


def err_print(tell_me, as_exception=False, exit_code=None, context=False, deep=0, ch='@', file=sys.stderr):

    msg = info_print(tell_me, context=context, deep=deep, ch=ch, file='str')

    if as_exception: raise Exception(stylized_print('fg_red', msg.strip(), file='str'))
    stylized_print('fg_red', msg, file=file)
    if type(exit_code) is int: sys.exit(exit_code)


def elegant_ctrl_c(function):

    def _elegant_ctrl_c(*args, **kwargs):
        try: function(*args, **kwargs)
        except KeyboardInterrupt:
            stylized_print(['fg_red', 'bright'], '   CTRL + C', file=sys.stderr)
            sys.exit(1)
        
    return _elegant_ctrl_c
