# Managing packages with APT

- [Wikipedia](https://en.wikipedia.org/wiki/APT_(software))
- [Debian Wiki](https://wiki.debian.org/Apt)
- [`apt` command reference](https://manpages.debian.org/latest/apt/apt.8.en.html)
- [`apt-get` command reference](https://manpages.debian.org/latest/apt-get/apt-get.8.en.html)


In Debian-based distributions, we can manage packages using APT package manager, typically in the `sudo` context.

There are two main commands:

- [`apt`](https://manpages.debian.org/latest/apt/apt.8.en.html): the main command, best for manual use
    - Not that the `apt` reference is only brief, as it shares most of the CLI with `apt-get`.
- [`apt-get`](https://manpages.debian.org/latest/apt-get/apt-get.8.en.html): the legacy command, best for automated use as the output is more consistent between different versions

The most used **subcommands** are:
- **update the list** of possible updates: `sudo apt update`
- **perform the update**: 
    - `sudo apt upgrade`: safe upgrade, does not remove any packages
    - `sudo apt full-upgrade`: full upgrade, removes packages if they block the upgrade (this used to be called `dist-upgrade`)
- **list installed** packages: `apt list --installed`
- **remove** a package: 
	- `apt remove <package>`: remove the package 
	- `apt purge <package>`: remove the package and its configuration
    - `apt autoremove`: remove packages that a) were installed as dependencies, not manually, and b) are no longer needed by any other package. 
        - Usually safe, but better to check the list whether we do not use any of the removed packages explicitly.
- **install** a package: `sudo apt install <package>`
- **find the install location** of a package: `dpkg -L <package>`
	- unfortunately, it is not possible to easily search for the user who installed the package.
- **search** for a package: `apt-cache search <package>`

The repositories for the packages are defined in the `/etc/apt/sources.list` file. Typically, we need to edit this file during the system upgrade process, or when we want to install a package from an alternative repository.

The most used **options** are:
- `-s`, `--simulate`: simulate the command, do not perform the actual action


## Analyzing installed packages

To see the info about an installed package, including the version, run `dpkg -s <package>`.


## Package repository configuration (`/etc/apt/sources.list`)
[Debian Wiki](https://wiki.debian.org/SourcesList)

The package repository configuration follows the typical uniz format:

- main configuration file: `/etc/apt/sources.list`. Should be edited if:
    - upgrading the system to a newer version, or
    - using an alternative mirror for better download speed (see [Finding the fastest package repository](#finding-the-fastest-package-repository))
- additional configuration files: `/etc/apt/sources.list.d/*.list`. This is typically used to add additional repositories for specific software.

We can edit the `source.list` file manually, however, to prevent the mistakes, it is better to use a dedicated python script: [`apt-mirror-updater`](https://apt-mirror-updater.readthedocs.io/en/latest/readme.html). Steps:

1. install the python script: `sudo pipx install apt-mirror-updater`
1. backup the old file: `cp sources.list sources.list.bak`
1. change the mirror with the script: `apt-mirror-updater -c <mirror URL>`

Note that the `apt-mirror-updater` script can also measure the bandwidth, however, the result does not seem to be reliable.


### Installing non-stable package versions
On Linux, the stable package versions are usually outdated, sometimes years behind the current version. To install the newer version, we have usually a few options:

- **upgrade the system**: if we use an old version of the system, we can check whether the newer version is available that includes the newer package version. For more, see the Upgrade section for the specific distribution.
- **install from source**: We can manually build the package from the source and install it. See the [C++ Workflow](../Programming/C++/C++%20Workflow.md) for more.
- **install package from an alternative repository**: We can add an alternative repository to the system and install the package from there.

The first two options are covered in different part of this manual. Here, we focus on the third option.

To use an alternative repository, we have to 

1. add the repository to the system, which is a one time task
2. install the specific package from the repository

To **add a repository**, we have to:

1. add the repository to the `/etc/apt/sources.list` (or to a separate file in the `/etc/apt/sources.list.d/` directory). Each repository should has the line that should be added to the file on its website.
2. `sudo apt update` to update the list of available packages

To **install a package from the repository**:
```bash
sudo apt install -t <repository> <package>
```

#### Some useful repositories

- [debian backports](https://backports.debian.org/Instructions/): the repository with the newer versions of the packages for the stable Debian version


### Finding the fastest package repository
If the downolad speed is not satisfactory, we can change the repositories. To find the fastest repository from the list of nearby repositories, run:
```bash
curl -s http://mirrors.ubuntu.com/mirrors.txt | xargs -n1 -I {} sh -c 'echo `curl -r 0-10240000 -s -w %{speed_download} -o /dev/null {}/ls-lR.gz` {}' | sort -g -r
```

The number in the leftmost column indicates the bandwidth in bytes (larger number is better).




## Possible issues

### `The repository '<repo>' no longer has a Release file`
This can happen when the repository is outdated, which can happen quickly if we use non-stable (non-LTS) versions of OS. The solution is to either:

- change the repository to a newer one manually or
- change the url of all repositories to `http://old-releases.ubuntu.com/ubuntu/` and then upgrade the system to the newer version:
	```bash
	sudo sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
	```