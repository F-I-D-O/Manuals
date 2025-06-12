# Usefull Comands

## Versions

### Check Ubuntu Version
```bash
lsb_release -a
```

### Check OS Distribution and Version
```bash
cat /etc/*-release
```

### Checking glibc version
```bash
ldd --version
```


## Printing used ports
```bash
sudo lsof -i -P
```


## Exit codes
Exit code of the last command: `$?`

[Common exit codes for C++ programs](https://www.geeksforgeeks.org/exit-codes-in-c-c-with-examples/)

## Show path to executable
Use the `which` command: `which <executable>`


## Unpack file
Foe unpacking, you can use the `tar -f <file>` command. The most used options are:

- `x`: extract



# Environment Variables
The environment variables are introduced with the `export` command:
```bash
export <variable>=<value>
```
without export, the variable is just a local shell variable:
```bash
<variable>=<value> # local variable
```

We will demonstrate the work with environment variables on the `PATH` example. If you have a program in a custom location, adding it to `$PATH` permanently and be able to run it under all circumstances is not an easy task on linux. Standard procedure is to add a system variable: 

1.  Create a dedicated `.sh` file in `/etc/profile.d.` for your configuration (config for each app should be stored in a separate file).
2.  the file should contain: `export PATH=$PATH:YOURPATH`
1. exit nano and save the file: `ctrl+x` and `y`
3.  logout and login again to load the newly added varibales
	- for WSL close the console and reopen it, it is not necessary to restart the WSL

([click here for detailed description](https://askubuntu.com/questions/866161/setting-path-variable-in-etc-environment-vs-profile))

## Enable Variable with sudo
To enable the variable even if you use `sudo`, you need to edit sudo config using `sudo visudo` and:

1.  exclude `PATH` from variable being reset when running `sudo`:  `Defaults env_keep += "PATH"`
2.  disable the safe path mechanism for `sudo`, i.e., comment the line: `Defaults secure_path = /sbin:/bin:/usr/sbin:/usr/bin`
3.  logout and login again to load the new added varibales

## Enable the Variable Outside Bash
If you need the variable outside bash, the above-mentioned approach wonâ€™t work. Currently, I do not know about any general solution for variables. The solution below, unfortunately, work only for [PAM shells](https://en.wikipedia.org/wiki/Linux_PAM)  (see [this SO answer](https://unix.stackexchange.com/questions/473001/env-vars-in-etc-environment-not-globally-visible) why).

Add the variable to `/etc/environment`. Note that it is not a script file, so you can use only simple variable assignments.

## Enable Variable on a Device Without Root Access
Without root access, we can only edit the user config files. put the necessary config into:

-   `~/.bash_profile` if it already exists   
-   or to `~/.profile`

Note that the `.profile` file is ignored when the `.bash_profile` file exists.


## Remove Windows `$PATH` from WSL
By default, the `PATH` environment variable from Windows is inluded in the `PATH` variable in Ubuntu running in WSL. This can lead to conflicts, when the same executables are used in both systems (e.g., vcpkg, cmake).  To turn of the Windows `PATH` inclusion:

1. open `/etc/wsl.conf`
1. add the fllowing code:
```
[interop]
appendWindowsPath = false
```

1. restart WSL



# File System

## List files
To list files, use `ls <path>`. By default, it lists the files in the current directory. The most used options are:

- `-l`: list in long format
- `-a`: list all files, including hidden ones
- `-1`: list one file per line (instead of multiple columns)
- `-d`: list directories themselves, not their contents

### List the full paths
There is no option of showing the full path. The trick is to use the `-d` option, as directories are listed in the long format by default. So for example, to list full paths of all subdirectories of `<dir>`, you can use:
```bash
ls -d <dir>/* 
```

## copy file
The `cp` command is used to copy files: `cp <source> <destination>`. The most used options are:

- `-r`, `-R`: copy recursively
- `-v`: verbose
- `-f`: force
- `-p`: preserve permissions and timestamps
- `-a`: same as `-p -R` plus some other options

For more sophisticated copying, use `rsync`: `rsync <source> <destination>`. The most used options are:

- `-h`: human readable
- `-a`: archive mode, equivalent to `-rlptgoD`
- `--progress`: show progress


## Remove file
The `rm` command is used to remove files. The most used options are:

- `-r`, `-R`: remove recursively

To remove all files in a directory, you can use


## Access rights
The Linux access rights use the same system for files and folders. The access rights are divided into three groups, from left to right:

- owner
- group
- other

Each group has three possible access rights:

- `r`: read
- `w`: write
- `x`: execute

Important aspects:

- to access a directory, the user has to have the `x` right on the directory.
- to access a file, the user has to have the `x` right on all folders in the path to the file.

## Compute directory size
To compute the size of a directory, use the `du` command:`du <path>`. The most used options are:

- `-h`: human readable
- `-s`: summarize


## Find files
To find files, use the `find` command: `find <where> <options> <params>`. The most used options are:

- `-name`: find by name. This option should be followed by a file name pattern.
- `-path`: find by path. This option should be followed by a path pattern. 

## List disks and partitions
To list disks and partitions, use the `lsblk` command. If we are not satisfied with the output, we can configure it with the `-o` option:
```bash
lsblk -o <list of columns, separated by commas>
```

Most important columns are:

- `NAME`: name of the disk or partition
- `SIZE`: size of the disk or partition
- `TYPE`: type of the disk or partition
- `FSTYPE`: file system type
- `FSAVAIL`: available file system space

# Network
## [`netstat`](https://en.wikipedia.org/wiki/Netstat)
The [`netstat`](https://en.wikipedia.org/wiki/Netstat) command is the basic command to monitor the networ. It displays the TCP connections. It is available both on Linux and on Windows, although the interface differs. Important parameters:

- `-n`: do not translate IP and ports into human readable names
- `-a`: show all connections. Without this, some connections can be skipped.



# Bash
[documentation](https://www.gnu.org/software/bash/manual/bash.html)

[wiki](https://en.wikipedia.org/wiki/Bash_(Unix_shell))

Bash can refer to a typical Unix shell, or just the command line interpreter for this shell or to the language used to write shell commands and scripts.

In bash, **commands can be separated** by

- a newline, or
- a semicolon.

Therefore, we can write even complicated commands to a single line in the terminal.


## General Remarks

- It's important to use Linux newlines, otherwise, bash scripts will fail with unexpected character error
- Empty constructs are not allowed, i.e, empty function or loop results in an error
- brackets needs spaces around them, otherwise, there will be a syntax error
- space around `=`, which is typical in other languages, is not allowed in bash 
- bash does not support any data structures, only arrays

## Bash modes and environment initialization
Bash can run in several modes. These modes have some effect, but mainly, it affects the initialization of the environment, i.e., which files are executed at the start of the shell. The modes are:

- **login shell**: mode is used when the user logs in. 
	- also used when the shell is run with the `-l`, `--login` parameter
- **interactive shell**: mode is used when the user interacts with the shell.
	- also used when the shell is run with the `-i` parameter
- **non-interactive shell**: mode is used when the shell is run in a script.
	- this shell mode is used when we run commands over ssh or wsl

The execution of the initialization files is displayed in the image below:

![Bash initialization files](Bash%20environment%20loading.png)

Note that the initialized environment persists in the system. In other words, the environment variables set in the files processed by the login shell are available even in the non-interactive non-login shells opened later on. However, there are still cases when the environment variables are not available because the login shell has not been run, e.g.:

- when the shell is run over ssh as a command: `ssh user@host <command>`
- when the shell is run from wsl as a command: `wsl <command>`

In those cases, if we need the environment variables, we have to run the login or interactive shell explicitly, e.g.: `wsl bash -lc <command>`.

## Variables
Variables can be defined as:
```bash
var=value
```
Note that **there must not be any spaces around `=`**. 

We can also declare variables with a specific type, so that no other type can be assigned to it using the `declare` command:
```bash
declare -i var # integer
declare -a var # array
declare -r var # read only
```

To access the value of a variable, we use `$`:
```bash
echo $var
```

### Assigning the output of a command to a variable
The output of a command can be assigned to a variable only with the [command substitution](#command-substitution):
```bash
var=<command> # wrong, the first token of the command is assigned to the variable

var=$(<command>) # correct, the output of the command is assigned to the variable
```

Example:
```bash
var=$(echo $var | sed 's/old/new/')
```






### List all variables
To list all variables, we can use the declare command:
```bash
declare
```
However, this command also lists the functions. To list only the variables, we can use:
```bash
declare -p
```
which also prints the type and attributes of the variables.

### Operations on variables
There are many operations on variables, the most important are:

- `${#<variable>}`: length of the variable
- `${<variable>%%<pattern>}`: remove the longest suffix matching the pattern
- `${<variable>##<pattern>}`: remove the longest prefix matching the pattern



## Working with I/O

### Output Forwarding
Output forwarding is a process of redirecting the output of a command to an input of another command. The operator for that is the pipe `|`. The syntax is:
```bash
<command 1> | <command 2>
```

Note that the content of the pipe cannot be examined, the process on the right hand side consume it. Therefore, **it is not possible to simply branch on pipe content** while use it in the subsequent process.


### Output Redirection
Output redirection is a process of redirecting the output (stdout, stderr,..) from the console to a file. The syntax is:
```bash
<command> <operator> <file>
```
The possible operators and their effects are listed in the table (full explanation on [SO](https://askubuntu.com/a/731237/603617)) below:

| Operator | Stdout | Stderr | Mode (in file) | 
| --- | --- | --- | --- |
| `>` | file | console | overwrite |
| `>>` | file | console | append |
| `&>` | file | file | overwrite |
| `&>>` | file | file | append |
| `2>` | console | file | overwrite |
| `2>>` | console | file | append |
| `\| tee` | both | console | overwrite |
| `\| tee -a` | both | console | append |
| `\|& tee` | both | both | overwrite |
| `\|& tee -a` | both | both | append | 

`tee` is actully a command, not an operator. It is used as follows:
```bash
<command> | tee <file>
```

We can also use `tee` to forward the output of a command to multiple commands:
```bash
<command 1> | tee >(<command 2>) | <command 3>
```
This forward `<command 1>` to both `<command 2>` and `<command 3>`.

### Use bash variables as input
Bash variables can be used as input of a command. Syntax:
```bash
<command> <<< $<variable>` 
```



## Command Substitution
When we need to use an output of a command instead of a constant or variable, we have to use command substtution:
```bash
`<command>`
# or equivalently
$(<command>)
```
e.g.:
```bash
echo resut is: `cut -d, -f 7`
# or equivalently
echo resut is: $(cut -d, -f 7)
```

## Bash Script Arguments
We refer the arguments of a bash script as

- `$0` - the name of the script
- `$1..$n` - the arguments of the script
- `$@` - all the arguments of the script

Sometimes, it is useful to throw away processed arguments. This can be done using the `shift` command `shift <n>`, where `<n>` is the number of arguments to be thrown away (default is 1). The remaining arguments are then shifted to the left, i.e., `$2` becomes `$1` and so on. 


## Conditions
In general, condition in bash has the following syntax:
```bash
if <condition> 
	then <command>
	else <command>
fi
```

The condition can have several formats:

- **plain command**: the condition is true if the command returns 0
	```bash
	if grep -q "$text" $file 
		then ...
	fi
	```

- **`[ <condition> ] or test <condition>`**: The standard POSIX test construct. Now only suitable if we want to run the script outside bash.
	```bash
	if [ $var = 1 ]
	then ...
	fi
	```

- **`[[ <condition> ]]`**: The extended test construct. This is the recommended way of writing conditions, due to [several practical features](https://stackoverflow.com/questions/3427872/whats-the-difference-between-and-in-bash) (e.g., no need to quote variables, regex support, logical operators, etc.).
	```bash
	if [[ $var = 1 ]]
	then ...
	fi
	```

- **`(( <condition> ))`**: The arithmetic test construct. This is used for arithmetic conditions.
	```bash
	if (( $var == 1 ))
	then ...
	fi
	```

Note that if we want to use some arbitrary value (e. g. the *return value* of a command), or comparisons in the condition (similar to programming languages), we have to use one of the test constructs. 


**Mind the spaces around the braces!**

### String comparison
Strings can be compared using the standard `=` operator or the `==` operator. 

If we use the `[ ]` construct, we have to quote the variables, otherwise, the script will fail on empty strings or strings containing spaces:
```bash
if [ "$var" = "string" ]
then ...
fi

# or equivalently
if [[ $var = "string" ]]
then ...
fi
```


## Loops
The syntax of the loop is:
```bash
while <condition>
do
   <command1>
   <command2>
   ...
done
```

### Forward to loop
We can forward an input into while loop using `|` as usuall. Additionally, it is possible to read from file directly by adding `<` to the end like this:
```bash
while condition
do
   <command1>
   <command2>
   ...
done < <input>
```

The same goes for the output, i.e., we can forward th outut of a loop with `|`.


## Strings literals
String literals can be easily defined as:
```bash
str="string literal"
# or equivalently
str='string literal'
```
If we use double quotes, the variables are expanded, e.g., `echo "Hello $USER"` will print `Hello <username>`.

The problem arises when we want to use double quotes in the string literal containing variables, e.g., `normal string "quotted string" $myvar`. In this case, we have to use quite cumbersome syntax:
```bash
a = "normal string "\""quotted string"\"
# or equivalently
a = "normal string "'"'"quotted string"'"'
```

### Multiline string literals
There is no dedicated syntax for multiline string literals. However, we can use the *here document* syntax:
```bash
<target> << <delimiter> <content> 
<delimiter>
```

For example, to store the command in a variable, we can use:
```bash
db_sql = $(cat << SQL
CREATE DATABASE test_$name OWNER $name;
grant all privileges on database test_$name to $name;
SQL)
```
Note that the `<delimiter>` must be at the beginning of the line, otherwise, it will not work.

## Functions
Functions are defined as:
```bash
function_name() {
	<command 1>
	<command 2>
	...
}
```
For access the arguments of the function, we use the same syntax as for the script arguments (e.g., `$1` for the first argument).

We can create local variables in the function using the `local` keyword:
```bash
function_name() {
	local var1="value"
	...
}
```


## Reading from command line
To read from command line, we can use the `read` command. The syntax is:
```bash
read <variable>
```
where `<variable>` is the name of the variable to store the input. Important parameters:

- `-p <prompt>`: prints	the `<prompt>` before reading the input
- `-s`: do not echo the input (usefull for passwords)


## Bash Script Header Content
Usually, here are some special lines at the beginning of the bash script.

First, we can specify the interpreter to be used:
```bash
#!/bin/bash
```

Then we can set the script to exit on error:
```bash
set -e
```


## Calling a script from another script in the same directory
To call a script *b* from script *a* in the same directory, it is not wise to use the relative path, it is evaluated from the current directory, not from the directory of the script. To be sure that we can call script *a* from anywhere, we need to change the working directory to the directory of the scripts first:
```bash
cd "$(dirname "$0")"
./B.sh
```


# Root Access
Some commands require root privilages. The basic way how to run a command as root, we can use the `sudo` command:
```bash
sudo <command>
```
A password of the current user is required to run the command. Also, the user has have the right to run `sudo`.

The password is usually required only once per some time period (e.g., 15 minutes). 

For some operations (e.g., browsing folders requiring root access), we have to run multiple commands as root. In this case, we have to switch the shell user to root. 

Resources:

- [SO](https://askubuntu.com/questions/376199/sudo-su-vs-sudo-i-vs-sudo-bin-bash-when-does-it-matter-which-is-used#376386)

## Changing shell user
To change the shell user, we can use the `su` command:
```bash
su <username>
```
If we omit the username, the root user is used. Note that the **password of the target user is required**. To change the shell user without the password of the target user, we can use the `sudo` command:
```bash
sudo su <username>
```
This way, the password of the current user is required.

The `su` command can be used the same way as the `sudo` command, i.e., we can pass the command:
```bash
su <username> -c "<command>"
```

To **exit** the shell user, we can use the `exit` command.


### Changing shell user in a script
In a script, we cannot change the shell user for the remaining commands in the script. If we do that, the script will execute a new shell, and the remaining commands will be executed in the old shell. 

To execute commands as a different user, we have several options. Every option pass the commands as a parameter to the change user command (e.g., `su -c "<command>"`). The options are:

1. for each command, create a new change user command 
2. create a single change user command and pass all the commands as a single parameter (e.g., with the heredoc syntax)
3. move commands to a separate script and execute the script as a different user


# Managing packages
To **update the list** of possible updates:
```bash
sudo apt update
```

To perform the **update**:
```bash
sudo apt upgrade
```

To **list installed** packages:
```bash
apt list --installed
```
We can filter the list using the `grep` command.

To **find the install location** of a package:
```bash
dpkg -L <package>
```
Unfortunately, it is not possible to easily search for the user who installed the package.

To **search** for a package:
```bash
apt-cache search <package>
```
We can limit the search to check only names of the packages using the `--names-only` parameter.

To **remove** a package:
```bash
sudo apt remove <package>
```


## Installing non-stable package versions
On Linux, the stable package versions are usually outdated, sometimes years behind the current version. To install the newer version, we have usually a few options:

- **upgrade the system**: if we use an old version of the system, we can check whether the newer version is available that includes the newer package version. For more, see the [Upgrade](#upgrade) section.
- **install from source**: We can manually build the package from the source and install it. See the [C++ Workflow](../Programming/C++/C++%20Workflow.md) for more.
- **install package from an alternative repository**: We can add an alternative repository to the system and install the package from there.

The first two options are covered in different part of this manual. Here, we focus on the third option.

To use an alternative repository, we have to a) add the repository to the system, which is a one time task, and b) install the specific package from the repository.

To **add a repository**, we have to:

1. add the repository to the `/etc/apt/sources.list` (or to a separate file in the `/etc/apt/sources.list.d/` directory). Each repository should has the line that should be added to the file on its website.
2. `sudo apt update` to update the list of available packages

To **install a package from the repository**:
```bash
sudo apt install -t <repository> <package>
```

### Some useful repositories

- [debian backports](https://backports.debian.org/Instructions/): the repository with the newer versions of the packages for the stable Debian version


## Changing default package repositories
If the downolad speed is not satisfactory, we can change the repositories. To find the fastest repository from the list of nearby repositories, run:
```bash
curl -s http://mirrors.ubuntu.com/mirrors.txt | xargs -n1 -I {} sh -c 'echo `curl -r 0-10240000 -s -w %{speed_download} -o /dev/null {}/ls-lR.gz` {}' | sort -g -r
```

The number in the leftmost column indicates the bandwidth in bytes (larger number is better).

To change the repositories to the best mirror, we need to replace the mirror in `etc/apt/source.list`. We can do it manually, however, to prevent the mistakes, it is better to use a dedicated python script: [`apt-mirror-updater`](https://apt-mirror-updater.readthedocs.io/en/latest/readme.html). Steps:

1. install the python script: `sudo pip install apt-mirror-updater`
1. backup the old file: `sudo cp sources.list sources.list.bak`
1. change the mirror with the script: `apt-mirror-updater -c <mirror URL>`

Note that the `apt-mirror-updater` script can also measure the bandwidth, however, the result does not seem to be reliable.

## Possible issues

### `The repository '<repo>' no longer has a Release file`
This can happen when the repository is outdated, which can happen quickly if we use non-stable (non-LTS) versions of Ubuntu. The solution is to either:

- change the repository to a newer one manually or
- change the url of all repositories to `http://old-releases.ubuntu.com/ubuntu/` and then upgrade the system to the newer version:
	```bash
	sudo sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
	```

# String Processing

## String filtering with `grep`
The `grep` command is used to filter lines containing a pattern. The syntax is:
```bash
grep <pattern> <file>
```
The pattern can be a simple string, or a regex. The most used options are:

- `-v`: invert the match, i.e., print only lines not matching the pattern
- `-e`: use multiple patterns (e.g., `-e <pattern 1> -e <pattern 2>`)
- `-i`: ignore case


## Word count with `wc`
The `wc` command counts words, lines, and characters. What is counted is determined by the parameters:

- `-w`: words
- `-l`: lines
- `-c`: characters



## String mofification with `sed`
[Documentation](https://www.gnu.org/software/sed/manual/sed.html)

[sed](https://en.wikipedia.org/wiki/Sed) (stream editor) is a command for string modification. It is mostly used for search and replace in string. The syntax is folowing:
The syntax is:
```bash
sed <options> <script> <input file> #or
<input stream> | sed <options> <script>
```

here, the parameter characteristic to sed is `<script>`, which a) defines the mode of operation and b) configure the operation.

In the sections below, each mode of operation is described separately.

### Regex support in sed
Regex can be used in sed, but the support is limited. The following is not supported:

- `\s`

Note that the **`<script>` is processed by bash before it is passed to sed. A proper quoting is required to avoid the shell interpreting or deleting characters.** Example:
```bash
echo $line | sed 's/\r//g' # removes carriage returns from the line
echo $line | sed s/\r//g # wrong, the backslash is interpreted by the shell and removed. As a result, the script is interpreted as `s/r//g` and all "r" characters are removed.
```


### Search and replace
The `<script>` for *substitution* is:
```bash
s/<search>/<replace>/[<occurance>]
```



Example:
```bash
s/$/,3/
```

This replace the end of the line with string `",3"`. Note that there is a slash at the end, despite we use the default option for occurance.



### Delete lines containing string
```bash
/<pattern>/d
```

## `cut`
Cut is a useful command for data with delimiters. Usage:
```bash
cut -f <columns>
```
Where columns are splited by comma, e.g., `2,4,7`. 

If we need to specify delimiters, we use the `-d` parameter:
```bash
cut -d, -f 1,5
```


## AWK
AWK is a powerful tool for text processing. It is a programming language, so it can be used for more complex tasks than `sed` or `cut`. The basic syntax is:
```bash
awk '<pattern> {<action>}'
```
Where `<pattern>` is a regex and `<action>` is a command. The `<action>` is executed only if the line matches the `<pattern>`. 



### Pattern
In the `awk`, `/` is used as a delimiter of the regex pattern. 


### Action
The `<action>` can be a sequence of commands, separated by `;`. We can use column values by using special column variables:

- `$0`: the whole line
- `$1`: the first column
...


## Trim string
```bash
<command with string output> | xargs
```


# Processes

- for checking **all processes**, we can use `htop`
- to get a **path to executable** of a process by PID, we can use `pwdx <PID>`
- for checking a specific process, we can use `ps`
- to kill a process, we can use `kill`
- to kill a process by name, we can use `pkill`
- to get information about a process selected by name, we can use [`pgrep`](https://en.wikipedia.org/wiki/Pgrep)

## pkill
The `pkill` command kills a process by name. The syntax is:
```bash
pkill <process name>
```
important parameters:

- `-f`: match the whole command line, not only the process name
- `-9`: force kill

## Process Info


# Users
The users are listed in `/etc/passwd`. The file contains one line per user, each line has the following format:
```
<username>:<password>:<user ID>:<group ID>:<GECOS>:<home folder>:<shell>
```
The password is typically stored in `/etc/shadow` and is represented by `x`. [GECOS](https://en.wikipedia.org/wiki/Gecos_field) is some kind of a comment storing arbitrary information about the user.

## Adding a user
To add a user, we can use either the `useradd` binary directly, or the `adduser` wrapper script. Here we describe the `adduser` script. The basic syntax is `adduser <username>`. Important parameters:

- `--gecos "<GECOS>"`: supply the content of the GECOS field. If skipped, the command will ask for the GECOS content interactively.
- `--shell <shell>`: The shell to be used by the user. If skipped, the default shell is used. This can be used to create a user without a shell by setting the shell to `/usr/sbin/nologin`.

Note that the `adduser` needs to be run as root. Otherwise it will fail with `bash: adduser: command not found`.


## User Groups
An important aspect of user management in Linux is the user groups. For example, by belonging to the `sudo` group, the user can execute commands with `sudo`. The groups are listed in `/etc/group`. The file contains one line per group, each line has the following format:
```
<group name>:<password>:<group ID>:<user list>
```

To **see the groups of a user**, we can use the `groups` command (no arguments needed).

To **manipulate groups and users**, we need a root access. 
To add a user to a group, we can use the `usermod` command:
```bash
usermod -a -G <group name> <username>
```

To **remove a user from a group**, we can use the same command:
```bash
usermod -G <group list> <username>
```
where `<group list>` is a comma separated list of groups the user should belong to.




## File ownership
Each file has a pair of owners: the user owner and the group owner. These ownerships are important, as file permissions in Linux are usually set for a triplet of:

- *owner*: the user owner
- *group*: the group owner
- *other*: all other users

To change the owner of a file, we can use the `chown` command. The syntax is:
```bash
chown <user>:<group> <file>
```
We can skip the `:<group>` part, in which case the group is not changed.

The `chown` command can also be used to change the owner of a directory. In this case, the `-R` parameter is used to change the owner recursively.





## Disable access to shell for a user
To disable access to shell for a user, we have to configure his/her shell to `/usr/sbin/nologin` or similar. 

- For new users, we can use the `--shell` parameter of the `adduser` command.
- For existing users, we can use the `usermod` command:
```bash
usermod --shell /usr/sbin/nologin <username>
```


Note that for some ssh client implementations, it is necessary to connect to a shell by default, otherwise, the connection is terminated immediately after login. In this case, the user has to connect to the server with the `-N` parameter, which tells the client not to execute any command after login.


# Services and systemd
The [systemd](https://en.wikipedia.org/wiki/Systemd) is a system and service manager for Linux. It is used to manage services, devices, and other aspects of the system. 

The main command to manage services is `systemctl`. The general syntax is:
```bash
sudo systemctl <action> <service name>
```
The most used actions are:

- `start`: start the service
- `stop`: stop the service
- `restart`: restart the service
- `status`: get the status of the service
- `reload`: reload the configuration of the service


## Get the status of a service
To get the status of a service, we can use the `status` action:
```bash
sudo systemctl status <service name>
```
The statuses can be:

- `active (running)`: the service is running
- `active (exited)`: the service has finished
- `active (waiting)`: the service is not running, but it is waiting for some event
- TODO: add more statuses

## Listing services
To list all services, we can use one of the following commands:

- `list-units` to list all units ever run on the server or
- `list-units-files` to list all units, including the ones that have never been run


# Frequently used software

## Installing Java
### Oracle JDK

1. Go to the download page, the link to the dowload page for current version of java is on the [main JDK page](https://www.oracle.com/java/technologies/javase-downloads.html).
2. Click on the debian package, accept the license, and download it.
	- If installing on system without GUI, copy now (after accepting the license) the target link and dowload the debian package with `wget`:  `
wget --header "Cookie: oraclelicense=accept-securebackup-cookie" <COPIED LINK>
`. More info on [SO](https://stackoverflow.com/questions/10268583/downloading-java-jdk-on-linux-via-wget-is-shown-license-page-instead).

3. Install the package with `sudo apt-get install <PATH TO DOWNLOADED .deb>`
	- if there is a problem with the isntallation, check the file integritiy with: `sha256 <PATH TO DOWNLOADED .deb>`. It should match with the checksums refered on the download page. If not cheksums do not match, go back to download step.
4. In case there is another version of Java alreadz install, we need to overwrite it using the `update-alternatives` command: `sudo update-alternatives --install /usr/bin/java java <PATH TO JAVA> <PRIORITY>`. Example: 
```
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-16/bin/java 2
```
To check the priorities, call `update-alternatives --query java`. The newly installed JDK should have the highest priority.


## Python
Python has to be executed with `python3` by default, instead of `python`.


## GCC
GCC is typically installed by default and itts minor versions are updated with the system updates. However, if we need a major version update, we have to install it manually as a new package:
```bash
sudo apt install gcc-<version>
```
This way, the new version is installed alongside the old version. To switch to the new version, we have to use the `update-alternatives` command:
```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-<version> <priority>
```
The `<priority>` is a number that determines the priority of the version. The version with the highest priority is used. To check the priorities, we can use the `update-alternatives --query gcc` command.

Note that **these steps only updates the C compiler**. To affect the C++ compiler as well, we have to repeat the steps with the `g++` command:
```bash
sudo apt install g++-<version>
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-<version> <priority>
```

# Other usefull commands


## Selecting lines from file
The `head` and `tail` commands are for that, printing the top and bottom 10 lines, respectively.

### Skip the header
```bash
tail -n +2
```

### Print lines from to
```bash
tail -n +<from line> | head -n <number of lines> 
```

## Progress bar
the progress bar can be printed using the `pv` command.
```bash
pv <file> | <other comands>
# or
<other comands> | pv | <other comands>
```


## Free disk space
```bash
df -h
```


## piping parameters using `xargs`
The [`xargs`](https://en.wikipedia.org/wiki/Xargs) command transfers the output of one command into call of another command with the output of the first command as parameters of the second command. This is usefull when the second command does not accept the output of the first command as input, but accepts the output as parameters.

Example:
```bash
ls | xargs rm # remove all files in the current directory
```




# Upgrade
For a system upgrade, follow these steps:

1. run the [update of the current version](#managing-packages).
2. Then optionaly backup the WSL
3. perform the upgrade:
	- If a) you are on a LTS version, and b) there is a new LTS version available, run `sudo do-release-upgrade`.
	- Otherwise, follow the steps in the next section.

- [Ubuntu versions](https://en.wikipedia.org/wiki/Ubuntu_version_history)

## Manual upgrade
For manual upgrade, follow these steps:

1. perform steps 1 and 2 from the normal upgrade
2. open the `/etc/update-manager/release-upgrades` file and set the `Prompt` parameter to `normal` or `lts` (depending on the desired version)
3. backup the `/etc/apt/sources.list` file
4. change the sources to the new version:
	- e.g., run `sudo sed -i 's/<current version name>/<new version name>/g' /etc/apt/sources.list`
5. run a normal upgrade: `sudo apt update && sudo apt upgrade`
6. finalizing the upgrade: `sudo apt dist-upgrade`

## WSL backup

1. check the WSL distro name: `wsl -l -v`
2. shutdown WSL: `wsl --shutdown`
3. backup the distro: `wsl --export <disto name> <backup folder path>/<backup name>.tar`



# vim
Vim is a console text editor. It is a modal editor, i.e., it has different modes for different operations. The most important modes are:

- **normal mode**: for navigation and file manipulation
- **insert mode**: for text editing
- **visual mode**: for text selection

## Normal Mode
In normal mode, we can:

- navigate the file using arrow keys or `hjkl` (left, down, up, right)
- enter global commands using `:` (e.g., `:q` for quit)
- edit file content using special commands (e.g., `dd` for delete line)

### Global Commands

- `:q`: quit
- `:w`: save
- `:wq`: save and quit
- `:q!`: quit without saving

### File Editing Commands

- `dd`: delete line

## Insert Mode
Insert mode is the normal text mode we know from other editors. To enter insert mode, press `i`. To exit insert mode, press `esc`.

## Visual Mode
Visual mode is used for text selection. To enter visual mode, press `v`. To exit visual mode, press `esc`.


## Copy and paste
Vim has its own clipboard for copy-pasting (yank, ...). However, this cannot be used to copy text outside of vim, nor to paste text from outside vim. 

To **copy** text to the system clipboard, we can:

1. select the text using mouse or keyboard
2. press enter to copy the text to the clipboard

To **paste** text from the system clipboard, we press `Ctrl` + `Shift` + `v`.


