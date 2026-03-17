[Wiki](https://en.wikipedia.org/wiki/Fedora_Linux)

# Basics
Fedora works mostly like other Linux distributions. The build in command-line text editor is `vi` not `vim`.


# Managing packages
Fedore uses the `dnf` package manager. It automatically updates the available packages, so a call like `apt get update` is not at all necessary.

To **list installed** packages:
```bash
dnf list installed
```

To **install** a package:
```bash
dnf install <package>
```

To **remove** a package:
```bash
dnf remove <package>
```

To **search** for available packages:
```bash
dnf search <package>
```

