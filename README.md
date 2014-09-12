random-sublime-text-plugin
==========================

Plugin for sublime text to generate random, ints, floats, strings and words.

It works in Sublime Text 2 *and* ST3


Usage
=====

This plugin can only be accessed through the *cmd/ctrl + shift + p* command.

Type *random* and you get the following choices:

* Random:int - requires a range from a-b separated with a: *-*. Default: 1-100
* Random:float - requires a range from a-b separated with a: *-*. Default: 1-100
* Random:letters - generatates a random string of lower and upper -case letters with a length between 3 and 17
* Random:letters and numbers - generatates a random string of lower and upper -case letters and numbers with a length between 3 and 17
* Random:word - picks a random word from /usr/share/dict/words
* Random:text - picks 24 random words from /usr/share/dict/words
* Random:first_name - picks a random first name from the built-in datafile
* Random:last_name - picks a random last name from the built-in datafile
* Random:full_name - picks a random full name from the built-in datafiles
* Random:url - generates a URL using random words from /usr/share/dict/words