# Terminals and Shells
There are two main [terminal applications](https://en.wikipedia.org/wiki/Terminal_emulator) in Windows: 
- [*Windows Console Host*](https://en.wikipedia.org/wiki/Windows_Console): an old terminal application present in Windows for years, and
- [*Windows Terminal*](https://en.wikipedia.org/wiki/Windows_Terminal): a new terminal application that is still in development.

To get the best experience similar to Linux, it is recommended to use the Windows Terminal. It is available in the [Microsoft Store](https://aka.ms/terminal).

The simplest [shell](https://en.wikipedia.org/wiki/Shell_(computing)) is the [command prompt](https://en.wikipedia.org/wiki/Cmd.exe) (`cmd.exe`). However, due to its limited functionality, it is better to use [PowerShell](https://en.wikipedia.org/wiki/PowerShell). For PowerShell solutions/guides, check the [PoweShell manual](./Powershell%20Manual.md).


## Run a non-default terminal application
It is not an easy task to manually tun a shell in a non-default terminal application. To do it, we need to execute the terminal application executable:
- Windows Terminal: `wt.exe`
- Windows Console Host: `conhost.exe`


## Windows Terminal
The Windows Terminal is a new terminal application with many great features:
- multiple tabs
- smart text selection

To configure Windows Terminal, click the `v` button in the top bar and select `Settings`. There are two kinds of settings:
- Global settings sorted in categories in the left panel
- Profile settings for each profile. The profiles are listed in the left panel. After selecting a profile, the settings are displayed in the right panel. Nonbasic settings are sorted in categories under the `Additonal settings` header. 


### Windows terminal pass stdout to text editor instead displaying it
This can happen if the output is too long or wide for the terminal. 

If a command outputs a text in Windows console host but passes it to a text editor in Windows Terminal, the possible cause is the font size. The default size in Windows Terminal is 12, which is much larger than the 16 in Windows Console Host (default). To fix it, change the font size in Windows Terminal to 10 which corresponds to the 16 in Windows Console Host.



# Keyboard Shortcuts
- `Alt` + `Shift`: change input language
- `Win` + `Space`: change keyboard input method


# Wireless Network

## Problem: Can't connect to this network
Solution: Forget the connection and connect to the network manually

## Connect to a Network Manually
1. `Control Panel` -> `Network and Internet` -> `Network and Sharing Center`
2. `Set up a new connection or network`
3. `Manually connect to a wireless network`
4. Fill the credentials:
	- Network name: SSID
	- Security type: depends, try WPA2 personal
	- Security key: password
5. Click next
6. Close the dialog 
7. Click the wifi icon in the taskbar and connect to the network

There are various usefull comands. For most of the commands, you need to open PowerShell as admin.

## Various Commands Related to the Wifi

### Show All Network Profiles
This command show network configurations stored on the device.
```
netsh wlan show profile
```

### Various Wifi Reports in HTML
```
netsh wlan show wlanreport
```
# Changing the input method
It is possible to let the system have a different input method for each app. It is not possible however, to remember the input method (after app/OS restart).

## Troubleshooting
### Nothing happens after clicking on the input method in the taskbar (windows 10)
restrat the computer :)





# Bluetooth
## Troiubleshooting
### Cannot connect to the device
1. Try to remove the device and pair it with the PC again
2. If it does not help, proceeed to the next section (even if the pairing is successfull)

### Cannot pair with the device
Turn off the device and unplug it from the electricity/remove batteries. Then plug it back after ~10 seconds, power it of, and try to pair with it again.

## Bluetooth Command Line Tools
https://bluetoothinstaller.com/bluetooth-command-line-tools

Bluetooth Command Line Tools is a set off tools that enables command line interaction with blootooth services. Basic usage:
- discover and list available devices: `btdiscovery -s`

# Filesytem

## Standard folder structure
In Windows, the standard folder structure is completely different for system and user instalation. Details are listed below, but the main difference is that the system instalations are stored in a single root folder for each application (similarly to Android), while the user instalations' files are distributed among multiple folders, depending on the type of the file (similarly to Linux).

### User home folder
The user home folder is located in `C:\Users\<username>` by default. It is aliased as `%userprofile%`. 

### System instalation folders
If an application is installed for all users, all its files are usually installed in a single folder per application. The location of the folder depends on the type of the application:
- `C:\Program Files`: 64-bit applications
- `C:\Program Files (x86)`: 32-bit applications

If the application needs to store some data, they are usually stored in the `C:\ProgramData` (aliased as `%programdata%`) folder.


### User instalation folders
User instalations are stored in multiple folders, depending on the type of the file. All these folders are located in the user's home folder, which is `C:\Users\<username>` by default. The folders are:
- `~\AppData\Local`: Program data and sometimes also executables
- `~\AppData\Local\Promgrams`: program files and executables
- `~\AppData\LocalLow`:
- `~\AppData\Roaming` (aliased as `%appdata%`):

### Start Menu folder
The user specific shortcuts are stored in: `%appdata%\Microsoft\Windows\Start Menu\Programs`.

The system wide shortcuts are stored in: `%programdata%\Microsoft\Windows\Start Menu\Programs`.


## Read Only Files and Folders
An ancient form of file protection on Windows is the read only flag that can be set on files and folders. It is not a real protection, as it can be easily removed by the user, but it can be used to prevent accidental changes.

Most of the programs can ignore this flag and work with the file anyway. However, some programs (e.g. Python) can have problems with it. 




# Sugarsync
Quick orientation in the desktop app:
- for file changes, check left menu -> `Activity`
- for deleted files, check left menu -> `Deleted Items`

## Solving sync problems
1. check if the file is updated in cloud using web browser
2. if not, check the activity log on the computer with the updated file
3. if the change is not in the log, a simple hack can help: copy the file outside SugarSync folder and back.




# Useful Commands
## Get Motherboard Info
```
wmic baseboard get product,Manufacturer,version,serialnumber
```
## Copy multiple files/dirs
[`robocopy`](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) is the best command for that. Usefull params:
- `/e`: Copy subdirectories, including empty ones
- `/b`: Copy in the backup mode, so that even files with a different owner can be copied
- `/xc`: Excludes changed files.
- `/xn`: Excludes newer files.
- `/xo`: Excludes older files.
- `/r:<n>`: Specifies the number of retries on failed copies. The default value of _n_ is 1,000,000 (one million retries).
- `/w:<n>`: Specifies the wait time between retries, in seconds. The default value of _n_ is 30 (wait time 30 seconds).


## User info
Information about users can be obtained with the [`Get-LocalUser`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/get-localuser?view=powershell-7.1) command. By default, the command lists all users. Some useful params:
- `-Name`: Specifies the user account names of the users to get. 
- `-SID`: Specifies the security identifier (SID) of the users to get. 


# Installation
## Windows 11
Windows 11 can be installed only as an update of Windows 10.

## Windows 10
Can be installed from bootable USB created by a tool downloaded from the official Miccosoft website. Single image for all Windows versions, a particular version is choosen based on the license key. Steps:
1. Download the install tool from Microsoft
2. Create a bootable USB
3. Start the installation
4. Fill in the licence key

### we couldn’t create a partition or locate an existing one
Ensure that the boot priority of the drive where the Windows should be installed is right behind the installation USB priority.

# Diskpart
Diskpart is a useful command line tool for work with diska, partitions, etc.

## Find out wheteher a disk is MBR or GPT

# Open Command Promp from the Windows 10 USB
1. Insert the USB stick
2. Wait till the first installation screen
3. `shift` + `F10`

# Firewall
## Generate firewall logs
1. Go to Windows firewall and select properties on the right
2. At the top, choose the profile corresponding to the current network profile
3. In the logging section, click to customizze
4. set both DROP and ACCEPT to yes

Do not forgot to turn of the logging after the investigation!



# SSH
For ssh, we can use the standard `ssh` commannd available in Windows (check Linux manual for more info). If the command is not available, it can be installed in `Apps & Features` -> `Optional features`.

One thing that differs from Linux is that the Windows ssh does not support the `<addres>:<port>` syntax. To specify the port, it is necessary to use the `-p` parameter

For more features, we can use other programs
- [KiTTY](http://www.9bis.net/kitty/index.html#!pages/Portability.md) for credentials storage, automatic reconection, etc.
- [WinSCP](https://winscp.net/eng/index.php) for file manipulation


## KiTTY
It is best to use the portable version, so that nothing is stored in the Windows registry. Configurtation:
- [copy the PuTTY credentials](): `.\kitty_portable-0.76.1.3.exe -convert-dir`
- auto reconnect: `Connection` -> `auto reconnect on connection failure` and `auto reconnect on system wakeup`


## WinSCP
WinSCP is a graphical tool for file manipulation. Ii can be used both for local and remote files, and it supports various protocols (FTP, SFTP, SCP, WebDAV, etc.). 

### Adding a new connection
There is a simple `New Site` button on the left, which opens a straightforward dialog. The only complicated thing can be the SSH key. To add it, click on the `Advanced` button and go to the `SSH` -> `Authentication` tab. There, we can select the private key file.


### Bookmarks
To add bookmarks, go to `Local`/`Remote` -> `Add Path to Bookmarks` or press `Ctrl` + `B`.

To open a bookmark, go to `Local`/`Remote` -> `Go To` -> `Open Drirectory/bookmark` or press `Ctrl` + `O`.



## SSH key agent
To enable the ssh-agent on Windows, one extra step is needed: we need to start the ssh-agent service. To do that, open the services manager and start the `OpenSSH Authentication Agent` service.


# Git
Most of the git functionality is the same as in Linux, so check the Linux manual for more info. However, there are some important differences mostly resulting from the fact that Git is not a native Windows application, but it runs in MinGW. 

## Git on Windows and SSH
As the git on Windows runs in MinGW, it does not use the Windows SSH command. That can be problematic if we want to debug the SSH connection using the env variable or configuring an ssh key agent. To force git to use the Windows SSH, we need to set the `sshCommand` config variable to the path to the Windows SSH:
```PowerShell
git config --global core.sshCommand C:/Windows/System32/OpenSSH/ssh.exe
```





# Problems

## Folder Sharing Problems
Note that updated **Windows 10 disabled anonymous sharing**, so password protected sharing has to be turned on. 

**To login, use the credentials for the computer with the shared folder**. 

Below is a list of possible problems, together with solutions.

### The user name or password is incorrect
1. Check whether the computer can be seen in the network. If not, resolve this issue first.
	- quick check by running `net view <IP address>`
2. Check that you are using the right username. You need to **use the username and password of the computer you are connecting to**.
	- Check that the user name is correct by running `net user` on the target computer
	- Check that the folder is shared with you in: right click on the folder -> `Properties` -> `Sharing` -> `Advanced Sharing...` -> `Permisions`. Note that your full name can be there instead of your username, which is OK.
4. Check that you are using the right password. You have to use the password associated with your microsoft account. Note that **it can differ from the password (PIN) you are using to log in to the computer!**
3. check it on the command line: `net use * \\<IP address>\<drive letter>$ /use:<username> <password>`

### Folder right and ownership cannot be read
Try to clear the windows filecache (CCcleaner or restart)

### Computer does not see itself in Network section in File Explorer
Solution to this problem is to restart the service called *Function Discovery Resource Publication*. Either restart it in Computer Management -> Services, or by:
```
net stop FDResPub
net start FDResPub
```


## PC wakes up or cannot enter sleep
### 1 Find the source
Using the Event viwer
1. open the event viewer
2. go to `windows logs` -> `system`
3. In case of wake up
	1. inspect the logs when the wake up happened and search for the Information log with the message *"The system has returned from a low power state."*
	2. There is a wake up source in the end of the log message. If the soure is Unknown go to the next section
4. In case of not entering sleep
	1. Search for the any *kernel power* event 
	2. If there is an event stating: *The system is entering connected standby*, it means that the modern fake sleep is present in the system, replacing the real sleep mode. 

Using command line (admin):
 1. Try `powercfg -lastwake`
 2. If the results are not know, try to call `powercfg -devicequery wake_armed` to get the list of devices that can wake the computer

### 2 Solve the problem
#### Device waken up by network adapter
1. Open device manager and search for the specific network adapter 
2. right click -> `Properties` -> `Power Management`
3. Check `Only allow a magic packet to wake up the computer` 

#### The real sleep mode is not available on the system
If this is the case, use the hibernate mode instead. To add it to the start menu:
1. go to `Control panel` -> `Hardware and sound` -> `Power options`
2. click on the left panel to `Choose what the power buttons does`
3. click on `Change settings that are currently unavailable`
4. check the `hibernate` checkbox below


## Camera problem
Symptoms: the screen is blank, black, single color, in all apps and there are no problems reported in device manager
Cause: it can be caused by some external cameras (now disconnected) that are still selected in the apps using the camera. Go 
Solution: Go to the app setting and select the correct camera


## Phone app cannot see the connected cell phone
It can be due to the fucked up Windows N edition. Just install the normal edition.


## `vmmem` process uses a lot of CPU
This process represents all virtual systems. One cultprit is therefore WSL. Try to shutdown the WSL using 
```
wsl --shutdown
```