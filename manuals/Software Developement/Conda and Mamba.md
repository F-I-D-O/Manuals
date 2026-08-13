# Introduction
Conda and Mamba are package managers that shares the same history, principles, and partially a CLI syntax. They are:

- multi-platform
- language-agnostic
- non-destructive (unlike linux system package managers, or Windows installers)

Mamba differs from Conda in that it is faster and more memory-efficient, which can be crucial for large projects.



# Installation and Initialization

## Windows

1. Download and Install [Miniforge](https://github.com/conda-forge/miniforge)
    - On windows, the best way to install Conda and Mamba is to install Miniforge. It is basivally an installation of Conda and Mamba together with some initialization scripts set up so that  it uses the conda-forge repository instead of the default conda repository.
2. Open the Miniforge Terminal from the start menu and run `conda init`: 
    - After the installation, we can ony use conda and mamba commands using a special terminal shortcut installed to start menu. We can enable the use of conda and mamba commands in PowerShell profile by running the `conda init` in this terminal.
3. Open new terminal Window with PowerShell and run `conda auto_activate false`
    - This will disable the automatic activation of the conda environment when the terminal is opened. Auto activation in PowerShell is dangerous, as this puts many conda executables early in the PATH, which can override the system executables (e.g., git, cmake)

## Linux
On linux, we have several options to install Conda and Mamba:

- install [Miniforge](https://github.com/conda-forge/miniforge) using the instructions on the website
- install mamba using the system package manager. Note that this typically installs micromamba, so:
    - only mamba executables are available, no conda
    - default environment location have to be set up using environment variables, as the installation defaults to `/envs`.


## Set up the environment root directory
Sometimes, we may want to change the default environment root directory. For this, we change the following environment variables:

- `CONDA_ROOT_PREFIX`: for conda
- `MAMBA_ROOT_PREFIX`: for mamba
- `MICROMAMBA_ROOT_PREFIX`: for micromamba

# Environments
Conda and Mamba use environments similar to virtual environments of pip. By default, these package managers use the `base` environment, which is pre-created. However, unlike with pip, **mamba discurages the use of the default (base) environment**.

Typically, commands can be run with the `-n <environment name>` parameter to specify the environment. If no environment is specified, the active environment is used.

To **create a new environment**, we use the `create` command:
```bash
<conda/mamba> create -n <environment name> <package names>
```

To **remove an environment**, we use the `remove` command:
```bash
<conda/mamba> remove -n <environment name> --all
```

# Packages
Packages in Conda and Mamba are similar to packages in pip, but they are not limited to Python. 


To **list the packages in an environment**, we use the `list` command:
```bash
<conda/mamba> list -n <environment name>
```

To **install a package into an environment**, we use the `install` command:
```bash
<conda/mamba> install -n <environment name> <package name>
```

If the package is not available in the conda-forge but in in PyPI, we can install it from PyPI using the `pip` command like we used to do normally. If we are in a conda/mamba environment, the conda/mamba pip will be used instead of the system pip. Usually, it is the best to install all the dependencies first to minimize the number of packages that need to be installed from PyPI instead of conda-forge.



# Other commands

## Run a single command
To run a single command in a conda/mamba environment we use the `run` command:
```bash
<conda/mamba> run <command> <command arguments>
```

Some important parameters:

- `--no-capture-output`: By default, the output is buffered. This parameter disables the buffering and prints the output to the console immediately.





# Mamba
- [Home](https://mamba.readthedocs.io/en/latest/)
- [User guide](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html)



# Conda
- [Wiki](https://en.wikipedia.org/wiki/Conda_(package_manager))

