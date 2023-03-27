# Commands
## Generating Build scripts
General syntax is:
```bash
cmake <dir>
```
Here `<dir>` is the `CMakeLists.txt` directory. The build scripts are build in current directory.

### Toolchain file
To work with package managers, a link to toolchain file has to be provided as an argument `-DCMAKE_TOOLCHAIN_FILE`. For `vcpkg`, the argument is as follows:

```bash
-DCMAKE_TOOLCHAIN_FILE=<vcpkg location>/scripts/buildsystems/vcpkg.cmake
```

Note that the toolchain is only loaded at the beginnning of the generation process. Once you forgot it, **you need to delete the build scripts diectory content to make this argument work** for subsequent cmake commands.

### Usefull arguments
`-LH` to see cmake nonadvanced variables together with the description. Use `-LHA` to see also the advanced variables. Note that this prints only cached variables, to print all variables, we have to edit the CmakeLists.txt.



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
- project name: `project(<name>)`
- language specification: `enable_language(<language>)`
- language standard, e.g.: `set(CMAKE_CXX_STANDARD <version>)`
- compile options: `add_compile_options(<option 1> <option 2> ...)`

### Compile options
Most of the compile options are now sets automatically based on the declarations in the CMakeLists.txt file. However, some notable exceptions exists. To set such options, we have to use the `add_compile_options` command:
```cmake
add_compile_options(<option 1> <option 2> ...)
```

#### MSVC
- [`/permissive-`](https://learn.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance?view=msvc-170&viewFallbackFrom=vs-2019) to enable the strictest mode of the compiler



## Searching for libraries
Although it is possible to hard-code the paths for includes and linking, it is usually better to initialize the paths automatically using a rich set of commands cmake offers.  It has the following advatages:
- Hardcoding the paths is error-prone, while cmake commands usually deliver correct paths
- It boost the productivity as we do not have to investigate where each library is installed
- The resulting `CMakeLists.txt` file is more portable
- And most importantly, **potential errors concerning missing libraries are reported prior to the compilation/linking**.

Most of the libraries have CMake support, so their CMake variables can be initialized simply by calling the `find_package` command described below. These packages have either:
- their own cmake config (cmake-aware libs usually installed through the package manager like `vcpkg`)
- or they have a `Find<package name>` script created by someone else that heuristically search for the packege (The default location for these scripts is `CMake/share/cmake-<version>/Modules`). 

For packages without the CMake support, we have to use lower-level cmake commands like `find_path` or `find_libraries`. For convinience, we can put these command to our own `Find<name>` script taht can be used by multiple project or even shared. 


### `find_package`
The [`find_package`](https://cmake.org/cmake/help/latest/command/find_package.html) command is the primary way of obtaining correct variables for a library including:
- include paths
- linking paths
- platform/toolchain specific enviromental variables

There are two types of package (library) info search:
- *module*, which uses cmake scripts provided by CMake or OS. The modules are typically provided only for the most used libraries (e.g. boost). All modules provided by CMake are listed in the [documentation](https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html#find-modules).
- *config* which uses CMake scripts provided by the developers of the package. They are typically distributed with the source code and downloaded by the package manager. 

Unless specified, the module mode is used. To force a speciic mode, we can use the `MODULE`/`CONFIG` parameters.


### `find_path`
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
- `<file names>` are **all possible** file names split by space that needs to be present in a path for it to be considered to be the found path
- `<paths>` are candidate paths split by space


### `find_library`
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


## Setting include directories
To inlude the headers, we need to use a `inlude_directories` (global), or better `target_include_directories` command.



## Linking configuration
For linkink, use the `target_link_libraries` command.





## Include directories
All the global include directories are stored in the `INCLUDE_DIRECTORIES` property, to print them, add this to the `CMakeLists.txt` file:
```cmake
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()
```