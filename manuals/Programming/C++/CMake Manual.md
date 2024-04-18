# Commands
## Generating Build scripts
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
We can use the `--target` parameter for that:
```cmake
cmake --build . --target <TARGET NAME>
```


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
The `if` command has the following syntax:
```cmake
if(<condition>)
...
elseif(<condition>)
...
else()
...
endif()
``` 


## Generator expressions
[`Manual`](https://cmake.org/cmake/help/v3.4/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions%287%29)

Generator expressions are a very useful tool to control the build process based on the build type, compiler type, or similar properties. CMake use them to generate mutliple build scripts from a single `CMakeLists.txt` file.

The syntax for a basic condition expression is:
```cmake
"$<$<condition>:<this will be printed if condition is satisfied>>"
```



# CMakeLists.txt
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
2. Build the dependency using the `FetchContent_MakeAvailable` command:
    ```cmake
    FetchContent_MakeAvailable(<NAME>)
    ```


## Target definition
The target definition is done using the `add_executable` command. The syntax is:
```cmake
add_executable(<target name> <source file 1> <source file 2> ...)
```
The target name is used to refer to the target in other commands. The target name is also used to name the output file. 

The list of source files should contain all the source files that are needed to build the target. There are some automatic mechanisms that can be used to add the source files (discussed e.g. on [cmake forums](https://discourse.cmake.org/t/is-glob-still-considered-harmful-with-configure-depends/808/2)), but they are not recommended.


## Setting include directories
To inlude the headers, we need to use a `inlude_directories` (global), or better `target_include_directories` command.



## Linking configuration
For linkink, use the [`target_link_libraries`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html) command.

Make sure that you **always link against all the libraries that are needed for the target to work!** Do not rely on the linker errors, these may not appear due to library preloading, indirect linkage, advenced linker heuristics, etc. The result is that on one machine the code will work, but on another, it will fail. To find out if and how to link against a library, refer to the documentation of the library.





## Include directories
All the global include directories are stored in the `INCLUDE_DIRECTORIES` property, to print them, add this to the `CMakeLists.txt` file:
```cmake
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()
```



# CMake Cache
The [CMake cache](https://cmake.org/cmake/help/book/mastering-cmake/chapter/CMake%20Cache.html) is an essential part of the CMake build system. It stores variables that are used to configure the build scripts. The cache is stored in the `CMakeCache.txt` file in the build directory.

The Cmake cache can be filled in the following ways:
- by the [`set`](https://cmake.org/cmake/help/latest/command/set.html) command in the `CMakeLists.txt` file with the `CACHE` option
- by the `-D` command line argument: `cmake -D<variable name>=<variable value> <dir>`
- by the cmake GUI
- by using the `-C` option: `cmake -C <cache file> <dir>`

The rule is that once a cache variable is set, it is not changed when the `cmake` command is run again (that is why it is called cache :) ). 

Moreover, the cache variables are not overwritten by the `set` command in the `CMakeLists.txt` file. In other words, the `set` command in the `CMakeLists.txt` is only used to set the default value of the variable. If the variable is already set in the cache, the `set` command is ignored.

However, the cache variables can be still overridden from the `CMakeLists.txt` if the `set` command is used without the `CACHE` option (by normal variables).




# CMake Directory Structure
## System Find_XXX.cmake files
The system find scripts are located in the `CMake/share/cmake-<version>/Modules/` directory.