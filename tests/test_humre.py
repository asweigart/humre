from __future__ import division, print_function
import pytest

from humre import *
import re

def test_random_regexes_I_found_online():
    # Basic American phone number regex:
    assert r'\d\d\d-\d\d\d-\d\d\d\d' == digit + digit + digit + '-' + digit + digit + digit + '-' + digit + digit + digit + digit

    # Basic American phone number regex using {3}:
    #assert r'\d{3}-\d{3}-\d{4}' == exactly_3(digit) + '-' + exactly_3(digit) + '-' + exactly_4(digit)
    assert r'\d{3}-\d{3}-\d{4}' == exactly(3, digit) + '-' + exactly(3, digit) + '-' + exactly(4, digit)

    # American phone number with groups:
    assert r'(\d{3})-(\d{3}-\d{4})' == group(exactly(3, digit)) + '-' + group(exactly(3, digit) + '-' + exactly(4, digit))

    assert 'First Name: (.*?)' == 'First Name: ' + group(anything)
    assert 'First Name: (.*)' == 'First Name: ' + group(everything)

    assert 'x*' == zero_or_more('x')
    assert 'x+' == one_or_more('x')

    assert 'x{3,5}' == between(3, 5, 'x')
    assert 'x{2,}' == at_least(2, 'x')

    assert 'x{,2}' == at_most(2, 'x')

    assert '^x' == starts_with('x')
    assert 'x$' == ends_with('x')
    assert '^x$' == starts_and_ends_with('x')

    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == \
        group(
            # Area code:
            optional(group(either(exactly(3, digit), open_paren + exactly(3, digit) + close_paren))) +
            optional(group(either(whitespace, '-', r'\.'))) +
            # First three digits:
            exactly(3, digit) +
            group(either(whitespace, '-', r'\.')) +
            # Last four digits:
            exactly(4, digit) +
            # Optional extension:
            optional(group(zero_or_more(whitespace) + group(either('ext', 'x', 'ext.')) + zero_or_more(whitespace) + between(2, 5, digit)))
            )

    # Use commas instead of + str concatenation:
    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == \
        group(
            optional(group(either(exactly(3, digit), open_paren + exactly(3, digit) + close_paren))),
            optional(group(either(whitespace, '-', r'\.'))),
            exactly(3, digit),
            group(either(whitespace, '-', r'\.')),
            exactly(4, digit),
            optional(group(zero_or_more(whitespace),
                     group(either('ext', 'x', 'ext.')),
                     zero_or_more(whitespace),
                     between(2, 5, digit)))
            )

    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == \
        group(
            optional_group(either(exactly(3, digit), r'\(' + exactly(3, digit) + r'\)')) +
            optional_group(either(whitespace, '-', r'\.')) +
            exactly(3, digit) +
            group_either(whitespace, '-', r'\.') +
            exactly(4, digit) +
            optional_group(zero_or_more(whitespace) + group(either('ext', 'x', 'ext.')) + zero_or_more(whitespace) + between(2, 5, digit))
            )

    assert '[YZ][BCE-HMO-Y][BEFN][A-Z][0-9][0-9]_KWBC_[0-9]{6}' == chars('YZ') + chars('BCE-HMO-Y') + chars('BEFN') + chars('A-Z') + chars('0-9') + chars('0-9') + '_KWBC_' + exactly(6, chars('0-9'))
    assert r'\s*\\\\$' == ends_with(zero_or_more(whitespace) + '\\\\\\\\')

    assert r"^Access:" == starts_with('Access:')

    import string
    assert "Check[ ]?sum[ ]+is[ ]+([{}])".format(string.printable) == \
        'Check' + optional(chars(' ')) + 'sum' + one_or_more(chars(' ')) + 'is' + one_or_more(chars(' ')) + group(chars(string.printable))
    # Use ''.join() so that I can have commas instead.
    assert "Check[ ]?sum[ ]+is[ ]+([{}])".format(string.printable) == \
        ''.join((
            # The word 'Checksum' with optional space between 'check' and 'sum':
            'Check', optional(chars(' ')), 'sum',
            # One or more spaces:
            one_or_more(chars(' ')),
            # The word 'is':
            'is',
            # One or more spaces:
            one_or_more(chars(' ')),
            # A printable character:
            group(chars(string.printable))
            ))

    assert r'[-]?\d\n' == optional(chars('-')) + digit + newline

    assert r'Student has an ([A-D]) grade' == 'Student has an ' + group(chars('A-D')) + ' grade'

    assert r'([-]?\d+) is the median' == group(optional(chars('-')), one_or_more(digit)) + ' is the median'

    assert '^[A-Z0-9]' == starts_with(chars('A-Z0-9'))

    assert r"\s(\S):\s" == whitespace + group(nonwhitespace) + ':' + whitespace
    assert r"\s(\S):\s" == ''.join([whitespace, group(nonwhitespace), ':', whitespace])
    assert re.compile(r"\s(\S):\s") == compile(whitespace, group(nonwhitespace), ':', whitespace)
    assert re.compile(r"\s(\S):\s") == re.compile(''.join((whitespace, group(nonwhitespace), ':', whitespace)))


    assert r"\*([^\*]+)\*" == asterisk + group(one_or_more(nonchars(asterisk))) + asterisk

    assert zero_or_more(backslash) == r'\\*'
    assert asterisk == r'\*'

    assert r"\s+" == one_or_more(whitespace)

    assert "^yslogin[0-9]+" == starts_with('yslogin', one_or_more(chars('0-9')))

    assert r"\$\((?P<name>[A-Za-z0-9_]+)\)" == dollar_sign + open_paren + named_group('name', one_or_more(chars('A-Za-z0-9_'))) + close_paren

    assert "ccd id: \\d+" == 'ccd id: ' + one_or_more(digit)

    #assert "[%:\r\n]" == chars(r'%:\r\n')  # Test this: is there a difference between "[%:\r\n]" and r"[%:\r\n]"

    assert "%([0-9a-fA-F][0-9a-fA-F])" == '%' + group(chars('0-9a-fA-F'), chars('0-9a-fA-F'))

    assert r'\?sid=(?P<sid>\d+)' == question_mark + 'sid=' + named_group('sid', one_or_more(digit))

    assert 'INPUT.*NAME="seui".*VALUE="(?P<uid>[^"]*)"' == 'INPUT' + everything + 'NAME="seui"' + everything + \
        'VALUE="' + named_group('uid', zero_or_more(nonchars('"'))) + '"'

    assert 'INPUT.*NAME="sdn".*VALUE="(?P<rnm>[^"]*)"' == 'INPUT' + everything + 'NAME="sdn"' + everything + \
        'VALUE="' + named_group('rnm', zero_or_more(nonchars('"'))) + '"'

    assert 'OPTION VALUE="(?P<mod>[^"]*)" SELECTED' == 'OPTION VALUE="' + named_group('mod', zero_or_more(nonchars('"'))) + '" SELECTED'

    assert 'INPUT.*NAME="sena" VALUE="(?P<ena>[^"]*)" CHECKED' == 'INPUT' + everything + 'NAME="sena" VALUE="' + \
        named_group('ena', zero_or_more(nonchars('"'))) + '" CHECKED'

    assert r"[.?!]" == chars('.?!')  # Functionally equivalent to chars(period + question_mark + '!')

    assert r"[A-Z]\w+" == chars('A-Z') + one_or_more(word)

    # This has a bug in it because the . dots can match anything:
    assert r'^pip-.*(zip|tar.gz|tar.bz2|tgz|tbz)$' == starts_and_ends_with('pip-' + everything + group_either('zip', 'tar.gz', 'tar.bz2', 'tgz', 'tbz'))

    assert r'/Python(?:-32|-64)*$' == '/Python' + ends_with(zero_or_more(noncapturing_group(either('-32', '-64'))))

    assert r'^CPU\(s\):\s*(\d+)' == starts_with('CPU' + open_paren + 's' + close_paren + ':' + zero_or_more(whitespace)) + group(one_or_more(digit))

    assert '^GOOGLE_RELEASE=(.+)$' == starts_and_ends_with('GOOGLE_RELEASE=', group(one_or_more(anychar)))

    assert '^(.+)=(.+)$' == starts_and_ends_with(group(greedy_something), '=', group(greedy_something))

    assert '<.*?>' == '<' + anything + '>'

    assert r'chr(\d+):(\d+)(-(\d+))?' == 'chr' + group(one_or_more(digit)) + ':' + group(one_or_more(digit)) + \
        optional_group('-', group(one_or_more(digit)))

    assert r'chr(\d+)(:(\d+)(-(\d+))?)?' == 'chr' + group(one_or_more(digit)) + \
        optional_group(':', group(one_or_more(digit)), optional_group('-', group(one_or_more(digit))))

    assert "[^a-zA-Z0-9']+" == one_or_more(nonchars("a-zA-Z0-9'"))

    # Purposefully left this as a non-raw string:
    assert re.compile(r"<person>([,\s]*(and)*[,\s]*<person>)+") == compile('<person>',
        one_or_more_group(zero_or_more(chars(r',\s')), zero_or_more_group('and'),
            zero_or_more(chars(r',\s')), '<person>'))

    #assert re.compile(r"[()[\].,|:;?!=+~\-\/{}]") == compile(chars('()[\].,|:;?!=+~\-\/{}'))
    assert re.compile(r"[()[].,|:;?!=+~-/{}]") == compile(chars('()[].,|:;?!=+~-/{}'))

    assert re.compile('''['"`]''') == compile(chars("""'"`"""))

    assert re.compile(r'(\s*"+\s*)+') == compile(one_or_more_group(zero_or_more(whitespace), one_or_more('"'),
            zero_or_more(whitespace)))

    assert re.compile(r"(\d),(\d{3})") == compile(group(digit), ',', group(exactly(3, digit)))

    assert r"(\w)\.(\w)" == group(word) + period + group(word)

    # TODO - research: positive lookahead and negative lookahead (?=
    #assert r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)" == "'" + group()

    assert r'<math.*?alttext="\{\\displaystyle (.*?)\}"' == '<math' + anything + 'alttext="' + open_brace + backslash +\
        'displaystyle ' + group(anything) + close_brace + '"'

    assert r'([^-+.:0-9])+' == one_or_more_group(nonchars('-+.:0-9'))

    assert r'(\d+)' == group(one_or_more(digit))

    assert r"(\w+(\W*\d+\W*)?\-?\w*?[^\S\t]*)*" == \
        zero_or_more_group(
            one_or_more(word),
            optional_group(zero_or_more(nonword), one_or_more(digit), zero_or_more(nonword)),
            optional(r'\-'),
            optional(zero_or_more(word)),
            zero_or_more(nonchars(nonwhitespace, tab)),
        )

    assert r"(\w+(\W*\d+\W*)?\-?\w*?[^\S\t]*)*" == zero_or_more_group(one_or_more(word),
        optional_group(zero_or_more(nonword), one_or_more(digit), zero_or_more(nonword)), optional('\\-'),
        optional(zero_or_more(word)), zero_or_more(nonchars(nonwhitespace, tab)))

    assert r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)" == "'" + positive_lookahead(group_either(
        chars('stdm'), group('ll'), group('re'), group('ve'), group('ll')), boundary)

    assert r"(\s*,+\s*)+" == one_or_more_group(zero_or_more(whitespace), one_or_more(','), zero_or_more(whitespace))

    assert r'[\W_]' == chars(nonword, '_')


def test_esc():
    assert esc(r'hello') == re.escape(r'hello') == 'hello'

    for char in '.^$*+?{}[]\\|()':
        assert esc(char) == re.escape(char)

    assert esc(r'+') == re.escape(r'+') == r'\+'

def test_compile():
    assert compile('hello') == re.compile('hello')
    assert compile('hello', flags=IGNORECASE | DOTALL) == re.compile('hello', re.IGNORECASE | re.DOTALL)

    assert compile('hello', flags=A) == re.compile('hello', re.A)
    assert compile('hello', flags=ASCII) == re.compile('hello', re.ASCII)
    assert compile('hello', flags=DEBUG) == re.compile('hello', re.DEBUG)
    assert compile('hello', flags=I) == re.compile('hello', re.I)
    assert compile('hello', flags=IGNORECASE) == re.compile('hello', re.IGNORECASE)
    # Humre is not going to support bytes objects, which LOCALE requires.
    #assert compile(b'hello', flags=L) == re.compile(b'hello', re.L)
    #assert compile(b'hello', flags=LOCALE) == re.compile(b'hello', re.LOCALE)
    assert compile('hello', flags=M) == re.compile('hello', re.M)
    assert compile('hello', flags=MULTILINE) == re.compile('hello', re.MULTILINE)
    assert compile('hello', flags=S) == re.compile('hello', re.S)
    assert compile('hello', flags=DOTALL) == re.compile('hello', re.DOTALL)
    assert compile('hello', flags=X) == re.compile('hello', re.X)
    assert compile('hello', flags=VERBOSE) == re.compile('hello', re.VERBOSE)

def test_group():
    assert group('cat') == '(cat)'
    assert group('cat', 'dog', 'moose') == '(catdogmoose)'
    assert group('cat', group('dog', 'moose')) == '(cat(dogmoose))'
    assert group('cat', group('dog', group('moose'))) == '(cat(dog(moose)))'


def test_positive_lookahead():
    assert positive_lookahead('cat') == '(?=cat)'
    assert positive_lookahead('cat', 'dog', 'moose') == '(?=catdogmoose)'

def test_negative_lookahead():
    assert negative_lookahead('cat') == '(?!cat)'
    assert negative_lookahead('cat', 'dog', 'moose') == '(?!catdogmoose)'

def test_positive_lookbehind():
    assert positive_lookbehind('cat') == '(?<=cat)'
    assert positive_lookbehind('cat', 'dog', 'moose') == '(?<=catdogmoose)'

def test_negative_lookbehind():
    assert negative_lookbehind('cat') == '(?<!cat)'
    assert negative_lookbehind('cat', 'dog', 'moose') == '(?<!catdogmoose)'

def test_named_group():
    with pytest.raises(ValueError) as excObj:
        named_group('', 'hello') # Blank name.
    with pytest.raises(ValueError) as excObj:
        named_group('2', 'hello') # Starts with number.
    with pytest.raises(ValueError) as excObj:
        named_group('!', 'hello') # Invalid character.

    assert named_group('foo', 'cat') == '(?P<foo>cat)'
    assert named_group('foo', 'cat', 'dog', 'moose') == '(?P<foo>catdogmoose)'


def test_noncapturing_group():
    assert noncapturing_group('cat') == '(?:cat)'
    assert noncapturing_group('cat', 'dog', 'moose') == '(?:catdogmoose)'


def test_optional():
    with pytest.raises(ValueError) as excObj:
        optional() # No args.
    with pytest.raises(ValueError) as excObj:
        optional('') # Blank arg.
    with pytest.raises(ValueError) as excObj:
        optional('', '') # Blank args.

    assert optional('c') == 'c?'
    assert optional('c', 'a', 't') == 'cat?'
    assert optional(group('cat')) == '(cat)?'
    assert group(optional('cat')) == '(cat?)'

def test_either():
    with pytest.raises(ValueError) as excObj:
        either()
    with pytest.raises(ValueError) as excObj:
        either('')
    with pytest.raises(ValueError) as excObj:
        either('', '')

    assert either('cat', 'dog', 'moose') == 'cat|dog|moose'
    assert either('cat', '', 'moose') == 'cat|moose'
    assert group(either('cat', 'dog', 'moose')) == '(cat|dog|moose)'


def test_exactly():
    with pytest.raises(TypeError) as excObj:
        exactly('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        exactly(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        exactly(1.0, 'cat')
    with pytest.raises(ValueError) as excObj:
        exactly(1)
    with pytest.raises(ValueError) as excObj:
        exactly(1, '')
    with pytest.raises(ValueError) as excObj:
        exactly(1, '', '')

    assert exactly(1, 'cat') == 'cat{1}'
    assert exactly(1, 'cat', 'dog') == 'catdog{1}'
    assert exactly(9999, 'cat') == 'cat{9999}'
    assert exactly(0, 'cat') == 'cat{0}'


def test_between():
    with pytest.raises(TypeError) as excObj:
        between('forty two', 1, 'cat')
    with pytest.raises(ValueError) as excObj:
        between(-1, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        between(1.0, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        between(1, 'forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        between(1, -1, 'cat')
    with pytest.raises(TypeError) as excObj:
        between(1, 1.0, 'cat')
    with pytest.raises(ValueError) as excObj:
        between(1, 2)
    with pytest.raises(ValueError) as excObj:
        between(1, 2, '')
    with pytest.raises(ValueError) as excObj:
        between(1, 2, '', '')

    assert between(1, 2, 'cat') == 'cat{1,2}'
    assert between(1, 2, 'cat', 'dog') == 'catdog{1,2}'
    assert between(9999, 99999, 'cat') == 'cat{9999,99999}'
    assert between(0, 0, 'cat') == 'cat{0,0}'

def test_at_least():
    with pytest.raises(TypeError) as excObj:
        at_least('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        at_least(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        at_least(1.0, 'cat')
    with pytest.raises(ValueError) as excObj:
        at_least(1)
    with pytest.raises(ValueError) as excObj:
        at_least(1, '')
    with pytest.raises(ValueError) as excObj:
        at_least(1, '', '')

    assert at_least(1, 'cat') == 'cat{1,}'
    assert at_least(1, 'cat', 'dog') == 'catdog{1,}'
    assert at_least(9999, 'cat') == 'cat{9999,}'
    assert at_least(0, 'cat') == 'cat{0,}'

def test_at_most():
    with pytest.raises(TypeError) as excObj:
        at_most('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        at_most(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        at_most(1.0, 'cat')
    with pytest.raises(ValueError) as excObj:
        at_most(1)
    with pytest.raises(ValueError) as excObj:
        at_most(1, '')
    with pytest.raises(ValueError) as excObj:
        at_most(1, '', '')

    assert at_most(1, 'cat') == 'cat{,1}'
    assert at_most(1, 'cat', 'dog') == 'catdog{,1}'
    assert at_most(9999, 'cat') == 'cat{,9999}'
    assert at_most(0, 'cat') == 'cat{,0}'

def test_zero_or_more():
    with pytest.raises(ValueError) as excObj:
        zero_or_more()
    with pytest.raises(ValueError) as excObj:
        zero_or_more('')
    with pytest.raises(ValueError) as excObj:
        zero_or_more('', '')

    assert zero_or_more('x') == 'x*'
    assert zero_or_more('x', 'y') == 'xy*'


def test_zero_or_more_lazy():
    with pytest.raises(ValueError) as excObj:
        zero_or_more()
    with pytest.raises(ValueError) as excObj:
        zero_or_more('')
    with pytest.raises(ValueError) as excObj:
        zero_or_more('', '')

    assert zero_or_more('x') == 'x*?'
    assert zero_or_more('x', 'y') == 'xy*?'


def test_one_or_more():
    with pytest.raises(ValueError) as excObj:
        one_or_more()
    with pytest.raises(ValueError) as excObj:
        one_or_more('')
    with pytest.raises(ValueError) as excObj:
        one_or_more('', '')

    assert one_or_more('x') == 'x+'
    assert one_or_more('x', 'y') == 'xy+'

def test_one_or_more_lazy():
    with pytest.raises(ValueError) as excObj:
        one_or_more()
    with pytest.raises(ValueError) as excObj:
        one_or_more('')
    with pytest.raises(ValueError) as excObj:
        one_or_more('', '')

    assert one_or_more('x') == 'x+?'
    assert one_or_more('x', 'y') == 'xy+?'


def test_starts_with():
    assert starts_with('') == '^'
    assert starts_with('', '') == '^'
    assert starts_with() == '^'
    assert starts_with('cat') == '^cat'
    assert starts_with('cat', 'dog', 'moose') == '^catdogmoose'

def test_ends_with():
    assert ends_with('') == '$'
    assert ends_with('', '') == '$'
    assert ends_with() == '$'
    assert ends_with('cat') == 'cat$'
    assert ends_with('cat', 'dog', 'moose') == 'catdogmoose$'


def test_starts_and_ends_with():
    assert starts_and_ends_with('') == '^$'
    assert starts_and_ends_with('', '') == '^$'
    assert starts_and_ends_with() == '^$'
    assert starts_and_ends_with('cat') == '^cat$'
    assert starts_and_ends_with('cat', 'dog', 'moose') == '^catdogmoose$'

def test_chars():
    with pytest.raises(ValueError) as excObj:
        chars()
    with pytest.raises(ValueError) as excObj:
        chars('')
    with pytest.raises(ValueError) as excObj:
        chars('', '')

    assert chars('a-z') == '[a-z]'
    assert chars('x', 'y') == '[xy]'

def test_nonchars():
    with pytest.raises(ValueError) as excObj:
        nonchars()
    with pytest.raises(ValueError) as excObj:
        nonchars('')
    with pytest.raises(ValueError) as excObj:
        nonchars('', '')

    assert nonchars('a-z') == '[^a-z]'
    assert nonchars('x', 'y') == '[^xy]'

def test_optional_group():
    assert optional_group() == '()?'
    assert optional_group('') == '()?'
    assert optional_group('c') == '(c)?'
    assert optional_group('c', 'a', 't') == '(cat)?'
    assert optional_group('cat') == '(cat)?'
    assert group(optional_group('cat')) == '((cat)?)'

def test_group_either():
    assert group_either() == '()'
    assert group_either('') == '()'
    assert group_either('', '') == '()'
    assert group_either('cat', 'dog', 'moose') == '(cat|dog|moose)'
    assert group_either('cat', '', 'moose') == '(cat|moose)'
    assert group_either('cat', 'dog', 'moose') == '(cat|dog|moose)'

def test_group_exactly():
    with pytest.raises(TypeError) as excObj:
        group_exactly('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        group_exactly(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_exactly(1.0, 'cat')

    assert group_exactly(1, 'cat') == '(cat){1}'
    assert group_exactly(1, 'cat', 'dog') == '(catdog){1}'
    assert group_exactly(9999, 'cat') == '(cat){9999}'
    assert group_exactly(0, 'cat') == '(cat){0}'

def test_group_between():
    with pytest.raises(TypeError) as excObj:
        group_between('forty two', 1, 'cat')
    with pytest.raises(ValueError) as excObj:
        group_between(-1, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_between(1.0, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_between(1, 'forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        group_between(1, -1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_between(1, 1.0, 'cat')

    assert group_between(1, 2) == '(){1,2}'
    assert group_between(1, 2, '') == '(){1,2}'
    assert group_between(1, 2, '', '') == '(){1,2}'
    assert group_between(1, 2, 'cat') == '(cat){1,2}'
    assert group_between(1, 2, 'cat', 'dog') == '(catdog){1,2}'
    assert group_between(9999, 99999, 'cat') == '(cat){9999,99999}'
    assert group_between(0, 0, 'cat') == '(cat){0,0}'

def test_group_at_least():
    with pytest.raises(TypeError) as excObj:
        group_at_least('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        group_at_least(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_at_least(1.0, 'cat')

    assert group_at_least(1) == '(){1,}'
    assert group_at_least(1, '') == '(){1,}'
    assert group_at_least(1, '', '') == '(){1,}'
    assert group_at_least(1, 'cat') == '(cat){1,}'
    assert group_at_least(1, 'cat', 'dog') == '(catdog){1,}'
    assert group_at_least(9999, 'cat') == '(cat){9999,}'
    assert group_at_least(0, 'cat') == '(cat){0,}'

def test_group_at_most():
    with pytest.raises(TypeError) as excObj:
        group_at_most('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        group_at_most(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        group_at_most(1.0, 'cat')

    assert group_at_most(1) == '(){,1}'
    assert group_at_most(1, '') == '(){,1}'
    assert group_at_most(1, '', '') == '(){,1}'
    assert group_at_most(1, 'cat') == '(cat){,1}'
    assert group_at_most(1, 'cat', 'dog') == '(catdog){,1}'
    assert group_at_most(9999, 'cat') == '(cat){,9999}'
    assert group_at_most(0, 'cat') == '(cat){,0}'

def test_zero_or_more_group():
    assert zero_or_more_group() == '()*'
    assert zero_or_more_group('') == '()*'
    assert zero_or_more_group('', '') == '()*'
    assert zero_or_more_group('x') == '(x)*'
    assert zero_or_more_group('x', 'y') == '(xy)*'

def test_one_or_more_group():
    assert one_or_more_group() == '()+'
    assert one_or_more_group('') == '()+'
    assert one_or_more_group('', '') == '()+'
    assert one_or_more_group('x') == '(x)+'
    assert one_or_more_group('x', 'y') == '(xy)+'

def test_group_chars():
    with pytest.raises(ValueError) as excObj:
        group_chars()
    with pytest.raises(ValueError) as excObj:
        group_chars('')
    with pytest.raises(ValueError) as excObj:
        group_chars('', '')

    assert group_chars('a-z') == '([a-z])'
    assert group_chars('x', 'y') == '([xy])'

def test_group_nonchars():
    with pytest.raises(ValueError) as excObj:
        group_nonchars()
    with pytest.raises(ValueError) as excObj:
        group_nonchars('')
    with pytest.raises(ValueError) as excObj:
        group_nonchars('', '')

    assert group_nonchars('a-z') == '([^a-z])'
    assert group_nonchars('x', 'y') == '([^xy])'


if __name__ == "__main__":
    pytest.main()
