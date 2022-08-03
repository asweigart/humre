# humre
A human-readable regular expression module for Python.

UNDER CONSTRUCTION


Why is Humre Better Than Python's re Module and regex syntax?

- more readable, it's like verbose mode except you can have actual python code and actual comments and spacing and your tool support is better cause it can do syntax highlighting
- missing parens in regex str isn't detectable by a linter, but typos in your humre code are because it's just python code.
- humre doesn't force you to mess around with raw strings and escape characters (i.e. you can backslash hell)
- you get autocomplete


Is Humre a New Reimplementation of Python's re Module?

No.





Design goal: never have to mess around with raw strings when working with humre.


I would like help translating this.



Interesting Python regex syntax that I learned making this:

- People escape the hyphen outside of character classes and it's unnecessary. re.compile(r'\-') is the same as re.compile(r'-'). The regex language allows you to have unnecessary escape characters like \-.

- [A-z] captures both uppercase and lowercase just like [A-Za-z]

- [À-ÿ] captures Roman letters with accent marks



>>> re.compile('A{,3}').search(' AAAAA+')
<re.Match object; span=(0, 0), match=''>
>>> re.compile('A{,3}').search('AAAAA+')
<re.Match object; span=(0, 3), match='AAA'>