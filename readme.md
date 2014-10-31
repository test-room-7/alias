View and set command aliases in Windows.

### How to setup?
Just run `setup.reg`. After that you can manage your aliases.  
Aliases file is located in `%USERPROFILE%\Documents\Scripts`.

### Managing aliases
Get list of available aliases:
```cmd
> alias
adbwifi, alias, apktool, at
```
Add an alias:
```cmd
> alias test=dir \b $*
Added test
```
Show the alias:
```cmd
> alias test
dir \b $*
```
Remove the alias:
```cmd
> alias test=
Removed test
```

### External links
`aliases.ini` [example][1]

[1]: https://raw.github.com/alexesprit/bat-scripts/master/aliases.ini
