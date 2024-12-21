Native libraries are an important part of programming in most languages. They allow us to run the code without the need for an interpreter or virtual machine. 

Native libraries can be written in any language that can be compiled to machine code. This includes C, C++, Rust, and many others.

There are two ways how to link a native library to your code: statically and dynamically:

- *Static libraries* are linked at compile time. This means that the library code is included in the final executable. This makes the executable larger, but it also means that the executable is self-contained and does not require the library to be installed on the target system.
- *Dynamic libraries* are usually linked at runtime. This means that the library code is not included in the final executable. Instead, the executable loads the library code from a separate file when it is run. This makes the executable smaller, but it also means that the library must be installed on the target system.

Each operating system has its own way of loading and using native libraries. Also,  The following table shows the extension of the library file for each operating system:

| Operating System | Static Library Extension | Dynamic (shared) Library Extension |
|------------------|--------------------------|---------------------------|
| Windows          | .lib                     | .dll                      |
| Linux            | .a                       | .so                       |

# Deciding between static and dynamic libraries
When deciding between static and dynamic libraries, there are a few things to consider:

| Property | Static Libraries | Dynamic Libraries |
|----------|------------------|-------------------|
| Memory footprint | Each executable includes a copy of all used library code | All executables share the same copy of the library code |
| Modularity | None | We can extend the functionality of the program by adding new shared libraries |
| Licensing | Some licenses (e.g. GPL) require that the source code of the library is made available if the library is linked statically | The library can be linked dynamically without having to make the source code available |
| Symbol export | All symbols are exported by default | Only symbols marked for export are exported |
| Linking of transitive dependencies | All transitive dependencies must be linked explicitly | Transitive dependencies are loaded automatically at runtime | 

Historically, there were other factors that are not relevant anymore:

- *Size*: The historical argument was that dynamic libraries can save disk space because only one copy of the library is needed in the system. However, a) disk space is cheap now and b) dynamic libraries are now distributed with the application on many platforms.
- *Maintenance*: The historical argument was that dynamic libraries are easier to maintain because they can be updated without recompiling the application and distributing a new version. However, this is now not true because on many platforms the dynamic libraries are distributed with the application.
- *Portability*: The historical argument was that static libraries are more portable because they do not depend on the presence of the library on the target system. However, we can distribute dynamic libraries with the application to mitigate this issue of dynamic libraries.


So finally, how to decide between static and dynamic libraries? 

- We create a library that will be used by many applications, and it is large -> dynamic libraries.
- We use a GPL library and we do not want to make the source code available -> dynamic libraries.
- Users are expected to only use a fraction of the library -> static libraries.
- Otherwise -> it does not matter.


# Runing a program depending on a native library
When running a program that depends on a native library, the operating system must be able to find the library. This search has a special logic and, most importantly, **there is no guarantee** that

- the library found is the one that the program was compiled and linked against, or
- that the library will be found at all.

A typical problem scenario:

1. The program is compiled and linked against a new version of the library.
2. An older version of the library is installed in a location that is searched before the location of the new version.
3. The library API has changed between the two versions.
4. The program crashes at runtime

The **search order** differs between operating systems. Here, we present only the  short (incomplete) order. See official documentation ([Windows](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order)) for full version. On Windows:

1. The directory containing the executable
1. The system directory and the Windows directory
1. The CWD (folder where the program is run)
1. The directories listed in the PATH environment variable in the order they are listed
