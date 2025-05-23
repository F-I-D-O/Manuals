This manual is focused on [asymmetric encryption](https://en.wikipedia.org/wiki/Public-key_cryptography). As the principles are more or less the same for all technologies, we will focus on the technical aspects that differs.

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


## Authentication
There are two ways to authenticate to the server:

- password
- private key

Note that the server needs to be properly configured to accept your credentials. Specifically:

- for password authentication, the `PasswordAuthentication` option in `/etc/ssh/sshd_config` has to be set to `yes`. This is often disabled for security reasons.
- for private key authentication, the public key has to be added to your user account on the server. 

### Generating a key pair
To generate a key pair, use the `ssh-keygen` command.


### Setting up the private key to be used for ssh connection
To use a private key for ssh connection, two conditions have to be met:

1. the private key has to have the right permissions:
	- in Linux, the permissions have to be read/write only for the owner (`600`)
1. you have to specify that the private key should be used for the connection. This can be done in multiple ways:
	- using the `-i` parameter of the `ssh` command
	- specifying the key in the `~/.ssh/config` file
	- using ssh agent (see the SSH Agent section below)
	- selecting the key in an application with GUI



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

1. install openssh:
	- `sudo apt update`
	- `sudo apt install openssh-server`
2. configure password access
	1. open `/etc/ssh/sshd_config`
	2. set `PasswordAuothentication yes`
	3. after restrat you can log in with the user and password used in Ubuntu
3. restart the ssh server: `sudo service ssh restart`


### Enabling key authentication for a user
The user can only use a private key for authentication if the corresponding public key is assigned to the user on server. This is done by adding the public key to the `~/.ssh/authorized_keys` file.

Note that **the `authorized_keys` file has to have the right permissions**, which is read/write only for the owner, and read only for the group and others (`644`).


### WSL configuration

1. port `22` can be used on Windows, so change the port to `2222`
2. when loging from Windows use `127.0.0.1` as a host

To change the port:

- on older systems:
	- change the port in the `/etc/ssh/sshd_config` file
	- restart the ssh server: `sudo service ssh restart`
- on newer systems:
	1. `mkdir /etc/systemd/system/ssh.socket.d`
	2. `vim /etc/systemd/system/ssh.socket.d/<some name>.conf`
	3. add the following content:
		```conf
		[Socket]
		ListenStream=
		ListenStream=2222
		```
	4. `systemctl daemon-reload`
	5. `systemctl restart ssh.socket`


## SSH Agent
Normally, the SSH client process runs only while the SSH session is active, then, it is terminated. That means that we have to reenter the passphrase for the private key every time we want to connect to the server. To overcome this limitation, we can use the an SSH agent program.

An SSH agent is a process for storing decrypted SSH keys in memory. This means that we have to enter the passphrase only once per each OS login. The agent can be configured to automatically run on OS startup. The default SSH agent is `ssh-agent`, the rest of the section is dedicated to this agent.

To successfully use the agent, we need to:

1.  start the agent, either manually or automatically on OS startup
2.  add the keys to the agent (only once)

### Starting the agent
The starting of the agent is different for each OS:

- **Linux**: the agent can be started manually by running:
	```bash
	eval `ssh-agent`
	```
	We need to evaluate this command as it sets some environment variables. As the process cannot set the environment variables of the parent process due to security reasons, the `ssh-agent` prints the necessary commands to the console. By using eval, the `ssh-agent` is executed first, it prints the environment setup commands to stdout, which is captured by the eval command and executed.
- **Windows**: we need to start the OpenSSH agent service. Consult the [Windows Manual](<Windows/Windows Manual.md#ssh-key-agent>) for more details.

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


## List all active connections on a server
To list all active connections on a server, we can use the `lsof` command and filter the output for the ssh connections:
```bash
lsof -i -n | grep ssh
```


## Debugging

**If the server does not respond:**

1. check the ssh status with: `service ssh status`
2. check the ssh port with `sudo netstat -tpln`

**If the key is not accepted:**
Check the log file: `sudo tail -c 5000 /var/log/auth.log`



# GNU Privacy Guard (GPG)
[GPG](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) is a second most popular tool for encryption, after the SSH keys. Apart from encryption capabilities, it offers also a management of subkeys, and a possibility to revoke the key. It can be downloaded from the [GNU-PG website](https://gnupg.org/download/).

GPG comes with a build in key agent. 

To **list** the keys added to the agent, use `gpg --list-keys`. 

To **import** a key, call `gpg --import <keyfile>`.


## Key expiration
There is a mechanism for key expiration in GPG. However, it is important to understand that the expiration date is mostly not a security feature! It can be useful in the following cases:

- you lose access to the key, and nobody else can access it as well. In that case, you cannot revoke the key, but you can just wait until the key expires.
- you set the expiration date for subkeys. For subkeys, the expiration date is a security feature, as it cannot be changed without the main key.

To prolong the expiration date, we can use the `gpg --edit-key <key-id>` command. After using it:

1. choose the key you want to edit by number
1. now the chosen key should be marked with an asterisk `*`. Enter `expire` 
1. choose the new expiration date
1. save the changes by `save`


## Troubleshooting

### `partial length invalid for packet type 63`
This can happen if the private key has a wrong encoding. It can be fixed by cnverting the key file to ASCII encoding.


# Storing passwords for the command line tools
Sometimes, we need to store passwords for the command line tools on the local machine. For non-sensitive passwords, we can just store them in a file that is not versioned. However, for sensitive passwords and authentication tokens, we should not store them in plain text. We have two options:

- Use a Credential Manager, or
- Encrypt the file where the passwords are stored.

### Credential Managers
There are plenty of credential managers available for each OS. If we want to avoid the differences between the OS, we can use the python [keyring](https://pypi.org/project/keyring/) package.

### Python keyring
[homepage](https://pypi.org/project/keyring/)

The keyring package is a Python library that provides a way to store passwords in a secure way. It uses a system-specific backend to store the passwords. 

To manage the passwords, we can use the `keyring` command provided by the package. The basic usage is:
```bash
keyring set <service> <username> # set the password. After running this command, the password is prompted
keyring get <service> <username> # get the password
```

To use the keyring in a Python script, we use the `keyring` package:
```python
import keyring

password = keyring.get_password("service", "username")
```
