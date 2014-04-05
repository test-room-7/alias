alias
=====
View and set command aliases in Windows.

How to setup?
=====
1. Run autorun.reg.
3. Put aliases.ini file with your aliases in %USERPROFILE%\Documents\Scripts. You can get example of aliases.ini [here][1].

Usage
=====
Get list of aliases:

    alias
Add an alias:

    alias test=dir \b $*
Remove some alias:

    alias test=

[1]: https://raw.github.com/alexesprit/bat-scripts/master/aliases.ini