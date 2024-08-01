# Introduction
CMake is 
- a cross-platform build system generator that generates build scripts for various build systems (e.g., make, ninja, Visual Studio, Xcode)
- a name of the language used to write the configuration files for the build system generator and other related scripts.

CMake can run in two modes:
- **project mode**: is the standard mode. This mode is used when the project is configured using the `cmake` command. Therefore, the `CMakeLists.txt` file is executed in this mode.
- **script mode**: is used when the `cmake` command is run with the `-P` option. In this mode, the `CMakeLists.txt` file is not executed, but the script specified by the `-P` option is executed.

Main resources:
- [CMake documentation](https://cmake.org/cmake/help/latest/index.html)
- [CMake tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)

## Generators
CMake not only supports multiple platforms but also multiple build systems on each platform. These build systems are called *generators*. To get a list of available generators, run:
```bash
cmake -E capabilities
``` 


# Commands
## Configuration: Generating Build scripts
General syntax is:
```bash
cmake <dir>
```
Here `<dir>` is the `CMakeLists.txt` directory. The build scripts are build in current directory.

We can set any cache variable using the `-D` argument. Example:
```bash
cmake <dir> -D <variable name>=<variable value>
# or equivalently
cmake <dir> -D<variable name>=<variable value>
```


### Toolchain file
To work with package managers, a link to toolchain file has to be provided as an argument. For `vcpkg`, the argument is as follows:

```bash
# new version
cmake <dir> --toolchain <vcpkg location>/scripts/buildsystems/vcpkg.cmake

# old version
cmake <dir> -DCMAKE_TOOLCHAIN_FILE=<vcpkg location>/scripts/buildsystems/vcpkg.cmake
```

Note that the toolchain is only loaded at the beginnning of the generation process. Once you forgot it, **you need to delete the build scripts diectory content to make this argument work** for subsequent cmake commands.

### Usefull arguments
- `-LH` to see cmake nonadvanced variables together with the description. 
- `-LHA` to see also the advanced variables. Note that this prints only cached variables, to print all variables, we have to edit the CmakeLists.txt.
- `-D`: To change build options (`option` in `CMakeLists.txt`), run cmake with `-D <option name>=<option value> <build dir>`. Example: 
```cmake
cmake -D BUILD_TESTING=OFF .
```

### Legacy arguments
- `-H`: to specify the source directory (where the `CMakeLists.txt` file is located). Now it is specified as the positional argument or using `-S`.


## Building
For building, use:
```bash
cmake --build <build dir>
```
where build dir is the directory containing the build scripts (`CmakeFiles` folder).

To list the build options:
```
cmake -L
```


### Specify the target
By default, all targets are built. We can use the `--target` to specify a single target:
```cmake
cmake --build . --target <TARGET NAME>
```
There is also a special target `all` that builds all targets, which is equivalent to not specifying the `--target` argument.


## Specify the build type (Debug, Release)
In CMake, we use a specific build type string instead of compiler and linker flags:
- `Debug` - Debug build
- `Release` - Release build
- `RelWithDebInfo` - Release build with debug information
- `MinSizeRel` - Release build with minimal size

Unfortunately, the way how the build type should be specified depends on the build system:
- **Single-configuration systems** (GCC, Clang, MinGW) 
- **Multi-configuration systems** (MSVC)

### Single-configuration systems
Single configuration systems have the compiler flags hardcoded in the build scripts. Therefore, we need to specify the build type for CMake when we generate the build scripts:
```bash
cmake ../ -DCMAKE_BUILD_TYPE=Release
```
**By default, the build type is an empty string**. This means that no extra flags are added to the compiler and linker so the compiler and linker run with their default settings.

Interesting info can be found in [this SO question](https://stackoverflow.com/questions/48754619/what-are-cmake-build-type-debug-release-relwithdebinfo-and-minsizerel).

### Multi-configuration systems
In multi-configuration systems, the `-DCMAKE_BUILD_TYPE` parameter is ignored, because the build configuration is supposed to be determined when building the code (i.e., same build scripts for debug and for release). Therefore, we omit it, and instead specify the `--config` parameter when building the code:
```bash
cmake --build . --config Release
```



## Clean the source files
Run:
```
cmake --build . --target clean
```

## Install
To be able to install the project, it needs to be configured to do so. For this, check the [installation configuration](#installation-configuration).

To install the project, run:
```bash
cmake --install <build dir>
```

Note that the project needs to be built first. If it is not, we can build and install in one step using the `--build` with the `--target install` argument:
```bash
cmake --build <build dir> --target install
```

Usually, we want to use a different directory when testing the installation. To do that, we need to configure the project with the `CMAKE_INSTALL_PREFIX` variable. Example:
```bash
cmake -DCMAKE_INSTALL_PREFIX=<test install dir> <source dir>
```


## CMake command-line tools
[documentation](https://cmake.org/cmake/help/latest/manual/cmake.1.html#run-a-command-line-tool)

Apart from standard commands listed in previous sections, CMake provides several command-line tools that are not directly related to the build process. These tools wrap the system commands so that we are able to use them in a cross-platform way. To run these tools, execute:
```bash
cmake -E <tool name> <arguments>
```

The most useful tools are:
- `copy` - copy files and directories
- `capabilities` - print the properties of the system related to the build process


### Copy tool
The copy tool has two signatures:
- `copy <source> <destination>` 
- `copy -t <destination> <source>` (**only available in CMake 3.26 and later**)

Here, `<source>` can be a directory, a file, or a list of files. The `<destination>` can be a directory or a file. 


# Syntax


## Variables
We can use the variable using their name:
```cmake
if(DEFINED <name>)
...
```
In string, we need to wrap the variable in `${}`:
```cmake
message(STATUS "dir=${dir}")
```

### Enviromental variables
We can use environmental variables using the `ENV` variable:
```cmake
if(DEFINED ENV{<name>})
...
```
Be aware that in string, we use only one pair of curly braces (see [variable references manual](https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#variable-references)):
```cmake
message(STATUS "dir=$ENV{dir}")
```

### Built-in variables
- `CMAKE_CURRENT_SOURCE_DIR` - the directory where the currently processed `CMakeLists.txt` file is located.


### List variables
List variables are defined similarly to scalar variables using the `set` command:
```cmake
set(<name> <value 1> <value 2> ...)
```

Then, we can use the list variable in:
- commands that accept lists (e.g., `add_executable`, `add_library`, `target_link_libraries`)
- for loops


### Print all variables
To print all variables, the following function can be used:
```cmake
function(dump_cmake_variables)
    if (ARGV0)
        message(STATUS "Printing variables matching '${ARGV0}'")
    else()
        message(STATUS "Printing all variables")
    endif()
    get_cmake_property(_variableNames VARIABLES)
    list (SORT _variableNames)
    foreach (_variableName ${_variableNames})
        if (ARGV0)
            unset(MATCHED)
            string(REGEX MATCH ${ARGV0} MATCHED ${_variableName})
            if (NOT MATCHED)
                continue()
            endif()
        endif()
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
    message(STATUS "Printing variables - END")
endfunction()
```

To print all variables related to HDF5 lib, call `dump_cmake_variables(HDF)` after the `find_package` call.


## Control structures
### `if`
The [`if`](https://cmake.org/cmake/help/latest/command/if.html) command has the following syntax:
```cmake
if(<condition>)
...
elseif(<condition>)
...
else()
...
endif()
``` 

The condition can be:
- a variable
- an expression

Each expression can use some of the supported operators:
- logical operators: `AND`, `OR`, `NOT`
- comparison operators: `EQUAL`, `LESS`, `GREATER`, `LESS_EQUAL`, `GREATER_EQUAL`, `STREQUAL`, `STRLESS`, `STRGREATER`, `STRLESS_EQUAL`, `STRGREATER_EQUAL`
- file operators: `EXISTS`, `IS_DIRECTORY`, `IS_REGULAR_FILE`, `IS_SYMLINK`, `IS_ABSOLUTE`, `IS_RELATIVE`, `IS_NEWER_THAN`, `IS_OLDER_THAN`
- string operators: `MATCHES`, `LESS`, `GREATER`, `LESS_EQUAL`, `GREATER_EQUAL`, `STREQUAL`, `STRLESS`, `STRGREATER`, `STRLESS_EQUAL`, `STRGREATER_EQUAL`
- and more...

For the full list of operators, see the [if command documentation](https://cmake.org/cmake/help/latest/command/if.html).


## Generator expressions
[`Manual`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html)

Generator expressions are a very useful tool to control the build process based on the build type, compiler type, or similar properties. CMake use them to generate mutliple build scripts from a single `CMakeLists.txt` file.

The syntax for a basic condition expression is:
```cmake
"$<$<condition>:<this will be printed if condition is satisfied>>"
```

Unlike, variables, the **generator expressions are evaluated during the build process, not during the configuration process**. Therefore, they cannot be dumped during the configuration process, and they cannot be used in the `if` command. However, they can be still used in variables and commands, if the evaluation is not needed during the configuration process.

Notable variable expressions:
- `$<TARGET_FILE_DIR:<target name>>` - the directory where the target will be built
- [`$<TARGET_RUNTIME_DLLS:<target name>>`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#genex:TARGET_RUNTIME_DLLS) - the list of runtime dependencies of the target

### Evaluating generator expressions during configuration
In case we need to see the evaluated generator expressions during cmake configuration, we can try to cheat using the following command:
```cmake
file(GENERATE OUTPUT <filename> CONTENT <string-with-generator-expression>)
```
This way, we receive the evaluated value of the generator expression in the file for one of the build configurations.


## File operations
To perform file operations, use the [`file`](https://cmake.org/cmake/help/latest/command/file.html) command. The most useful subcommands are:
- `MAKE_DIRECTORY <directory>` - create a directory
- `RENAME <from> <to>` - renames/moves a file or directory. The `<from>` must exist, and the parent directory of `<to>` must exist. 
- `REMOVE <file>` - remove a file 
- `REMOVE_RECURSE <directory>` - remove a directory and all its content


## Functions
Functions are defined using the [`function`](https://cmake.org/cmake/help/latest/command/function.html) command. The syntax is:
```cmake
function(<function name> <argument 1> <argument 2> ...)
...
endfunction()
```

This way, we have a function with simple positional arguments. These arguments can be used in the function body as variables:
```cmake
function(print_arguments arg1 arg2)
    message(STATUS "arg1=${arg1}")
    message(STATUS "arg2=${arg2}")
endfunction()
```

To call the function, use the following syntax:
```cmake
print_arguments("value 1" "value 2")
```

More resources:
- https://hsf-training.github.io/hsf-training-cmake-webpage/11-functions/index.html

### Named arguments
We can notice that a typical cmake function has named arguments, e.g., `add_custom_command(TARGET <target name> POST_BUILD COMMAND <command>)`. To achieve this, we can use the [`cmake_parse_arguments`](https://cmake.org/cmake/help/latest/command/cmake_parse_arguments.html) command. The syntax is:
```cmake
function(<function name>)
    cmake_parse_arguments(
        PARSE_ARGV 
        <required args count> 
        <variable prefix> 
        <options>
        <one_value_keywords> 
        <multi_value_keywords>
    )
```
This way, we say that the function has:
- `<required args count>` required arguments,
- all argument values are stored in variables with the name `<variable prefix>_<variable_name>`,
- and the variable names available for the caller as well as the `<variable_name>` values are determined by the `<options>`, `<one_value_keywords>`, and `<multi_value_keywords>` arguments.

Each of the `<options>`, `<one_value_keywords>`, and `<multi_value_keywords>` arguments is a list of argument names divided by a semicolon. The `<options>` are the arguments that can be either present or not, the `<one_value_keywords>` are the arguments that have a single value, and the `<multi_value_keywords>` are the arguments that have multiple values.


### Default values for arguments
There is no specific syntax for default values for arguments. We can achieve this, for example, by using the `if` command:
```cmake
if(NOT DEFINED <variable>)
    set(<variable> <default value>)
endif()
```



# CMakeLists.txt
The `CMakeLists.txt` file is the main configuration file for any CMake project. This file is executed during the [configuration step](#configuration-generating-build-scripts) (when the `cmake` command is run without arguments specifying another step).
 It contains commands written in the CMake language that are used to configure the build process.

The typical structure of the `CMakeLists.txt` file is as follows:
1. Top section contains project wide setting like name, minimum cmake version, and the language specification.

1. Targets sections containing:
    - the target definition together with sources used
    - target includes
    - target linking


## Typical Top section content 
The typical content of the top section is:
- minimum cmake version: `cmake_minimum_required(VERSION <version>)`
- project name and version: `project(<name> VERSION <version>)`
- language specification: `enable_language(<language>)`
- cmake variables setup, e.g.: `set(CMAKE_CXX_STANDARD <version>)`
- compile options: `add_compile_options(<option 1> <option 2> ...)`
- cmake module inclusion: `include(<module name>)`

### Language standards
The language standard is set using the `set` command together with the `CMAKE_<LANG>_STANDARD` variable. Example:
```cmake
set(CMAKE_CXX_STANDARD 17)
```
This way, the standard is set for all targets and the compiler should be configured for that standard. However, if the compiler does not support the standard, the build script generation continues and the failure will appear later during the compilation. To avoid that, we can make the standard a requirement using the `set` command together with the `CMAKE_<LANG>_STANDARD_REQUIRED` variable. Example:
```cmake
set(CMAKE_CXX_STANDARD_REQUIRED ON)
``` 

However, the required standard is not always correctly supported by the compiler (e.g., GCC up to version 13 does not support C++20). Therefore, we need to specify the minimum version for these compilers:
```cmake
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS 13.0.0)
    message(FATAL_ERROR "GCC version must be at least 13.0.0!")
endif()
```


### Compile options
Most of the compile options are now sets automatically based on the declarations in the `CMakeLists.txt` file. However, some notable exceptions exists. To set such options, we have to use the `add_compile_options` command:
```cmake
add_compile_options(<option 1> <option 2> ...)
```

#### MSVC
- [`/permissive-`](https://learn.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance?view=msvc-170&viewFallbackFrom=vs-2019) to enable the strictest mode of the compiler

#### GCC
- [`-pedantic-errors`](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html) to report all cases where non-standard GCC extension is used and treat them as  errors


### Linker Options
Linker options can be set with `add_link_options` command. Example: 
```Cmake
add_link_options("/STACK: 10000000")
```


## Dependency management
There are many ways how to manage dependencies in CMake, for complete overview, see the [documentation](https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html#guide:Using%20Dependencies%20Guide). 

Although it is possible to hard-code the paths for includes and linking, it is usually better to initialize the paths automatically using a rich set of commands cmake offers.  It has the following advatages:
- Hardcoding the paths is error-prone, while cmake commands usually deliver correct paths
- It boost the productivity as we do not have to investigate where each library is installed
- The resulting `CMakeLists.txt` file is more portable
- And most importantly, **potential errors concerning missing libraries are reported prior to the compilation/linking**.

Most of the libraries have CMake support, so their CMake variables can be initialized simply by calling the `find_package` command described below. These packages have either:
- their own cmake config (cmake-aware libs usually installed through the package manager like `vcpkg`)
- or they have a `Find<package name>` script created by someone else that heuristically search for the packege (The default location for these scripts is `CMake/share/cmake-<version>/Modules`). 

For packages without the CMake support, we have to use lower-level cmake commands like `find_path` or `find_libraries`. For convinience, we can put these command to our own `Find<name>` script taht can be used by multiple project or even shared. 


### Standard way: `find_package`
The [`find_package`](https://cmake.org/cmake/help/latest/command/find_package.html) command is the primary way of obtaining correct variables for a library including:
- include paths
- linking paths
- platform/toolchain specific enviromental variables

There are two types of package (library) info search:
- *module*, which uses cmake scripts provided by CMake or OS. The modules are typically provided only for the most used libraries (e.g. boost). All modules provided by CMake are listed in the [documentation](https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html#find-modules).
- *config* which uses CMake scripts provided by the developers of the package. They are typically distributed with the source code and downloaded by the package manager. 

Unless specified, the module mode is used. To force a speciic mode, we can use the `MODULE`/`CONFIG` parameters.


#### Config packages
Config packages are CMake modules that were created as cmake projects by their developers. They are therefore naturally integrated into Cmake. 

The configuration files are executed as follows:
1. Package version file: `<package name>-config-version.cmake` or `<package name>ConfigVersion.cmake`. This file handles the version compatibility, i.e., it ensures that the installed version of the package is compatible with the version requested in the `find_package` command.
1. Package configuration file: `<package name>-config.cmake` or `<package name>Config.cmake`.


#### Module Packages
Module packages are packages that are not cmake projects themselves, but are hooked into cmake using custom find module scrips. These scripts are automatically executed by `find_package`.

They are located in e.g.: `CMake/share/cmake-3.22/Modules/Find<package name>.cmake`. 


### Searching for include directories with `find_path`
The [`find_path`](https://cmake.org/cmake/help/latest/command/find_path.html) command is intended to find the path (e.g., an include directory).
A simple syntax is:
```cmake
find_path(
	<var name>
	NAMES <file names>
	PATHS <paths>
)
```
Here:
- `<var name>` is the name of the resulting variable
- `<file names>` are **all possible** file names split by space. At least one of the files needs to be present in a path for it to be considered to be the found path.
- `<paths>` are candidate paths split by space



### Low level command: `find_library`
The [`find_library`](https://cmake.org/cmake/help/latest/command/find_library.html) command is used to populate a variable with a result of a specific file search optimized for libraries. 

The search algorithm works as follows:
1. ?
2. Search package paths
    - order:
        1. `<CurrentPackage>_ROOT`, 
        2. `ENV{<CurrentPackage>_ROOT}`, 
        3. `<ParentPackage>_ROOT`,
        4. `ENV{<ParentPackage>_ROOT}`
    - this only happens if the `find_library` command is called from within a `find_<module>` or `find_package`
    - this step can be skipped using the `NO_PACKAGE_ROOT_PATH` parameter 
3. Search path from cmake cache. During a clean cmake generation, these can be only supplied by command line. 
    - Considered variables:
        - `CMAKE_LIBRARY_ARCHITECTURE`
        - `CMAKE_PREFIX_PATH`
        - `CMAKE_LIBRARY_PATH`
        - `CMAKE_FRAMEWORK_PATH`
    - this step can be skipped using the `NO_CMAKE_PATH` parameter
4. Same as step 3, but the variables are searched among system environmental variables instead
    - this step can be skipped using the `NO_CMAKE_ENVIRONMENT_PATH` parameter
5. Search paths specified by the `HINTS` option
6. Search the standard system environmental paths
    - variables considered are `LIB` and `PATH`
    - this step can be skipped using the `NO_SYSTEM_ENVIRONMENT_PATH` parameter
7. Search in system paths
    - Considered variables:
        - `CMAKE_LIBRARY_ARCHITECTURE`
        - `CMAKE_SYSTEM_PREFIX_PATH`
        - `CMAKE_SYSTEM_LIBRARY_PATH`
        - `CMAKE_SYSTEM_FRAMEWORK_PATH`
    - this step can be skipped using the `NO_CMAKE_SYSTEM_PATH` parameter
8. Search the paths specified by the `PATHS` option


#### Searching for libraries in the project dir
Note that the project dir is not searched by default. To include in the search, use: `HINTS ${PROJECT_SOURCE_DIR}`. Full example on the Gurobi lib stored in `<CMAKE LISTS DIR/lib/gurobi_c++.a>`:

```cmake
find_library(GUROBI_CXX_LIBRARY
    NAMES gurobi_c++
    HINTS ${PROJECT_SOURCE_DIR}
    PATH_SUFFIXES lib
    NO_CMAKE_ENVIRONMENT_PATH
    REQUIRED
)
```


### Creating a custom find script
The structure of a simple find scripts is described in the [documentation](https://cmake.org/cmake/help/latest/manual/cmake-developer.7.html#find-modules). 

We can either put the find script to the default location, so it will be available for all projects, or we can put it in the project directory and add that directory to the `CMAKE_MODULE_PATH`:
```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")
```

The usual structure of the find script is:
1. the comment section describing the file:
```cmake
#[=======================================================================[.rst:
FindMOSEK
-------

Finds the MOSEK library.

Result Variables
^^^^^^^^^^^^^^^^
This will define the following variables:

``MOESK_FOUND``
  True if the system has the MOSEK library.
``MOSEK_INCLUDE_DIRS``
  Include directories needed to use MOSEK.
``MOSEK_LIBRARIES``
  Libraries needed to link to MOSEK.

#]=======================================================================]
```
2. find commands that fils some temp variables:
```cmake
find_path(
	MOSEK_INCLUDE_DIR
	NAMES mosek.h
	PATHS "$ENV{MOSEK_HOME}/h"
)

find_library(
	MOSEK_LIBRARY
	NAMES libmosek64.so.10.0 libfusion64.so.10.0
	PATHS "$ENV{MOSEK_HOME}/bin"
)
```
3. handeling of the result of the file commands. The standard approach is:
```cmake
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MOSEK
  FOUND_VAR MOSEK_FOUND
  REQUIRED_VARS
    MOSEK_LIBRARY
    MOSEK_INCLUDE_DIR
)
``` 
4. setting the final variables:
```cmake
if(MOSEK_FOUND)
	set(MOSEK_LIBRARIES ${MOSEK_LIBRARY})
	set(MOSEK_INCLUDE_DIRS ${MOSEK_INCLUDE_DIR})
endif()
```


### Downolad dependencies during configuration and build them from source
To download and build dependencies during the configuration, we can use the [`FetchContent`](https://cmake.org/cmake/help/latest/module/FetchContent.html) module. For details, see the [dependency management documentation](https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html#fetchcontent-and-find-package-integration).

The usual workflow is:
1. Download the dependency using the `FetchContent_Declare` command
    ```cmake
    FetchContent_Declare(
    <NAME>
    <SPECIFICATION>
    )
    ```
    - The specification can be either a URL or a git repository.
2. Configure the dependency using the [`FetchContent_MakeAvailable`](https://cmake.org/cmake/help/latest/module/FetchContent.html#command:fetchcontent_makeavailable) command:
    ```cmake
    FetchContent_MakeAvailable(<NAME>)
    ```
    - If the dependency is a CMake project, the `FetchContent_MakeAvailable` command will automatically configure the project by calling the `add_subdirectory` command with the path to the downloaded source code.

Both the dependency source code and the build directory are stored in the build directory in `_deps` folder. This directory contains:
- `<NAME>-src` - the source code of the dependency
- `<NAME>-build` - the build directory of the dependency


## CMake Targets
Targets define logical units of the build process. These can be:
- executables
- libraries
- custom targets doing all sorts of things
- sets of targets, i.e., aliases for building multiple targets at once

Available targets are either user-defined or automatically generated by CMake.  


### Target definition
The target definition is done using the `add_executable` command. The syntax is:
```cmake
add_executable(<target name> <source file 1> <source file 2> ...)
```
The target name is used to refer to the target in other commands. The target name is also used to name the output file. 

The list of source files should contain all the source files that are needed to build the target. There are some automatic mechanisms that can be used to add the source files (discussed e.g. on [cmake forums](https://discourse.cmake.org/t/is-glob-still-considered-harmful-with-configure-depends/808/2)), but they are not recommended.


### Targets automatically generated by CMake
[listed here](https://cmake.org/cmake/help/latest/guide/user-interaction/index.html#selecting-a-target).

Besides the user-defined targets, CMake automatically generates some targets. These are:
- **all**: alias for building all targets. Default target if the `--target` argument is not specified. 
    - In Visual Studio and Xcode generators, this target is called `ALL_BUILD`.
    - we can exclude some targets from the `all` target using the [`EXCLUDE_FROM_ALL` target property](https://cmake.org/cmake/help/latest/prop_tgt/EXCLUDE_FROM_ALL.html#prop_tgt:EXCLUDE_FROM_ALL) or the [`EXCLUDE_FROM_ALL` directory property](https://cmake.org/cmake/help/latest/prop_dir/EXCLUDE_FROM_ALL.html#prop_dir:EXCLUDE_FROM_ALL).
- **clean** target that cleans the build directory
- **install** target that installs the project. It depends on the `all` target.
    - this target is only available if the `CMakelists.txt` file contains the `install` command (see [installation configuration](#installation-configuration)).
- and some more...


## Include directories
To include the headers, we need to use a `inlude_directories` (global), or better `target_include_directories` command. The difference:
- **target specification**: `target_include_directories` specifies the include directories for a specific target, while `include_directories` specifies the include directories for all targets in the current directory.
- **mode specification**: `target_include_directories` specifies the mode of the include directories (e.g., `PUBLIC`, `PRIVATE`, `INTERFACE`), while `include_directories` behaves simillar to `PRIVATE`. Therefore, for libraries, the `target_include_directories` has to be used.

### Inspect the Include directories
All the global include directories are stored in the `INCLUDE_DIRECTORIES` property, to print them, add this to the `CMakeLists.txt` file:
```cmake
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()
```



## Linking configuration
For linking, use the [`target_link_libraries`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html) command.

Make sure that you **always link against all the libraries that are needed for the target to work!** Do not rely on the linker errors, these may not appear due to library preloading, indirect linkage, advanced linker heuristics, etc. The result is that on one machine the code will work, but on another, it will fail. To find out if and how to link against a library, refer to the documentation of the library.




## Copying Runtime Dependencies
Some generators (e.g., Visual Studio) do not copy the runtime dependencies to the output directory. To do that, we can use the [`add_custom_command`](https://cmake.org/cmake/help/latest/command/add_custom_command.html) command together with the [`$<TARGET_RUNTIME_DLLS:<target name>>`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#genex:TARGET_RUNTIME_DLLS) generator expression. Be careful to wrap this code by a condition that checks the generator type, as the generator expression is only available for DLL-aware generators.
```cmake
if(CMAKE_GENERATOR MATCHES "Visual Studio.*")
    add_custom_command(
        TARGET <target name>
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:<target name>> $<TARGET_FILE_DIR:<target name>>
        COMMAND_EXPAND_LISTS
    )
endif()
```

Here, the `COMMAND_EXPAND_LISTS` is used to expand the generator expressions in the command. We use it for the [`$<TARGET_RUNTIME_DLLS:<target name>>`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#genex:TARGET_RUNTIME_DLLS) generator expression that returns the list of runtime dependencies of the target. 


## Installation Configuration
To enable installation, we have to provide several commands and do some adjustments in the `CMakeLists.txt` file. Specific steps depends on what we want to achieve.

The minimal installation that installs only binaries can be set up using two commands:
- Install binaries with the [`install(TARGETS...`](https://cmake.org/cmake/help/latest/command/install.html#targets) command. The basic syntax is:
    ```cmake
    install(TARGETS <target name 1> <target name 2>)
    ```
- Install headers with the [`install(FILES...`](https://cmake.org/cmake/help/latest/command/install.html#files) command. The basic syntax is:
    ```cmake
    install(FILES <file 1> <file 2> DESTINATION <destination>)
    ```
    - We have to install both public API headers and their internal dependencies. Usually, this means installing most of the headers.
    - The `<destination>` is the directory where the files will be installed. Typically, it is `${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}` for header files.
    - We usually only want a single set of headers to be installed for both Debug and Release builds (**for vcpkg, this is required**). This can be achieved by using the `CONFIGURATIONS` parameter of the `install` command. Example:
        ```cmake
        install(
            FILES <file 1> <file 2> 
            DESTINATION <destination> 
            CONFIGURATIONS Release
        )
        ```

This command provides the `install` target that builds all targets (it depends on the `all` target) and then installs the project, which means that it copies the binary files to the installation directory.


### Install CMake files
If we want our library to be used from CMake projects, the basic configuration is not enough. We have to provide the CMake configuration files that will be used by the `find_package` command when searching for the dependency. Usually, CMake packages have the following cmake files:
- `<package name>Targes.cmake` - contains the targets that are installed by the package
- `<package name>Config.cmake` - contains the configuration of the package, i.e., the include directories, linking directories, and other variables that are needed to use the package.
- `<package name>ConfigVersion.cmake` - contains the version of the package and the compatibility check.


#### Installing the Targets file
This involves two steps:
1. use the `EXPORT` parameter of the `install(TARGETS...` command to create a reference to installed targets that we can use further
    ```cmake
    install(TARGETS <target name 1> <target name 2>
        EXPORT <export name>
    )
    ```
    - The `<export name>` is the name of the export set that will be used in the CMake configuration file. Typically, it is `${PROJECT_NAME}Targets`.
2. use the [`install(EXPORT...`](https://cmake.org/cmake/help/latest/command/install.html#export) command to install the cmake files
    ```cmake
    install(EXPORT <export name>
        DESTINATION <destination>
    )
    ```
    - The `<export name>` is the name of the export set that was used in the `install(TARGETS...` command
    - The `<destination>` is the directory where the CMake configuration files will be installed. Typically, it is ([source](https://discourse.cmake.org/t/what-should-the-destination-be-for-a-header-only-librarys-cmake-config-file/8473)):
        - `${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}` for binaries
        - `share/cmake/${PROJECT_NAME}` for header-only libraries
        - **for vcpkg**: `share/${PROJECT_NAME}`. Otherwise, we need to mess with the `CONFIG_PATH` parameter of the `vcpkg_cmake_config_fixup` function.
    - for using the `CMAKE_INSTALL_LIBDIR` variable, we have to include the `GNUInstallDirs` module using the `include` command.


#### Installing the package configuration file and the version file
In order for these files to be portable, they should be generated. The appropriate functions for this are in the [`CMakePackageConfigHelpers module](https://cmake.org/cmake/help/latest/module/CMakePackageConfigHelpers.html), which has to be included. 

To generate the package configuration file:
1. create the input file somewhere in the project directory with the
name `<package name>Config.cmake.in` and fill it with the following content:
    ```cmake
    @PACKAGE_INIT@

    include ("${CMAKE_CURRENT_LIST_DIR}/<package name>Targes.cmake")
    
    optional content ...
    ``` 
    - The `@PACKAGE_INIT@` is a placeholder that will be replaced by the `write_basic_package_version_file` command.
1. then generate the package configuration file by ading the `configure_package_config_file` command to the `CMakeLists.txt` file:
    ```cmake
    configure_package_config_file(
        <path to in file>
        <path to package config file in the build dir>
        INSTALL_DESTINATION <cmake files installation path>
    )
    ```
    - here, the <cmake files installation path> is the same as the `<destination>` parameter in the `install(EXPORT...` command.


The version file is generated using the [`write_basic_package_version_file`](https://cmake.org/cmake/help/latest/module/CMakePackageConfigHelpers.html#write-basic-package-version-file) command. The syntax is:
```cmake
write_basic_package_version_file(
    <version file build path>
    VERSION <version>
    COMPATIBILITY AnyNewerVersion
)
```
- The `<version file build path>` is the path where the version file will be generated. 
- The `<version>` is the version of the package. Typically, it is the version of the project: `${<project name>Major}.${<project name>Minor}.${<project name>Patch}`.


Finally, to install both files, we use the [`install(FILES...`](https://cmake.org/cmake/help/latest/command/install.html#files) command:
```cmake    
install(FILES
    <path to package config file in the build dir>
    <path to version file in the build dir>
    DESTINATION <cmake files installation path>
)
```




#### Sanitation of the public include directories
Additionally, an extra step is needed in case we define include directories to be accessible from other projects (i.e., `PUBLIC` or `INTERFACE` mode). In this case, we have to use a special configuration for those directories so that a different path is used when the library is installed. For example, if we include the `src` directory using:
```cmake
target_include_directories(<target name> PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
``` 
we have to change it to:
```cmake
target_include_directories(<target name> PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    $<INSTALL_INTERFACE:include>
)
```

### Specify the targets to install
The [`install`](https://cmake.org/cmake/help/latest/command/install.html)
 command has a parameter `TARGETS` that can specify the targets that should be installed. The syntax is:


However, **the `TARGETS` parameter only affects the installation part of the `install` target**. In other words, it determines what files are copied to the installation directory, but it does not affect the build process. Therefore, **all targets are built regardless of the `TARGETS` parameter**.

To prevent the building of some targets when installing, we have several options:
- exclude selected targets from the `all` target using the [`EXCLUDE_FROM_ALL` target property](https://cmake.org/cmake/help/latest/prop_tgt/EXCLUDE_FROM_ALL.html#prop_tgt:EXCLUDE_FROM_ALL) or the [`EXCLUDE_FROM_ALL` directory property](https://cmake.org/cmake/help/latest/prop_dir/EXCLUDE_FROM_ALL.html#prop_dir:EXCLUDE_FROM_ALL).
- disable building for the `install` target and use a custom wrapper target that builds only the targets that should be installed and then calls the `install` target.


#### Selecting the targets to build using the `EXCLUDE_FROM_ALL` property
For user targets added by the `add_executable` or `add_library` command, we can use the [`EXCLUDE_FROM_ALL`](https://cmake.org/cmake/help/latest/prop_tgt/EXCLUDE_FROM_ALL.html#prop_tgt:EXCLUDE_FROM_ALL) target property:
```cmake
add_executable(my_target EXCLUDE_FROM_ALL <source file 1> <source file 2> ...)
```

For targets added by the `FetchContent_MakeAvailable` command. The situation is more complicated. The `FetchContent_Declare` command provides the `EXCLUDE_FROM_ALL` option, but it does not work as expected. Instead, we have to set the `EXCLUDE_FROM_ALL` property for the target after the `FetchContent_MakeAvailable` command:
```cmake
FetchContent_Declare(
    <declaration name>
    ...
)
FetchContent_MakeAvailable(<declaration name>)
set_target_properties(<target name> PROPERTIES EXCLUDE_FROM_ALL TRUE)
```


#### Disabling the building of the `install` target and using a custom wrapper target
For this solution,we first need to disable the building of the `install` using: `set(CMAKE_SKIP_INSTALL_ALL_DEPENDENCY true)`. Then, we need to create a target that: a) builds the selected targets, b) calls the `install` target. 

[`CMAKE_SKIP_INSTALL_ALL_DEPENDENCY` documentation](https://cmake.org/cmake/help/latest/variable/CMAKE_SKIP_INSTALL_ALL_DEPENDENCY.html#variable:CMAKE_SKIP_INSTALL_ALL_DEPENDENCY) 


### Specific configuration for frequentlly used libraries
- for google test, we want to prevent the installation of the `gtest` targets. To do that, turn it off before the gtets config in the `CMakeLists.txt` file:
    ```cmake
    # GOOGLE TEST
    # do not install gtest
    set(INSTALL_GTEST OFF)

    include(FetchContent)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
    )
    # For Windows: Prevent overriding the parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
    ```


## Multiple `CMakeLists.txt` files in subdirectories
The configuration can be modularized by splitting the `CMakeLists.txt` file into multiple files, each in a separate directory. Then, these files can be executed using the `add_subdirectory` command in the main `CMake_lists.txt` file or one of the `CMakeLists.txt` files already added by the `add_subdirectory` command.

The order of execution follows the order of the `add_subdirectory` commands, i.e., the processing of the `CMakeLists.txt` containing the `add_subdirectory` command is paused until the added `CMakeLists.txt` file is processed.

### Variables scope
The variable scope for multiple `CMakeLists.txt` files is hierarchical. This means that the variables defined in the parent `CMakeLists.txt` file are visible in the child `CMakeLists.txt` file, but not vice versa.


## Decide based on the build configuration
Sometimes is essential to decide based on the build configuration in the `CMakeLists.txt` file. However, this is not possible for the multi-configuration generators like Visual Studio or Xcode because the build configuration is not known during the CMake configuration step. However, there are measures that can be taken to achieve the result for particular tasks.

For `install` command, we can use the `CONFIGURATIONS` parameter to install the files only for the selected build configuration. Example:
```cmake
install(
    FILES <file 1> <file 2> 
    DESTINATION <destination> 
    CONFIGURATIONS Release
)
```

For building, there are ways to limit the build based on the build configuration for both single- and multi-configuration generators. For single configuration generators, we can use the [`CMAKE_BUILD_TYPE`](https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html) variable and simply exclude the target from the build using the `EXCLUDE_FROM_ALL` target property:
```cmake
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
   set_target_properties(<target name> PROPERTIES EXCLUDE_FROM_ALL TRUE)
endif()
```
For multi-configuration generators, this variable is not set, but we can use the
`EXCLUDE_FROM_DEFAULT_BUILD_DEBUG` property:
```cmake
set_target_properties(<target name> PROPERTIES EXCLUDE_FROM_DEFAULT_BUILD_DEBUG TRUE)
```
To support both single- and multi-configuration generators, we have to first check whether we use a single- or multi-configuration generator using the [`CMAKE_CONFIGURATION_TYPES`](https://cmake.org/cmake/help/latest/variable/CMAKE_CONFIGURATION_TYPES.html) variable and then set the property accordingly:
```cmake
if(CMAKE_CONFIGURATION_TYPES)
    set_target_properties(<target name> PROPERTIES EXCLUDE_FROM_DEFAULT_BUILD_DEBUG TRUE)
else()
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        set_target_properties(<target name> PROPERTIES EXCLUDE_FROM_ALL TRUE)
    endif()
endif()
```


## Executing external commands
There are different ways to execute external commands in the `CMakeLists.txt`, the proper way depends on the time when we want to execute the command:
- **configuration time**: use the [`execute_process`](https://cmake.org/cmake/help/latest/command/execute_process.html) command
- **build time**: use the [`add_custom_command`](https://cmake.org/cmake/help/latest/command/add_custom_command.html) command
    - can be run both before and after the build step using the `PRE_BUILD` and `POST_BUILD` options



# CMake Variables and Cache
CMake has two types of variables:
- *normal variables* that are used just like in any other programming language and
- *cache variables*, which are configured in the first cmake run and then stored in the `CMakeCache.txt` file in the build directory.
The [CMake cache](https://cmake.org/cmake/help/book/mastering-cmake/chapter/CMake%20Cache.html) is an essential part of the CMake build system. It stores variables that are used to configure the build scripts. 

In order to use a variable in the `CMakeLists.txt` file, we have to use the `${}` syntax:
```cmake
message(STATUS "dir=${dir}")
```

Normal variables are set using the [`set`](https://cmake.org/cmake/help/latest/command/set.html) command:
```cmake
set(<variable name> <variable value>)
```

Cache variables can be set in the following ways:
- by the [`set`](https://cmake.org/cmake/help/latest/command/set.html) command in the `CMakeLists.txt` file with the `CACHE` option
- by the `-D` command line argument: `cmake -D<variable name>=<variable value> <dir>`
- by the cmake GUI
- by using the `-C` option: `cmake -C <cache file> <dir>`

The rule is that once a cache variable is set, it is not changed when the `cmake` command is run again (that is why it is called cache :) ). Moreover, the cache variables are not overwritten by the `set` command in the `CMakeLists.txt` file. In other words, the `set` command in the `CMakeLists.txt` is only used to set the default value of the variable. If the variable is already set in the cache, the `set` command is ignored. However, the cache variables can be still overridden from the `CMakeLists.txt` if the `set` command is used without the `CACHE` option (by normal variables).



## The `option` command
The [`option`](https://cmake.org/cmake/help/latest/command/option.html) command is used to define a cache variable that can be set by the user. The syntax is:
```cmake
option(<option name> <option description> <default value>)
```
The behavior of the `option` command is as follows:
- If variable is already set (either a cache variable or a normal variable), the `option` command is ignored.
- Otherwise, a cache variable is created if we are in the project mode, and a normal variable is created if we are in the script mode.


## Built-in variables
There are some variable generated by default by CMake. These are:
- `CMAKE_CURRENT_SOURCE_DIR`: the directory where the currently processed `CMakeLists.txt` file is located.
- `CMAKE_CURRENT_BINARY_DIR`: the directory where the build scripts are located.




# CMake Directory Structure
## System Find_XXX.cmake files
The system find scripts are located in the `CMake/share/cmake-<version>/Modules/` directory.


# Various Tasks

## Showing the generator for a configured directory
If the configuration step is already done, we can show the generator used for the configuration by reading the `CMAKE_GENERATOR` variable from the `CMakeCache.txt` file:
```powershell
Get-Content CMakeCache.txt | Select-String -Pattern "CMAKE_GENERATOR"
```


# Debugging CMake 

## Debugging CMake using CLion CMake debugger
[documentation](https://www.jetbrains.com/help/clion/cmake-debug.html)

In CLion, we can debug the CMake configuration process by:
1. opening the `CMakeLists.txt` file
1. setting the breakpoint(s)
1. starting the debugging process
    - by clicking on the play button which is located on the first line of the `CMakeLists.txt` file on the left side of the editor window.
    - or by clicking on the debug button in the main toolbar


## Getting a a complete output of the CMake configuration
We can get the complete output of the CMake configuration by running the `cmake` command with the `--trace` option. This can be especially useful when investigating included scripts, as the debuggers usually cannot step into CMake calls. Usually, the output is very long, so it is recommended to redirect it to a file:
```powershell
cmake --trace <dir> *> cmake_trace.txt
```
If we want to also expand the variables, we can use the `--trace-expand` option.