# Restarting or shutting down Linux

There are several commands available. All stops the OS, but they differ in what happens next.

- `reboot`: restarts the computer
- `poweroff`: shuts down the computer
- `halt`: nothing, just stops the OS

Addiditonaly, there is a `shutdown` command that has more options (like delays), and depending on the main parameters, it can deliver all the above actions (reboot, poweroff, halt).

Note that none of these commands are standardized accross Linux distributions (but works on almost all of them). On systems with systemd, these commans call `systemctl` subcommands internally


# Usefull Comands

## Versions

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
Use the `which` command: `which <executable>`.

Other option is to use the [`command`](https://manned.org/man/command) command: `command -v <executable>`.


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
If you need the variable outside bash, the above-mentioned approach won't work. Currently, I do not know about any general solution for variables. The solution below, unfortunately, work only for [PAM shells](https://en.wikipedia.org/wiki/Linux_PAM)  (see [this SO answer](https://unix.stackexchange.com/questions/473001/env-vars-in-etc-environment-not-globally-visible) why).

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
Unlike Windows, Linux typically doe not split the filesystem into partitions that much. Moreover, each partition path can start anywhere, instead of `<drive letter>:` like in Windows. Typically, the main partition is mounted at `/`. 


## Standard folder structure
The [standard folder structure](https://en.wikipedia.org/wiki/Filesystem_hierarchy_standard) is:

- `/bin` core binaries, usually a limited set distributed with the OS
- `/home/<user name>` home directory for the user `<user name>`
- `/opt` for software packages distributed in the Windows style, i.e., as a single installation directory.
- `/sbin` same as `/bin`, but for system binaries, i.e., binaries for system maintenance
- `/usr/bin` and `/usr/sbin` For binares installed by package managers. Binaries from other sources should not be installed here, as there is a risk of overwritting them by the package manager.
- `/usr/local/bin` and `/usr/local/sbin`: For binaries installed by the user, i.e., not by the package manager.

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

## Copy files
The `cp` command is used to copy files: `cp <source> <destination>`. The most used options are:

- `-r`, `-R`: copy recursively
- `-v`: verbose
- `-f`: force
- `-p`: preserve permissions and timestamps
- `-a`: same as `-p -R` plus some other options


### rsync
For more sophisticated copying, use [`rsync`](https://rsync.samba.org/) ([documentation](https://download.samba.org/pub/rsync/rsync.1)): `rsync <source> <destination>`. 

Unlike the `cp` command, the `<source>` have a different meaning depending on the trailing slash:

- if the `<source>` ends with a slash, it behaves like `cp`:
    ```bash
    rsync -r /path/to/source/ /path/to/destination
    # the content of the source directory is copied to the /path/to/destination directory
    ```
- if the `<source>` does not end with a slash, it behaves differently:
    ```bash
    rsync -r /path/to/source /path/to/destination
    # the content of the source directory is copied to the /path/to/destination/source directory
    ```



The most used options are:

- `-r`, `--recursive`: recurse into directories. Only files are copied without this option.
- `-h`: human readable

#### Preserving metadata

- `-l`, `--links`: preserve links
- `-p`, `--perms`: preserve permissions
- `-t`, `--times`: preserve modification times
- `-U`, `--atimes`: preserve access times
- `-N`, `--crtimes`: preserve creation times
- `-g`, `--group`: preserve group
- `-o`, `--owner`: preserve owner
- `--specials`: preserve special files
- `--devices`: preserve device files
- `-D`: equivalent to `--devices --specials`
- `-a`: archive mode, equivalent to `-rlptgoD`

#### Formatting the output

- `--progress`: show progress bar for each file transfer
- [`--info=<FLAG>[<FLAG_VALUE>]`](https://download.samba.org/pub/rsync/rsync.1#opt--info): detailed configuration of the rsync output. Here, 
    - `<FLAG>` is the specific output parameter we want to set:
        BACKUP     Mention files backed up
        - `COPY`: Mention files copied locally on the receiving side
        - `DEL`: Mention deletions on the receiving side
        - `FLIST`: Mention file-list receiving/sending (levels 1-2)
        - `MISC`: Mention miscellaneous information (levels 1-2)
        - `MOUNT`: Mention mounts that were found or skipped
        - `NAME`: Mention 1) updated file/dir names, 2) unchanged names
        - `PROGRESS`: Mention 1) per-file progress or 2) total transfer progress
        - `REMOVE`: Mention files removed on the sending side
        - `SKIP`: Mention files that are skipped due to options used
        - `STATS`: Mention statistics at end of run (levels 1-3)
        - `SYMSAFE`: Mention symlinks that are unsafe
        - `ALL`: Set all --info options (e.g. all4)
    - `<FLAG_VALUE>` is the value of the parameter.
        - `0`: disable the output
        - `1`: default value
        - `< Number > 1 >`: more detailed output. The maximum level depends on the output parameter we want to set.

    - Example: `--info=progress2` will show the progress total progress, instead of the progress bar for each file transfer.

#### Overwriting files

- `--ignore-existing`: ignore files that already exist on the destination.
- `--update`: ignore newer files on the destination.
- `--checksum`: use checksum to compare files, not the file size and modification time.


## Remove file
The `rm` command is used to remove files. The most used options are:

- `-r`, `-R`: remove recursively
- `-f`: force

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
To find files, use the [`find`](https://man7.org/linux/man-pages/man1/find.1.html) command: `find <where> <options>`. If the `<where>` is not specified, the current directory is used. If the `<options>` are not specified, all files matching the `<where>` are listed.

The most used options are:

- `-name <name pattern>`: find by name.
- `-path <path pattern>`: find by path.
- `-regex <regex pattern>`: find by path specified as regex. Note that by default, the regex type is emacs-style. Therefore, we have to set the type to `posix-extended` to work reasonably with regexes. so in the end, we have to use:
	```bash
	find -regextype posix-extended -regex '.*<regex pattern>.*'
	```
	- note the order of the options. **Specifying the `-regextype` after the `-regex` option does not work.**
- `-printf <format>`: set the output format. 
	- The most important format specifiers are:
		- `%f`: file name
		- `%p`: file path
		- `%TY`: year
		- `%Tm`: month
		- `%Td`: day
		- `%TH`: hour
		- `%TM`: minute
		- `%TS`: second
	- modifiers can be used to format the output:
		- `%.2<format specifier>`: format the output to 2 digits


## Access standard input as a file (`/dev/stdin`)
[GNU manual](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)

In Linux, standard input can be accessed as a file through `/dev/stdin`. This allows commands that expect a file as input to read from standard input. For example:
```bash
cat /dev/stdin
```
You can then type input and press `Ctrl+D` to signal the end of input.


## `install` command

- [Wikipedia](https://en.wikipedia.org/wiki/Install_(Unix))
- [GBU Reference](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html)
- [Man 7 Reference](https://man7.org/linux/man-pages/man1/install.1.html)

In Linux the `install` command is not a command for software installation, but for a wrapper to copy files, create necessary directories, and set file attributes in one step. The basic syntax is:
```bash
install <source> <destination> # installing files
install -d <directory> # creating directories
```

Besides, there exist an idiom to use a string instead of a `<source>` by using `/dev/stdin`:

```bash
echo "Hello, World!" | install /dev/stdin /tmp/hello.txt
```

Unlike the `cp` command, 

- `install` creates executable copies of the files,
- if the target file exists, `install` unlike it instead of overwriting the content, so it is safe to use for replacing running executables,
- only files can be installed, not directories (unless the `-d` option is used).


Important options:

- [`-m <mode>`, `--mode=<mode>`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html#index-_002d_002ddirectory-1): set the file mode (permissions)
- [`-o <owner>`, `--owner=<owner>`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html#index-_002d_002downer): set the file owner
- [`-g <group>`, `--group=<group>`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html#index-_002d_002dgroup-1): set the file group
- [`-d`, `--directory`](https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html#index-_002d_002ddirectory-1): create any necessary parent directories, then create the specified directory. Only the specified directory gets the specified attributes, parent directories get default attributes.


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

## `netstat`
The [`netstat`](https://en.wikipedia.org/wiki/Netstat) command is the basic command to monitor the networ. It displays the TCP connections. It is available both on Linux and on Windows, although the interface differs. Important parameters:

- `-a`: show all connections. Without this, some connections can be skipped.
- `-n`: do not translate IP and ports into human readable names
- `-o`: 



# Bash
See [Bash Manual](Bash%20Manual.md) for detailed information about Bash scripting and commands.


# Users
The users are listed in `/etc/passwd`. The file contains one line per user, each line has the following format:
```text
<username>:<password>:<user ID>:<group ID>:<GECOS>:<home folder>:<shell>
```
The password is typically stored in `/etc/shadow` and is represented by `x`. [GECOS](https://en.wikipedia.org/wiki/Gecos_field) is some kind of a comment storing arbitrary information about the user.

There are several commands that can be used to manage users on any distribution:

- `useradd`: add a new user
- [`usermod`](https://man7.org/linux/man-pages/man8/usermod.8.html): modify an existing user
- `deluser`: delete a user


## Adding a user
To add a user, we can use either the `useradd` binary directly, or, on some distributions, an interactive `adduser` wrapper script.



## Modifying a user
[`usermod` Reference](https://man7.org/linux/man-pages/man8/usermod.8.html)

The basic syntax of the `usermod` command is:
```bash
usermod <options> <username>
```

Important options:

- `-a`: add user to new groups (only used with `-G`)
- `-G <group list>`, `--groups <group list>`: specify the list of groups the user should belong to. The groups are comma-separated, and must exist already.
    - if the user is a member of any groups not listed in `<group list>`, they will be removed from those groups. This behavior can be changed by using the `-a` option, in that case, user will be added to the `<group list>` without being removed from non-listed groups.


## User Groups

- [`chgrp POSIX reference`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/chgrp.html)

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

To **change the group ownership of a file**, we can use one of the following commands:

- `chgrp <group> <files>`
- `chown :<group> <files>`

In both commands, `<files>` can be a single file or multiple files separated by spaces.


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


## User password management

- [man 7 Reference](https://man7.org/linux/man-pages/man1/passwd.1.html)
- [Wikipedia](https://en.wikipedia.org/wiki/Passwd)

For password management, we use the `passwd` command. The syntax is:
```bash
passwd [<username>]
```

This prompts the current user to enter a new password for the specified user. If no username is provided, it changes the password for the current user. 

THe command can be also used to see the **password status** of a user by running:
```bash
passwd -S <username>
```
The output fields are:

- user name
- password status:
    - `P` for a usable password
    - `L` for a locked password
    - `NP` for no password set
- last password change date
- minimum age for password change
- maximum age for password change
- warning period for password expiration
- inactivity period for password

The last four fields are in days.


## Disable access to shell for a user
To disable access to shell for a user, we have to configure his/her shell to `/usr/sbin/nologin` or similar. 

- For new users, we can use the `--shell` parameter of the `adduser` command.
- For existing users, we can use the `usermod` command:
    ```bash
    usermod --shell /usr/sbin/nologin <username>
    ```


Note that for some ssh client implementations, it is necessary to connect to a shell by default, otherwise, the connection is terminated immediately after login. In this case, the user has to connect to the server with the `-N` parameter, which tells the client not to execute any command after login.



# Privileged Access
[`sudo` Wikipedia](https://en.wikipedia.org/wiki/Sudo)

In Linux the security model is simple: some potentially sensitive operations require elevated privileges (called *root privileges*). The user with root privileges is usually named `root` and it's called the *superuser*.

Unlike on Windows, the recommended way to run commands with elevated privileges is not to directly switch to the superuser account, but to use the `sudo` command. This command let a user to execute a command with root privileges without switching to the root user:
```bash
sudo <command>
```
A password of the current user is required to run the command (if not cached in case of recent use).

A user must me allowed to run `sudo`. This is usually configured by adding the user to a specific group:

- `sudo` group on Debian-based systems (e.g., Ubuntu)
- `wheel` group on Red Hat-based systems (e.g., CentOS, Fedora)

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
Package management heavily depends on the distribution. Therefore, check the manual for the specific distribution:

- [Ubuntu package management](Ubuntu.md#managing-packages)


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
[POSIX Reference](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cut.html)

Cut is a useful command for data with delimiters. Usage:
```bash
cut -f <columns>
```
Where columns are data fields separated by the delimiter (default is tab).

If we need to specify delimiters, we use the `-d` parameter:
```bash
cut -d , -f 1,5
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


# SSH
[SSH Manual](../Security.md#ssh)

To see the last login of each user, we can use the `lastlog` command.

## Inspecting commands executed over SSH
There are various possible ways to inspect the commands executed over SSH. Commands from interactive console should appear in history and we should see them when running `history` command, just like in local console. 

Much more complicated is to see the commands executed over SSH in a non-interactive way, e.g., when running a command over ssh (`ssh user@host <command>`). One way to do this is to use a command wrapper script for a specific ssh key:

1. create the wrapper script:
    ```bash
    #!/usr/bin/env bash
    log="$HOME/ssh_commands.log"

    # Log who/when/where and the command (or "<interactive>" if none)
    printf '%s user=%s from=%s cmd=%q\n' \
        "$(date '+%F %T')" "$USER" "${SSH_CONNECTION%% *}" \
        "${SSH_ORIGINAL_COMMAND:-<interactive>}" >> "$log"

    # Run the original command or a login shell
    if [ -n "$SSH_ORIGINAL_COMMAND" ]; then
        exec bash -lc "$SSH_ORIGINAL_COMMAND"
    else
        exec bash -l
    fi
    ```
1. make the script executable: `chmod +x <path to the script>`
1. create the log file: 
    ```bash
    touch <path to the log file>
    chmod 600 <path to the log file>
    ```
1. add the script to the `authorized_keys` file:
    ```bash
    echo "command=<path to the script> ssh-rsa AAAA..." >> ~/.ssh/authorized_keys
    ```


## Screen: executing a long-running process over SSH 
When the SSH connection to a server is disconnected (either manually, or by network failure or timeout), the process running in the console is canceled. To overcome this limitation, we can use the `screen` command, which is especially usefull for long running processes.

A typical **workflow** can look like this:

1. execute `screen` to start the screen session
2. run the long-running command
3. disconnect
4. connect to the server again
5. run `screen -r` to reconnect to the session and see the results of the command.
1. after the command is finished, exit the screen session with `exit`

To **detect** if we are running in a screen session, we can use `echo "$STY"`. If the output is not empty, we are running in a screen session.

To **exit** the screen session, we can use `exit` command.

When using screen, we cannot scroll back. To **scroll back**, we need to switch to the insert mode using `Ctrl` + `a` + `[`.

### What to do if the reconnect fails
Sometimes, the server does not detect the connection failure and do not allow you to resume the session (step 5). In this way, we need to find the screen session ID and perform a detach and atach:

6. `screen -ls`
7. read the ID from the output and exec `screen -rd <ID>`


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
the progress bar can be printed using the [`pv`](https://man7.org/linux/man-pages/man1/pv.1.html) command.
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
For a system upgrade, refer to the manual for the specific distribution:
- [Ubuntu upgrade](Ubuntu.md#upgrade)



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


## Troubleshooting

### If `vim` complains about existing swap file
Some programs create temporary files when editing files. When such a file exists for the file you are trying to edit, `vim` will complain about it. If you do not suspect that your file is actually modified, you can safely delete the swap file.

To see the swap file, you need to use the `-a` option of the `ls` command. Typically, it is named `.<your file name>.swp`.
