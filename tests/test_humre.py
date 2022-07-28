from __future__ import division, print_function
import pytest
import humre
from humre import group, decimal, exactly, anything, everything, zero_or_more, one_or_more, between, at_least, at_most, \
    starts_with, ends_with, starts_and_ends_with, either, optional, whitespace, optional_group, group_either, chars, \
    named_group, newline, tab, backslash, quote, double_quote, nonwhitespace, nonchars, compile, \
    period, caret, dollar_sign, asterisk, plus_sign, question_mark, open_brace, close_brace, \
    open_bracket, close_bracket, backslash, pipe, open_paren, close_paren, noncapturing_group, anychar, something

from humre import word

import re

def test_basic():
    # Basic American phone number regex:
    assert r'\d\d\d-\d\d\d-\d\d\d\d' == decimal + decimal + decimal + '-' + decimal + decimal + decimal + '-' + decimal + decimal + decimal + decimal

    # Basic American phone number regex using {3}:
    #assert r'\d{3}-\d{3}-\d{4}' == exactly_3(decimal) + '-' + exactly_3(decimal) + '-' + exactly_4(decimal)
    assert r'\d{3}-\d{3}-\d{4}' == exactly(3, decimal) + '-' + exactly(3, decimal) + '-' + exactly(4, decimal)

    # American phone number with groups:
    assert r'(\d{3})-(\d{3}-\d{4})' == group(exactly(3, decimal)) + '-' + group(exactly(3, decimal) + '-' + exactly(4, decimal))

    # .* tests:
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
            optional(group(either(exactly(3, decimal), open_paren + exactly(3, decimal) + close_paren))) +
            optional(group(either(whitespace, '-', r'\.'))) +
            exactly(3, decimal) +
            group(either(whitespace, '-', r'\.')) +
            exactly(4, decimal) +
            optional(group(zero_or_more(whitespace) + group(either('ext', 'x', 'ext.')) + zero_or_more(whitespace) + between(2, 5, decimal)))
            )

    # Use commas instead of + str concatenation:
    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == \
        group(
            optional(group(either(exactly(3, decimal), open_paren + exactly(3, decimal) + close_paren))),
            optional(group(either(whitespace, '-', r'\.'))),
            exactly(3, decimal),
            group(either(whitespace, '-', r'\.')),
            exactly(4, decimal),
            optional(group(zero_or_more(whitespace),
                     group(either('ext', 'x', 'ext.')),
                     zero_or_more(whitespace),
                     between(2, 5, decimal)))
            )

    assert r'((\d{3}|\(\d{3}\))?(\s|-|\.)?\d{3}(\s|-|\.)\d{4}(\s*(ext|x|ext.)\s*\d{2,5})?)' == \
        group(
            optional_group(either(exactly(3, decimal), r'\(' + exactly(3, decimal) + r'\)')) +
            optional_group(either(whitespace, '-', r'\.')) +
            exactly(3, decimal) +
            group_either(whitespace, '-', r'\.') +
            exactly(4, decimal) +
            optional_group(zero_or_more(whitespace) + group(either('ext', 'x', 'ext.')) + zero_or_more(whitespace) + between(2, 5, decimal))
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

    assert r'[-]?\d\n' == optional(chars('-')) + decimal + newline

    assert r'Student has an ([A-D]) grade' == 'Student has an ' + group(chars('A-D')) + ' grade'

    assert r'([-]?\d+) is the median' == group(optional(chars('-')), one_or_more(decimal)) + ' is the median'

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

    assert "ccd id: \\d+" == 'ccd id: ' + one_or_more(decimal)

    #assert "[%:\r\n]" == chars(r'%:\r\n')  # Test this: is there a difference between "[%:\r\n]" and r"[%:\r\n]"

    assert "%([0-9a-fA-F][0-9a-fA-F])" == '%' + group(chars('0-9a-fA-F'), chars('0-9a-fA-F'))

    assert r'\?sid=(?P<sid>\d+)' == question_mark + 'sid=' + named_group('sid', one_or_more(decimal))

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

    assert r'^CPU\(s\):\s*(\d+)' == starts_with('CPU' + open_paren + 's' + close_paren + ':' + zero_or_more(whitespace)) + group(one_or_more(decimal))

    assert '^GOOGLE_RELEASE=(.+)$' == starts_and_ends_with('GOOGLE_RELEASE=', group(one_or_more(anychar)))

    assert '^(.+)=(.+)$' == starts_and_ends_with(group(something), '=', group(something))

    assert '<.*?>' == '<' + anything + '>'

    assert r'chr(\d+):(\d+)(-(\d+))?' == 'chr' + group(one_or_more(decimal)) + ':' + group(one_or_more(decimal)) + \
        optional_group('-', group(one_or_more(decimal)))

    assert r'chr(\d+)(:(\d+)(-(\d+))?)?' == 'chr' + group(one_or_more(decimal)) + \
        optional_group(':', group(one_or_more(decimal)), optional_group('-', group(one_or_more(decimal))))

    assert "[^a-zA-Z0-9']+" == one_or_more(nonchars("a-zA-Z0-9'"))

    # Purposefully left this as a non-raw string:
    assert "<person>([,\s]*(and)*[,\s]*<person>)+" == '<person>' + one_or_more_group()

r"""


re.sub("<person>([,\s]*(and)*[,\s]*<person>)+", " people ", t)

re.sub("[()[\].,|:;?!=+~\-\/{}]", ",", t)

re.sub('''['"`]''', ' " ', t)



re.sub('(\s*"+\s*)+', ' " ', t)
re.sub("(\d),(\d{3})", r"\1\2", t)
re.sub("(\w)\.(\w)", rf"\1{temp_token}dot{temp_token}\2", t)
r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)", rf"{temp_token}quote{temp_token}", t



'<math.*?alttext="\{\\displaystyle (.*?)\}"'

'([^-+\.\:0-9])+'

'(\d+)'

re.compile(U"[?-??]",re.U|re.I)

re.compile(r"(\w+(\W*\d+\W*)?\-?\w*?[^\S\t]*)*" + delims, re.I|re.U)

re.sub(f"{temp_token}slash{temp_token}", "/", t)

re.sub(
        r"'(?=([stdm]|(ll)|(re)|(ve)|(ll))\b)", rf"{temp_token}quote{temp_token}", t

re.sub("(\s*,+\s*)+", ", ", t)


for w in re.sub(rb'[\W_]', b' ', line.strip()).split(b' '):
    if w: count[w] += 1


"""












if __name__ == "__main__":
    pytest.main()

