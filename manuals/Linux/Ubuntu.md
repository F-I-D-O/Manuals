# Usefull Comands

## Check Ubuntu Version
```bash
lsb_release -a
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
