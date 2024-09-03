# Compilation

## General rules

-   Make the code you want to compile reachable.  **In C++, only reachable methods/classes are compiled!**
-   Solve errors that stop the compilation first.
-   Warnings can stay in logs even if solved until the main error is gone and the build is finished
-   Be aware that the cause of the error can be on a different line than the one in the error log!

### If the source of the compilation bug cannot be found
1.  read the error examples below
2. check that the code follow the [my guidelines](https://drive.google.com/file/d/1fIwSVqSojOxIZFJCvSszu4xEUvfVPA5P/view?usp=sharing) and [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html). 
3.  read the [cpp reference](http://cppreference.com) for the parts of the problematic code
4. check the *const correctness*. It is a causes a lot of problems.
5.  try a different compiler, the error message can be more informative
6.  try to isolate the case in some small example
7.  copy the project and remove the stuff until the problem is gone

## Practical static assertions
Test for concept satisfaction:
```cpp
static_assert(My_concept<My_class>);
```
### Useful Predicates
- [`std::is_same_as`](https://en.cppreference.com/w/cpp/types/is_same) for checking the type equality. 

## Determining type at compile time
Sometimes, it is practical to know the exact type during compile time. There is no direct way for that, but we can trick the compiler to print the type in an error message:
```cpp
template <typename...> struct Get_type;
class Something {};
Get_type<<TYPE TO GET>> my_type{};
```

This should print an error message similar to: `error: variable ‘Get_type<<TYPE TO GET RESOLVED>> my_type’ has initializer but incomplete type`.

## Errors with a missing copy constructor
e.g. `error C2280: 'Solution<N>::Solution(const Solution<N> &)': attempting to reference a deleted function`

These can be split into two groups:

### We want to copy the object, but the copy constructor is missing

### We do not want to copy the object, but the copy constructor is still called

First, check if the class is move-constructible in the first place:

```cpp
static_assert(std::is_move_constructible<Solution<Cordeau_node>>::value);
```
  
If the above check fails, check why the move constructor is not present. Possible reasons, why the move constructor is not available:

1.  Move constructor is not implicitly declared due to a broken rule of five, i.e., one of the other constructors/assignments/destructors is defined
2.  Implicitly declared move constructor is deleted. Possible reasons:
	-  the class have a member that cannot be moved from
    -   const member
    
If the check passes, and the copy constructor is still being called:

## Errors with missing move constructor
First, we should check whether the object's type `T` is movable using `static_assert(std::is_move_constructible_v<T>)`

If the static assertion is false:
1. Check whether all base classes has move constructors available
	- the `std::is_move_constructible_v<T>` cannot be used for that, as the move operations can be protected. Instead, look for the presence of the move constructors in base classes (any base class should have them declared, as the implicit declaration of copy/move/destruction does not work with virtual classes)
2. Check whether all class members are move constructible using the `std::is_move_constructible_v<T>` concept. Do not forget the const qualifiers!

## Multiply Defined Symbols
e.g. name already used for a template in the current scope. The source of the duplicate should be in the compiler output. Usually, this can be solved by using namespaces.

## Conversion is inaccessible
This mostly happens if we forgot to add the `public` keyword when inheriting from a base class, resulting in the (default) private inheritance.

## Cannot convert from 'initializer list' to...
This happans when there is no function signature matching the arguments. Sometimes, the specific argument can be found by using constructor instead of initializer list. Otherwise, check the arguments one by one. For each argument:
1. check if the type matches
2. check if the value type matches, i.e. value/ref/pointer
3. **check if the const matches**
4. check if the problem is not in wrong template argument deduction. The automatic deduction can use value type instead of reference type...

## Returning address of local variable or temporary
This happens when we assign a lambda to `std::function` and the labda return by reference and does not have an explicit return type. The solution is to add an explicit return type.

## Cannot resolve symbol
or alternatively: `'identifier' was unexpected here; expected 'type specifier'`.

It simply means that the type cannot be reolved from the code location.

Possible reasons:
- Circular dinclude

# Linker Errors

## Undefined
Something like `unresolved external symbol...`.

1.  check that all used files are listed in `CMakeLists.txt` (`add_executable` command…)
2.  check that all templates are defined in header files
3.  check that all functions are defined correctly (even `unsigned` vs `unsigned int` can make problems...)
4.  check this list: [https://stackoverflow.com/questions/12573816/what-is-an-undefined-reference-unresolved-external-symbol-error-and-how-do-i-fix?](https://stackoverflow.com/questions/12573816/what-is-an-undefined-reference-unresolved-external-symbol-error-and-how-do-i-fix?)
    

## Multiply Defined
1.  Check the recent includes, are all of them correct?
2.  Check the multiply defined symbol. If it is a function defined in a header file, it has to be static or inline.
1.  there can be a bug even in an external library!
    
[https://stackoverflow.com/questions/30180145/general-techniques-for-debugging-the-multiple-definition-of-error](https://stackoverflow.com/questions/30180145/general-techniques-for-debugging-the-multiple-definition-of-error)



# Runtime errors
**First, identify the exception context**. To do that, look at the line where the exception is thrown. If the throwing line is not on the call stack, it is possible that the debugger does not break on the particular exception type. to change that go to the `Exception Settings` and check the exception type there.

If the cause of the exception is not clear from the context, it may be usefull to **check the exception details**. First, look at the exception message. The easiest way is to catch the exception in the code and print the message. In Google Test, there is a catch-all handler, just run the test without the `--gtest_break_on_failure` flag. 

If the message is not enough, look at the exception content in the debugger. Unfortunately, it is not possible to inspect unhandled exception object easily. To do so, add the following watch:

```cpp
(<exception type>*) <exception address>
```
where `<exception type>` is the type of the exception (e.g. `std::exception`) and `<exception address>` is the address from the exception dialog.

Finally, if the cause of the exception is still unclear, look at the exception type, and proceed to the respective section below, if there is one. 


## Error codes
Error codes are the only thing visible when the exception is not caught and no debugger is attached. Unfortunately, the error codes are platform-specific, and mostly undocumented even for operating system facilities and standard libraries. 


### Windows Error Codes
On windows, many error codes can be emitted by the system or standard libraries:
- `0x0` to `0x3e7f`: [Win32 error codes](https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes): Errors emitted by Windows high-level functionalities
- `0xC0000000` to `0xCFFFFFFF`: [NT status codes](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-erref): Standardized 32-bit error codes used in Windows kernel, drivers, and protocols. Notable examples:
  - [`0xC0000005`](https://learn.microsoft.com/en-us/shows/inside/c0000005): Access violation



## Improve debugger experience with natvis
[Natvis](https://learn.microsoft.com/en-us/visualstudio/debugger/create-custom-views-of-native-objects?view=vs-2022) is a visualization system that enables to enhance the presentation of variables in debugger locals or watch windows. It is a XML file, where we can define visualization rules for any type. Structure:
```XML
  <Type Name="My_class">
    ... visualization rules
  </Type>
```
The name must be fully qualified, i.e., **we have to include namespaces.**

The big advantage is that **natvis files can be changed while the debugger is running** and the presentation of the type in locals/watch window is changed immediatly after saving the natvis file.

### Natvis expressions
The expression in natvis are sorounded by `{}`. If we want curly braces in the text, we can double them `{{...}}`.
**Unfortunatelly, function calles cannot be used in natvis expressions**.

### Natvis Errors
Natvis errors can be displayed in the output window if turned on in settins: `Debug` -> `Options` -> `Debugging` -> `Output Window`.

### Existing visualisations
Existing natvis files are stored in `<VS Installation Folder>\Common7\Packages\Debugger\Visualizers` folder. The STL visualizations are in `stl.natvis`


## Debugger manual
Be aware that in **CLion debugger, the program does not terminate on unhandled exceptions by default.** 

### Address breakpoints
Address breakpoints can be used to watch a change of a variable or in general, a change of any memory location.

To set an address breakpoint, we nned to first find the address of the variable. To do that, we can:
- use the `&` operator on the variable in the watch window
- use the `&` operator on the variable in the immediate window

The address should have a format `0x0000000000000000`.




## Memory Errors
These exception are raised when an unallocated memory is accesed.  The following signalize a memory error:
- *Read Access Violation*
-  *HEAP CORRUPTION DETECTED* 

First, **most of the memory errors can be caught by various assertions and guards in the debug mode.** If possible, try to run the program in the debugg mode, even if it takes a long time, because this way, you can catch the problem when it happens, before the memory is corrupted. If that does not help, read the following sections.

Other reassons are also discussed [here](https://localcoder.org/access-violation-exception-when-calling-a-method)

### Accessing null pointer 
A frequent cause of memory errors is accessing a null pointer object's data. In this case, the cause of the problem can be quickly determined in the debugger. Just follow the lifetime of the pointer and find the momemnt when it becom null.

### Read Access Violation Caused by a Demaged vtable
In case of some previous memory mismanagement, the heap can be demaged, possibly resulting in a corrupted virtual table for objects on the heap. 
To check whether the virtual table is corrupted, add the following watch to the debugger:
```cpp
<var name>.__vfptr
```
Where `<var name>` is the name of the object you want to inspect.

To resolve this problem, see debugging memory errors.

### Using Application Verifier to find causes of memory related errors.
A lot of memory errors can be caught just by running the program in the debugger. The STL containers, for example, containst various assertions that break the code on wrong memory access related to these collections. 

To add even more assert guards (e.g., for dynamic arrays), we can use the [Application Verifier](https://docs.microsoft.com/en-us/windows-hardware/drivers/devtest/application-verifier) which is installed as a part of Windows SDK (which is typically installed together with Visual Studio).

To debug the application with the Application verifier enabled:
1. Open AV
2. `right click` -> `add executable` and select the executable to test 
3. select the appropriete test suite (the basic one is enouh for the memory testing)
4. click save
5. close AV
6. run the executable in the debugger, find the problem, fix it
7. open AV
8. delete the exectable from the list


### Using Address Sanitizer
A linux memory tool called address sanitizer can be used to debug memory related errors. To use it from the Visual Studio:
1. Check that the `libasan` lib is installed on WSL
1. In Cmake Settings for the debug configuration, check `Enable AddressSanitizer`
1. build the project
1. run

The program should now break on the first problem. The details are displayed in the output window

More at [Microsoft learn](https://learn.microsoft.com/en-us/cpp/linux/linux-asan-configuration?view=msvc-170&viewFallbackFrom=vs-2019#install-the-asan-debug-symbols)


### Using Valgrinfd to debug memory errors
Valgrind is a toolbox for debugging C/C++ code. The most famous tool is calle [Memcheck](https://valgrind.org/docs/manual/mc-manual.html) and is intended for memory error detection.
Basic usage:
```bash
valgrind --leak-check=yes <program> <program arguments>
```

The explanation of the error messages can be found on the [Valgrind website](https://valgrind.org/docs/manual/mc-manual.html#mc-manual.errormsgs)


The most common errors and tips:
- `Conditional jump or move depends on uninitialised value`:
  - triggers on the first usage (not copy) of the uninitialized data
  - note that the uninitialized variable can look normal (e.g. if it is a number), just the value is random.
- `Invalid read of size ...`:
  - can happen to both stack and heap memory
  - the content can still be in memory, it just means that the memory has been freed/invalidated.


There are some expected messeges not to be worried about:
```
Warning: set address range perms: large range
```



## Logical Errors
### C++ Specific Numerical Errors
- First possible error is *overflow*. **C++ does not handle or report overflow!** The behaviour is undefined.
- Second potential danger is the *unsigned integer overflow*. In case the result below zero is stored in unsigned integer, the number is wrapped around, resulting in large positive integer.
- Another thing is that when signed and unsigned integers are used in one operation, the **signed integer is implicitely converted to unsigned integer before the operation!** This is called promotion and it also works for other types (see in a [table on SO](https://stackoverflow.com/questions/5563000/implicit-type-conversion-rules-in-c-operators)).

In general to prevent the overflow:
- check each operation for the potential overflow, inluding the unsigned integer overflow with negative numbers
- if the overflow can happen, cast the types before any arithmetic operation to prevent the overflow
- also, one have to use the right type in templates like `std::max`

# Testing - Google Test

## Debugging tests

To debug a test, you need to run it with the flag some flags:

-   `--gtest_break_on_failure`. This flag breaks the test on a failed test or failed assertion.
-   `--gtest_catch_exceptions=0`. This flag stops google test from catching exceptions, hence the program breaks at the place where the exception occurred, which is what you want
-   `--gtest_filter=Some_test_prefix*` for choosing just some tests

Also, you need to run tests from Visual Studio, otherwise, the program ends when clicking on the retry button.

# Visual Studio Errors
## False errors appears in a file / in many files
1. close visual studio
2. delete the `out` folder
3. open the visual studio again

## Refactoring options not present
If the refactoring options like change signature are not present, try to send the Resharper bug reports :), or create a new project.

## IntalliSense false errors
Sometimes, the errors disappears by deleting the `.suo` file located in `<project dir>/.vs/<project name>/<VS version>`


# Running the debugger

## Clion
Unlike in Visual Studio, the Clion debugger does not break be default. To break on exceptions or breakpoints, we need to use the debug button instead of the run button.

To debug multiple targets at once:
1. Open the `Run/Debug Configurations` dialog
2. Add a new configuration of type `Compound`
3. Add the configurations you want to run together using the `+` button
4. Debug the compound configuration



# Profiling
There are multiple [profiler options for C++](https://docs.google.com/spreadsheets/d/1nvOmqWVMX6H1Q-Y6JDqRW5Ocaj6oPoKDQogz2kRkHHE/edit?usp=sharing), but not all the tools are easy to use or maintained.

## CPU Profiling
### VTune
VTune can be run ftom the Visual Studio only for VS solution projects. In case of CMake projects, we need to run the VTune GUI and configure the debugging there.

## Memory Profiling 
For memory profiling to work, two things needs to be taken care of:
- if the application allocates a lot memory inside parallel region, **disable paralelization** for profiling. Otherwise, there can be too many allocation events for the profiler to handle 
- if you use a custom memory allocator, disable it and use a standard allocator for memory profiling

### Memory Profiling in Visual Studio
To profile memory in Visul Studio
1. Set a breakpoint before the region of interest
2. Run the app and wait for the hit
3. In `Diagnostic Tools` tab -> `Summary`, click `Enable heap profiling for next session`
4. Restart the app and wait for the hit.
5. Take memory snapshot
6. Add a breakpoint to the end of the region of interest
7. Wait for the hit, take snapshot and check both snapshots

### Memory