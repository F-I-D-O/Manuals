# Dev Stack
I use the following stack:
-  the latest Python, 64 bit
-  pip as the package manager
-  Pycharm IDE
-  pytest test suite
-  Visual Studio for deugging native code


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


# Installing Packages
Normal packages are installed using: pip install `<package name>`.

However, if a package uses a C/C++ backend and does not contain the compiled wheel on PyPy, this approach will fail on Windows. Instead, you have to download the wheel from [the Chris Gohlke page](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and install it: `pip install <path to wheel>`. Also, you have to install the dependencies mentioned on that page.

## Troubleshooting
If the installation fails, check the following:
1.  if you installed the package by name, check for the wheel on the Chris Golthke page.
2.  if you installed the package from a wheel, check the notes/requirement info on Chris Golthke page
3.  Check the log. Specifically, no building should appear there whatsoever. If a build starts, it means that some dependency that should be installed as a prebuild wheel is missing. Possible reasons:
	1.  you forget to install the dependency, go back to step 2
	2.  the dependency version does not correspond with the version required by the package you are installing. Check the log for the required version.

# Pycharm
## Configuration
### Settings synchronization
Same as in IDEA:
1. Log in into JetBrains Toolbox or to the App
1. Click on the gear icon on the top-right and choose Sync
1. Check all categories and click on pull settings from the cloud

### Do Not Run scripts in Python Console by Default
`Run configuration select box` -> `Edit Configurations...` -> `Edit configuration templates` -> `Python` -> uncheck the `Run with Python Console`

### Enable Progress Bars in output console
`Run configuration select box` -> `Edit Configurations...` -> Select the configuration -> check the `Emulate terminal in output console`

## Project Configuration
- configure the correct test suite in `File` -> `Settings` -> `Tools` -> `Python Integrated Tools` -> `testing`

## Known problems & solutions

### Non deterministic output in the run window
Problem: It can happen that the output printing/logging can be reordered randomly (not matching the order of calls in the source, neither the system console output).
Solution: `Edit Configurations...` -> select configuration for the script -> check `Emulate terminal in output console`.


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
- `Ctrl` + `-`: split cell


## Web Browser Configuration
### Install Extension Manager with basic extensions
Best use the [official installation guide](https://github.com/ipython-contrib/jupyter_contrib_nbextensions). The extensions then can be toggled on in the Nbextensions tab in the jupyter homepage. Be sure to unselect the *disable configuration for nbextensions without explicit compatibility (they may break your notebook environment, but can be useful to show for nbextension development)* checkbox, otherwise, all extensions will be disabled.

# Debugging
Pycharm contains a good debuger for python code. However, it cannot step into most standard library functions, as those are native, implemented in C/C++. For that, we need mixed python/native debugging.

# Testing
To run pytest, simply go to the folder and run `pytest`. Arguments:
- `-x`: stop on first failure

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
