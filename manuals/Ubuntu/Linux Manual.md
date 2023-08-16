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
The `cp` command is used to copy files. The most used options are:
- `-r`, `-R`: copy recursively
- `-v`: verbose
- `-f`: force
- `-p`: preserve permissions and timestamps
- `-a`: same as `-p -R` plus some other options


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


# Network
## [`netstat`](https://en.wikipedia.org/wiki/Netstat)
The [`netstat`](https://en.wikipedia.org/wiki/Netstat) command is the basic command to monitor the networ. It displays the TCP connections. It is available both on Linux and on Windows, although the interface differs. Important parameters:
- `-n`: do not translate IP and ports into human readable names
- `-a`: show all connections. Without this, some connections can be skipped.

# SSH
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

## Debugging a SSH tunnel
This guide suppose that the tunnel creation comman run without any error message.
1. If the tunnel seems to not work, first use a command line tool to be sure:
	- web browser for HTTP tunnels (remote port 80)
	- `psql` for postgeSQL tunnels (remote port 5432)
	- `telnet` for telnet tunnels (reote port 23)
2. If the test is unsucessful, try to kill all ssh connections to the server by shutting down all applications with ssh connections tunnels, untill there will be only one connection at the server (the console). The number of ssh connections can be checked with: `sudo netstat -nap | grep :22`

## Enabnling SSH Access to Server
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

## Executing a long running process over SSH 
When the SSH connection to a server is disconnected (either manually, or by network failure or timeout), the process running in the console is canceled. To overcome this limitation, we can use the `screen` command, which is especially usefull for long running processes.

A typical workflow can look like this:
1. execute `screen` to start the screen session
2. run the long running command
3. disconnect
4. connect to the server again
5. run `screen -r` to recconect to the session and see the results of the command.

Sometimes, the server does not detect the connection failure and do not allow you to resume the session (step 5). In this way, we need to find the screen session ID and perform a detach and atach:
6. `screen -ls`
7. read the ID from the output and exec `screen -rd <ID>`


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

## Working with I/O
- `<command A> | <command B>` forward output of `<command A>` to th input of `<command B>`.
- `<command> <<< $<variable>` forward `<variable>` to the input of `<command>`
- `<command 1> | tee >(<command 2>) | <command 3>`: forward `<command 1>` to both `<command 2>` and `<command 3>`.

Note that the content of the pipe cannot be examined, the process on the right hand side consume it. Therefore, **it is not possible to simply branch on pipe content** while use it in the subsequent process.

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


## Conditions
In general, condition in bash has the following syntax:
```bash
if <condition> 
	then <command>
	else <command>
fi
```

The condition above uses the *exit code* of a command to determine the logical value. When testing that the command succeeded, we can use it like:
```bash
if <command> 
	then ...
fi
```
Example:
```bash
if grep -q "$text" $file 
	then ...
fi
```

But if we want to use some arbitrary value (e. g. the *return value* of a command), or comparisons in the condition (simmilar to programming languages), we have to use the test command:

```bash
if test <comparison>
then ...
fi
```
The test command is also invoked if we use square brackets:
```bash
if [ <comparison> ]
then ...
fi
```
Example:
```bash
if [ $var = 1 ]
then ...
fi
```
The test command expects to compare to values. If we want to compare a result of some command, we need to usethe command substtitution.

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



# String Modification

## `sed`
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

## Trim string
```bash
<command with string output> | xargs
```



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


nabling SSH Access to Server
1.  install openssh:
	- `sudo apt update`
    - `sudo apt install openssh-server`
2.  configure access
	- password:
		1.  open `/etc/ssh/sshd_config`
		2.  set `PasswordAuthentication yes`
		3.  Now you can log in with the user and password you use in Ubuntu
3.  keys: TODO


# Upgrade
1. First run the **update of the current version**.
2. Then optionaly backup the WSL
3. run `sudo do-release-upgrade`

## WSL backup
1. check the WSL distro name: `wsl -l -v`
2. shutdown WSL: `wsl --shutdown`
3. backup the distro: `wsl --export <disto name> <backup folder path>/<backup name>.tar`

