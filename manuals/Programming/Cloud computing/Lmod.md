
Lmod is a module system that simplify the package management on the Linux cloud computing clusters. It is used on the RCI cluster.

- [home](https://lmod.readthedocs.io/en/latest/)
- [user guide](https://lmod.readthedocs.io/en/latest/010_user.html)
- [RCI cluster documentation](https://login.rci.cvut.cz/wiki/modules)

# `module` (`ml`) command
The `module` performs different operations based on its first argument. The default operation (if the first/main argument is omited) is `load`.

- `load <module name>`: loads the module. Specific version can be used by adding `/` and the version number. If the version is not specified, the latest version is loaded. 
- `list`: lists all loaded modules