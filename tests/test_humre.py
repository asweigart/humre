from __future__ import division, print_function
import pytest

from humre import *
import re, sys


def test_random_regexes_I_found_online():
    # Basic American phone number regex:
    assert (
        r'\d\d\d-\d\d\d-\d\d\d\d'
        == DIGIT + DIGIT + DIGIT + '-' + DIGIT + DIGIT + DIGIT + '-' + DIGIT + DIGIT + DIGIT + DIGIT
    )

    # Basic American phone number regex using {3}:
    # assert r'\d{3}-\d{3}-\d{4}' == exactly_3(DIGIT) + '-' + exactly_3(DIGIT) + '-' + exactly_4(DIGIT)
    assert r'\d{3}-\d{3}-\d{4}' == exactly(3, DIGIT) + '-' + exactly(3, DIGIT) + '-' + exactly(4, DIGIT)

    # American phone number with groups:
    assert r'(\d{3})-(\d{3}-\d{4})' == group(exactly(3, DIGIT)) + '-' + group(
        exactly(3, DIGIT) + '-' + exactly(4, DIGIT)
    )

    assert 'First Name: (.*?)' == 'First Name: ' + group(ANYTHING)
    assert 'First Name: (.*)' == 'First Name: ' + group(EVERYTHING)

    assert 'x*' == zero_or_more('x')
    assert 'x+' == one_or_more('x')

    assert 'x{3,5}' == between(3, 5, 'x')
    assert 'x{2,}' == at_least(2, 'x')

    assert 'x{,2}' == at_most(2, 'x')

    assert '^x' == starts_with('x')
    assert 'x$' == ends_with('x')
    assert '^x$' == starts_and_ends_with('x')

    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == group(
        # Area code:
        optional(group(either(exactly(3, DIGIT), OPEN_PAREN + exactly(3, DIGIT) + CLOSE_PAREN)))
        + optional(group(either(WHITESPACE, '-', PERIOD)))
        +
        # First three digits:
        exactly(3, DIGIT)
        + group(either(WHITESPACE, '-', PERIOD))
        +
        # Last four digits:
        exactly(4, DIGIT)
        +
        # Optional extension:
        optional(
            group(
                zero_or_more(WHITESPACE)
                + group(either('ext', 'x', 'ext.'))
                + zero_or_more(WHITESPACE)
                + between(2, 5, DIGIT)
            )
        )
    )

    # Use commas instead of + str concatenation:
    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == group(
        optional(group(either(exactly(3, DIGIT), OPEN_PAREN + exactly(3, DIGIT) + CLOSE_PAREN))),
        optional(group(either(WHITESPACE, '-', PERIOD))),
        exactly(3, DIGIT),
        group(either(WHITESPACE, '-', PERIOD)),
        exactly(4, DIGIT),
        optional(
            group(
                zero_or_more(WHITESPACE),
                group(either('ext', 'x', 'ext.')),
                zero_or_more(WHITESPACE),
                between(2, 5, DIGIT),
            )
        ),
    )

    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == group(
        optional_group(either(exactly(3, DIGIT), r'\(' + exactly(3, DIGIT) + r'\)'))
        + optional_group(either(WHITESPACE, '-', PERIOD))
        + exactly(3, DIGIT)
        + group_either(WHITESPACE, '-', PERIOD)
        + exactly(4, DIGIT)
        + optional_group(
            zero_or_more(WHITESPACE)
            + group(either('ext', 'x', 'ext.'))
            + zero_or_more(WHITESPACE)
            + between(2, 5, DIGIT)
        )
    )

    assert '[YZ][BCE-HMO-Y][BEFN][A-Z][0-9][0-9]_KWBC_[0-9]{6}' == chars('YZ') + chars('BCE-HMO-Y') + chars(
        'BEFN'
    ) + chars('A-Z') + chars('0-9') + chars('0-9') + '_KWBC_' + exactly(6, chars('0-9'))
    assert r'\s*\\\\$' == ends_with(zero_or_more(WHITESPACE) + '\\\\\\\\')

    assert r"^Access:" == starts_with('Access:')

    import string

    assert "Check[ ]?sum[ ]+is[ ]+([{}])".format(string.printable) == 'Check' + optional(
        chars(' ')
    ) + 'sum' + one_or_more(chars(' ')) + 'is' + one_or_more(chars(' ')) + group(chars(string.printable))
    # Use ''.join() so that I can have commas instead.
    assert "Check[ ]?sum[ ]+is[ ]+([{}])".format(string.printable) == ''.join(
        (
            # The WORD 'Checksum' with optional space between 'check' and 'sum':
            'Check',
            optional(chars(' ')),
            'sum',
            # One or more spaces:
            one_or_more(chars(' ')),
            # The WORD 'is':
            'is',
            # One or more spaces:
            one_or_more(chars(' ')),
            # A printable character:
            group(chars(string.printable)),
        )
    )

    assert r'[-]?\d\n' == optional(chars('-')) + DIGIT + NEWLINE

    assert r'Student has an ([A-D]) grade' == 'Student has an ' + group(chars('A-D')) + ' grade'

    assert r'([-]?\d+) is the median' == group(optional(chars('-')), one_or_more(DIGIT)) + ' is the median'

    assert '^[A-Z0-9]' == starts_with(chars('A-Z0-9'))

    assert r"\s(\S):\s" == WHITESPACE + group(NONWHITESPACE) + ':' + WHITESPACE
    assert r"\s(\S):\s" == ''.join([WHITESPACE, group(NONWHITESPACE), ':', WHITESPACE])
    assert re.compile(r"\s(\S):\s") == compile(WHITESPACE, group(NONWHITESPACE), ':', WHITESPACE)
    assert re.compile(r"\s(\S):\s") == re.compile(''.join((WHITESPACE, group(NONWHITESPACE), ':', WHITESPACE)))

    assert r"\*([^\*]+)\*" == ASTERISK + group(one_or_more(nonchars(ASTERISK))) + ASTERISK

    assert zero_or_more(BACKSLASH) == r'\\*'
    assert ASTERISK == r'\*'

    assert r"\s+" == one_or_more(WHITESPACE)

    assert "^yslogin[0-9]+" == starts_with('yslogin', one_or_more(chars('0-9')))

    assert (
        r"\$\((?P<name>[A-Za-z0-9_]+)\)"
        == DOLLAR + OPEN_PAREN + named_group('name', one_or_more(chars('A-Za-z0-9_'))) + CLOSE_PAREN
    )

    assert "ccd id: \\d+" == 'ccd id: ' + one_or_more(DIGIT)

    # assert "[%:\r\n]" == chars(r'%:\r\n')  # Test this: is there a difference between "[%:\r\n]" and r"[%:\r\n]"

    assert "%([0-9a-fA-F][0-9a-fA-F])" == '%' + group(chars('0-9a-fA-F'), chars('0-9a-fA-F'))

    assert r'\?sid=(?P<sid>\d+)' == QUESTION_MARK + 'sid=' + named_group('sid', one_or_more(DIGIT))

    assert (
        'INPUT.*NAME="seui".*VALUE="(?P<uid>[^"]*)"'
        == 'INPUT'
        + EVERYTHING
        + 'NAME="seui"'
        + EVERYTHING
        + 'VALUE="'
        + named_group('uid', zero_or_more(nonchars('"')))
        + '"'
    )

    assert (
        'INPUT.*NAME="sdn".*VALUE="(?P<rnm>[^"]*)"'
        == 'INPUT'
        + EVERYTHING
        + 'NAME="sdn"'
        + EVERYTHING
        + 'VALUE="'
        + named_group('rnm', zero_or_more(nonchars('"')))
        + '"'
    )

    assert (
        'OPTION VALUE="(?P<mod>[^"]*)" SELECTED'
        == 'OPTION VALUE="' + named_group('mod', zero_or_more(nonchars('"'))) + '" SELECTED'
    )

    assert (
        'INPUT.*NAME="sena" VALUE="(?P<ena>[^"]*)" CHECKED'
        == 'INPUT' + EVERYTHING + 'NAME="sena" VALUE="' + named_group('ena', zero_or_more(nonchars('"'))) + '" CHECKED'
    )

    assert r"[.?!]" == chars('.?!')  # Functionally equivalent to chars(PERIOD + QUESTION_MARK + '!')

    assert r"[A-Z]\w+" == chars('A-Z') + one_or_more(WORD)

    # This has a bug in it because the . dots can match ANYTHING:
    assert r'^pip-.*(zip|tar.gz|tar.bz2|tgz|tbz)$' == starts_and_ends_with(
        'pip-' + EVERYTHING + group_either('zip', 'tar.gz', 'tar.bz2', 'tgz', 'tbz')
    )

    assert r'/Python(?:-32|-64)*$' == '/Python' + ends_with(zero_or_more(noncap_group(either('-32', '-64'))))

    assert r'^CPU\(s\):\s*(\d+)' == starts_with(
        'CPU' + OPEN_PAREN + 's' + CLOSE_PAREN + ':' + zero_or_more(WHITESPACE)
    ) + group(one_or_more(DIGIT))

    assert '^GOOGLE_RELEASE=(.+)$' == starts_and_ends_with('GOOGLE_RELEASE=', group(one_or_more(ANYCHAR)))

    assert '^(.+)=(.+)$' == starts_and_ends_with(group(GREEDY_SOMETHING), '=', group(GREEDY_SOMETHING))

    assert '<.*?>' == '<' + ANYTHING + '>'

    assert r'chr(\d+):(\d+)(-(\d+))?' == 'chr' + group(one_or_more(DIGIT)) + ':' + group(
        one_or_more(DIGIT)
    ) + optional_group('-', group(one_or_more(DIGIT)))

    assert r'chr(\d+)(:(\d+)(-(\d+))?)?' == 'chr' + group(one_or_more(DIGIT)) + optional_group(
        ':', group(one_or_more(DIGIT)), optional_group('-', group(one_or_more(DIGIT)))
    )

    assert "[^a-zA-Z0-9']+" == one_or_more(nonchars("a-zA-Z0-9'"))

    # Purposefully left this as a non-raw string:
    assert re.compile(r"<person>([,\s]*(and)*[,\s]*<person>)+") == compile(
        '<person>',
        one_or_more_group(
            zero_or_more(chars(r',\s')), zero_or_more_group('and'), zero_or_more(chars(r',\s')), '<person>'
        ),
    )

    # assert re.compile(r"[()[\].,|:;?!=+~\-\/{}]") == compile(chars('()[\].,|:;?!=+~\-\/{}'))
    assert re.compile(r"[()[].,|:;?!=+~-/{}]") == compile(chars('()[].,|:;?!=+~-/{}'))

    assert re.compile('''['"`]''') == compile(chars("""'"`"""))

    assert re.compile(r'(\s*"+\s*)+') == compile(
        one_or_more_group(zero_or_more(WHITESPACE), one_or_more('"'), zero_or_more(WHITESPACE))
    )

    assert re.compile(r"(\d),(\d{3})") == compile(group(DIGIT), ',', group(exactly(3, DIGIT)))

    assert r"(\w)\.(\w)" == group(WORD) + PERIOD + group(WORD)

    # TODO - research: positive lookahead and negative lookahead (?=
    # assert r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)" == "'" + group()

    assert (
        r'<math.*?alttext="\{\\displaystyle (.*?)\}"'
        == '<math'
        + ANYTHING
        + 'alttext="'
        + OPEN_BRACE
        + BACKSLASH
        + 'displaystyle '
        + group(ANYTHING)
        + CLOSE_BRACE
        + '"'
    )

    assert r'([^-+.:0-9])+' == one_or_more_group(nonchars('-+.:0-9'))

    assert r'(\d+)' == group(one_or_more(DIGIT))

    assert r"(\w+(\W*\d+\W*)?\-?\w*?[^\S\t]*)*" == zero_or_more_group(
        one_or_more(WORD),
        optional_group(zero_or_more(NONWORD), one_or_more(DIGIT), zero_or_more(NONWORD)),
        optional(r'\-'),
        optional(zero_or_more(WORD)),
        zero_or_more(nonchars(NONWHITESPACE, TAB)),
    )

    assert r"(\w+(\W*\d+\W*)?\-?\w*?[^\S\t]*)*" == zero_or_more_group(
        one_or_more(WORD),
        optional_group(zero_or_more(NONWORD), one_or_more(DIGIT), zero_or_more(NONWORD)),
        optional('\\-'),
        optional(zero_or_more(WORD)),
        zero_or_more(nonchars(NONWHITESPACE, TAB)),
    )

    assert r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)" == "'" + positive_lookahead(
        group_either(chars('stdm'), group('ll'), group('re'), group('ve'), group('ll')), BOUNDARY
    )

    assert r"(\s*,+\s*)+" == one_or_more_group(zero_or_more(WHITESPACE), one_or_more(','), zero_or_more(WHITESPACE))

    assert r'[\W_]' == chars(NONWORD, '_')


def test_join():
    assert join('dog', 'cat', 'moose') == ''.join(['dog', 'cat', 'moose'])
    assert join() == ''


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
    # assert compile(b'hello', flags=L) == re.compile(b'hello', re.L)
    # assert compile(b'hello', flags=LOCALE) == re.compile(b'hello', re.LOCALE)
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
    assert lookahead('cat') == '(?=cat)'
    assert lookahead('cat', 'dog', 'moose') == '(?=catdogmoose)'

    assert positive_lookahead('cat') == '(?=cat)'
    assert positive_lookahead('cat', 'dog', 'moose') == '(?=catdogmoose)'


def test_negative_lookahead():
    assert negative_lookahead('cat') == '(?!cat)'
    assert negative_lookahead('cat', 'dog', 'moose') == '(?!catdogmoose)'


def test_positive_lookbehind():
    assert lookbehind('cat') == '(?<=cat)'
    assert lookbehind('cat', 'dog', 'moose') == '(?<=catdogmoose)'

    assert positive_lookbehind('cat') == '(?<=cat)'
    assert positive_lookbehind('cat', 'dog', 'moose') == '(?<=catdogmoose)'


def test_negative_lookbehind():
    assert negative_lookbehind('cat') == '(?<!cat)'
    assert negative_lookbehind('cat', 'dog', 'moose') == '(?<!catdogmoose)'


def test_named_group():
    with pytest.raises(ValueError) as excObj:
        named_group('', 'hello')  # Blank name.
    with pytest.raises(ValueError) as excObj:
        named_group('2', 'hello')  # Starts with number.
    with pytest.raises(ValueError) as excObj:
        named_group('!', 'hello')  # Invalid character.

    assert named_group('foo', 'cat') == '(?P<foo>cat)'
    assert named_group('foo', 'cat', 'dog', 'moose') == '(?P<foo>catdogmoose)'


def test_noncap_group():
    assert noncap_group('cat') == '(?:cat)'
    assert noncap_group('cat', 'dog', 'moose') == '(?:catdogmoose)'


def test_optional():
    with pytest.raises(ValueError) as excObj:
        optional()  # No args.
    with pytest.raises(ValueError) as excObj:
        optional('')  # Blank arg.
    with pytest.raises(ValueError) as excObj:
        optional('', '')  # Blank args.

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
    with pytest.raises(ValueError) as excObj:
        between(2, 1, '')

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
        zero_or_more_lazy()
    with pytest.raises(ValueError) as excObj:
        zero_or_more_lazy('')
    with pytest.raises(ValueError) as excObj:
        zero_or_more_lazy('', '')

    assert zero_or_more_lazy('x') == 'x*?'
    assert zero_or_more_lazy('x', 'y') == 'xy*?'


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
        one_or_more_lazy()
    with pytest.raises(ValueError) as excObj:
        one_or_more_lazy('')
    with pytest.raises(ValueError) as excObj:
        one_or_more_lazy('', '')

    assert one_or_more_lazy('x') == 'x+?'
    assert one_or_more_lazy('x', 'y') == 'xy+?'


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


def test_optional_noncap_group():
    assert optional_noncap_group() == '(?:)?'
    assert optional_noncap_group('') == '(?:)?'
    assert optional_noncap_group('c') == '(?:c)?'
    assert optional_noncap_group('c', 'a', 't') == '(?:cat)?'
    assert optional_noncap_group('cat') == '(?:cat)?'
    assert group(optional_noncap_group('cat')) == '((?:cat)?)'


def test_group_either():
    assert group_either() == '()'
    assert group_either('') == '()'
    assert group_either('', '') == '()'
    assert group_either('cat', 'dog', 'moose') == '(cat|dog|moose)'
    assert group_either('cat', '', 'moose') == '(cat|moose)'
    assert group_either('cat', 'dog', 'moose') == '(cat|dog|moose)'


def test_noncap_group_either():
    assert noncap_group_either() == '(?:)'
    assert noncap_group_either('') == '(?:)'
    assert noncap_group_either('', '') == '(?:)'
    assert noncap_group_either('cat', 'dog', 'moose') == '(?:cat|dog|moose)'
    assert noncap_group_either('cat', '', 'moose') == '(?:cat|moose)'
    assert noncap_group_either('cat', 'dog', 'moose') == '(?:cat|dog|moose)'


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


def test_noncap_group_exactly():
    with pytest.raises(TypeError) as excObj:
        noncap_group_exactly('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_exactly(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_exactly(1.0, 'cat')

    assert noncap_group_exactly(1, 'cat') == '(?:cat){1}'
    assert noncap_group_exactly(1, 'cat', 'dog') == '(?:catdog){1}'
    assert noncap_group_exactly(9999, 'cat') == '(?:cat){9999}'
    assert noncap_group_exactly(0, 'cat') == '(?:cat){0}'


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
    with pytest.raises(ValueError) as excObj:
        group_between(2, 1, '')
    with pytest.raises(ValueError) as excObj:
        group_between(2, 1, '', '')

    assert group_between(1, 2) == '(){1,2}'
    assert group_between(1, 2, '') == '(){1,2}'
    assert group_between(1, 2, '', '') == '(){1,2}'
    assert group_between(1, 2, 'cat') == '(cat){1,2}'
    assert group_between(1, 2, 'cat', 'dog') == '(catdog){1,2}'
    assert group_between(9999, 99999, 'cat') == '(cat){9999,99999}'
    assert group_between(0, 0, 'cat') == '(cat){0,0}'


def test_noncap_group_between():
    with pytest.raises(TypeError) as excObj:
        noncap_group_between('forty two', 1, 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_between(-1, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_between(1.0, 1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_between(1, 'forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_between(1, -1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_between(1, 1.0, 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_between(2, 1, '')
    with pytest.raises(ValueError) as excObj:
        noncap_group_between(2, 1, '', '')

    assert noncap_group_between(1, 2) == '(?:){1,2}'
    assert noncap_group_between(1, 2, '') == '(?:){1,2}'
    assert noncap_group_between(1, 2, '', '') == '(?:){1,2}'
    assert noncap_group_between(1, 2, 'cat') == '(?:cat){1,2}'
    assert noncap_group_between(1, 2, 'cat', 'dog') == '(?:catdog){1,2}'
    assert noncap_group_between(9999, 99999, 'cat') == '(?:cat){9999,99999}'
    assert noncap_group_between(0, 0, 'cat') == '(?:cat){0,0}'


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


def test_noncap_group_at_least():
    with pytest.raises(TypeError) as excObj:
        noncap_group_at_least('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_at_least(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_at_least(1.0, 'cat')

    assert noncap_group_at_least(1) == '(?:){1,}'
    assert noncap_group_at_least(1, '') == '(?:){1,}'
    assert noncap_group_at_least(1, '', '') == '(?:){1,}'
    assert noncap_group_at_least(1, 'cat') == '(?:cat){1,}'
    assert noncap_group_at_least(1, 'cat', 'dog') == '(?:catdog){1,}'
    assert noncap_group_at_least(9999, 'cat') == '(?:cat){9999,}'
    assert noncap_group_at_least(0, 'cat') == '(?:cat){0,}'


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


def test_noncap_group_at_most():
    with pytest.raises(TypeError) as excObj:
        noncap_group_at_most('forty two', 'cat')
    with pytest.raises(ValueError) as excObj:
        noncap_group_at_most(-1, 'cat')
    with pytest.raises(TypeError) as excObj:
        noncap_group_at_most(1.0, 'cat')

    assert noncap_group_at_most(1) == '(?:){,1}'
    assert noncap_group_at_most(1, '') == '(?:){,1}'
    assert noncap_group_at_most(1, '', '') == '(?:){,1}'
    assert noncap_group_at_most(1, 'cat') == '(?:cat){,1}'
    assert noncap_group_at_most(1, 'cat', 'dog') == '(?:catdog){,1}'
    assert noncap_group_at_most(9999, 'cat') == '(?:cat){,9999}'
    assert noncap_group_at_most(0, 'cat') == '(?:cat){,0}'


def test_zero_or_more_group():
    assert zero_or_more_group() == '()*'
    assert zero_or_more_group('') == '()*'
    assert zero_or_more_group('', '') == '()*'
    assert zero_or_more_group('x') == '(x)*'
    assert zero_or_more_group('x', 'y') == '(xy)*'


def test_zero_or_more_noncap_group():
    assert zero_or_more_noncap_group() == '(?:)*'
    assert zero_or_more_noncap_group('') == '(?:)*'
    assert zero_or_more_noncap_group('', '') == '(?:)*'
    assert zero_or_more_noncap_group('x') == '(?:x)*'
    assert zero_or_more_noncap_group('x', 'y') == '(?:xy)*'


def test_zero_or_more_lazy_group():
    assert zero_or_more_lazy_group() == '()*?'
    assert zero_or_more_lazy_group('') == '()*?'
    assert zero_or_more_lazy_group('', '') == '()*?'
    assert zero_or_more_lazy_group('x') == '(x)*?'
    assert zero_or_more_lazy_group('x', 'y') == '(xy)*?'


def test_zero_or_more_lazy_noncap_group():
    assert zero_or_more_lazy_noncap_group() == '(?:)*?'
    assert zero_or_more_lazy_noncap_group('') == '(?:)*?'
    assert zero_or_more_lazy_noncap_group('', '') == '(?:)*?'
    assert zero_or_more_lazy_noncap_group('x') == '(?:x)*?'
    assert zero_or_more_lazy_noncap_group('x', 'y') == '(?:xy)*?'


def test_one_or_more_group():
    assert one_or_more_group() == '()+'
    assert one_or_more_group('') == '()+'
    assert one_or_more_group('', '') == '()+'
    assert one_or_more_group('x') == '(x)+'
    assert one_or_more_group('x', 'y') == '(xy)+'


def test_one_or_more_noncap_group():
    assert one_or_more_noncap_group() == '(?:)+'
    assert one_or_more_noncap_group('') == '(?:)+'
    assert one_or_more_noncap_group('', '') == '(?:)+'
    assert one_or_more_noncap_group('x') == '(?:x)+'
    assert one_or_more_noncap_group('x', 'y') == '(?:xy)+'


def test_one_or_more_lazy_group():
    assert one_or_more_lazy_group() == '()+?'
    assert one_or_more_lazy_group('') == '()+?'
    assert one_or_more_lazy_group('', '') == '()+?'
    assert one_or_more_lazy_group('x') == '(x)+?'
    assert one_or_more_lazy_group('x', 'y') == '(xy)+?'


def test_one_or_more_lazy_noncap_group():
    assert one_or_more_lazy_noncap_group() == '(?:)+?'
    assert one_or_more_lazy_noncap_group('') == '(?:)+?'
    assert one_or_more_lazy_noncap_group('', '') == '(?:)+?'
    assert one_or_more_lazy_noncap_group('x') == '(?:x)+?'
    assert one_or_more_lazy_noncap_group('x', 'y') == '(?:xy)+?'


def test_group_chars():
    with pytest.raises(ValueError) as excObj:
        group_chars()
    with pytest.raises(ValueError) as excObj:
        group_chars('')
    with pytest.raises(ValueError) as excObj:
        group_chars('', '')

    assert group_chars('a-z') == '([a-z])'
    assert group_chars('x', 'y') == '([xy])'


def test_noncap_group_chars():
    with pytest.raises(ValueError) as excObj:
        noncap_group_chars()
    with pytest.raises(ValueError) as excObj:
        noncap_group_chars('')
    with pytest.raises(ValueError) as excObj:
        noncap_group_chars('', '')

    assert noncap_group_chars('a-z') == '(?:[a-z])'
    assert noncap_group_chars('x', 'y') == '(?:[xy])'


def test_group_nonchars():
    with pytest.raises(ValueError) as excObj:
        group_nonchars()
    with pytest.raises(ValueError) as excObj:
        group_nonchars('')
    with pytest.raises(ValueError) as excObj:
        group_nonchars('', '')

    assert group_nonchars('a-z') == '([^a-z])'
    assert group_nonchars('x', 'y') == '([^xy])'


def test_noncap_group_nonchars():
    with pytest.raises(ValueError) as excObj:
        noncap_group_nonchars()
    with pytest.raises(ValueError) as excObj:
        noncap_group_nonchars('')
    with pytest.raises(ValueError) as excObj:
        noncap_group_nonchars('', '')

    assert noncap_group_nonchars('a-z') == '(?:[^a-z])'
    assert noncap_group_nonchars('x', 'y') == '(?:[^xy])'


def test_back_reference():
    with pytest.raises(TypeError) as excObj:
        back_reference('one')
    with pytest.raises(ValueError) as excObj:
        back_reference(-1)
    with pytest.raises(ValueError) as excObj:
        back_reference(-0)

    for i in range(1, 20):
        assert back_reference(i) == '\\' + str(i)

    assert back_reference(1) == BACK_1
    assert back_reference(2) == BACK_2
    assert back_reference(3) == BACK_3
    assert back_reference(4) == BACK_4
    assert back_reference(5) == BACK_5
    assert back_reference(6) == BACK_6
    assert back_reference(7) == BACK_7
    assert back_reference(8) == BACK_8
    assert back_reference(9) == BACK_9

    with pytest.raises(TypeError) as excObj:
        back_ref('one')
    with pytest.raises(ValueError) as excObj:
        back_ref(-1)
    with pytest.raises(ValueError) as excObj:
        back_ref(-0)

    for i in range(1, 20):
        assert back_ref(i) == '\\' + str(i)


# Taking out these ASCII_* tests since the constants have been
# removed for now (and probably permanently.)
"""
def test_ascii_letter_class():
    assert compile(ASCII_LETTER).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_LETTER).match(chr(i))
    for i in range(97, 123):  # a-z
        assert compile(ASCII_LETTER).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_LETTER).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_LETTER).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(ASCII_LETTER).match(chr(i)) is None


def test_ascii_nonletter_class():
    assert compile(ASCII_NONLETTER).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NONLETTER).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NONLETTER).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NONLETTER).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NONLETTER).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NONLETTER).match(chr(i))


def test_ascii_uppercase_class():
    assert compile(ASCII_UPPERCASE).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_UPPERCASE).match(chr(i))
    for i in range(97, 123):  # a-z
        assert compile(ASCII_UPPERCASE).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_UPPERCASE).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_UPPERCASE).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(ASCII_UPPERCASE).match(chr(i)) is None


def test_ascii_nonuppercase_class():
    assert compile(ASCII_NONUPPERCASE).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NONUPPERCASE).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NONUPPERCASE).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NONUPPERCASE).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NONUPPERCASE).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NONUPPERCASE).match(chr(i))


def test_ascii_lowercase_class():
    assert compile(ASCII_LOWERCASE).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_LOWERCASE).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(ASCII_LOWERCASE).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_LOWERCASE).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_LOWERCASE).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(ASCII_LOWERCASE).match(chr(i)) is None


def test_ascii_nonlowercase_class():
    assert compile(ASCII_NONLOWERCASE).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NONLOWERCASE).match(chr(i))
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NONLOWERCASE).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NONLOWERCASE).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NONLOWERCASE).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NONLOWERCASE).match(chr(i))


def test_ascii_alphanumeric():
    assert compile(ASCII_ALPHANUMERIC).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_ALPHANUMERIC).match(chr(i))
    for i in range(97, 123):  # a-z
        assert compile(ASCII_ALPHANUMERIC).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_ALPHANUMERIC).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_ALPHANUMERIC).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(ASCII_ALPHANUMERIC).match(chr(i)) is None


def test_ascii_nonalphanumeric_class():
    assert compile(ASCII_NONALPHANUMERIC).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NONALPHANUMERIC).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NONALPHANUMERIC).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NONALPHANUMERIC).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NONALPHANUMERIC).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NONALPHANUMERIC).match(chr(i))


def test_ascii_numeric():
    # TODO - test that this doesn't match numeric characters outside of 0-9.
    assert compile(ASCII_NUMERIC).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NUMERIC).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NUMERIC).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NUMERIC).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NUMERIC).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NUMERIC).match(chr(i)) is None


def test_ascii_nonnumeric():
    assert compile(ASCII_NONNUMERIC).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(ASCII_NONNUMERIC).match(chr(i))
    for i in range(97, 123):  # a-z
        assert compile(ASCII_NONNUMERIC).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(ASCII_NONNUMERIC).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(ASCII_NONNUMERIC).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(ASCII_NONNUMERIC).match(chr(i))
"""


def test_number_pattern():
    assert compile(NUMBER).match('') is None
    for i in range(65, 91):  # A-Z
        assert compile(NUMBER).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(NUMBER).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(NUMBER).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(NUMBER).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(NUMBER).match(chr(i)) is None

    assert compile(NUMBER).match('') is None
    assert compile(NUMBER).match('1.00')
    assert compile(NUMBER).match('12345')
    assert compile(NUMBER).match('-12345')
    assert compile(NUMBER).match('+12345')
    assert compile(NUMBER).match('12345.00')
    assert compile(NUMBER).match('3.14159265')
    assert compile(NUMBER).match('1,234.00')
    assert compile(NUMBER).match('9,991,234.00')
    assert compile(NUMBER).match('+1,234.00')
    assert compile(NUMBER).match('-1,234.00')


def test_euro_number_pattern():
    for i in range(65, 91):  # A-Z
        assert compile(EURO_NUMBER).match(chr(i)) is None
    for i in range(97, 123):  # a-z
        assert compile(EURO_NUMBER).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(EURO_NUMBER).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(EURO_NUMBER).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(EURO_NUMBER).match(chr(i)) is None

    assert compile(EURO_NUMBER).match('') is None
    assert compile(EURO_NUMBER).match('1,00')
    assert compile(EURO_NUMBER).match('12345')
    assert compile(EURO_NUMBER).match('-12345')
    assert compile(EURO_NUMBER).match('+12345')
    assert compile(EURO_NUMBER).match('12345,00')
    assert compile(EURO_NUMBER).match('3,14159265')
    assert compile(EURO_NUMBER).match('1.234,00')
    assert compile(EURO_NUMBER).match('9.991.234,00')
    assert compile(EURO_NUMBER).match('+1.234,00')
    assert compile(EURO_NUMBER).match('-1.234,00')


def test_hexadecimal():
    assert compile(HEXADECIMAL).match('') is None
    for i in range(65, 71):  # A-F
        assert compile(HEXADECIMAL).match(chr(i))
    for i in range(97, 103):  # a-f
        assert compile(HEXADECIMAL).match(chr(i))
    for i in range(71, 91):  # G-Z
        assert compile(HEXADECIMAL).match(chr(i)) is None
    for i in range(103, 123):  # g-z
        assert compile(HEXADECIMAL).match(chr(i)) is None
    for i in range(192, 377):  # À-Ÿ
        assert compile(HEXADECIMAL).match(chr(i)) is None
    for i in range(48, 58):  # 0-9
        assert compile(HEXADECIMAL).match(chr(i))
    for i in range(33, 48):  # !-/
        assert compile(HEXADECIMAL).match(chr(i)) is None


def test_nonhexadecimal():
    assert compile(NONHEXADECIMAL).match('') is None
    for i in range(65, 71):  # A-F
        assert compile(NONHEXADECIMAL).match(chr(i)) is None
    for i in range(97, 103):  # a-f
        assert compile(NONHEXADECIMAL).match(chr(i)) is None
    for i in range(71, 91):  # G-Z
        assert compile(NONHEXADECIMAL).match(chr(i))
    for i in range(103, 123):  # g-z
        assert compile(NONHEXADECIMAL).match(chr(i))
    for i in range(192, 377):  # À-Ÿ
        assert compile(NONHEXADECIMAL).match(chr(i))
    for i in range(48, 58):  # 0-9
        assert compile(NONHEXADECIMAL).match(chr(i)) is None
    for i in range(33, 48):  # !-/
        assert compile(NONHEXADECIMAL).match(chr(i))


def test_hexadecimal_number():
    assert compile(HEXADECIMAL_NUMBER).match('') is None
    assert compile(HEXADECIMAL_NUMBER).match('100')
    assert compile(HEXADECIMAL_NUMBER).match('FF')
    assert compile(HEXADECIMAL_NUMBER).match('1234567890ABCDEF')
    assert compile(HEXADECIMAL_NUMBER).match('0x100')
    assert compile(HEXADECIMAL_NUMBER).match('0xFF')
    assert compile(HEXADECIMAL_NUMBER).match('0x1234567890ABCDEF')
    assert compile(HEXADECIMAL_NUMBER).match('0X100')
    assert compile(HEXADECIMAL_NUMBER).match('0XFF')
    assert compile(HEXADECIMAL_NUMBER).match('0X1234567890ABCDEF')


def test_letter_character_class():
    assert compile(LETTER).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if chr(i).isalpha():
            assert compile(LETTER).match(chr(i))
        else:
            assert compile(LETTER).match(chr(i)) is None


def test_nonletter_character_class():
    assert compile(NONLETTER).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if not chr(i).isalpha():
            assert compile(NONLETTER).match(chr(i))
        else:
            assert compile(NONLETTER).match(chr(i)) is None


def test_lowercase_character_class():
    assert compile(LOWERCASE).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if chr(i).islower():
            assert compile(LOWERCASE).match(chr(i))
        else:
            assert compile(LOWERCASE).match(chr(i)) is None


def test_nonlowercase_character_class():
    assert compile(NONLOWERCASE).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if not chr(i).islower():
            assert compile(NONLOWERCASE).match(chr(i))
        else:
            assert compile(NONLOWERCASE).match(chr(i)) is None


def test_uppercase_character_class():
    assert compile(UPPERCASE).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if chr(i).isupper():
            assert compile(UPPERCASE).match(chr(i))
        else:
            assert compile(UPPERCASE).match(chr(i)) is None


def test_nonuppercase_character_class():
    assert compile(NONUPPERCASE).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if not chr(i).isupper():
            assert compile(NONUPPERCASE).match(chr(i))
        else:
            assert compile(NONUPPERCASE).match(chr(i)) is None


def test_alphanumeric_character_class():
    assert compile(ALPHANUMERIC).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if chr(i).isalnum():
            assert compile(ALPHANUMERIC).match(chr(i))
        else:
            assert compile(ALPHANUMERIC).match(chr(i)) is None


def test_nonalphanumeric_character_class():
    assert compile(NONALPHANUMERIC).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if not chr(i).isalnum():
            assert compile(NONALPHANUMERIC).match(chr(i))
        else:
            assert compile(NONALPHANUMERIC).match(chr(i)) is None


def test_numeric_character_class():
    assert compile(NUMERIC).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if chr(i).isnumeric():
            assert compile(NUMERIC).match(chr(i))
        else:
            assert compile(NUMERIC).match(chr(i)) is None


def test_nonnumeric_character_class():
    assert compile(NONNUMERIC).match('') is None
    # for i in range(0, sys.maxunicode + 1):
    for i in range(0, 1000):
        if not chr(i).isnumeric():
            assert compile(NONNUMERIC).match(chr(i))
        else:
            assert compile(NONNUMERIC).match(chr(i)) is None


def test_constants():
    assert DIGIT == r'\d'
    assert WORD == r'\w'
    assert WHITESPACE == r'\s'
    assert NONDIGIT == r'\D'
    assert NONWORD == r'\W'
    assert NONWHITESPACE == r'\S'
    assert BOUNDARY == r'\b'

    # Constants copied from the re module:
    # Changed in version 3.6: Flag constants are now instances of RegexFlag, which is a subclass of enum.IntFlag.
    assert A == re.A
    assert ASCII == re.ASCII
    assert DEBUG == re.DEBUG
    assert I == re.I
    assert IGNORECASE == re.IGNORECASE
    assert L == re.L
    assert LOCALE == re.LOCALE
    assert M == re.M
    assert MULTILINE == re.MULTILINE
    assert NOFLAG == 0  # re.NOFLAG  # New in 3.11
    assert S == re.S
    assert DOTALL == re.DOTALL
    assert X == re.X
    assert VERBOSE == re.VERBOSE

    # Built-in Humre character classes:

    # These ranges include more than just A-Za-z, but all Unicode characters
    # that islower(), isupper(), and isalpha() identify as lowercase, uppercase,
    # and alphabetical letter characters.
    assert len(LETTER) == 1604
    assert len(NONLETTER) == 1605
    assert len(UPPERCASE) == 839
    assert len(NONUPPERCASE) == 840
    assert len(LOWERCASE) == 872
    assert len(NONLOWERCASE) == 873
    assert len(ALPHANUMERIC) == 2073
    assert len(NONALPHANUMERIC) == 2074
    assert len(NUMERIC) == 471
    assert len(NONNUMERIC) == 472

    # These ASCII_* constants have been taken out for now, and probably
    # permanently.
    """
    assert ASCII_LETTER == '[A-Za-z]'
    assert ASCII_NONLETTER == '[^A-Za-z]'
    assert ASCII_UPPERCASE == '[A-Z]'
    assert ASCII_NONUPPERCASE == '[^A-Z]'
    assert ASCII_LOWERCASE == '[a-z]'
    assert ASCII_NONLOWERCASE == '[^a-z]'
    assert ASCII_ALPHANUMERIC == '[A-Za-z0-9]'
    assert ASCII_NONALPHANUMERIC == '[^A-Za-z0-9]'
    assert ASCII_NUMERIC == '[0-9]'
    assert ASCII_NONNUMERIC == '[^0-9]'
    """

    assert HEXADECIMAL == '[0-9A-Fa-f]'
    assert NONHEXADECIMAL == '[^0-9A-Fa-f]'

    # Built-in Humre Patterns:
    assert ANYTHING == '.*?'
    assert EVERYTHING == '.*'
    assert GREEDY_SOMETHING == '.+'
    assert SOMETHING == '.+?'
    assert ANYCHAR == '.'

    assert PERIOD == r'\.'
    assert CARET == r'\^'
    assert DOLLAR == r'\$'
    assert ASTERISK == r'\*'
    assert PLUS == r'\+'
    assert MINUS == r'\-'
    assert QUESTION_MARK == r'\?'
    assert OPEN_BRACE == r'\{'
    assert CLOSE_BRACE == r'\}'
    assert OPEN_BRACKET == r'\['
    assert CLOSE_BRACKET == r'\]'
    assert BACKSLASH == r'\\'
    assert PIPE == r'\|'
    assert OPEN_PAREN == OPEN_PARENTHESIS == r'\('
    assert CLOSE_PAREN == CLOSE_PARENTHESIS == r'\)'

    assert NEWLINE == r'\n'
    assert TAB == r'\t'
    assert QUOTE == r"\'"
    assert DOUBLE_QUOTE == r'\"'

    assert BACK_1 == r'\1'
    assert BACK_2 == r'\2'
    assert BACK_3 == r'\3'
    assert BACK_4 == r'\4'
    assert BACK_5 == r'\5'
    assert BACK_6 == r'\6'
    assert BACK_7 == r'\7'
    assert BACK_8 == r'\8'
    assert BACK_9 == r'\9'


def test_inline_flags():
    with pytest.raises(TypeError) as excObj:
        inline_flag(42, 'foo', 'bar')
    with pytest.raises(ValueError) as excObj:
        inline_flag('au', 'foo', 'bar')
    with pytest.raises(ValueError) as excObj:
        inline_flag('ua', 'foo', 'bar')
    with pytest.raises(ValueError) as excObj:
        inline_flag('z', 'foo', 'bar')

    assert inline_flag('a', 'foo', 'bar') == '(?a:foobar)'
    assert inline_flag('i', 'foo', 'bar') == '(?i:foobar)'
    # TODO - L flag requires passing a bytes object and not a string
    # assert inline_flag('L', 'foo', 'bar') == '(?a:foobar)'
    assert inline_flag('m', 'foo', 'bar') == '(?m:foobar)'
    assert inline_flag('s', 'foo', 'bar') == '(?s:foobar)'
    assert inline_flag('u', 'foo', 'bar') == '(?u:foobar)'
    assert inline_flag('x', 'foo', 'bar') == '(?x:foobar)'

    # TODO - test that "-" must be followed by only 'imsx' flags.
    # TODO - test that exceptions get raised


def test_atomic_group():
    assert atomic_group() == '(?>)'
    assert atomic_group('') == '(?>)'
    assert atomic_group('', '') == '(?>)'
    assert atomic_group('x') == '(?>x)'
    assert atomic_group('x', 'y') == '(?>xy)'


def test_zero_or_more_possessive():
    with pytest.raises(ValueError) as excObj:
        zero_or_more_possessive()
    with pytest.raises(ValueError) as excObj:
        zero_or_more_possessive('')
    with pytest.raises(ValueError) as excObj:
        zero_or_more_possessive('', '')

    assert zero_or_more_possessive('x') == 'x*+'
    assert zero_or_more_possessive('x', 'y') == 'xy*+'


def test_one_or_more_possessive():
    with pytest.raises(ValueError) as excObj:
        one_or_more_possessive()
    with pytest.raises(ValueError) as excObj:
        one_or_more_possessive('')
    with pytest.raises(ValueError) as excObj:
        one_or_more_possessive('', '')

    assert one_or_more_possessive('x') == 'x++'
    assert one_or_more_possessive('x', 'y') == 'xy++'


def test_optional_possessive():
    with pytest.raises(ValueError) as excObj:
        optional_possessive()
    with pytest.raises(ValueError) as excObj:
        optional_possessive('')
    with pytest.raises(ValueError) as excObj:
        optional_possessive('', '')

    assert optional_possessive('x') == 'x?+'
    assert optional_possessive('x', 'y') == 'xy?+'


if __name__ == "__main__":
    pytest.main()
