# Usefull Comands
## Check Ubuntu Version
```bash
lsb_release -a
```
## Printing used ports
```bash
sudo lsof -i -P
```

## Checking GLIBC version
```
ldd --version
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
If you need the variable outside bash, the above-mentioned approach won’t work. Currently, I do not know about any general solution for variables. The solution below, unfortunately, work only for [PAM shells](https://en.wikipedia.org/wiki/Linux_PAM)  (see [this SO answer](https://unix.stackexchange.com/questions/473001/env-vars-in-etc-environment-not-globally-visible) why).

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



# Network
## [`netstat`](https://en.wikipedia.org/wiki/Netstat)
The [`netstat`](https://en.wikipedia.org/wiki/Netstat) command is the basic command to monitor the networ. It displays the TCP connections. It is available both on Linux and on Windows, although the interface differs. Important parameters:
- `-n`: do not translate IP and ports into human readable names
- `-a`: show all connections. Without this, some connections can be skipped.

# SSH
The SSH is a protocol for secure communication between two computers. The basic usage is to connect to a remote computer:
```bash
ssh <username>@<address>
```

To close the connection, type `exit` to the console and press enter.

If we do not want to establish a connection, but just run a single command, we can add the command at the end of the ssh command:
```bash
ssh <username>@<address> <command>
```


## SSH Tunneling
An SSH tunnel can be created by the `ssh` command. The usuall syntax is following:
```bash
ssh -L <local port>:<remote machine>:<remote port> <ssh server username>@<ssh server address>
```

The `-L` argument stands for *local port forwarding*, i.e., we forward a local port to some remote port.

Example:
```bash
ssh -L 1111:localhost:5432 fiedler@its.fel.cvut.cz
```
The *local port* (here `1111`) is arbitrary, we can use any free port. The aplications using the tunnel should then be configured as:
- host=`localhost`
- port:=`1111`

The *remote machine* is the address of the machine we want to access relative to the *ssh server*. If the ssh server is running on the computer we want to access through the tunnel, we can use `localhost`. Analogously, the *remote port* is the port we wan to use on the remote machine (here `5432` is a PostgreSQL db port).

The `ssh server username` and `ssh server address` are then the username/address of the remote machine. On top of that, we need  password or priveta key to validate our identity. Note that the credential here are the credential for the server, not the credentials of the service we are accessing through the ssh connection. Those credentials has to be usually supplied by the application accessing the service through the ssh tunnel.

The connection can be canceled any time byping `exit` to the console.

[More information](https://linuxize.com/post/how-to-setup-ssh-tunneling/)

### Debugging a SSH tunnel
This guide suppose that the tunnel creation comman run without any error message.
1. If the tunnel seems to not work, first use a command line tool to be sure:
	- web browser for HTTP tunnels (remote port 80)
	- `psql` for postgeSQL tunnels (remote port 5432)
	- `telnet` for telnet tunnels (reote port 23)
2. If the test is unsucessful, try to kill all ssh connections to the server by shutting down all applications with ssh connections tunnels, untill there will be only one connection at the server (the console). The number of ssh connections can be checked with: `sudo netstat -nap | grep :22`


## Enabnling SSH Access on Server
1.  install openssh:
	- `sudo apt update`
    - `sudo apt install openssh-server`
2.  configure access
	- password:
		1.  open `/etc/ssh/sshd_config`
		2.  set `PasswordAuothentication yes`
		3.  after restrat you can log in with the user and password used in Ubuntu
	- keys: TODO
3. restart the ssh server: `sudo service ssh restart`

###  WSL configuration
1. port `22` can be used on Windows, so change the port to `2222` in `sshd_config`
2. when loging from Windows use `127.0.0.1` as a host

### Debugging
1n from now e  as a t euin.  check the ssh status with: `s th service ssh status`
2.  check the ssh porot with `sudso netstat t-tpln`


## SSH Agent
Normally, the SSH client process runs only while the SSH session is active, then, it is terminated. That means that we have to reenter the passphrase for the private key every time we want to connect to the server. To overcome this limitation, we can use the SSH agent programe.

An SSH agent is a process for storing decrypted SSH keys in memory. This means that we have to enter the passphrase only once per each OS login. The agent can be configured to automatically run on OS startup. The default SSH agent is `ssh-agent`, the rest of the section is dedicated to this agent.

To successfully use the agent, we need to:
1.  start the agent, either manually or automatically on OS startup
2.  add the keys to the agent (only once)

### Starting the agent
The agent can be started manually by running:
```bash
eval `ssh-agent`
```
We need to evaluate this command as it sets some environment variables. As the process cannot set the environment variables of the parent process due to security reasons, the `ssh-agent` prints the necessary commands to the console. By using eval, the `ssh-agent` is executed first, it prints the environment setup commands to stdout, which is captured by the eval command and executed.

### Listing keys
To list the keys stored in the agent, run:
```bash
ssh-add -l
```

### Adding keys
To add a key to the agent, run:
```bash
ssh-add <path to key>
```

### Debuging
If the agent is running and the key is listed, the first thing to try is to connect via ssh to see whether it is an agent/ssh issue or an issue of the program using the SSH (like git, IDE, file manager...)


## Configuration
For configuration, we can use the `git config` command. There are three levels of configuration:
- *system*: the configuration is applied to all users on the system. This configuration is set during the installation of git.
- *global*: the configuration is applied to all repositories of the current user. This configuration is set by the `--global` parameter.
- *local*: the configuration is applied only to the current repository. This configuration is set by the `--local` parameter.

To list the configuration, use the `-l`/`--list` parameter of the `git config` command. To list the configuration for a specific level, use the `--system`, `--global`, `--local` parameters.


To see the default value of a configuration, search in the [git config documentation](https://git-scm.com/docs/git-config#_variables).


## `known_hosts` file
To know that a connection leads to the desired server and not to some impersonator, the server sends its public key to the client. The client then checks the public key against the list of keys previously set as valid. This list is stored in the `.ssh/known_hosts` file. The format of the file is:
```
<server address> <key type> <key>
```
Each line contains one server record. What is confusing here is that each server can have multiple records, due to:
- different key type (e.g., RSA, ECDSA)
- key for both host name and IP address (e.g., `github.com` and `140.82.121.3`)
It is important to delete/updete all of these recorsds in case the server change its keys.

More info is at this [SO answer](https://security.stackexchange.com/questions/20706/what-is-the-difference-between-authorized-keys-and-known-hosts-file-for-ssh/20710#20710).


## Screen: executing a long running process over SSH 
When the SSH connection to a server is disconnected (either manually, or by network failure or timeout), the process running in the console is canceled. To overcome this limitation, we can use the `screen` command, which is especially usefull for long running processes.

A typical workflow can look like this:
1. execute `screen` to start the screen session
2. run the long running command
3. disconnect
4. connect to the server again
5. run `screen -r` to recconect to the session and see the results of the command.
1. after the command is finished, exit the screen session with `exit`

Sometimes, the server does not detect the connection failure and do not allow you to resume the session (step 5). In this way, we need to find the screen session ID and perform a detach and atach:
6. `screen -ls`
7. read the ID from the output and exec `screen -rd <ID>`


## Copying files over SSH using `scp`
The `scp` command is used to copy files over SSH. The syntax is:
```bash
scp <source> <destination>
```
The `<source>` and `<destination>` can be either local or remote. The remote files are specified using the `<username>@<address>:<path>` syntax. 

Note that **if the remote path contains spaces, double quoting is necessary**, one for local and one for remote:
```bash
scp <source> "<username>@<address>:'<path with spaces>'"
```


### Problems
- `protocol error: filename does not match request`: This error is triggered if the path contains unexpected characters. Sometimes, it can be triggered even for correct path, if the local console does not match the remote console. In that case, the solution is to use the `-T` parameter to disable the security check.



## WSL configuration
1.  port `22` can be used on Windows, so change port to `2222` in `sshd_config`
2.  when loging from Windows use `127.0.0.1` as a host


## Debugging
1.  check the ssh status with: `service ssh status`
2.  check the ssh port with `sudo netstat -tpln`




# Bash
## General Remarks
- It's important to use Linux newlines, otherwise, bash scripts will fail with unexpected character error
- Empty constructs are not allowed, i.e, empty function or loop results in an error
- brackets needs spaces around them, otherwise, there will be a syntax error
- space around `=`, which is typical in other languages, is not allowed in bash 
- bash does not support any data structures, only arrays



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

```bash
while condition
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


# Managing packages with `apt` and `dpkg`
To **update the list** of possible updates:
```bash
sudo apt update
```

To perform the **update**:
```bash
sudo apt upgrade
```

To find the location of an **installed package**:
```bash
dpkg -L <package>
```

To **search** for a package:
```bash
apt-cache search <package>
```


## Changing package repositories
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
Sed is a multi purpose command for string modification.

It can search and replace in string. The syntax is folowing:
```bash
sed s/<search>/<replace>/[<occurance>]
```
Example:
```bash
s/$/,3/
```

Any regex can be used as `<search>`. Some characters (e.g. `|`) must be escaped with backslash and used together with the `-E` parameter.

This replace the nd of the line with string `",3"`. Note that there is a slash at the end, despite we use the default option for occurance.

Also, it can delete lines containing string using:
```bash
sed /<pattern>/d
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
- for checking all processes, we can use `htop`
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

To see the groups of a user, we can use the `groups` command (no arguments needed).

To manipulate groups and users, we need a root access. 
To add a user to a group, we can use the `usermod` command:
```bash
usermod -a -G <group name> <username>
```

To remove a user from a group, we can use the same command:
```bash
usermod -G <group list> <username>
```
where `<group list>` is a comma separated list of groups the user should belong to.


# Installing Java
## Oracle JDK
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


# Python
Python has to be executed with `python3` by default, instead of `python`.


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
1. First run the **update of the current version**.
2. Then optionaly backup the WSL
3. run `sudo do-release-upgrade`

## WSL backup
1. check the WSL distro name: `wsl -l -v`
2. shutdown WSL: `wsl --shutdown`
3. backup the distro: `wsl --export <disto name> <backup folder path>/<backup name>.tar`

