# Dev Stack
I use the following stack:

- the latest Python, 64 bit
- pip as the package manager
- Pycharm IDE
- pytest test suite
- Visual Studio for deugging native code


# Python
Python should be installed from the [official web page](https://www.python.org/), not using any package manager. Steps:

1. Dowload the 64-bit installer
2. Run the installer, choose advanced install
	- Include the GUI tools (Tkinter, TK)
	- Includ	`*.py` launcher, but **only if** there is no newer python version installed. If this is checked and there is a newer vesrsion of Python installed, the setup will fail.
	- Include documentation
	- Check download debug symbols to enable native code debugging

The source code for python can be inspected on [GitHub](https://github.com/python/cpython)


## Command line
We execute python scripts from the command line as: `python <path to the .py file>`.

Parameters:

- `-m` executes a module as a script, e.g. `python -m venv`. This is useful for executing scripts whithout knowing the path to the script.


# pip
[official documentation](https://pip.pypa.io/en/stable/)

## Installing Packages
Normal packages are installed using: `pip install <package name>`.

However, if a package uses a C/C++ backend and does not contain the compiled wheel on PyPy, this approach may fail on Windows. Instead, you have to download the wheel from [the Chris Gohlke page](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and install it: `pip install <path to wheel>`. Also, you have to install the dependencies mentioned on that page.


### Troubleshooting package installation
If the installation fails, check the following:

1.  if you installed the package by name, check for the wheel on the Chris Golthke page.
2.  if you installed the package from a wheel, check the notes/requirement info on Chris Golthke page
3.  Check the log. Specifically, no building should appear there whatsoever. If a build starts, it means that some dependency that should be installed as a prebuild wheel is missing. Possible reasons:
	1.  you forget to install the dependency, go back to step 2
	2.  the dependency version does not correspond with the version required by the package you are installing. Check the log for the required version.


## Uninstalling packages
To uninstall a package, use `pip uninstall <package name>`.

There is no way how to uninstall more packages using some wildcard. To uninstall more packages efficiently (not one by one):

1.  create a file with the list of all installed packages: `pip freeze > packages.txt`
2.  edit the file and remove all packages you want to keep
3.  uninstall all packages from the file: `pip uninstall -r packages.txt -y`





## Upgrading pip
To upgrade pip, use `python -m pip install --upgrade pip`. Sometimes, this command end ith an error. There can be specific solutions to this, but what always seems to fix the pip is the [get-pip script](https://bootstrap.pypa.io/get-pip.py). Download the script and run it using `python get-pip.py`.


## Local packages
[official documentation](https://pip.pypa.io/en/stable/topics/local-project-installs/)



Instead of installing from a repository, we can install from a local package. There are two ways how to do this:

- editable install: `pip install -e <path to the package>`. This way, we can update the package and the changes are immediately reflected in the code that uses the package.
- regular install: `pip install <path to the package>`. Normall install which takes files from the specified local directory.

Note that the package needs to be properly initialized first, i.e.:

- at least one `__init__.py` file in the package root (optionally others in subpackages)
- a `setup.py` file in the parent directory of the package root


### Editable install
[official documentation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html)

A useful method how to develop and test packages is to have them installed in editable (development) mode. This way, each change in the source code is immediately reflected in the package and also in the code that uses the package. 

To install a package in development mode, use `pip install -e <path to the package>`.

Instead of installing the package into the package folder inside the python installation folder (typically `<Python installation folder>/Lib/site-packages`), the editable install leaves the package folder almost empty (only some metadata files are present), and creates special files in the python installation folder:

- `<Python installation folder>/__editable__.<package name>-<version>.pth`: Contains name of the package finder and the function that should be called.
- `<Python installation folder>/__editable__<package name>_<version>_finder.py`: Contains the code that should be executed to find the package.
	- most important is the `MAPPING` dictionary that contains all the paths to the package files.

Note that the **editable package works correctly only if**:

- the root folder of the package stays the same as the one used for the installation
- the package configuration in `setup.py` stays the same as the one used for the installation

If any of these conditions is not met, we need to reinstall the package.


# IDE

## Pycharm

### Configuration

#### Settings synchronization
Same as in IDEA:

1. Log in into JetBrains Toolbox or to the App
1. Click on the gear icon on the top-right and choose Sync
1. Check all categories and click on pull settings from the cloud

#### Do Not Run scripts in Python Console by Default
`Run configuration select box` -> `Edit Configurations...` -> `Edit configuration templates` -> `Python` -> uncheck the `Run with Python Console`

#### Enable Progress Bars in output console
`Run configuration select box` -> `Edit Configurations...` -> Select the configuration -> check the `Emulate terminal in output console`


#### Setup the Docstring format
In `Tools` -> `Python Integrated Tools` -> `Docstring format`.


### Project Configuration

- configure the correct test suite in `File` -> `Settings` -> `Tools` -> `Python Integrated Tools` -> `testing`

### Known problems & solutions

#### Non deterministic output in the run window
Problem: It can happen that the output printing/logging can be reordered randomly (not matching the order of calls in the source, neither the system console output).
Solution: `Edit Configurations...` -> select configuration for the script -> check `Emulate terminal in output console`.


#### Pycharm does not recognize a locally installed package
It can happen that a locally installed package (`-e`) is not recognized by Pycharm. If that happens, first try to invalidate the cache by

1. `File` -> `Invalidate Caches...`
1. check `Clear file system cache and Local History`
1. click `Invalidate and Restart`

If this does not work, it can be solved by adding the path to the package to the interpreter paths:

1. `File` -> `Settings` -> `Python` -> `Interpreter`
1. Click on the arrow next to the interpreter name and choose `Show All...`
1. Click on the desired interpreter and click on the filetree icon on the top of the window
1. Add the path to the package to the list of paths


#### No problems found in the code of a single project
This can be due to a broken Idea settings. To fix:

1. Close Pycharm
1. Move the `.idea` folder from the project directory to a backup location
1. Start Pycharm and open the project again


## VS Code

### Formatting
For formatting, we can use the [`black`](https://github.com/psf/black) formatter. To install it:

1. `pip install black`
1. install the `black` extension in VS Code

### Code Analysis
The code analysis in VS Code is provided by the language server. The language server can be configured the settings is `python.languageServer`.

By default, the language server is set to [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

## Cursor
In this section we provide the differences between Cursor and VS Code workflow, and also the limitations of Cursor for Python development.

### Limitations
The main limitation is the static analysis tool. The cursor uses a built-in static analysis tool that is a fork of the [basedpyright](https://docs.basedpyright.com/latest/) [[source]](https://forum.cursor.com/t/cursor-pyright-python-extension-information/92522/9?u=david_fiedler). This tool have some limitations compared to Pylance or the code analysis available in Pycharm, and cannot be replaced (the classical VS Code setting `python.languageServer` is reverted to None on restart). A typical example is an object returned from a function. In Cursor, this object, when type hints are missing, is declared as `Any`, and its members cannot be accessed, searched or renamed.


# Project Structure
A typical project structure is:

```plaintext
<project root>/
├── src/
│  ├── <package name>
|      ├── __init__.py
|      ├── <module files>
|      ├── resources/
|      |   ├── <resource files for main module>
|      ├── <submodule>/
|          ├── __init__.py
|          ├── <submodule files>
|          ├── resources/
|              ├── <resource files for submodule>
├── tests/
│   ├── <test files>
|   ├── resources/
|       ├── <resource files for tests>
├── docs/
|   ├──<documentation files>
├── setup.py
├── README.md
```

Sometimes, we skip the `src` directory and put the package directly into the project root. This is typical for projects with a single package.

# Jupyter
Jupyter can be used both in Pycharm and in a web browser.

## Jupyter in Pycharm
The key for the effectivity of Jupyter in Pycharm is using the *command mode*. To enter the command mode, press `Esc`. To enter the edit mode, pres enter.

### Command mode shortcuts

- `m`: change cell type to markdown
- `Ctrl` + `C`: copy cell
- `Ctrl` + `V`: paste cell
- `Ctrl` + `Shift` + `Up`: move cell up
- `Ctrl` + `Shift` + `Down`: move cell down

Text mode shortcuts:

- `Ctrl` + `Shift` + `-`: split cell on cursor position


## Web Browser Configuration

### Install Extension Manager with basic extensions
Best use the [official installation guide](https://github.com/ipython-contrib/jupyter_contrib_nbextensions). The extensions then can be toggled on in the Nbextensions tab in the jupyter homepage. Be sure to unselect the *disable configuration for nbextensions without explicit compatibility (they may break your notebook environment, but can be useful to show for nbextension development)* checkbox, otherwise, all extensions will be disabled.


## Jupyter in VS Code
[Documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

To **move a cell** just use drag and drop, on the left side of the cell.



# Debugging
Pycharm contains a good debuger for python code. However, it cannot step into most standard library functions, as those are native, implemented in C/C++. For that, we need mixed python/native debugging.

# Testing

## Pycharm Configuration
By default, all exceptions are handled by test frameworks, and therefore, the debugger does not stop on them. To stop on exceptions in test, we need to edit the breakpoint configuration -> `Activation policy` :

- check `On raise`
- check `Ignore library files`

## Pytest
To run pytest, simply go to the folder and run `pytest`. Arguments:

- `-x`: stop on first failure

For mocking, we need to install the `pytest-mock` package, otherwise we get an error `fixture 'mocker' not found`.


# Mixed Python-native debugging
In theory, there are two ways how to debug python native code:

- use a tool that can step from python to C++ (only Visual Studio offers this possibility AFAIK)
- use two debuggers, start with a python debugger, and attach a native debugger to the python process. This way, the debuggers can be independent. However, one needs to put a breakpoint in the native code, and for that, we need to know the location of the code that will be executed from python (non-trivial for standard library)

## Python-native debugger in Visual Studio
First check and install the requirements:

- Python 3.5-3.9, including debugging symbols
	- Python 3.10 is not compatible yet
- in Visual Studio, a Python development component needs to be installed, including *Python native development tools*

Then, configure the Visual studio:

- Go to `Tools` -> `Options` -> `Python` -> `Debugging` and check: *Enable debugging of the Python standard library*.

Finally, create a new Python project (either clean, or from existing code) and configure it:

- use the interpreter directly, do not create a virtual environment
- enable native code debugging:
	1. Go to project properties -> `Debug`
	2. Check enable native code debugging
- use the `-i ` flag to always see the debug console, even if the program ends without breaking
	1. Go to project properties -> `Debug`
	2. Add the `-i` flag to the `Interpreter Arguments` field

### Known issues
*The reference assemblies for .NETFramework,Version=v4.7.2 were not found.* -> Install this component using the visual studio installer


### Other Sources
[Microsoft official documentation](https://docs.microsoft.com/en-us/visualstudio/python/debugging-mixed-mode-c-cpp-python-in-visual-studio?view=vs-2022)
[Python tools for Visual Studio GitHub page](https://github.com/microsoft/PTVS)


# Distribution
In the past, the python packaging was determined by the packiging tool used. However, now it is standardized

To turn a project into a setuptools package:

- create a root package folder named `<package name>` with an `__init__.py` file,
- create a `pyproject.toml` file in the same folder where the root package folder is.

## `pyproject.toml`

- [Official Python Specification](https://peps.python.org/pep-0621/)
- [Official Python Documentation](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [setuptools documentation](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

The `pyproject.toml` is now a standard Python way to provide a project metadata. It is also the recommended configuration format for setuptools.

There are three standardized `pyproject.toml` sections (tables):

- `[build-system]`: sets the toolchain to build the package. Strongly recommended.
- `[project]`: contains the project metadata. This is the section most builders will use to configure the build.
- `[tool]`: for configuration of specific tools like mypy

### `[build-system]`
[Official documentation](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#declaring-the-build-backend)

The build system section contains only two parameters:

- `requires`: a list of dependencies required to build the package.
- `build-backend`: the backend to use to build the package.

Typically, we fill both parameters according to the builder documentation. Below are examples for the most common builders:

- **setuptools**: 
	```toml
	requires = ["setuptools"]
	build-backend = "setuptools.build_meta"
	```

### `[project]`
The project section contains the project metadata used by the builders. 

Some builders support automatic filling of certain parameters. These should be listed under the `dynamic` parameter, e.g.:
```toml
dynamic = ["version"]
```

The fields recognized by most builders are:

- [`name`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#name): the name of the package

## Configuration files
There are three configuration file formats:

- `setup.py` (legacy, original procedural approach)
- `pyproject.toml` (recommended)
- `setup.cfg` (legacy, INI format)

Each of the formats has a very similar underlying model (set of setup parameters). Most of the setup parameters are optional, but most of the time, we provide at least these:

- [`name`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#name): the name of the package. Required, and cannot be dynamic.
- [`version`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#version): the version of the package. Required, and can be dynamic.
- [`dependencies`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#dependencies): the runtime dependencies of the package. Listed as a TOML array.
- [`python-requires`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#python-requires): the minimum Python version required to use the package.
- [`authors`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#authors-maintainers): the authors of the package. Listed as an array of objects with each object having a `name` (required) and `email` field.




### `setup.py`
The `setup.py` typically looks like this:

```Python
from setuptools import setup

setup(
    <setup parameters>
)
```


## Releasing a new version

1. [licensing](../Common.md#licenses)
2. check that setup.py contains all requirements: `pipreqs`
3. release to PyPi (see [Releasing libraries to PyPi](#releasing-libraries-to-pypi))
4. update the min version in dependencies

### Releasing libraries to PyPi

1. raise version in `setup.py`
2. run `sdist`
	- in Pycharm: `Tools` -> `Run setup.py task` -> `sdist`
3. upload to pypi: `twine upload dist/*`
