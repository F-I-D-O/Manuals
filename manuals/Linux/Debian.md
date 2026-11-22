# Debian

- [Wikipedia](https://en.wikipedia.org/wiki/Debian)
- [Official Website](https://www.debian.org/)
- [Official Wiki](https://wiki.debian.org/Debian)

This manual describes tool specific to Debian-based Linux distributions (Debian, Ubuntu, Mint, etc.). A manual specific to each distribution (e.g., [Ubuntu Manual](./Ubuntu.md)) may provide additional details and instructions tailored to that distribution.

# Users
[`adduser` Reference](https://manpages.debian.org/trixie/adduser/adduser.8.en.html)

On top of low-level commands like `useradd` and `usermod`, Debian provides an interactive Perl script `adduser` for adding new users to the system. In one step, it

- creates a new user with a specified username and group
- sets up the home directory for the new user
- prompts for a password
- creates a primary group for the user (group with the same name as the username)
- and more

The default configuration for this script is in `/etc/adduser.conf`. The basic syntax is

```bash
adduser <username>
```

Important parameters:

- [`--disabled-password`](https://manpages.debian.org/trixie/adduser/adduser.8.en.html#disabled~2): create the user without setting a password, i.e., with the password authentication disabled.
- `--gecos "<GECOS>"`: supply the content of the [GECOS field](https://en.wikipedia.org/wiki/Gecos_field). If skipped, the command will ask for the GECOS content interactively.
- `--shell <shell>`: The shell to be used by the user. If skipped, the default shell is used. This can be used to create a user without a shell by setting the shell to `/usr/sbin/nologin`.

Note that the `adduser` needs to be run as root. Otherwise it will fail with `bash: adduser: command not found`.


# System Upgrade

- [Official Wiki - general tips](https://wiki.debian.org/DebianUpgrade)
- [Release Notes for Debian 13 (Trixie)](https://www.debian.org/releases/trixie/release-notes/index.en.html)
- [Release Notes for Debian 12 (Bookworm)](https://www.debian.org/releases/bookworm/amd64/release-notes/)

The instructions for upgrade are in the release notes of the version we want to upgrade to. Note that **skipping versions is not supported**, it is only safe to upgrade to the next major version.

## About Uninstalling Obsolete Packages `apt purge '~o'`
Typically, release notes advise to uninstall obsolete packages with `apt purge '~o'`. However, **this is typically safe and can lead to uninstallation of important software, including the running system kernel!** 

To be safe, first run `apt list '~o'`, and check the output. If the output contains

- a kernel package (e.g., `linux-image<some version>`), or,
- any software that looks familiar (ssh, database, java, ...)

do not run the `apt purge '~o'` command. Instead, inspect and remove other obsolete packages one by one, or leave them installed.


## Backing up leftover configuration files
Instructions sometimes mention to delete leftover configuration files (and specify a `find` command to do so). If we want to back up them, we can use the following command:

```bash
sudo find /etc -name '*.dpkg-*' -o -name '*.ucf-*' -o -name '*.merge-error' | while IFS= read -r f; do
    base=${f##*/}
    sudo mv -- "$f" "$HOME/config_backups-bookworm/$base"
done
```

## System Reboot
Even when the system kernel is updated, we are still booted in the old one. So the upgrade is not complete until we reboot the system. 

The procedure is usually safe, but it is better to make some checks before rebooting.

1. check the current kernel: `uname -r`
1. check that we really have a new kernel image to boot to: `dpkg -l 'linux-image*' | grep '^ii'`
    - we should see the newer kernel image.
1. check that the new image is in GRUB: `grep "menuentry '" /boot/grub/grub.cfg`
1. check image entries (both should be present for the new kernel):
    - `ls -lh /boot/initrd.img*`
    - `ls -lh /boot/vmlinuz*`
1. update GRUB and initramfs:
    - `sudo update-grub`
    - `sudo update-initramfs -u -k all`
    - there should be no errors
1. check that there is enough disk space: `df -h`
1. check ssh status: `systemctl status ssh --no-pager` - should be active
1. check recent ssh problems: `journalctl -u ssh -b --no-pager | tail -n 50`

If everything seems to be in order, we can reboot the system: `sudo reboot`.


## Troubleshooting
Usually, it is enough to follow the instructions in the release notes. But sometimes, problems occur, these are described in this section.

### `The repository 'http://deb.debian.org/debian <debian version>-backports Release' no longer has a Release file`
Backports are typically disabled even before the stable release end-of-life is reached. The solution is to delete the backports repository from the sources.list file.

