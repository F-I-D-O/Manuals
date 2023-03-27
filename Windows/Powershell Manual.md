
# Important Aspects
## New PowerShell
The PowerShell Integrated in Windows is version 5. You can recognize it by the iconical blue background color. This old version has some important limitations (e. g. [it cannot pass arguments containing arguments with spaces](https://stackoverflow.com/questions/6714165/powershell-stripping-double-quotes-from-command-line-arguments)).

Therefore, it is best to install the [new PowerShell](https://github.com/PowerShell/PowerShell) first.

## Quick Edit / Insert Mode
PowerShell enables copy/pase of commands. The downside is that every time you click inside PowerShell, the execution (if PowerShell is currently executing somethig) stops. To resume the execution, hit `enter`.

## Arguments starting with `-` 
If a program argument starts with `-`, **and** contains `.` it needs to be wrapped by `'`. Otherwise, the argument will be split on the dot. Example:
In sommand prompt or on Linux:
```
mvn exec:java -Dexec.mainClass=com.example.MyExample -Dfile.encoding=UTF-8
```

In Powershell, this needs to be converted to:
```
mvn exec:java '-Dexec.mainClass=com.example.MyExample' '-Dfile.encoding=UTF-8'
``` 

## Escaping `"` and `'` in Arguments
Double quotes `"` contained in arguments can be preserved by escaping with backslash: `\"`. Example for that can be passing an argument list to some executable:
```
'args=\"arg1 arg2\"'
```

Single quotes `'` are esceped by duble single quote: `''`. Example can be passing a list of args, where some of them contains space:

```
'args=\"''arg1 with space'' arg2\"'
```

## No Output for EXE file
Some errors are unfortunatelly not reported by powershell (e.g. [missing dll](https://stackoverflow.com/questions/23012332/how-to-make-powershell-tell-me-about-missing-dlls)). The solution is to run such program in cmd, which reports the error.

# SSH
More details can be found in the [Linux Manual](https://docs.google.com/file/d/1G8q2ZhsJMKkeJQuGKA9IjpFLvMlAahKJ/edit)
-   `ssh` should be ready in PowerShell, if not, add it in -> `Apps & Features` -> `Optional features`
-   specifying port by `<addres>:<port>` is not supported in PowerShell, it is necessary to use the `-p` parameter
-   if we need something else than the default shell just append the command at the end of the script



# Network

## [`netstat`](https://en.wikipedia.org/wiki/Netstat)
The [`netstat`](https://en.wikipedia.org/wiki/Netstat) is the basic network monitoring program. It displays TCP connections. It originated on Linux, so the usage and parameters are described in the Linux manual. Below, we discuss the differencies in the command interface and behavior of the Windows version of the command.

[Winndows manual](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat).

### Lot of kubernetes entries in the log
By default, the netstat command translates IPs into names. Unfortunatelly, on Windows, it also uses the information from the hosts file (`C:\Windows\System32\drivers\etc\hosts`). This is a problem, because some services, like Docker, can use the `hosts` file to redirect some adddress to localhost. Therefore, at the end, all localhost entries are named kubernetes. Solution options:
- use the `-n` parameter for `netstat` or
- remove the redirection to `localhost` in the `hosts` file 

### Display executable for connection
To display executable for all connection, just use the `-b` swith. For filtering out only some, you have to use the `-Context` parameter in the `Select-String` command, as the executable is printed one line below the connection: `netstat -b | sls <search pattern> -Context 0,1`


# `Select-String`
The `Select-String` is the `grep` equivalent for PowerShell. The alias for the comand is `sls`. Parameters:
- `-Content <before>[, <after>]`: Select also `<before>` lines before the matched line and `<after>` lines after the matched line



# Usefull Commands
## Print system variable
```
echo $env:PATH
```


## File Encoding Conversion

`gc [INPUT PATH] | Out-File -en [ENCODING] [OUTPUT PATH]`

example: 
```
gc "C:\AIC data\Roadmaptools big data test/map-filtered.osm" | Out-File -en utf8 "C:\AIC data\Roadmaptools big data test/map-filtered-utf8.osm"
```
NOTE: it is not very fast :)

## Delete all files with a certain extension
```
ls *.extension -Recurse | foreach {rm $_}
```

to try it, add the `-WhatIf` parameter to `rm`

## Batch rename 
Example
```ps
dir . | % { $newName = $_.Name -replace '^DSC_0(.*)', 'DSC_1$1'; rename-item -newname $newName -literalPath $_.Fullname -whatif}
```
## Count Lines in large file

`switch -File FILE { default { ++$count } }`
