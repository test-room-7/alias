# alias [![Version][PyPIBadge]][PyPIUrl] [![Test status][WorkflowBadge]][WorkflowUrl]

Manage command aliases in Windows.

## Installation

```sh
> pip install alias-windows
```

By default aliases are stored in `%USERPROFILE%\Documents\Scripts\Aliases`. You can set the directory to store aliases by changing the environment variable called `%ALIASES_DIR%`.

## Managing aliases

Get the list of available aliases:
```cmd
REM Default output
> alias
apktool, gsh, gst

REM Verbosed output
> alias -v
apktool = %SOFTWARE%\apktool\apktool.bat %*
gsh = git show $*
gst = git status --short --branch %*
```

Add an alias:
```cmd
> alias test=dir \b %*
Added test
```

Add an alias with multiple commands:
```cmd
REM Use double quotes to wrap commands joined with &&
> alias gpht="git push %* && git push --tags %*"
```

Show the alias:
```cmd
REM List aliases start with a given input
> alias g
gsh, gst

REM Show the alias
> alias test
dir \b %*
```

Search for a text in alias commands:
```cmd
REM Default output
> alias -s apk
baksmali, smali

REM Verbosed output
> alias -s apk -v
baksmali = %SOFTWARE%\apktool\apktool.bat d %*
smali = %SOFTWARE%\apktool\apktool.bat b %*
```

Delete the alias:
```cmd
> alias -d test
Deleted test
```

## Environment variables

`alias` changes two variables:
1. `%ALIASES_DIR%`
Directory where aliases are stored.
2. `%PATH%`
Adds `%ALIASES_DIR%` to `%PATH%`.

## License

This project is licensed under the [MIT License][License].

[License]: https://github.com/test-room-7/alias/blob/master/LICENSE.md
[PyPIBadge]: https://img.shields.io/pypi/v/alias-windows
[PyPIUrl]: https://pypi.org/project/alias-windows/
[WorkflowBadge]: https://img.shields.io/github/workflow/status/alexesprit/alias/Test?label=Test
[WorkflowUrl]: https://github.com/test-room-7/alias/actions
