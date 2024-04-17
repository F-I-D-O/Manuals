PowerShell is the new command line interface for Windows that replaces the old command prompt. It is superior in almost every aspect so it is recommended to use it instead of the old command prompt. 

The PowerShell script files have the `.ps1` extension. 


# Important Aspects
## New PowerShell
The PowerShell Integrated in Windows is version 5. You can recognize it by the iconical blue background color. This old version has some important limitations (e. g. [it cannot pass arguments containing arguments with spaces](https://stackoverflow.com/questions/6714165/powershell-stripping-double-quotes-from-command-line-arguments)).

Therefore, it is best to install the [new PowerShell](https://github.com/PowerShell/PowerShell) first.

## Quick Edit / Insert Mode
PowerShell enables copy/pase of commands. The downside is that every time you click inside PowerShell, the execution (if PowerShell is currently executing somethig) stops. To resume the execution, hit `enter`.

## Arguments starting with `-` and containing `.`
If a program argument starts with `-`, **and** contains `.` it needs to be wrapped by `'`. Otherwise, the argument will be split on the dot. Example:
```
mvn exec:java -Dexec.mainClass=com.example.MyExample -Dfile.encoding=UTF-8
```

In Powershell, this needs to be converted to:
```PowerShell
mvn exec:java '-Dexec.mainClass=com.example.MyExample' '-Dfile.encoding=UTF-8'
```

The problem may arise if the argument or its part needs to be quotted as well. Then:
- for first level of quoting, use `"` (double quotes)
- for second level of quoting, use `''` (two single quotes)
Example:
```PowerShell
mvn exec:exec '-Dexec.executable="java"' '-Dexec.args="-Xmx30g -Djava.library.path=''C:\Program Files\HDF_Group\HDF5\1.14.3\bin'' -classpath %classpath cz.cvut.fel.aic.simod.OnDemandVehiclesSimulation"'
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


# Command execution
Normal commands are executed by just typing them. However, if the command contains a space, wrapping it in quotes does not work. In this case, the `&` operator has to be used. Example:
```PowerShell
& "C:\Program Files\Java\jdk1.8.0_181\bin\java.exe" -version
```


# I/O
Output forwading is done using `|` (pipe) operator, just like in Linux. For redirecting the output to a file, there are the following operators:
- `>`: redirect to file, overwrite if exists
- `>>`: redirect to file, append if exists
- `>&1`: redirect to standard output stream

When using any of these operators, by default, the standard output stream is redirected. If we want to redirect the standard error stream, we have to prepend 2 to the operator. Example:
```PowerShell
dir > out.txt # redirect standard output stream to out.txt
dir 2> err.txt # redirect standard error stream to err.txt
```

If we want both see the output and redirect it to a file, we can use the `Tee-Object` command which is the equivalent of the `tee` command from Linux


# Control Structures

## Cycles

### `foreach`
The `foreach` cycle iterates over a collection. The syntax is:
```PowerShell
foreach ($item in $collection) {
    # do something with $item
}
```


# String Manipulation

## Replace
The `Replace` method replaces all occurences of a string with another string. The syntax is:
```PowerShell
$myString.Replace("oldString", "newString")
```

# `Select-String`
The `Select-String` is the `grep` equivalent for PowerShell. The alias for the comand is `sls`. Parameters:
- `-Content <before>[, <after>]`: Select also `<before>` lines before the matched line and `<after>` lines after the matched line



# Arrays
To creante an array, use the `@()` operator: `a = @()` To add an element to an array, use the `+=` operator: `a += 1`. The arrays can be iterated over using the `foreach` loop.



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


## Get Help
[Mirosoft documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-help)

To get help about a command, use the `Get-Help` (alias `man`) command. Example:
```PowerShell
Get-Help Get-ChildItem
```
If the output is the list of articles, it means that there is no help for the command. 


## Translate alias to command
To translate an alias to a command, use the `Get-Alias` command. Example:
```PowerShell
Get-Alias ls # returns Get-ChildItem
```
