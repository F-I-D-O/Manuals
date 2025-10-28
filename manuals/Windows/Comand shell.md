# Introduction

- [wiki cmd.exe](https://en.wikipedia.org/wiki/Cmd.exe)
- [Windows Commands Overview and Reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
- [Wikibook](https://en.wikibooks.org/wiki/Windows_Batch_Scripting)



Command shell is the basic shell in Windows and one of the two preinstalled shells (the other is PowerShell).

The commands available in the Command shell are refered to as *Windows commands*.

As the PowerShell was designed as an extension of the Command shell, **the Windows commands can be executed in PowerShell**.

Script files for the Command shell are often called [batch files](https://en.wikipedia.org/wiki/Batch_file), and have the `.bat` or `.cmd` extension.


# Comments
Instead of some conventional comment syntax, the Command shell uses the [`rem`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rem) command. Example:

```batch
rem This is a comment. We print Hello, World! below it.
echo Hello, World!
```


# `echo`: Displaying text and automatic command printing
The [`echo`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/echo) command serve two important purposes:

- displaying text, like in PowerShell and
- switching on/off the automatic command printing feature of the Command shell.

The automatic command printing basically prints every command that is executed. We can skip the printing by prefixing the command with `@`. Example:
```batch
echo Hello, World! # prints echo Hello, World!\nHello, World!
@echo Hello, World! # prints Hello, World!
```
However, typically, we want to disable the automatic command printing for the whole script, this can be done by adding call `echo` with parameter `off`. To turn it back on, we can call `echo` with parameter `on`. So the typical first command in a batch file is:
```batch
@echo off 
```
Which disables the automatic command printing and also skips it for the disabeling command itself.

# Executable Execution


## Executable path resolution
[Old reference for Windows NT](https://learn.microsoft.com/en-us/previous-versions//cc723564(v=technet.10)#command-search-sequence)

Unfortunatelly, there is no up-to-date reference for Command Shell execution logic. However, using the information from the old reference, the execution logic is as follows:

- If the specified executable is a path, the path is evaluated. If the path is valid, the executable is executed. Otherwise, error is raised.
- If the specified executable is a name, the name is searched in the locations below (in order):
    1. Windows Commands
    1. Current directory
    1. directories listed in the `PATH` environment variable, in the order they are listed

When we mention the executable name, we mean the name of the executable file with the extension. Executables names can be also specified without the extension, but only if the extension is listed in the `PATHEXT` environment variable.


# Variables
**Variables are set** using the [`set`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1) command. Example:
```batch
set myVar=Hello
```

To **use a variable**, we use its name surrounded by `%`. Example:
```batch
echo %myVar%
rem prints Hello
```

To **display all variables**, use the `set` command without any arguments.

Note that unlike in PowerShell, **there is no distinction between local and environment variables**. For example, to set the value of the `PATH` environment variable, we can use the `set` command:

```batch
set PATH=C:\Program Files\Java\jdk1.8.0_181\bin;%PATH%
```



## The `set` command and its important nuances

- [official documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1)
- [ss64 documentation](https://ss64.com/nt/set.html)

The variable setting has several surprising nuances with important consequences:

- all whitespaces are interpreted and not discarded:
    ```batch
    set myVar=Hello
    rem variable 'myVar' is set to 'Hello'
    
    set myVar= Hello
    rem variable 'myVar' is set to ' Hello'

    set myVar =Hello
    rem variable 'myVar ' is set to 'Hello'
    ```

- The quoting for set use a different syntax than expected:

    ```batch
    set myVar="Hello, World!"
    rem myVar is set to '"Hello, World!"'

    set "myVar=Hello, World!" 
    rem myVar is set to 'Hello, World!'
    ```
- no quoting is needed for spaces in the value:
    ```batch
    set myVar=Hello World!
    rem myVar is set to 'Hello World!'
    ```


# String Manipulation
Unlike in PowerShell or programming languages, there is no concatenation operator in Command Shell. Instead, we just place the strings/variables next to each other. Example:

```batch
set myVar=Hello, 
set myVar=%myVar% World!
echo %myVar% # prints "Hello, World!"
```


# Control Statements

## `if`
[documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/if)

The `if` statement has the following syntax:
```batch
if <condition> <then command> [else <command>]
```

There are three types of conditions:

- `<string 1>==<string 2>`: most useful,
- `ERRORLEVEL <number>`: test the return value of the last command, and
- `exists <file>`: test if the file exists

Any of the conditions can be negated by using `if not` instead of `if`.


## `goto`
[documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/goto)

The `goto` statement has the following syntax:
```batch
goto <label>
```

The `<label>` is then prese in the script as `:<label>`. Example:
```batch
goto label

...

:label
echo Hello, World!
```

# Output redirection
[unofficial documentation](https://www.robvanderwoude.com/redirection.php)

The `|` operator is used to redirect the standard output of a command to the input of another command as usual.

The `>` is used to redirect the standard output of a command to a file. By prependind `2`  (`2>`), we redirect the standard error output instead. When changing `>` to `>>`, we write to the file in the append mode.

Using `<` we can redirect a file to the standard input of a command.

Finally, `2>&1` redirects the standard error output to the standard output. This can be combined with the output to file: `<command> > <file> 2>&1` writes both the standard output and the standard error output to the file.

As any `<file>` we can use `NUL` which basically discards the output.


# Command Separation
We can execute multiple commands in the same line. We can use

- `<command 1> & <command 2>`: commands are executed independently, or
- `<command 1> && <command 2>`: `<command 2>` is executed only if `<command 1>` exits with code 0.


# Batch Script Arguments

- [wikibook](https://en.wikibooks.org/wiki/Windows_Batch_Scripting#Command-line_arguments)
- [ss64 documentation](https://ss64.com/nt/syntax-args.html)

When we call commands from a batch script, we can refer to the called arguments called *replacement parameters*. These are `%0` (the name of the script), `%1`--`%9` (the arguments of the script). To refer all script arguments (`%1`--`%9`), we can use `%*`.

Contrary to a typical programming language behavior, the **arguments are not split just by spaces** but also commas (`,`), semi-colons (`;`), equal signs (`=`), and by a horizontal tab. Therefore, one has to be careful if some of these characters are used in the arguments.

## Parameter extension for files
If the argument is a file name, we can get several additional information about the file by applying parameters extensions. These extensions are in format `~<extension>` where `<extension>` is a single letter long and are placed between the `%` and the parameter number. Example:
```batch
echo %~f1
```
The above command prints the full path of the file passed as the first argument.

Most commonly used extensions are:

- `~`: remove any surrounding quotes
- `~f`: full path
- `~d`: drive letter
- `~p`: path, without the drive letter and the file name

We can also combine some extensions:

```batch
echo %~dp1
```
The above command prints the directory of the file passed as the first argument.


# Usefull Commands

## Get the path of the executable/command
To get the path of the executable/command, we can use the `where` command. Example:
```batch
where java
```

If there are more than one executable/command with the same name, all are listed (one per line), from the one to be executed, to the one with the lowest priority.


## `findstr`: Select lines containing a pattern
The [`findstr`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/findstr) command is used to select lines containing a pattern. It is similar to the grep or `Select-String` in PowerShell. However, it can only ever select the whole line, not parts of it.

The command can either:

- read from a file: `findstr <pattern> <file>`, or
- read from the standard input: `<command> | findstr <pattern>`.

By default, the pattern is interpreted as a regular expression. However, `findstr` has a plenty of options to configure the matching:

- `/i`: ignore case
- `/c:<pattern>`: use a literal pattern, instead of a regular expression

## `mklink`: Create a symlink
The [`mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink) command is used to create a symlink. Example:
```batch
mklink <source> <target>
```


# Limitations
The command shell is very limited compared to any other shell that is used in practice. Some of the limitations are:

- no command for selecting line by a number like head/tail
- no command for matching substrings, only whole line can be matched