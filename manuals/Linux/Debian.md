# Debian

- [Wikipedia](https://en.wikipedia.org/wiki/Debian)
- [Official Website](https://www.debian.org/)
- [Official Wiki](https://wiki.debian.org/Debian)

# System Upgrade
- [Official Wiki - general tips](https://wiki.debian.org/DebianUpgrade)
- [Release Notes for Debian 13 (Trixie)](https://www.debian.org/releases/trixie/release-notes/index.en.html)
- [Release Notes for Debian 12 (Bookworm)](https://www.debian.org/releases/bookworm/amd64/release-notes/)

The instructions for upgrade are in the release notes of the version we want to upgrade to. Note that **skipping versions is not supported**, it is only safe to upgrade to the next major version.

## About Uninstalling Obsolete Packages `apt purge '~o'`
Typically, release notes advise to uninstall obsolete packages with `apt purge '~o'`. However, **this is not always safe and can lead to uninstallation of a running system kernel!** 

To be safe, first run `apt list '~o'`, and check the output. If the output contains a kernel package (e.g., `linux-image<some version>`), do not run the `apt purge '~o'` command. Instead, remove other obsolete packages one by one, or leave them installed.

## Troubleshooting
Usually, it is enough to follow the instructions in the release notes. But sometimes, problems occur, these are described in this section.

### `The repository 'http://deb.debian.org/debian <debian version>-backports Release' no longer has a Release file`
Backports are typically disabled even before the stable release end-of-life is reached. The solution is to delete the backports repository from the sources.list file.

