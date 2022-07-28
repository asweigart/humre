"""Humre
By Al Sweigart al@inventwithpython.com

A human-readable regular expression module for Python."""

# TODO - do performance testing on all these string concats

import re
from typing import ParamSpecArgs

__version__ = '0.1.0'

decimal = r'\d'  # TODO - maybe digit is the better name here?
word = r'\w'  # TODO - word or wordchar?
whitespace = r'\s'
nondecimal = r'\D'
nonword = r'\W'
nonwhitespace = r'\S'

# Custom character classes - TODO do we want these?
#letter = '[a-zA-Z]'
#nonletter = '[^a-zA-Z]'
#uppercase = '[A-Z]'
#nonuppercase = '[^A-Z]'
#lowercase = '[a-z]'
#nonlowercase = '[^a-z]'
#alphanumeric = '[a-zA-Z0-9]'
#nonalphanumeric = '[^a-zA-Z0-9]'
#digit = '[0-9]'
hexadecimal = '[0-9a-fA-F]'
nonhexadecimal = '[^0-9a-fA-F]'




anything = '.*?'  # TODO - better name "lazy_anything"?
everything = '.*'  # TODO - better name "greedy_anything"?
something = '.+' # TODO - better name?


anychar = '.'  # TODO - better name "dot"? I don't think so, that's just the name of the regex operator.




# labels for escaped regex metacharacters: . ^ $ * + ? { } [ ] \ | ( )
# This full list copied from https://docs.python.org/3/howto/regex.html
# TODO - these names... figure it out
period = r'\.'
caret = r'\^'
dollar_sign = r'\$'
asterisk = r'\*'
plus_sign = r'\+'
question_mark = r'\?'
open_brace = r'\{'
close_brace = r'\}'
open_bracket = r'\['
close_bracket = r'\]'
backslash = r'\\'
pipe = r'\|'
open_paren = open_parenthesis = r'\('
close_paren = close_parenthesis = r'\)'

newline = r'\n' # TODO - double check this: do I want r'\n' or '\n' here?
tab = r'\t'
quote = r"\'"
double_quote = r'\"'

# TODO - should it be *_group() or group_*()?


def esc(*regexStrs):
    return re.escape(''.join(regexStrs))

def compile(*regexStrs, **kwargs):  # TODO fix type hint
    # This is a wrapper for re.compile(), but we don't call it compile() because there's already a built-in function named that.
    return re.compile(''.join(regexStrs), flags=kwargs.get('flags', 0))

def group(*regexStrs):  # type: (str) -> str
    return '(' + ''.join(regexStrs) + ')'

def named_group(name, *regexStrs):  # type: (str, str) -> str
    return '(?P<' + str(name) + '>' + ''.join(regexStrs) + ')'

# TODO - is there a better name than this?
def noncapturing_group(*regexStrs):
    return '(?:' + ''.join(regexStrs) + ')'

def optional(*regexStrs):  # type: (str) -> str
    return ''.join(regexStrs) + '?'

def either(*regexStrs): # TODO - it's going to be really easy to get this wrong when people pass multiple comma-separated arguments when they intended to pass fewer string arguments in. How do we avoid this problem?
    return '|'.join(regexStrs)

def exactly(quantity, *regexStrs):  # type: (int, str) -> str
    if not isinstance(quantity, int):
        raise TypeError('quantity must be a positive int')
    if quantity < 0:
        raise ValueError('quantity must be a positive int')
    return ''.join(regexStrs) + '{' + str(quantity) + '}'

def between(minimum, maximum, *regexStrs):  # type: (int, int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    return ''.join(regexStrs) + '{' + str(minimum) + ',' + str(maximum) + '}'

def at_least(minimum, *regexStrs):  # type: (int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    return ''.join(regexStrs) + '{' + str(minimum) + ',}'

def at_most(maximum, *regexStrs):  # type: (int, str) -> str
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    return ''.join(regexStrs) + '{,' + str(maximum) + '}'

def zero_or_more(*regexStrs):  # type: (str) -> str
    return ''.join(regexStrs) + '*'

def one_or_more(*regexStrs):  # type: (str) -> str
    return ''.join(regexStrs) + '+'

def starts_with(*regexStrs):  # type: (str) -> str
    return '^' + ''.join(regexStrs)

def ends_with(*regexStrs):  # type: (str) -> str
    return ''.join(regexStrs) + '$'

def starts_and_ends_with(*regexStrs):  # type: (str) -> str
    return '^' + ''.join(regexStrs) + '$'

def chars(*regexStrs):  # type: (str) -> str
    return '[' + ''.join(regexStrs) + ']'

def nonchars(*regexStrs):  # type: (str) -> str
    return '[^' + ''.join(regexStrs) + ']'



# TODO - should I have these group_*() functions? It does help cut down on the parentheses hell.
def optional_group(*regexStrs):  # type: (str) -> str
    return '(' + ''.join(regexStrs) + ')?'

def group_either(*regexStrs):
    return '(' + either(*regexStrs) + ')'

def group_exactly(quantity, *regexStrs):  # type: (int, str) -> str
    if not isinstance(quantity, int):
        raise TypeError('quantity must be a positive int')
    if quantity < 0:
        raise ValueError('quantity must be a positive int')
    return '(' + ''.join(regexStrs) + '{' + str(quantity) + '}' + ')'

def group_between(minimum, maximum, *regexStrs):  # type: (int, int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    return '(' + ''.join(regexStrs) + '{' + str(minimum) + ',' + str(maximum) + '})'

def group_at_least(minimum, *regexStrs):  # type: (int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    return '(' + ''.join(regexStrs) + '{' + str(minimum) + ',})'

def group_at_most(maximum, *regexStrs):  # type: (int, str) -> str
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    return '(' + ''.join(regexStrs) + '{,' + str(maximum) + '})'

def zero_or_more_group(*regexStrs):  # type: (str) -> str
    return '(' + ''.join(regexStrs) + ')*'

def one_or_more_group(*regexStrs):  # type: (str) -> str
    return '(' + ''.join(regexStrs) + ')+'

def group_chars(*regexStrs):  # type: (str) -> str
    return '([' + ''.join(regexStrs) + '])'

def group_nonchars(*regexStrs):  # type: (str) -> str
    return '([^' + ''.join(regexStrs) + '])'

