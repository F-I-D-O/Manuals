# Introduction
Conda and Mamba are package managers that shares the same history, principles, and partially a CLI syntax. They are:

- multi-platform
- language-agnostic
- non-destructive (unlike linux system package managers, or Windows installers)

Mamba differs from Conda in that it is faster and more memory-efficient, which can be crucial for large projects.

# Common commands

## Create a new environment
When using Conda and Mamba, we usually work with environments. By default, these package managers use the `base` environment, which is pre-created. To create a new environment, we use the `create` command:
```bash
<conda/mamba> create -n <environment name> <package names>
```


## Run a single command
To run a single command in a conda/mamba environment we use the `run` command:
```bash
<conda/mamba> run <command> <command arguments>
```

Some important parameters:

- `--no-capture-output`: By default, the output is buffered. This parameter disables the buffering and prints the output to the console immediately.


## Remove an environment
To remove an environment, we use the `remove` command:
```bash
<conda/mamba> remove -n <environment name> --all
```


# Mamba
- [Home](https://mamba.readthedocs.io/en/latest/)
- [User guide](https://mamba.readthedocs.io/en/latest/user_guide/index.html)


# Conda
- [Wiki](https://en.wikipedia.org/wiki/Conda_(package_manager))

