# Introduction
Vcpkg is a package manager for C++ libraries it serves as a developement package manager rather than a system package manager.

Vcpkg can work in two modes:

- **Classic mode**: vcpkg is installed centrally. This mode is useful for development and testing.
- [**Manifest mode**](https://learn.microsoft.com/en-us/vcpkg/concepts/manifest-mode): vcpkg is installed in the project directory. This mode is useful for deployment. 

To install vcpkg:

1. clone the repo to the desired location (project directory for manifest mode, any directory for classic mode)
1. run the bootstrap script (`bootstrap-vcpkg.bat` on Windows, `bootstrap-vcpkg.sh` on Linux)
1. for classic mode, add the vcpkg directory to `PATH`, so the program can be run from anywhere
	- Beware that to run it with sudo on linux, [it is not that easy](https://docs.google.com/document/d/19CBUHtO0aUpg-kipnTrbQ3ozn_M1PiM0rH4IHoYrXS0/edit?usp=sharing).

# Basic commands

## Install a package
To install a package, use the `install <package name>` command. Important options are:

- `--triplet <triplet>`: the target triplet. 

## Remove a package
To remove a package, use the `remove <package name>` command. Important options are:

- `--triplet <triplet>`: the target triplet.

## Search for a package
To search for a package, use the `search <package name>` command. 

## List installed packages
To list the installed packages, use the `list` command. The first positional argument is the triplet filter, e.g., `list x64-windows` lists only the packages for the `x64-windows` triplet.

# CMake Integration
[documentation](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration)

By default, CMake does not see the vcpkg. To set up the appropriate enviroment variables, paths, etc., we need to run cmake commands with path to cmake toolchain file: `vcpkg/scripts/buildsystems/vcpkg.cmake`. See the IDE and command line section for the detailed instructions how to execute cmake with the path to the vcpkg toolchain file. 

The toolchain file is executed early on, so it is safe to assume that the environment will be correctly set up before the commands in yor cmake script.


# Directory Structure
vcpkg has the following directory structure:

- `buildtrees`: contains the build directories for each installed package. Each build directory contains the build logs.
- `installed`: contains the installed packages. It has subdirectories for each triplet. Each triplet directory is than divided into folloeing subdirectories:
	- `bin`: contains the shared libraries
	- `debug`: contains the debug version of everything in a similar structure as the triplet directory
	- `examples`: contains example binaries
	- `include`: contains the header files
	- `lib`: contains the static libraries
	- `share`: contains the cmake scripts and other files needed for the integration of the package into a cmake project
	- `tools`: contains the executables installed with vcpkg packages
- `ports`: Contains the package information for each package from the official vcpkg list. There is no special way how to update just the port dir, so update the whole vcpkg by `git pull` in case you need to update the list of available packages.
- `scripts`: various scripts
	- `toolchains`: cmake files that configure the toolchains. There is a special file for each platform (windows, linux, etc.)
- `triplets`: contains the triplet files.

## Modules
Vcpkg has it s own `find_package` macro in the toolchain file. It executes the script: `vcpkg/installed/<tripplet>/share/<package name>/vcpkg-cmake-wrapper.cmake`, if exists. Then, it executes the cmake scripts in that directory using the standard `find_package`, like a cmake config package.

# Triplets
[documentation](https://learn.microsoft.com/en-us/vcpkg/concepts/triplets)

Vcpkg supports installing packages built for multiple platforms and compilers in the same vcpkg installation. To do this, vcpkg uses the concept of *triplets*. A triplet is definition of target environment. Usually, the triplet defines three things:

- the target platform (e.g., x64, arm)
- the target operating system (e.g., windows, linux)
- the target compiler (e.g., msvc, gcc)

The triplet definition is stored in the triplet file in the `<vcpkg root>/triplets` directory.

## Changing the default triplet
To change the default triplet, add a new system variable `VCPKG_DEFAULT_TRIPLET`, so your default library version installed with vcpkg will be x64 (like our builds),  set it to:

- `x64-linux` for Linux Compilers
- `x64-windows` for MSVC
- `x64-MinGW` for MinGW


## Using a custom triplet
If you need to test a specific system environment with vcpkg, you can use a custom triplet.

Typically, you can **create** such a triplet by copying an existing one and modifying it. Typically, you just modify the [triplet variables](https://learn.microsoft.com/en-us/vcpkg/users/triplets) in the file.

To **use** the custom triplet add two arguments to the vcpkg command:

- `--triplet <triplet name>`: the name of the custom triplet
- `--overlay-triplets=<path to the directory containing the custom triplet>`: the path to the directory containing the custom triplet file

To **change the compiler**, it is a little bit more complicated, as there is no triplet variable for the compiler. Instead, we need to provide a custom toolchain:

1. copy an existing toolchain file from the `<vcpkg root>/scripts/toolchains`.
1. modify the toolchain file to use the desired compiler, e.g., by setting the `CMAKE_CXX_COMPILER` variable.
1. in the custom triplet file, set the `VCPKG_CHAINLOAD_TOOLCHAIN_FILE` variable to point to the custom toolchain file.

# Update

1.  `git pull`
2.  bootstrap vcpkg again
	1.  Windows: `bootstrap-vcpkg.bat`   
	2.  Linux: `bootstrap-vcpkg.sh`

# Update package

1. [Update vcpkg](#update)
2. `vcpkg update` to get a list of available updates
3. `vcpkg upgrade --no-dry-run` to actually perform the upgrade

All packages are upgraded by default. To upgrade just one package, supply the name of the package (e.g., zlib:x64-windows) as an argument to `upgrade ` command.

## Upgrade packages matching a pattern
For libraries that are divided into many interdependent packages (like boost), it is useful to upgrade all packages that match a pattern at once. Unfortunately, the `upgrade` command does not support the pattern matching. The following command can be used to upgrade all packages that match a pattern in PowerShell:
```PowerShell
vcpkg update | sls -pattern "boost-\w+" | foreach-object { vcpkg upgrade $_.Matches.Value --no-dry-run }
```

# Package Features
Some libraries have optional features, which are not installed by default, but we can install them explicitely. For example `llvm`. After `vcpkg install llvm` and typing `vcpkg search llvm`:

```
llvm                 10.0.0#6         The LLVM Compiler Infrastructure
llvm[clang]                           Build C Language Family Front-end.
llvm[clang-tools-extra]               Build Clang tools.
...
llvm[target-all]                      Build with all backends.
llvm[target-amdgpu]                   Build with AMDGPU backend.
llvm[target-arm]                      Build with ARM backend.
```
Above, we can see that there are a lot of optional targets. To install the the arm target, for example, we can use `vcpkg install llvm[target-arm]`. Sometimes, a new build of the main package is required, in that case, we need to type `vcpkg install llvm[target-arm] --recurse`.


# Package Versions
In classic mode, there is no way how to control the version of a package. For that, we have to use the manifest mode


# Making vcpkg available for all CMake projects
The cmake has no mechanism to set a default toolchain, so we cannot configure it to use vcpkg by default. The only way is to use a Shim for cmake, that calls cmake with the toolchain argument set to the vcpkg toolchain file. Such schim can be found in the [cpp dev support repository](https://github.com/F-I-D-O/cpp-dev-support).

The shim will work in most contexts, but it is still ignored in CLion, as it has its own mechanism for finding the cmake executable.
In Clion, we need to set up the path to shim as a cmake executable in the toolchain settings.


# Integrate your library to vcpkg
For complete integration of your library to vcpkg, the following steps are needed:

1. Configure and test the [*CMake installation*](CMake%20Manual.md#install)
1. Crate the port and test it locally (*vcpkg installation*)
3. Submit the port to the vcpkg repository (*publishing*) 

Resources:

- [decovar tutorial](https://decovar.dev/blog/2022/10/30/cpp-dependencies-with-vcpkg/)

## Create the Port

- [The official guide for packageing](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started-packaging)
- [Maintainer guide](https://learn.microsoft.com/en-us/vcpkg/contributing/maintainer-guide)
	- missing details from other guides
	- contains the list of deprecated functions

Vcpkg works with ports which are special directories containing all files describing a C++ package. The usuall process is:
The usual port contain these files:

- `portfile.cmake`: the main file containing the calls to cmake functions that install the package
- `vcpkg.json`: metadata file containing the package name, version, dependencies, etc.
- `usage`: a file containing the usage instructions for the package. These instructions are displayed at the end of the installation process.
	- [example](https://github.com/microsoft/vcpkg-docs/blob/main/vcpkg/examples/adding-usage.md)

A simple `portfile.cmake` can look like this:
```cmake

# download the source code
vcpkg_from_github(
	OUT_SOURCE_PATH SOURCE_PATH
	REPO <reo owner>/<repo name>
	REF <tag name>
	SHA512 <hash of the files>
	HEAD_REF <branch name>
)

# configure the source code
vcpkg_cmake_configure(
	SOURCE_PATH <path to source dir>
)

# build the source code and install it
vcpkg_cmake_install()

# fix the cmake generaed files for vcpkg
vcpkg_cmake_config_fixup(PACKAGE_NAME <package name>)

# install the license
vcpkg_install_copyright(FILE_LIST "${SOURCE_PATH}/LICENSE.txt")

# install the usage file
file(INSTALL "${CMAKE_CURRENT_LIST_DIR}/usage" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}")
```

Explanation:

- [`vcpkg_from_github`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_from_github): downloads the source code from the github repository
	- the `<path to source dir>` is the directory where the `CMakeLists.txt` file is located. It is usually the directory where the source code is downloaded, so we can set it to `${SOURCE_PATH}`
	- the `<hash of the files>` can be easily obtained by:
		1.  setting the `<hash of files> to 0
		2.  running the `vcpkg install <port name>`
		3.  copying the hash from the error message
- [`vcpkg_cmake_configure`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_cmake_configure): configures the source code using cmake (wraps the `cmake` command)
- [`vcpkg_cmake_install`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_cmake_install): builds and installs the source code (wraps the `cmake --build . --target install` command)
	- the majority of code is in the subroutine [`vcpkg_cmake_build`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_cmake_build)
	- **if we need some libraries installed with vcpkg at runtime during the build of the package, we need to use the `ADD_BIN_TO_PATH` option in the `vcpkg_cmake_install` function**. This is needed as the automatic dll copy to the output dir (`VCPKG_APPLOCAL_DEPS`) is disabelled by the `vcpkg_cmake_build` function. This option solve the problem by prepending the `PATH` environment variable with the path to the vcpkg installed libraries (`<vcpkg root>/installed/<triplet>/bin` for release and `<vcpkg root>/installed/<triplet>/debug/bin` for debug).
- [`vcpkg_cmake_config_fixup`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_cmake_config_fixup): fixes the cmake generated files for vcpkg. This is needed because the cmake generated files are not compatible with vcpkg. The function fixes the `CMakeConfig.cmake` and `CMakeConfigVersion.cmake` files.
	- the `<package name>` is the name of the package, usually the same as the port name
- [`vcpkg_install_copyright`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_install_copyright) installs the license files listed in the `FILE_LIST` argument to `share/<port name>/copyright` file. The `copyright` file is obligatory for the package to be accepted to the vcpkg repository.


The `vcpkg.json` file can look like this:
```json
{
	{
    "name": "fconfig",
    "version-string": "0.1.0",
    "description": "C++ implementation of the fconfig configuration system",
    "homepage": "https://github.com/F-I-D-O/Future-Config",
	"license": "MIT",
    "dependencies": [
        {
            "name" : "vcpkg-cmake",
            "host" : true
        },
        "yaml-cpp",
        "spdlog",
        "inja"
    ]
}
}
```
Here:

- the `license` key is obligatory and has to match the license file of the package
- The dependencies with the `host` key set to `true` are the dependencies that are required for the build, but not for the runtime. 

### Variables and Functions available in the portfile.cmake
The variables and functions available in the `portfile.cmake` are described in the [create command documentation](https://learn.microsoft.com/en-us/vcpkg/commands/create). The most important variables are:

- `CURRENT_PACKAGES_DIR`: the directory where the package is installed: `<vcpkg root>/installed/<triplet>/<port name>`


## Installation
To install the port locally, run:
```bash
vcpkg install <port name>
```

For this command to work, the port has to be located in `<vcpkg root>/ports/<port name>`. If we want to install the port from an alternative location, we can use the `--overlay-ports` option.  For example, if we have the port stored in the `C:/custom_ports/our_new_port` directory, we can install it by:
```bash
vcpkg install our_new_port --overlay-ports=C:/custom_ports
```

If the port installation is failing and the reason is not clear from stdout, check the logs located in `<vcpkg root>/buildtrees/<port name>/`


### Reinistallation after changes
During testing, we can reach a scenario where a) we successfully installed the port, b) we need to make some changes. In this case, we need to reinstall the port. However, it is not completely straightforward due to [binary caching](https://learn.microsoft.com/en-us/vcpkg/consume/binary-caching-default). The following steps are needed to reinstall the port:

1. uninstall the port: `vcpkg remove <port name>`
2. disable the binary cache by setting the [`VCPKG_BINARY_SOURCES`](https://learn.microsoft.com/en-us/vcpkg/reference/binarycaching) environment variable to `clear`
	- in PowerShell: `$env:VCPKG_BINARY_SOURCES = "clear"`
	- in bash: `export VCPKG_BINARY_SOURCES=clear`
	- if setting the environment variable does not work (WSL), we can specify the `--binarysource=clear` option in the next step
1. install the port again: `vcpkg install <port name>`




### Executable installation
In general vcpgk does not allow to install executables, as it is a dependency manager rather than a package manager for OS. However, it is possible to install executables that are intedned to be used as tools (to the `installed/<triplet>/tools` directory) used in the build process. To do so, you have to add the [`vcpgk_copy_tools`](https://learn.microsoft.com/en-us/vcpkg/maintainers/functions/vcpkg_copy_tools) call to the `portfile.cmake` file:
```cmake
vcpkg_copy_tools(
	TOOL_NAMES <tool target name>
	AUTO_CLEAN
)
```
The `AUTO_CLEAN` option ensures that the tools are deleted from the `bin` directory. Without it the tools will be kept in the `bin` directory, resulting in warnings and non-complicance with the vcpkg rules.

The `vcpgk_copy_tools` function also automatically copies the runtime dependencies of the tools to the `tools` directory. 


### Executing installed tools from cmake
The installed tools can be executed from cmake using cmake comands specified in the [CMake manual](CMake%20Manual.md#executing-external-commands). 

To specify the path to the tools directory, use the [`VCPKG_INSTALLED_DIR`](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration#vcpkg_installed_dir) and [`VCPKG_TARGET_TRIPLET`](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration#vcpkg_target_triplet) variables:
```cmake
execute_process(
	COMMAND ${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/tools/${PROJECT_NAME}/<tool name>
)
```

## Publishing
[official guide](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started-adding-to-registry)

Before publishing the port, we should check for the following:

- all dependencies in `CMakelists.txt` are required (`find_package(<package name> REQUIRED)`) **and** listed in the `vcpkg.json` file in the `dependencies` array
- the port follows the [maintainer guide](https://github.com/microsoft/vcpkg-docs/blob/main/vcpkg/contributing/maintainer-guide.md), especially:
	- the port name does not clash with existing packages (check at [repology](https://repology.org/))
	- the port should work for both Windows and Linux and on both platforms, the port should support both static and dynamic linking.
- the [PR checklist](https://learn.microsoft.com/en-us/vcpkg/contributing/pr-review-checklist) is followed

Then, the submission process is as follows (The *emphezised* steps are not needed in case of fixing a failed release, i.e., when the release was rejected by vcpkg):

1. *create a fork of the vcpkg repository*
1. commit and push the changes to the project repository if not done yet
1. create or replace a release in the projects GitHub repository
1. update the verison in the `vcpkg_from_github` call in `portfile.cmake`
1. update the version in the `vcpkg.json` file
1. pull from the vcpgk fork repository
1. copy the port (`portfile.cmake`, `vcpkg.json` and `usage`) to the vcpkg repository
1. remove the local `SOURCE_PATH` overrides and uncomment the `vcpkg_from_github` call
1. in portfile, assign the correct hash to the `vcpkg_from_github` call
1. test the port installation locally without the `--overlay-ports` option
1. format the `vcpkg.json` file using the `vcpkg format-manifest <path to the vcpkg.json file>` command
1. *create a new branch for the package*
1. commit the changes to the package branch in the vcpkg repository
1. update the port version using the `vcpkg x-add-version <port name>` command
1. commit again to the package branch in the vcpkg repository
1. push the branch to the forked vcpkg repository
1. *open the forked repository in the browser and create a new pull request to the main vcpkg repository*

