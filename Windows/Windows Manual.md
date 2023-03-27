# General Guides
For PowerShell solutions/guides, check the [PoweShell manual](https://drive.google.com/file/d/1yCSdzN_KVykt2CH-3USMVmTU2djAtfN9/view?usp=sharing)

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
	- Security type: dpends, try WPA2 personal
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


# Folder Sharing Problems
Note that updated **Windows 10 disabled anonymous sharing**, so password protected sharing has to be turned on. 

**To login, use the credentials for the computer with the shared folder**. 

Below is a list of possible problems, together with solutions.

## The user name or password is incorrect
1. Check whether the computer can be seen in the network. If not, resolve this issue first.
	- quick check by running `net view <IP address>`
2. Check that you are using the right username. You need to **use the username and password of the computer you are connecting to**.
	- Check that the user name is correct by running `net user` on the target computer
	- Check that the folder is shared with you in: right click on the folder -> `Properties` -> `Sharing` -> `Advanced Sharing...` -> `Permisions`. Note that your full name can be there instead of your username, which is OK.
4. Check that you are using the right password. You have to use the password associated with your microsoft account. Note that **it can differ from the password (PIN) you are using to log in to the computer!**
3. check it on the command line: `net use * \\<IP address>\<drive letter>$ /use:<username> <password>`

## Folder right and ownership cannot be read
Try to clear the windows filecache (CCcleaner or restart)

## Computer does not see itself in Network section in File Explorer
Solution to this problem is to restart the service called *Function Discovery Resource Publication*. Either restart it in Computer Management -> Services, or by:
```
net stop FDResPub
net start FDResPub
```


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


# PC wakes up or cannot enter sleep
## 1 Find the source
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

## 2 Solve the problem
### Device waken up by network adapter
1. Open device manager and search for the specific network adapter 
2. right click -> `Properties` -> `Power Management`
3. Check `Only allow a magic packet to wake up the computer` 

### The real sleep mode is not available on the system
If this is the case, use the hibernate mode instead. To add it to the start menu:
1. go to `Control panel` -> `Hardware and sound` -> `Power options`
2. click on the left panel to `Choose what the power buttons does`
3. click on `Change settings that are currently unavailable`
4. check the `hibernate` checkbox below


# Sugarsync
Quick orientation in the desktop app:
- for file changes, check left menu -> `Activity`
- for deleted files, check left menu -> `Deleted Items`

## Solving sync problems
1. check if the file is updated in cloud using web browser
2. if not, check the activity log on the computer with the updated file
3. if the change is not in the log, a simple hack can help: copy the file outside SugarSync folder and back.


# Camera problem
Symptoms: the screen is blank, black, single color, in all apps and there are no problems reported in device manager
Cause: it can be caused by some external cameras (now disconnected) that are still selected in the apps using the camera. Go 
Solution: Go to the app setting and select the correct camera

# Phone app cannot see the connected cell phone
It can be due to the fucked up Windows N edition. Just install the normal edition.

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
For ssh, we can use the standard `ssh` commannd available in PowerShell (check Linux manual for more info).

However, for more features, we can use more sophisticated programs
- [KiTTY](http://www.9bis.net/kitty/index.html#!pages/Portability.md) for credentials storage, automatic reconection, etc.
- [WinSCP] for file manipulation

## KiTTY
It is best to use the portable version, so that nothing is stored in the Windows registry. Configurtation:
- [copy the PuTTY credentials](): `.\kitty_portable-0.76.1.3.exe -convert-dir`
- auto reconnect: `Connection` -> `auto reconnect on connection failure` and `auto reconnect on system wakeup`
