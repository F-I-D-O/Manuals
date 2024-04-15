
This guide presents how to prepare the following working environment:

-   One or more from the following toolchains
	-   MinGW  
	-   MSVC
	-   GCC
-   Cmake
-   Clion and/or Visual studio
-   vcpkg

# Toolchain
There are various toolchains available on Windows and Linux, but we limit this guide for only some of them, specifically those which are frequently updated and works great with Clion.

## MSYS2 (Windows only)
-   [download](https://www.msys2.org/)
-   follow the installation guide on the homepage
-   install MinGW64 using: `pacman -S mingw-w64-x86_64-gcc`
    

## MSCV (Windows only)
-   install [Visual Studio 2019 Comunity Edition](https://visualstudio.microsoft.com/cs/vs/)


### Common Compiler Flags
- [`/MD`, `/MT`, and similar](https://learn.microsoft.com/en-us/cpp/build/reference/md-mt-ld-use-run-time-library): these determines the version of the standard run-time library. The `/MD` flag is the default and also prefered.
- [`/nologo`](https://learn.microsoft.com/en-us/cpp/build/reference/nologo-suppress-startup-banner-c-cpp): do not print the copyright banner and information messages
- [`/EH`](https://learn.microsoft.com/en-us/cpp/build/reference/eh-exception-handling-model): exception handeling flags
    

## GCC (Linux/WSL)
1.   If on Windows, [Install the WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) first (preferably WSL 2)
2.   `sudo apt-get update`
3.  `sudo apt-get upgrade`
4.   `sudo apt-get install build-essential rsync zip ninja-build make`3

For using gcc 10:
-   `sudo apt-get install gcc-10 g++-10`

# Cmake
-   Windows: Install CMake from [https://cmake.org/download/](https://cmake.org/download/)
	-  if your CMake is too old (e.g. error: “CMake 3.15 or higher is required”), update CMake (same as new install)
-   Linux:
	-   If cmake is installed already, uninstall it!
	-   Do not use the cmake from linux repositories!!
	-   Download CMake `sh` installer from [https://cmake.org/download/](https://cmake.org/download/)
	-   install:
		1. `sudo chmod +x <INSTALLER>`
		2. `sudo <INSTALLER>`
		3. `sudo rm <INSTALLER>`
	-   add cmake executable to path

Other details about CMake can be found in the CMake Manual.

# vcpkg
-   follow the [installation guide](https://github.com/microsoft/vcpkg), including the user and PowerShell/bash integration
-   add the vcpkg directory to `PATH`, so the program can be run from anywhere
-   Beware that to run it with sudo on linux, [it is not that easy](https://docs.google.com/document/d/19CBUHtO0aUpg-kipnTrbQ3ozn_M1PiM0rH4IHoYrXS0/edit?usp=sharing).
-   add a new system variable `VCPKG_DEFAULT_TRIPLET`, so your default library version installed with vcpkg will be x64 (like our builds),  set it to:
	-   `x64-linux` for Linux Compilers
	-   `x64-windows` for MSVC
	-   `x64-MinGW` for MinGW
    
## CMake Integration
By default, CMake does not see the vcpkg. To set up the appropriate enviroment variables, paths, etc., we need to run cmake commands with path to cmake toolchain file: `vcpkg/scripts/buildsystems/vcpkg.cmake`. See the IDE and command line section for the detailed instructions how to execute cmake with the path to the vcpkg toolchain file. 

The toolchain file is executed early on, so it is safe to assume that the environment will be correctly set up before the commands in yor cmake script.

## Update
1.  `git pull`
2.  bootstrap vcpkg again
	1.  Windows: `bootstrap-vcpkg.bat`   
	2.  Linux: `bootstrap-vcpkg.sh`

## Update package
1. [Update vcpkg](#update)
2. `vcpkg update` to get a list of available updates
3. `vcpkg upgrade --no-dry-run` to actually perform the upgrade
	- you can supply the name of the package (e.g., zlib:x64-windows) as an argument to upgrade just one package

## Package Features
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

## Directory Structure
### Module Installation Scripts
They are located in the `ports` directory. There is no special way how to update just the port dir, so update the whole vcpkg by `git pull` in case you need to update the list of available packages.

### Modules
Vcpkg has it s own `find_package` macro in the toolchain file. It executes the script: `vcpkg/installed/<tripplet>/share/<package name>/vcpkg-cmake-wrapper.cmake`, if exists. Then, it executes the cmake scripts in that directory using the standard `find_package`, like a cmake config package.



# IDE

## Clion

### Configuration
#### Set default layout
`Window` -> `Layouts` -> `Save changes in current layout`


#### Set up new surround with template
In Clion, there are two types of surround with templates: `surrond with` and `surround with live template`. The first type use simple predefined templates and cannot be modified. However, the second type can be modified and new templates can be added. 


### Toolchain configuration
Go to `settings` -> `Build, Execution, Deployment` -> `toolchain`, add new toolchain and set:
-   Name to whatever you want
-   The environment should point to your toolchain:
	-   MSVC: `C:\Program Files (x86)\Microsoft Visual Studio\2019\Community`
	-   MSYS: `C:\MSYS2` 
	-   WSL: From the drop-down list, choose the environment you configured for using with CLion in the previous steps
-   Credentials (WSL) click to the setting button next to the credentials and fill
	-   host: `localhost`
	-   port: `2222`
	-   user and password according to your WSL system credentials
-   Architecture (non WSL): amd64
-   CMake: `C:\Program Files\CMake\bin\cmake.exe`, for WSL, leave it as it is
-   other fields should be filled automatically

### Project configuration
Most project settings resides (hereinafter *Project settings*) in `settings` -> `Build, Execution, Deployment` -> `CMake`. For each build configuration, add a new template and set:
-   `Name` to whatever you want   
-   `Build type` to `debug`
-   To `Cmake options`, add:
	-   path to vcpkg toolchain file:
		-   Linux: `-DCMAKE_TOOLCHAIN_FILE=/opt/vcpkg/scripts/buildsystems/vcpkg.cmake`
		-   Windows: `-DCMAKE_TOOLCHAIN_FILE=C:/vcpkg/scripts/buildsystems/vcpkg.cmake`
	-   Set the correct vcpkg triplet
		-   MSVC:   `-DVCPKG_TARGET_TRIPLET=x64-windows`
		-   MinGW:  `-DVCPKG_TARGET_TRIPLET=x64-MinGW`
		-   Linux: `-DVCPKG_TARGET_TRIPLET=x64-linux`

#### WSL extra configuration
The CLion does not see the WSL's environment variables (as of 2023-03, see [here](https://intellij-support.jetbrains.com/hc/en-us/community/posts/5633934229906-Programs-cannot-get-environment-variables-from-wsl)). To fix it, go to *Project settings* and set add the necessary environment variables to `Environment` field. 


### WSL configuration - Deprecated
Clion connects to WSL through SSH. Therefore, you need to configure SSH in WSL. To do it, run the following script:

```
wget https://raw.githubusercontent.com/JetBrains/clion-wsl/master/ubuntu_setup_env.sh && bash ubuntu_setup_env.sh
```
  
Next, It’s necessary to modify the WSL/create the WSL initialization script to fix a CMake issue when connecting from CLion. Download the wsl.conf file, and put it in /etc/.  The restart the WSL (wsl.exe -t Ubuntu-20.04)
    
## Visual Studio
### Installation
1.   Install Visual Studio
2.   Open/Create a CMake project
3.  Install ReSharper C++

### Setting Synchronization
1. Sign-in in Visual Studio using a Mictosoft account. [A lot of settings should be synchronized automatically](https://docs.microsoft.com/en-us/visualstudio/ide/synchronized-settings-in-visual-studio?view=vs-2022).
2. Apply the layout: `Window` -> `Apply Window Layout` -> `<Layout Name>`
3. Sync ReSharper settings: you can share the file: `%APPDATA%\JetBrains\Shared\vAny\` (`~\AppData\Roaming\JetBrains\Shared\vAny\`). 
	- This does not work good though as the files are changed on both sides constantly.
	- unfortunately, as of 01/2023, there is no good way how to share resharper settings
4. Install roamed plugins

### Basic Configuration
1. [Add 120 char guideline](https://marketplace.visualstudio.com/items?itemName=PaulHarrington.EditorGuidelines)
	- install the extension 
	- add the guideline in command window: `Edit.AddGuideline 120`
	- if there is an error *extension ... did not load properly*, you need to install the *developer analytic tools* package to the Visual Studio:
		- Visual Studio Installer -> `modify`
		- Go to the `Individual Components` tab
		- search for the extension and select it
		- proceed with the Visual Studio Modification
1. If you need to use the system CMake, configure it now (described below)
1. If you use `*.tpp` file, configure a support for them (described below).


installation
#### Enable template implementation files (`.*tpp`) syntax highlighting:
-   Go to `Tools` -> `Options` -> `Text Editor` -> `File Extension`
-   select Microsoft Visual C++
-   write `tpp` to the field and click add
-   (reopen the file to see changes)

#### To Change the Build Verbosity
1. Go to `Tools` -> `Options` -> `Projects and Solutions` -> `Build and Run`
2. Change the value of the MSBuild project build output verbosity.
    
### Project Setting

#### Configure Visual Studio to use system CMake:
-   Go to `Project` -> `CMake Settings`
-   it should open the `CMakeSettings.json` file
-   Scroll to the bottom and click on `show advanced settings` 
-   Set the CMake executable to point to the `cmake.exe` file of your system CMake 

#### Build Setting and Enviromental Variables
The build configuration is in the file `CMakePresets.json`, located in the root of the project. The  file can be also opened by right clicking on `CMakeLists.txt` ad selecting `Edit CMake presets`.

##### Set the CMake Toolchain File
To set the vcpkg toolchain file add the following value to the base configuration `cacheVariables` dictionary:
```json
"CMAKE_TOOLCHAIN_FILE": {
    "value": "C:/vcpkg/scripts/buildsystems/vcpkg.cmake",
    "type": "FILEPATH"
}
```

##### Set the Compiler
The MSVC toolchain has two compiler executables, default one, and clang. The default compiler configuration looks like this:

```json
"cacheVariables": {
	...
	"CMAKE_C_COMPILER": "cl.exe",
	"CMAKE_CXX_COMPILER": "cl.exe"
	...
},
```

To change the compiler to clang, replace `cl.exe` by `clang-cl.exe` in both rows.

##### Old Method Using CMakeSettings.json
We can open the build setting by right click on `CMakeList.txt` -> `Cmake Settings`

To configure configure vcpkg toolchain file: Under `General`, fill to the `Cmake toolchain file` the following: `C:/vcpkg/scripts/buildsystems/vcpkg.cmake`

To configure the enviromental variable, edit the `CmakeSettings.json` file directly. The global variables can be set in the `environments` array, the per configuration ones in `<config object>/environments` ([exmaple](https://devblogs.microsoft.com/cppblog/set-environment-variables-for-debug-launch-and-tools-with-cmake-and-open-folder/)).

#### Launch Setting 
The launch settings determins the launch configuration, most importantly, the run arguments. To modify the run arguments:
 1. open the `launch.vs.json` file:
	- use the context menu:
			-   Right-click on `CMakeLists.txt` -> `Add Debug Configuration`
			-   select `default`
	- or open the file directly, it is stored in `<PROJECT DIR>/.vs/`
2.   in `launch.vs.json` configure:
		- `type`: `default` for MSVC or `cppgdb` for WSL
		- `projectTarget`: the name of the target (executable)
		- `name`: the display name in Visual Studio
		- `args`: json array with arguments as strings
			- arguments with spaces have to be quoted with escaped quotes
		- `cwd`: the working directory
3.  Select the launch configuration in the drop-down menu next to the play button

[`launch.vs.json` reference](https://learn.microsoft.com/en-us/cpp/build/launch-vs-schema-reference-cpp?view=msvc-170)

##### Other launch.vs.json options
- `cwd`: the working directory

[Microsoft reference for `launch.vs.json`](https://learn.microsoft.com/en-us/cpp/build/launch-vs-schema-reference-cpp?view=msvc-170)

### WSL Configuration
For using GCC 10:
- go to `CmakeSettings.json` -> `CMake variables and cache`
- select `show advanced variables checkbox`
- set `CMAKE_CXX_COMPILER` variable to `/usr/bin/g++-10`


### Other Configuration
- show white spaces: `Edit` -> `Advanced` -> `View White Space`.
- configure indentation: described [here](https://docs.microsoft.com/en-us/visualstudio/ide/reference/options-text-editor-all-languages-tabs?view=vs-2022)


### Determine Visual Studio version
At total, [there are 5 different versionigs related to Visual Studio](https://blog.knatten.org/2022/08/26/microsoft-c-versions-explained/). 

The version which the [compiler support table](https://en.cppreference.com/w/cpp/compiler_support) refers to is the version of the compiler (`cl.exe`).
we can find it be examining the compiler executable stored in `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64`.

### Problems & solutions
#### Cannot regenerate Cmak cache
go to `./vs` and look for file named `CmakeWorkspaceSettings`. It most likelz contains a line with `disable = true`. Just delete the file, or the specific line.
    
# Installing Library Dependencies

## Vcpkg Libraries
-   type `vcpkg list`, if the library you need is not listed, continue to the next steps
-   type `vcpkg search <library simple name>` and inspect the result to determine the exact name of the package you need
-   if the library is not listed, check the presence in [vcpkg repo](https://repology.org/projects/?inrepo=vcpkg)
-   if the library is in repo, but search does not find it, [update vcpkg](#update)
-   type `vcpkg install <exact name>` to install the package
-   at the end of the installation log, there will be a cmake command needed to integrate the library, put it to the appropriate place to your `CMakeList.txt file`
    
### Boost
With boost, we should install only the necessary components. Then to include boost, we need:
- `find_package(Boost REQUIRED)`
	- with all compiled components listed
- `target_include_directories(<YOUR TARGET NAME> PUBLIC ${Boost_INCLUDE_DIRS}) `




### JNI
for JNI, a `JAVA_HOME` system property needs to be set to the absolute path to the JDK, e.g., `C:\Program Files\Java\jdk-15.0.1`

## Gurobi
 1.  If you don’t have Gurobi installed, do it now, and check that the installation is working
	-   Windows: just install as usual  
	-   Linux:
		1. download the archive to `/opt`
		2. `sudo tar xvfz <gurobi archive>`
		3. add the the [file that introduce environment variables needed for gurobi](https://drive.google.com/file/d/1Vr5VReq2_rOMNm4bsC7HJ9xELeiKeiTR/view?usp=sharing) to `etc/profile.d`
 2.  **Linux only:** it is necessary to build the C++ library for your version of the compiler. Steps:
    	1. `cd <GUROBI DIR>/linux64/src/build/`
    	2. `make`
    	3.  `mv libgurobi_c++.a ../../lib/libgurobi_c++_<some id for you, like version>.a`
    	4.  `cd ../../lib/`
    	5.  `ln -sf ./libgurobi_c++<some id for you, like version>.a libgurobi_c++.a`
 3.   Follow [this guide](https://support.gurobi.com/hc/en-us/articles/360039499751-CMake-C-C-compilation-of-Gurobi-projects), specifically:
		1.   put the attached  [our custom FindGUROBI script](https://drive.google.com/file/d/1h9JovBfjxnnQKLjBPIjSfQQpmEhn3VKC/view?usp=sharing) to: 
			 - Windows: `C:\Program Files\CMake\share\cmake-<your cmake
   version>\Modules/`
			 - Linux: `/opt/<CMAKNAME>/share/cmake-<VERSION>/Modules`
		2.   to your `CMakeLists.txt`, add:
				-   `find_package(GUROBI REQUIRED)`
				-   `target_include_directories(<your executable> PRIVATE ${GUROBI_INCLUDE_DIRS})`
				-   `target_link_libraries(<your executable> PRIVATE ${GUROBI_LIBRARY})`
				-   `target_link_libraries(<your executable> PRIVATE optimized ${GUROBI_CXX_LIBRARY} debug ${GUROBI_CXX_DEBUG_LIBRARY})`
		3.   try to load the cmake projects (i.e., generate the build scripts using cmake).
		4.   if the C++ library is not found (`Gurobi c++ library not found`), check whether the correct C++ library is in the gurobi home, the file `<library name>.lib` has to be in the `lib` directory of the gurobi installation. If the file is not there, it is possible that your gurobi version is too old

### Update Gurobi
-   Updating is done by [installing the new version](https://www.gurobi.com/downloads/gurobi-software/) and generating and using [new licence key](https://www.gurobi.com/downloads/end-user-license-agreement-academic/).
-   after update, you need to delete your build dir in order to prevent using of cached path to old Gurobi install
- Also, you need to update the library name on line 10 of the `FindGUROBI.cmake` script.




## Other Libraries Not Available in vcpkg
### Test Library linking/inclusion
For testing purposes, we can follow this simple pattern:
1. build the library
2. include the library: `target_include_directories(<target name> PUBLIC <path to include dir>)`, where include dir is the directory with the main header file of the library.
3. if the library is not the header only library, we need to:
	3.1  link the library: `target_link_libraries(<target name> PUBLIC <path to lib file>)`, where path to lib file is the path to the dynamic library file used for linking (`.so` on Linux, `.lib` on Windows).
	3.2. add the dynamic library to some path visible for the executable
		- here the library file is `.so` on Linux and `.dll` on Windows
		- there are plenty options for the visible path, the most common being the system `PATH` variable, or the directory with the executable. 


## Dependencies with WSL and CLion
In WSL, when combined with CLion, some find scripts does not work, because they depend on system variables, that are not correctly passed from CLIon SSH connection to CMake. Therefore, it is necessary to add hints with absolute path to these scripts. Some of them can be downloaded [here](https://drive.google.com/drive/folders/1rWVl_T3p0cIf6QBYFtc-sEfuA-TUs2CU?usp=sharing). Package that require these hints:
-   JNI
-   Gurobi
    


# Refactoring
The refactoring of C++ code is a complex process, so the number of supported refactoring operations is limited. In Visual Studio, the only supported refactoring operation is renaming. In IntelliJ tools (CLion, ReSharper C++), there are more tools available, but still, the refactoring is not as powerful nor reliable as in Java or Python.

Other alternative is to implement the refactoring manually, with a help of some compiler tools like [clang Refactoring Engine](https://clang.llvm.org/docs/RefactoringEngine.html) ([example project](https://github.com/realincubus/clang-refactor)). 


## Changing Method Signature
As of 2023-10, there is no reliable way how to change the method signature in C++. The most efficient tool is the method signature refactorin in either CLion or ReSharper C++. However, it does not work in all cases, so it is necessary to check and fix the code manually.



 # Compilation for a specific CPU
 ## MSVC
 MSVC cannot compile for a specific CPU or CPU series. It can, however, use new instructions sets more efficiently if it compiles the code without the support for CPUs thad does not support these instruction sets.

The command for the compiler is: `/arch:<set name> (see [MSVC documentation](https://learn.microsoft.com/en-us/cpp/build/reference/arch-x64?view=msvc-170) for details).


 ## GCC
 In GCC, the [`march`](https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html) option enables compilation for a specific hardware.
ml) option enables compilation for a specific hardware.

pects that you use vcpkg in a per-project configuration. To make it work, add: `-DCMAKE_TOOLCHAIN_FILE=<vcpkg location>/scripts/buildsystems/vcpkg.cmake`
	- To change build options (`option` in `CMakeLists.txt`), run cmake with `-D <option name>=<option value> <build dir>`. Example: `cmake -D BUILD_TESTING=OFF .`

    
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

### Specify the build type (Debug, Release)
To build in release mode, or any other build mode except for the default, we need to specify the parameters for CMake. Unfortunately, these parameters depends on the build system:
- **Single-configuration systems** (Unix, MinGW) 
- **Multi-configuration systems** (Visual Studio)

#### Single-configuration systems
Single configuration systems have the build type hardcoded in the build scripts. Therefore, we need to specify the build type for CMake when we generate the build scripts:
```bash
cmake ../ -DCMAKE_BUILD_TYPE=Release
```
**By default, the build type is `Release`**.

#### Multi-configuration systems
In multi-configuration systems, the `-DCMAKE_BUILD_TYPE` parameter is ignored, because the build configuration is supposed to be determined when building the code (i.e., same build scripts for debug and for release). Therefore, we omit it, and instead specify the `--config` parameter when building the code:
```bash
cmake --build . --config Release
```

### Specify the target
We can use the `--target` parameter for that:
```cmake
cmake --build . --target <TARGET NAME>
```

## Clean the source files
Run:
```
cmake --build . --target clean
```


# Handling Case Insensitivity
Windows builds are, in line with the OS, case insensitive. Moreover, the Visual Studio does some magic with names internally, so the build is case insensitive even on VS WSL builds.

The case insensitivity can bring inconsistencies that later breake Unix builds. Therefore, it is desirable to have the build case sensitive even on Windows. Fortunatelly, we can toggle the case sensitivity at the OS level using this PowerShell command:

```PowerShell
Get-ChildItem <PROJECT ROOT PATH> -Recurse -Directory | ForEach-Object { fsutil.exe file setCaseSensitiveInfo $_.FullName enable }
```

Note that this can break the git commits, so it is necessary to also configure git in your case-sensitive repo:
```
git config core.ignorecase false
```




