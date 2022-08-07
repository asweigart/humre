# Humre

A human-readable regular expression module for Python. Humre handles regex syntax for you and creates regex strings to pass to Python's re.compile(). Pronounced "hum, ree".

It is similar to [Swift's regex DSL](https://swiftregex.com/) or an advanced form of Python regex's `re.VERBOSE` mode.

Note that until version 1.0 is released, the API for this module could change. Please send suggestions and feedback to [al@inventwithpython.com](mailto://al@inventwithpython.com).

Quickstart
----------

    >>> from humre import *
    >>> regexStr = either(OPEN_PAREN + exactly(3, digit) + CLOSE_PAREN, exactly(3, DIGIT)) + '-' + exactly(3, digit) + '-' + exactly(4, DIGIT)
    >>> regexStr
    '\\(\\d{3}\\)|\\d{3}-\\d{3}-\\d{4}'
    >>> patternObj = compile(regexStr)
    >>> matchObj = patternObj.search('Call 415-555-1234 today!')
    >>> matchObj
    <re.Match object; span=(5, 17), match='415-555-1234'>
    >>> matchObj.group()
    '415-555-1234'


Frequently Asked Questions
--------------------------

**What Does Humre Provide?**

Humre provides a collection of functions and constants to create regex strings without having to know the specific regex symbols. These offer more structure and readability than regex strings.

**What's Wrong with Python's re Module?**

It's more what's wrong with regular expression syntax. Regex strings can look like a cryptic mess of punctuation marks, and even if you're an experienced software engineer, complex regex strings can be hard to read and debug.

**Doesn't Verbose Mode Fix That Problem?**

A little. But because verbose mode still has the regex string as a string value, dev tools such as linters, syntax highlighting, and matching parentheses highlighting can't be employed. Also, dealing with escape characters can still be a pain.

**Is Humre a New Reimplementation of Python's re Module?**

No. Humre only creates the regex strings to pass to `re.compile()` (or to pass to `humre.compile()` which wraps it.)

**What Are Benefits of Using Humre Instead of Writing My Own Regex Strings?**

* Your editor's parentheses matching works.
* Your editor's syntax highlight works.
* Your editor's linter and type hints tool picks up typos.
* Your editor's autocomplete works.
* Auto-formatter tools like Black can automatically format your regex code.
* Humre handles raw strings/string escaping for you.
* You can put actual Python comments alongside your Humre code.
* Better error messages for invalid regexes

**Is It A Good Idea To Use The `from humre import *` Importing Syntax?**

In this case, sure. Generally this form importing is frowned on, but it'll keep your `optional(group('cat' + DIGIT))` code from becoming `humre.optional(humre.group('cat' + humre.DIGIT))`. Note that this will overwrite the (infrequently-used) built-in `compile()` function with `humre.compile()`, which is a wrapper for `re.compile()`.

**How Do I Combine Humre's Functions and Constants Together?**

Every Humre function returns a regex string, so you can use f-strings and string concatenation to combine them:

    exactly(5, DIGIT) + optional(WHITESPACE) + one_or_more(NONWHITESPACE)

Humre vs re Comparison
----------------------

Here's a comparison of the code for Python's `re` module versus the equivalent code with Humre (formatted with the Black code-formatting tool.)

American Phone Number with re:

    import re
    re.compile('\d{3}-\d{3}-\d{4}')

American Phone Number with Humre:

    from humre import *
    compile(exactly(3, DIGIT), "-", exactly(3, DIGIT), "-", exactly(4, DIGIT))

Hexadecimal Number with Optional Leading `0x` or `0X` and Consistent Casing with re:

    import re
    re.compile('(?:(?:0x|0X)[0-9a-f]+)|(?:(?:0x|0X)[0-9A-F]+)|(?:[0-9a-f]+)|(?:[0-9A-F]+)')

Hexadecimal Number with Optional Leading `0x` or `0X` and Consistent Casing with re:

    from humre import *
    compile(
        either(
            noncap_group(noncap_group(either('0x', '0X')), one_or_more(chars('0-9a-f'))),
            noncap_group(noncap_group(either('0x', '0X')), one_or_more(chars('0-9A-F'))),
            noncap_group(one_or_more(chars('0-9a-f'))),
            noncap_group(one_or_more(chars('0-9A-F')))
        )
    )

Number with or without comma-formatting including decimal point with re:

    import re
    re.compile(r'(?:\+|-)?(?:(?:\d{1,3}(?:,\d{3})+)|\d+)(?:\.\d+)?')

Number with or without comma-formatting including decimal point with Humre:

    from humre import *
    compile(
        # optional negative or positive sign:
        optional(noncap_group(either(PLUS_SIGN, '-'))),
        # whole number section:
        noncap_group(either(
            # number with commas:
            noncap_group(between(1, 3, DIGIT), one_or_more(noncap_group(',', exactly(3, DIGIT)))),
            # number without commas:
            one_or_more(DIGIT)
        )),
        # fractional number section (optional)
        optional(noncap_group(PERIOD, one_or_more(DIGIT)))
        )

Or you can use Humre's included `NUMBER` pattern:

    from humre import *
    compile(NUMBER)




Quick Reference
----------------

Here's a quick list of all of Humre's functions and constants, and the regex strings that they produce:

| Function | Regex Equivalent |
|----------------|------------------|
| `group('A')` | `'(A)'` |
| `optional('A')` | `'A?'` |
| `either('A', 'B', 'C')` | `'A|B|C'` |
| `exactly(3, 'A')` | `'A{3}'` |
| `between(3, 5, 'A')` | `'A{3:5}'` |
| `at_least(3, 'A')` | `'A{3,}'` |
| `at_most(3, 'A')` | `'A{,3})'` |
| `chars('A-Z')` | `'[A-Z]'` |
| `nonchars('A-Z')` | `'[^A-Z]'` |
| `zero_or_more('A')` | `'A*'` |
| `zero_or_more_lazy('A')` | `'A*?'` |
| `one_or_more('A')` | `'A+'` |
| `one_or_more_lazy('A')` | `'A+?'` |
| `starts_with('A')` | `'^A'` |
| `ends_with('A')` | `'A$'` |
| `starts_and_ends_with('A')` | `'^A$'` |
| `named_group('group_name', 'A')` | `'(?P<group_name>A)'` |
| `noncap_group('A')` | `'(?:A)'` |
| `positive_lookahead('A')` | `'(?=A)'` |
| `negative_lookahead('A')` | `'(?!A)'` |
| `positive_lookbehind('A')` | `'(?<=A)'` |
| `negative_lookbehind('A')` | `'(?<!A)'` |
| `back_reference(1)` | `r'\1'` |
| `back_ref(1)` | `r'\1'` |
| `atomic_group('A')` | `'(?>A)'` |
| `zero_or_more_possessive('A')` | `'A*+'` |
| `one_or_more_possessive('A')` | `'A++'` |
| `optional_possessive('A')` | `'A?+'` |


The convenience functions combine a Humre function with the `group()` function since putting regexes in groups is so common, such as with `([A-Z])+` putting the character class

| Convenience Function | Function Equivalent | Regex Equivalent |
|----------------------------|---------------------|------------------|
| `optional_group('A')` | `optional(group('A'))` | `'(A)?'` |
| `group_either('A')` | `group(either('A', 'B', 'C'))` | `'(A|B|C)'` |
| `group_exactly('A')` | `group(exactly(3, 'A'))` | `'(A){3}'` |
| `group_between('A')` | `group(between(3, 5, 'A'))` | `'(A){3,5}'` |
| `group_at_least('A')` | `group(at_least(3, 'A'))` | `'(A){3,}'` |
| `group_at_most('A')` | `group(at_most(3, 'A'))` | `'(A){,3}'` |
| `zero_or_more_group('A')` | `zero_or_more(group('A'))` | `'(A)*'` |
| `zero_or_more_lazy_group('A')` | `zero_or_more_lazy_group('A'))` | `'(A)*?'` |
| `one_or_more_group('A')` | `one_or_more(group('A'))` | `'(A)+'` |
| `one_or_more_lazy_group('A')` | `one_or_more_lazy(group('A'))` | `'(A)+?'` |
| `group_chars('A-Z')` | `group(chars('A-Z'))` | `'([A-Z])'` |
| `group_nonchars('A-Z')` | `group(nonchars('A-Z'))` | `(['^A-Z])'` |

Humre provides constants for the `\d`, `\w`, and `\s` character classes as well several other characters that need to be escaped:

| Constant | Regex Equivalent |
|----------------|------------------|
| `DIGIT` | `r'\d'` |
| `WORD` | `r'\w'` |
| `WHITESPACE` | `r'\s'` |
| `NONDIGIT` | `r'\D'` |
| `NONWORD` | `r'\W'` |
| `NONWHITESPACE` | `r'\S'` |
| `BOUNDARY` | `r'\b'` |
| `NEWLINE` | `r'\n'` |
| `TAB` | `r'\t'` |
| `QUOTE` | `r"\'"` |
| `DOUBLE_QUOTE` | `r'\"'` |
| `PERIOD` | `r'\.'` |
| `CARET` | `r'\^'` |
| `DOLLAR_SIGN` | `r'\$'` |
| `ASTERISK` | `r'\*'` |
| `PLUS_SIGN` | `r'\+'` |
| `QUESTION_MARK` | `r'\?'` |
| `OPEN_PARENTHESIS` | `r'\('` |
| `OPEN_PAREN` | `r'\('` |
| `CLOSE_PARENTHESIS` | `r'\)'` |
| `CLOSE_PAREN` | `r'\)'` |
| `OPEN_BRACE` | `r'\{'` |
| `CLOSE_BRACE` | `r'\}'` |
| `OPEN_BRACKET` | `r'\['` |
| `CLOSE_BRACKET` | `r'\]'` |
| `BACKSLASH` | `r'\\'` |
| `PIPE` | `r'\|'` |
| `BACK_1` | `r'\1'` |
| `BACK_2` | `r'\2'` |
| `BACK_3` | `r'\3'` |
| `BACK_4` | `r'\4'` |
| `BACK_5` | `r'\5'` |
| `BACK_6` | `r'\6'` |
| `BACK_7` | `r'\7'` |
| `BACK_8` | `r'\8'` |
| `BACK_9` | `r'\9'` |

Humre also provides constants for commonly used patterns:

| Humre Pattern Constants | Regex Equivalent | Note |
|----------------------------------|------------------|------|
| `ANYTHING` | `'.*?'` | lazy "zero or more of anything" match |
| `EVERYTHING` | `'.*'` | greedy "zero or more of anything" match, aka dot star |
| `SOMETHING` | `'.+?'` | lazy "one or more of anything" match |
| `GREEDY_SOMETHING` | `'.+'` | greedy "one or more of anything" match |
| `ANYCHAR` | `'.'` | |
| `LETTER` | (too big to display) | Matches `isalpha()` |
| `NONLETTER` | (too big to display) | Matches `not isalpha()` |
| `UPPERCASE` | (too big to display) | Matches `isupper()` |
| `NONUPPERCASE` | (too big to display) | Matches `not isupper()` |
| `LOWERCASE` | (too big to display) | Matches `islower()` |
| `NONLOWERCASE` | (too big to display) | Matches `not islower()` |
| `ALPHANUMERIC` | (too big to display) | Matches `isalnum()` |
| `NONALPHANUMERIC` | (too big to display) | Matches `not isalnum()` |
| `HEXADECIMAL` | `'[0-9A-f]'` | |
| `NONHEXADECIMAL` | `'[^0-9A-f]'` | |
| `NUMBER` | `r'(?:\+|-)?(?:(?:\d{1,3}(?:,\d{3})+)|\d+)(?:\.\d+)?'` | Comma-formatted numbers |
| `EURO_NUMBER` | `r'(?:\+|-)?(?:(?:\d{1,3}(?:\.\d{3})+)|\d+)(?:,\d+)?'` | Period-formatted numbers |
| `HEXADECIMAL_NUMBER` | `'(?:(?:0x|0X)[0-9a-f]+)|(?:(?:0x|0X)[0-9A-F]+)|(?:[0-9a-f]+)|(?:[0-9A-F]+)'` | Can have leading `0x` or `0X`. |
| `ASCII_LETTER` | `'[A-Za-z]'` | |
| `ASCII_NONLETTER` | `'[^A-Za-z]'` | |
| `ASCII_UPPERCASE` | `'[A-Z]'` | |
| `ASCII_NONUPPERCASE` | `'[^A-Z]'` | |
| `ASCII_LOWERCASE` | `'[a-z]'` | |
| `ASCII_NONLOWERCASE` | `'[^a-z]'` | |
| `ASCII_ALPHANUMERIC` | `'[A-Za-z0-9]'` | |
| `ASCII_NONALPHANUMERIC` | `'[^A-Za-z0-9]'` | |
