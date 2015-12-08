View and set command aliases in Windows.

### How to setup?
Just run `setup.py`.

By default aliases are stored in `%USERPROFILE%\Documents\Scripts\Aliases`.

### Managing aliases
Get list of available aliases:
```cmd
> alias
apktool, gsh, gst
> alias --verbose
apktool = %SOFTWARE%\apktool\apktool.bat %*
gsh = git show $*
gst = git status --short --branch %*
```
Add an alias:
```cmd
> alias test=dir \b %*
Added test
```
Show the alias:
```cmd
> alias g
gsh, gst
> alias test
dir \b %*
```
Remove the alias:
```cmd
> alias test=
Removed test
```

### External links
`aliases.ini` [example][1]

[1]: https://raw.github.com/alexesprit/bat-scripts/master/aliases.ini
