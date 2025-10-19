# Introduction

- [wiki](https://en.wikipedia.org/wiki/Cmd.exe)
- [Windows Commands Overview and Reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
- [Wikibook](https://en.wikibooks.org/wiki/Windows_Batch_Scripting)



Command shell is the basic shell in Windows and one of the two preinstalled shells (the other is PowerShell).

The commands available in the Command shell are refered to as *Windows commands*.

As the PowerShell was designed as an extension of the Command shell, **the Windows commands can be executed in PowerShell**.

Script files for the Command shell are often called [batch files](https://en.wikipedia.org/wiki/Batch_file), and have the `.bat` or `.cmd` extension.



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
set myVar=Hello, World!
```

To **use a variable**, we use its name surrounded by `%`. Example:
```batch
echo %myVar% # prints "Hello, World!"
```

Note that unlike in PowerShell, **there is no distinction between local and environment variables**. For example, to set the value of the `PATH` environment variable, we can use the `set` command:

```batch
set PATH=C:\Program Files\Java\jdk1.8.0_181\bin;%PATH%
```

To **display all variables**, use the `set` command without any arguments.



# String Manipulation
Unlike in PowerShell or programming languages, there is no concatenation operator in Command Shell. Instead, we just place the strings/variables next to each other. Example:

```batch
set myVar=Hello, 
set myVar=%myVar% World!
echo %myVar% # prints "Hello, World!"
```