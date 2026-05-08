# Usefull Comands

## Check Ubuntu Version
```bash
lsb_release -a
```

# Managing packages
In Debian-based distributions, we can manage packages using the `apt` command, typically in the `sudo` context.

- **update the list** of possible updates: `sudo apt update`
- **perform the update**: `sudo apt upgrade`
- **list installed** packages: `apt list --installed`
- **remove** a package: `sudo apt remove <package>`
- **install** a package: `sudo apt install <package>`
- **find the install location** of a package: `dpkg -L <package>`
	- unfortunately, it is not possible to easily search for the user who installed the package.
- **search** for a package: `apt-cache search <package>`

The repositories for the packages are defined in the `/etc/apt/sources.list` file. Typically, we need to edit this file during the system upgrade process, or when we want to install a package from an alternative repository.


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
This can happen when the repository is outdated, which can happen quickly if we use non-stable (non-LTS) versions of OS. The solution is to either:

- change the repository to a newer one manually or
- change the url of all repositories to `http://old-releases.ubuntu.com/ubuntu/` and then upgrade the system to the newer version:
	```bash
	sudo sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
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
