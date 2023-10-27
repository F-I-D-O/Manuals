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


# Testing private methods
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