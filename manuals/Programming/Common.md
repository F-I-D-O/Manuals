# Keymap

- **Copy**: `Ctrl` + `C`
- **Cut**: `Ctrl` + `X`
- **Paste**: `Ctrl` + `V`
- **Toggle comment**: `Ctrl` + `Q`
- **Search in file**: `Ctrl` + `S`
- **Sellect all**: `Ctrl` + `A`
- **Format selection**: `Ctrl` + `F`
- **Format File**: `Ctrl` + `Shift` + `F`
- **Build**: `Ctrl` + `B`

## Refactoring

- **Rename**: `Ctrl` + `R` 
- **Change signature**: `Ctrl` + `G`
- **Text transform**: `Ctrl` + `T`
    - ` + U`: to upper case
- **Surround with**: `Ctrl` + `W`



# Command Line Interface (CLI)
This chapter should guide you on how to design CLI in a user-friendly and predictable way. Mostly, it follows the [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html), with the [GNU long option extensions](https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html).

There are two main types of CLI arguments:

- **Options**: (e.g., `--help`, `-h`) are used to change the behavior of the program. They are usually optional and can be in any order.
- **Operands**: (e.g., `file.txt`) are the input data for the program. They are usually required and their order is important.

All operands should be placed after all options. 


## Options
Options can be of two types:

- **Short options**: (e.g., `-h`) are one character long and are prefixed with a single dash.
- **Long options**: (e.g., `--help`) are multi-characcter and are prefixed with two dashes.

Options can have arguments:

- **Short options** and their arguments are separated by a space or can be concatenated, e.g., `-o file.txt` or `-ofile.txt`. The first variant is strongly recommended.
- **Long options** and their arguments are separated by a space or can be concatenated with an equal sign, e.g., `--output file.txt` or `--output=file.txt`. 

Also, short options can be grouped, e.g., `-h -v -o file.txt` can be written as `-hvo file.txt`.


## Multiple values in one option or operand
If an option or operand contains multiple values (e.g., a list of files), the values should be separated by a comma, e.g., `--files file1.txt,file2.txt,file3.txt`.



# Exceptions
Exceptions should be used to handle erroneus situations that are expected to happen. Exceptions should **not** be used for:

- **Flow control**, e.g., parse float from input, catch exception and try integer, then catch exception and try string... 
- **Unexpected situations**, e.g., a method should always return a positive number, but it returns a negative one. For this we should use assertions, not exceptions.

There are many types of exceptions, encapsulating different types of error description data. However, to begin with, it is not important to use some specific exception type. Using some general exception class is always much better than not using exceptions at all.


# Tests
There are many types of software tests:

- **Unit tests**: The most common and known ype of tests. They test individual units of code, e.g., functions, classes, or modules.
- **Integration tests**: test how different units of code work together.
- **Functional tests**: test the functionality of the software from the user's perspective.
- [**Smoke tests**](https://en.wikipedia.org/wiki/Smoke_testing_(software)): Test the minimum functionality of the software.
    - sometimes, it just builds the software. In this case, it may be called a *build verification test*.
    - sometimes, it runs the software with a minimal set of inputs. This way, we can check if the runtime libraries are correctly linked and if the software can be executed.
- [**Regression tests**](https://en.wikipedia.org/wiki/Regression_testing): test if the new version of the software behaves the same as the previous one. This can mean testing the equivalence of:
    - the output of the software,
    - the performance of the software,
    - the compilation time or the size of the binary,..

Test cases for each test type can be written using two main approaches:

- [**Black-box testing**](https://en.wikipedia.org/wiki/Black-box_testing): the test cases are written without knowing the internal structure of the software. It does not require any knowledge of the implementation details. However, it can be less effective in finding bugs: multiple test cases can test the same functionality, and some functionalities can be left untested.
- [**White-box testing**](https://en.wikipedia.org/wiki/White-box_testing): the test cases are written with the knowledge of the internal structure of the software. It can be more effective in finding bugs, but it requires a deep understanding of the software. It can also lead to a situation where the tests are too tightly coupled with the implementation, and the tests need to be rewritten when the implementation changes.

Common terms in testing:

- **Test case**: a single test that checks a single aspect of the code.
- **Test suite**: a collection of test cases.
- **Test runner**: a tool that runs the test suite and reports the results.
- **Test fixture**: a set of initial conditions for a test case. Typically, it is a function that is run before *each* test case and that sets up the environment for the test case.

## Testing private methods
An urgent need to test privete method accompanied with a lack of knowledge of how to do it is a common problem. In almost all programming languages, the testing of private methods is obsturcted by the language itself, i.e., the test frameworks does not have a special access to private methods. In this section we disscuss the usuall solutions to this problem. These implementation is specific  to a particular language, but the general ideas are the same.

The possible approaches are:

- **Makeing the method public**: Only recommended if the method should be exposed, i.e., its functionality is not limited to the class itself.
- **Move the method to a different class**: Maybe, the method is correcly marked as private in the current context, but it can also be extracted to its own class, where it will become the main method of the class. This applies to methods that can be used in other contexts, or for methods contained in large classes.
- **Mark the method as internal and make it public**: This is a strategy that can be always applied with minimum effort. Various ways how to signalize that the method is intended for internal use are:
    - **Naming convention**: The method name can start with an underscore, e.g., `_my_method`.
    - **Documentation**: The comments can contain a warning that the method is intended for internal use.
    - **Namespace**: The method can be placed in a namespace that signals that it is intended for internal use, e.g., `internal::my_method`.
- **Special access**: We can use special language-dependant tools that can provide a special access to private methods:
    - in C++ the `friend` keyword can be used to grant access to a class to another class. 
    - In Java, the `@VisibleForTesting` annotation can be used to mark a method as visible for testing. 
    - In Python, the `__test__` attribute can be used to mark a method as visible for testing.


# Finding Duplicates
For finding duplicates, there are two possible approaches:

- **Using hash sets**: iteratively checking if the current element is in the set of already seen elements and adding it to the set if not. 
- **Sorting**: sorting the collection and then for each element checking if the current element is the same as the previous one. 

Comparison:
| Approach | Time complexity (worst case asymptothic)| Time complexity (average expected) | Space complexity | allocation complexity |
| --- | --- | --- | --- | --- |
| Sets | *O(log n)* (both contains and add) | *O(1)* (both contains and add) | *O(n)* | *O(1)* |
| Sorting | *O(n log n)* (sorting) | *O(n log n)* (sorting) + *O(n)* (duplicates check) | *0* or *O(n)* if we need to left the source collection unsorted | *0* or *O(1)* in case of new collection |


# JetBrains Products 

## Configuration

### Compact tabs

- **Settings** -> **Appearance & Behavior** -> **New UI** and select `Compact mode`

### Advanced Configuration - Registry
Sometimes, we need to edit advenced settings like with id `cidr.debugger.gdb.usePythonToLoadData`. This registry can be accessed by `Help` -> `Find Action...` -> type `Registry` -> find the desired setting.


## Troubleshooting


### Update is paused and does not resume even after closing the IDE
Probably, the IDE installation directory is blocked by some other process. Try to close the WSL. If it does not help, find out which process is blocking the directory (On Windows: `C:\Users\<User>\AppData\Local\Programs\<IDE name>`)


# Releasing the software
When releasing the software, you should follow the steps for each particular language and distribution channel. However, there are some common steps that should be done for each release which are described in this section, namely:

- **Versioning**: update the version number in the distribution files (e.g., `setup.py`, `pom.xml`, `package.json`, etc.).
- **Changelog**: update the changelog file with the new version and the changes.
- **License**: check if the license is present in all files and if it is up-to-date.

## Licenses
Licensing has two parts:

- add the `LICENSE` file to the root of the project if not already present and
- add the license to the top of each source file.

The first part is easy, just copy the license text to an empty file named `LICENSE` at the root of the project. To choose a license for your project, you can use the [Choose a License](https://choosealicense.com/) website.

The second part can be automated using the [licenseheaders fork]() of the original [licenseheaders](https://github.com/johann-petrak/licenseheaders) project. A typical usage is:
```bash
licenseheaders -t mit -o "Czech Technical University in Prague" -cy -n ShoDi -u "https://github.com/aicenter/ShoDi" -d C:\Workspaces\AIC\shortest-distances\
```
where:

- `-t mit` specifies the template to use (MIT license in this case),
- `-o "Czech Technical University in Prague"` specifies the organization name,
- `-cy` specifies to replace the years in the existing headers with the current year,
- `-n ShoDi` specifies the project name,
- `-u "https://github.com/aicenter/ShoDi"` specifies the project URL,
- `-d C:\Workspaces\AIC\shortest-distances\` specifies the directory to process.


