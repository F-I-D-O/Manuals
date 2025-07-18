# Introduction
PowerShell is the new command line interface for Windows that replaces the old command prompt. It is superior in almost every aspect so it is recommended to use it instead of the old command prompt.

The PowerShell script files have the `.ps1` extension.

In addition to system commands, PowerShell can also execute native PowerShell commands called [cmdlets](https://learn.microsoft.com/en-us/powershell/scripting/powershell-commands).


## New PowerShell
The PowerShell Integrated in Windows is version 5. You can recognize it by the iconical blue background color. This old version has some important limitations (e. g. [it cannot pass arguments containing arguments with spaces](https://stackoverflow.com/questions/6714165/powershell-stripping-double-quotes-from-command-line-arguments)).

Therefore, it is best to install the [new PowerShell](https://github.com/PowerShell/PowerShell) first.


## Quick Edit / Insert Mode
PowerShell enables copy/pase of commands. The downside is that every time you click inside PowerShell, the execution (if PowerShell is currently executing somethig) stops. To resume the execution, hit `enter`.

## Resources

- [Microsoft documentation](https://learn.microsoft.com/en-us/powershell/scripting/overview)
- [SS64](https://ss64.com/ps/)


# Script Blocks: standalone blocks, functions, and scripts
[documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_script_blocks)

A basic unit of execution in PowerShell is a *script block*. A script block can be:

- a piece of code enclosed in curly braces `{}`,
- a function,
- a script

A script block can have parameters. The parameters are defined using the `param` keyword. Example:
```PowerShell
$myFunction = {
    param($param1, $param2)
    # do something
}

# or in a function
function MyFunction {
    param($param1, $param2)
    # do something
}

# or in a script
param($param1, $param2)
```

## Parameter blocks
The parameter block defines the parameters of the script block. By default (`param()`), only the build in parameters are available. In the parameter block, individual parameters are divided by commas. Example:
```PowerShell
$myFunction = {
    param($param1, $param2)
    # do something
}
```

Parameters can be **typed**. Example:
```PowerShell
$myFunction = {
    param([int]$param1, [string]$param2, [switch]$param3)
    # do something
}
```
The [`switch` type](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters?view=powershell-7.5#switch-parameters) is a boolean parameter that does not require a value. It is set to `True` if the parameter is present.

Parameters can be **mandatory**. Example:
```PowerShell
$myFunction = {
    param(
        [Parameter(Mandatory)][int]$param1, 
        [Parameter(Mandatory)][string]$param2, 
        [switch]$param3
    )
    # do something
}
```

We can also **validate** the parameters. Example:
```PowerShell
$myFunction = {
    param(
        [Parameter(Mandatory)][ValidateRange(0, 100)][int]$param1, 
        [Parameter(Mandatory)][ValidateSet("a", "b", "c")][string]$param2, 
        [Parameter(Mandatory)][ValidateScript({$_ -eq "a" -or $_ -eq "b"})][string]$param3
    )
    # do something
}
```
Also with custom error message:
```PowerShell
$myFunction = {
    param(
        [Parameter(Mandatory)][ValidateScript({ Test-Path $_ }, ErrorMessage="Path does not exists: {0}")][string]$path
    )
    # do something
}
```

The advanced usage of parameters is described in the [documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters).



# Quoting
[documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)

In PowerShell, there are two types of quoting:

- `"` (double quotes): for expandable strings. These strings can contain variables and expressions that are evaluated.
    - non-basic variables need to be wrapped by expression `$()`, e.g. `$($PSVersionTable.PSVersion)`
    - To separate the variable from the following text, use `${}`. Example: `${myVar}Text`
    - to escape (not evaluate) the `$` sign, use the backtick: `` echo "`$myVar" `` prints `$myVar`
- `'` (single quotes): for literal strings. These strings are not evaluated.


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



# Command execution
There are several ways how to execute a command in PowerShell:

- The standard way is to just type the command.
- Another option is the `&` operator: `& <command> <arguments>`. This way, we can
    - **execute a program with spaces in the path**: `"C:/Program Files/a/a"` does not work, but `& "C:/Program Files/a/a"` does
    - prepare the command or arguments dynamically:
        ```PowerShell
        $command = 'ls'
        & $command # prints the content of the current directory
        $command $ # prints ls
        ```
- The third option is to use the [`Invoke-Expression`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression) command. This command executes a string as a command with arguments. Example:
    ```PowerShell
    $argument = "--version"
    Invoke-Expression "java $argument"
    ```

## Using the call (`&`) operator

- [documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators#call-operator-)
- [ss64 documentation](https://ss64.com/ps/call.html)

The syntax is `& <command> <arguments>`. Here:

- `<command>` is the command to be executed. If the path to the command contains spaces, it has to be wrapped in quotes.
- `<arguments>` are either
    - inline arguments, e.g.: `& vcpkg list x64-windows-static`
    - array of arguments, e.g.: `& vcpkg @("list", "x64-windows-static")`


Note that **passing the array of arguments to a cmdlet does not work as expected**. Cmdlets uses special named parameters. For example the `ls` (alias for `Get-ChildItem` cmdlet) has the `-Depth` parameter that can have an integer value. However, the cmdlet expects such arguments to be passed as key-value pairs. For inline parameters, the key-value pairs are automatically created from the positionally passed arguments. But this is not the case for the array of arguments. So:
```PowerShell
& ls -Depth 2 # works
& ls @("-Depth", 2) # does not work. Each element of the array is treated as a separate positional argument -> a path is expected
```
Unfortunatelly, there is no nice solution for this, if we want to use the call operator (there is no such problem with `Invoke-Expression`). There are two options:

- pass the arguments as key-value pairs. Example:
    ```PowerShell
    $params = @{"Depth" = 2}
    & ls @params # this unrolls the dictionary into key-value pairs
    ```
    - do not mistake the second line with `& ls $params`. This would pass the dictionary as a single argument.
- use the code block and pass the arguments inside it. Example:
    ```PowerShell
    & {ls -Depth 2}
    ```


## Using the Invoke-Expression command
The [`Invoke-Expression`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression) command executes a string as a command with arguments. Example:
```PowerShell
$argument = "--version"
Invoke-Expression "java $argument"
```

A big caution is needed when using the `Invoke-Expression` as its typical usage **with double-quoted strings triggers expression evaluation twice**, which can lead to unexpected behavior. Example:
```PowerShell
# we want to print $test
echo $test # prints nothing as variable is not defined
echo `$test # prints $test standard escape solution
Invoke-Expression "echo `$test" # prints nothing as variable is not defined. The problem is that the escape character is evaluated during the first string evaluation, and then, during the Invoke-Expression evaluation, there is no escape character.
Invoke-Expression 'echo `$test' # prints $test. The single quotes prevent the evaluation of the escape character during the first string evaluation.
```

## Print the exit code
To print the exit code of the last command, there are two options:

- `$?`: returns `True` if the last command was successful, `False` otherwise
- `$LastExitCode` variable contains the exit code of the last command


## No Output for EXE file
Some errors are unfortunatelly not reported by powershell (e.g. [missing dll](https://stackoverflow.com/questions/23012332/how-to-make-powershell-tell-me-about-missing-dlls)). The solution is to run such program in cmd, which reports the error.



# Variables
Variables are defined by the `$` sign. Example:
```PowerShell
$myVar = "Hello, World!"
```
To print the variable, just type its name. Example:
```PowerShell
$myVar
```

## Environment variables
They are accessed by the `$env:` prefix. Example:
```PowerShell
$env:PATH
```

## Operations on Variables
The variables can be used in expressions. Example:
```PowerShell
$myVar = 5
$myVar + 3
```

### String Operations
Strings can be concatenated using the `+` operator. Examples:
```PowerShell
$myVar = "Hello, " + "World!"

# append to a path:
$env:PATH += ";C:\Program Files\Java\jdk1.8.0_181\bin"

# prepend to a path:
$env:PATH = "C:\Program Files\Java\jdk1.8.0_181\bin;" + $env:PATH
```

# Operators

## Comparison and String Operators
[documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators)

Equality operators:

- `-eq`: equal
- `-ne`: not equal
- `-gt`: greater than
- `-lt`: less than
- `-ge`: greater or equal
- `-le`: less or equal

Matching operators:

- `-match`: match

## Logical Operators
[documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logical_operators)

- `-and`: logical and
- `-or`: logical or
- `-not`: logical not


# Control Structures

## Conditions

### `if`
The `if` statement is used for conditional execution. The syntax is:
```PowerShell
if ($condition) {
    # do something
}
elseif ($anotherCondition) {
    # do something else
}
else {
    # do something else
}
```

The `if` structure is also available as a cmdlet `If`. Example:
```PowerShell
If ($condition) { "True" } Else { "False" }
```
The `If` cmdlet is also available as an alias `if` and `?`.





## Loops

### `foreach`
The `foreach` cycle iterates over a collection. The syntax is:
```PowerShell
foreach ($item in $collection) {
    # do something with $item
}
```

The foreach structure is also available as a cmdlet `ForEach-Object`. In this case, we access the current item using the `$_` variable. Example:
```PowerShell
Get-ChildItem | ForEach-Object { $_.Name }
```
The above command lists the names of all files in the current directory.

The alias for the `ForEach-Object` cmdlet is `foreach` and `%`.

# Inputs and Outputs

## Inputs
To read a file, use the [`Get-Content`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-content) cmdlet. Example:
```PowerShell
Get-Content "C:\Users\user\file.txt"
```

##  Outputs
There are many output streams in PowerShell. We can use:

- `Write-Output`: for standard output
- `Write-Error`: for standard error
- `Write-Warning`: for warnings
- `Write-Verbose`: for verbose output
- [`Write-Debug`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-debug): for debug output
- `Write-Information`: for information output
- [`Write-Host`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-host): for writing directly to the console. No output stream is used.

By default, only the standard and error output streams are displayed. To display the other streams, we have several options:

- manually set the `$VerbosePreference`, `$DebugPreference`, `$WarningPreference`, `$InformationPreference` variables to `Continue` (default is `SilentlyContinue`), or
- make the function or script we are running an *Advanced Function or Script* and use the `-Verbose`, `-Debug`, `-WarningAction`, `-InformationAction` parameters


# Pipes and Redirection
[pipe documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines)

[redirection documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection)

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

In new PowerShell, we have even more options:

- `3>`: redirect Warning stream
- `4>`: redirect Verbose stream
- `5>`: redirect Debug stream
- `6>`: redirect Information stream
- `*>`: redirect all streams



# Data Types
Powershell uses .NET types for data types. We can encounter nubers, characters strings, or boolean values. Additionally, we can have composite types, like arrays, or objects.

## Dates
The date is represented by the `System.DateTime` type. To create a date, we can use the [`Get-Date`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-date) command. Example:
```PowerShell
$date = Get-Date # current date
$date = Get-Date -Date "2025-01-01" # date from a string
```

Dates can be compared using the standard comparison operators. Example:
```PowerShell
if ($date1 -lt $date2) {
    ...
}
```


## Arrays
To **create** an array, use the `@()` operator: `a = @()`.

To **add an element** to an array, use the `+=` operator: `a += 1`. The same operator can be used to **append** one array to another: `a += @("1", "bar")`.

The arrays can be **iterated** over using the `foreach` loop.

To join the elements of an array into a space-separated string, we can just use the array in a string context. Example:
```PowerShell
$a = @("foo", "bar")
"$a" # prints "foo bar"
```



# String Manipulation

## Replace
For replacing a substring in a string, we have two options:

- `Replace` method
- `-replace` operator

The `Replace` method replaces all occurences of a string with another string. The syntax is:
```PowerShell
$myString.Replace("oldString", "newString")
```

The `-replace` operator uses regular expressions for replacing. The syntax is:
```PowerShell
$myString -replace "pattern", "newString"
```
Multiple replacements can be done using chained `-replace` operators. Example:
```PowerShell
$myString -replace "pattern1", "newString1" -replace "pattern2", "newString2"
```

## Match
To test if a string matches a regular expression, use the `Match` method. The syntax is:
```PowerShell
$myString -match "pattern"
```

# `Select-String`
The [`Select-String`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-string) is the `grep` equivalent for PowerShell. The alias for the comand is `sls`. Parameters:

- `-Content <before>[, <after>]`: Select also `<before>` lines before the matched line and `<after>` lines after the matched line
- `-Pattern`: If we want to use a regular expression for searching, not a plain string

## Selecting the matched string
If we use the `Select-String` with the `-Pattern` parameter, the matching lines are returned with the matching string highlighted. If we want to get only the matching string, we have to access the `Matches.Value` property for each line. Example:
```PowerShell
Select-String -Pattern "pattern" | ForEach-Object { $_.Matches.Value }
```


# `Select-Object`
The [`Select-Object`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-object) selects the specified properties of an object. Example:
```PowerShell
Get-Process | Select-Object -Property Name, Id
```




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



# System Information
[CIM documentation](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets)

[WMI classes](https://learn.microsoft.com/en-us/windows/win32/wmisdk/wmi-classes)

There are several interfaces for getting system information in PowerShell:

- Using the [*Common Information Model* (CIM)](https://en.wikipedia.org/wiki/Common_Information_Model_(computing))
- Using the [*`Windows Management Instrumentation` (WMI)*](https://en.wikipedia.org/wiki/Windows_Management_Instrumentation) 
- By reading from the [*registry*](https://en.wikipedia.org/wiki/Windows_Registry)

## CIM and WMI
Because the CIM and WMI interfaces are very similar, we will discuss them together. The main difference is that the CIM is the newer interface, which is more powerful and more user-friendly. The CIM is also cross-platform, while the WMI is Windows-only.

The advantage of the CIM and WMI interfaces is that they are clear and object-oriented. The information can be queried using database-like operations. The disadvantage is that they are slow.

The main command for getting system information is:

- [`Get-CimInstance`](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance): for CIM
- [`Get-WmiObject`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-wmiobject): for WMI

For both commands, we need to specify the class of the object we want to get using the `-ClassName` (CIM) or `-Class` (WMI) parameter. The classes are the same for both interfaces. Typical classes are:

- `Win32_ComputerSystem`: information about the computer
- `Win32_OperatingSystem`: information about the operating system
- [`Win32_InstalledWin32Program`](https://learn.microsoft.com/en-us/windows/win32/wmisdk/win32-installedwin32program): information about installed programs
- [`Win32_Product`](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/aa394378(v=vs.85)): information about programs installed using the MSI installer
    - contains more information than `Win32_InstalledWin32Program`


## Windows Registry
To access the Windows registry, we use the same commands that are used for file system:

- [`Get-ItemProperty`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itemproperty): to get the value of a registry key
 - [`Get-ChilItem`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem) to get a list of child keys



# Advanced Script blocks
Any script block can be made an advanced script block. Advanced script blocks are run similarly to the compiled cmdlets. To make a script block an advanced script block, we have to use the `[CmdletBinding()]` attribute at the beginning of the script block. 

Example:
```PowerShell
function MyFunction {
    [CmdletBinding()]
    # do something
}
```

The advanced functions and scripts have the following features:

- parameters are not available as `$args` (have to be parsed using the `param` block)
- builtin parameters like `-Verbose`, `-Debug`, `-WarningAction`, `-InformationAction` are parsed automatically
- support for pipeline input


# Elevation
Some commands may require administrator privileges. Therefore, it is wise to check if the script is running with administrator privileges so that the execution is not interrupted. To check if the script is running with administrator privileges, use the following code:
```PowerShell
$myWindowsID=[Security.Principal.WindowsIdentity]::GetCurrent()
$myWindowsPrincipal=new-object Security.Principal.WindowsPrincipal($myWindowsID)
if (!$myWindowsPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "This script requires elevated privileges. Please run it as an administrator."
        exit
    }
```

Another solution may be to restart the script with administrator privileges. However, this has several limitations:

- when the script is run with administrator privileges a new terminal window is opened
- parameters are not passed automatically to the new script. We can manually pass them using the `-ArgumentList` parameter. However, this is problematic for non-string parameters, especially in an advanced script block. 

To restart the script with administrator privileges, use the following code:
```PowerShell
$argString = $args -join ' '
Start-Process "pwsh" -Verb RunAs -ArgumentList "-noexit -File `"$PSCommandPath`" $argString"
exit
```


# PowerShell History
To iterate over the commands used in the past, we use the `up arrow` and `down arrow` keys.

To list the history, use the `Get-History` command.

To **clear** the history, use the [`Clear-History`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/clear-history) command:

- `Clear-History -Id <id>`: clear the command with the specified id (use `Get-History` to get the id)
- `Clear-History -Count <count>`: clear the last `count` commands
- `Clear-History -CommandLine <pattern>`: clear the commands that match the pattern. The pattern use the simple matching (e.g. `*` is the wildcard), and have to be wrapped in quotes if it contains spaces.



# Including scripts
[documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts?view=powershell-7.5&viewFallbackFrom=powershell-7.1#script-scope-and-dot-sourcing)

Script including in PowerShell is called *dot sourcing*. To include a script, use the `.` operator. Example:
```PowerShell
. "C:\Users\user\script.ps1"
```

- To include a script from the **current directory**, use the `.` operator:
    ```PowerShell
    . .\script.ps1
    ```
- To include a **relative to the script directory**, use the `$PSScriptRoot` variable. Example:
    ```PowerShell
    . "$PSScriptRoot\script.ps1"
    ```



# Usefull Commands



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

## Get the path of the current script
To get the path of the current script, use the `$PSCommandPath` variable.


## Compute the hash of a file
To compute the hash of a file, use the `Get-FileHash` command. Example:
```PowerShell
Get-FileHash "C:\Users\user\file.txt"
```

Important parameters:

- `-Algorithm`: the algorithm used for hashing. The default is `SHA256`. Other options are `SHA1`, `SHA256`, `SHA384`, `SHA512`, `MD5`


## Get path of the executable/command
If we need to know the installed path of an executable or command, similar to the `which` command in Linux, we can use the `Get-Command` command. 


