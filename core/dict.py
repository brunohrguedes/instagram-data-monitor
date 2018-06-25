""" Docstring for dict """
import re

DIGITO = {}

DIGITO['\\u00c7'] = 'Ç'
DIGITO['\\u00e7'] = 'ç'

DIGITO['\\u00c0'] = 'À'
DIGITO['\\u00c1'] = 'Á'
DIGITO['\\u00c2'] = 'Â'
DIGITO['\\u00c3'] = 'Ã'
DIGITO['\\u00c4'] = 'Ä'

DIGITO['\\u00e0'] = 'à'
DIGITO['\\u00e1'] = 'á'
DIGITO['\\u00e2'] = 'â'
DIGITO['\\u00e3'] = 'ã'
DIGITO['\\u00e4'] = 'ä'

DIGITO['\\u00c8'] = 'È'
DIGITO['\\u00c9'] = 'É'
DIGITO['\\u00ca'] = 'Ê'
DIGITO['\\u00cb'] = 'Ë'

DIGITO['\\u00e8'] = 'è'
DIGITO['\\u00e9'] = 'é'
DIGITO['\\u00ea'] = 'ê'
DIGITO['\\u00eb'] = 'ë'

DIGITO['\\u00cc'] = 'Ì'
DIGITO['\\u00cd'] = 'Í'
DIGITO['\\u00ce'] = 'Î'
DIGITO['\\u00cf'] = 'Ï'

DIGITO['\\u00ec'] = 'ì'
DIGITO['\\u00ed'] = 'í'
DIGITO['\\u00ee'] = 'î'
DIGITO['\\u00ef'] = 'ï'

DIGITO['\\u00d2'] = 'Ò'
DIGITO['\\u00d3'] = 'Ó'
DIGITO['\\u00d4'] = 'Ô'
DIGITO['\\u00d5'] = 'Õ'
DIGITO['\\u00d6'] = 'Õ'

DIGITO['\\u00f2'] = 'ò'
DIGITO['\\u00f3'] = 'ó'
DIGITO['\\u00f4'] = 'ô'
DIGITO['\\u00f5'] = 'õ'
DIGITO['\\u00f6'] = 'õ'

DIGITO['\\u00d9'] = 'Ù'
DIGITO['\\u00da'] = 'Ú'
DIGITO['\\u00db'] = 'Û'
DIGITO['\\u00dc'] = 'Ü'

DIGITO['\\u00f9'] = 'ù'
DIGITO['\\u00fa'] = 'ú'
DIGITO['\\u00fb'] = 'û'
DIGITO['\\u00fc'] = 'ü'

DIC = DIGITO

def to_utf8(string):
    """Convert a string to UTF-8""""
    idx = []
    iterator = re.finditer('\\\\u....', string)
    idx = [i.start() for i in iterator]

    if len(idx) == 0:
        return string

    i = 0
    right_string = ''

    for j in idx:
        fatia = string[j:j + 6]
        utf_right = DIC[fatia]
        right_string = right_string + string[i:j] + utf_right
        i = j + 6

    right_string = right_string + string[j+6 : ]

    return right_string
