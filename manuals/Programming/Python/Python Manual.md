
# Basic Data types

## Numbers
Python has the following numeric types:

- `int` - integer
- `float` - floating point number

The `int` type is unlimited, i.e., it can represent any integer number. The `float` type is limited by the machine precision, i.e., it can represent only a finite number of real numbers.

### Check whether a float number is integer
To check whether a float number is integer, we can use the `is_integer` function:

### Check whether a number is NaN
To check whether a number is NaN, we can use the `math.isnan` function or the `numpyp.isnan` function:



## Strings
Strings in Python can be enclosed in single or double quotes (equivalent). The triple quotes can be used for multiline strings.

### String formatting
The string formatting can be done in several ways:

- using the `f` prefix to string literal: `f'{<VAR>}'`
- using the `format` method: `'{}'.format(<VAR>)`

Each variable can be formatted for that, Python has a [string formatting mini language](https://docs.python.org/3/library/string.html#formatspec). 

The format is specified after the `:` character (e.g., `f'{47:4}'` set the width of the number 47 to 4 characters). Most of the format specifiers have default values, so we can omit them (e.g., `f'{47:4}'` is equivalent to `f'{47:4d}'`).

The following are the most common options:

To use the character `{` and `}` in the string, we have to escape them using double braces: `{{` and `}}`. 

### String methods

- `capitalize`: capitalize the first letter of the string
- `lower`: convert the string to lowercase
- `upper`: convert the string to uppercase
- `strip`: remove leading and trailing whitespaces
- `lstrip`: remove leading whitespaces
- [`rstrip`](https://docs.python.org/3/library/stdtypes.html#str.rstrip): remove trailing whitespaces


## Checking the type
To check the exact type:
```python
if type(<VAR>) is <TYPE>:
# e.g.
if type(o) is str:
```

To check the type in the polymorphic way, including the subtypes:
```Python
if isinstance(<VAR>, <TYPE>):
# e.g.
if isinstance(o, str):
```

# Conditions and boolean context

## Comparison operators
Python uses the standard set of comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`).

They are functionally similar to C++ operators: they can be overloaded and the semantic meaning of `==` is equality, not identity (in contrast to Java).


## Automatic conversion to `bool`
Unlike in other languages, any expression can be used in boolean context in python, as there are rules how to convert any type to `bool`. The following statement is valid, foor example:
```Python
s = 'hello'
if s: 
    print(s)
```
The code above prints 'hello', as the variable `s` evaluates to `True`.

Any object in Python evaluates to `True`, with exeption of:

- `False`
- `None`
- numerically zero values (e.g., `0`, `0.0`)
- standard library types that are empty (e.g., empty string, `list`, `dict`)

The automatic conversion to bool in boolean context has some couner intuitive consequences. The following conditions are not equal:
```Python
s = 'hello'

if s: # s evaluates to True

if s == True: # the result of s == True is False, then False evaluete to False
```


# Functions

## Argument unpacking
if we need to conditionaly execute function with a different set of parameters (supposed the function has optional/default parameters), we can avoid multiple function calls inside the branching tree by using argument unpacking.

Suppose we have a function with three optional parameters: `a`, `b`, `c`.
If we skip only last *n* parameters, we can use a `list` for parameters and unpack it using `*`:
```Python
def call_me(a, b, c):
    ...

l = ['param A', True]
call_me(*l) # calls the function with a = 'param A' and b = True
``` 

If we need to skip some parameters in the middle, we have to use a dict and unpack it using `**`:
```python
d = {'c': 142}
call_me(**d) # calls the function with c = 142
```


```


# String formatting
To format python strings we can use the format function of the string or the equivalen fstring:
```Python
a = 'world'
message = "Hello {} world".format(a)
message = f"Hello {a}" # equivalent
```

If we need to a special formatting for a variable, we can specify it behind `:` as we can see in the following example that padds the number from left:
```Python
uid = '47'
message = "Hello user {:0>4d}".format(a) # prints "Hello user 0047"
message = f"Hello {a:0>4d}" # equivalent
```

More formating optios can be found in the [Python string formatting cookbook](https://mkaz.blog/code/python-string-format-cookbook/).



# Classes
[Official Manual](https://docs.python.org/3/tutorial/classes.html)

Classes in Python are defined using the `class` keyword:
```Python
class MyClass:
    ...
```
Unlike in other languages, we only declare the function members, other members are declared in the constructor or even later.

## Constructor
The constructor is a special function named `__init__`. Usually, non-function members are declared in the constructor:
```Python
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = 0
        self.d = None
```

## Check if an object contains a member
To check whether an object contains a member, we can use the `hasattr` function:
```Python
if hasattr(obj, 'member'):
    ...
```


### Constructor overloading
Python does not support function overloading, including the constructor. That is unfortunate as default arguments are less powerfull mechanism. For other functions, we can supplement overloading using a function with a different name. However, for the constructor, we need to use a different approach.

The most clean way is to use a class method as a constructor. Example:
```Python
class MyClass:
    def __init__(self, a, b = 0):
        self.a = a
        self.b = b
        self.c = 0
        self.d = None

    @classmethod
    def from_a(cls, b):
        return cls(0, b)
```



# Built-in data structures and generators
Python has several built-in data structures, most notably `list`, `tuple`, `dict`, and `set`. These are less efficient then comparable structures in other languages, but they are very convenient to use.

Also, there is a special generator type. It does not store the data it is only a convinient way how to access data generated by some function.

## Generator
[Python wiki](https://wiki.python.org/moin/Generators)

Generators are mostly used in the iteration, we can iterte them the same way as lists. 

To get the first item of the generator, we can use the `next` function:
```Python
g = (x for x in range(10))
first = next(g) # 0
```

To create a generator function (a function that returns a generator), we can use the `yield` keyword. The following function returns a generator that yields the numbers 1, 2, and 3:
```Python
def gen():
    yield 1
    yield 2
    yield 3
```

The **length** of the generator is not known in advance, to get the length, we have to iterate the generator first, for example using `len(list(<generator>))`


## Dictionary
[Official Manual](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

Disctionaries are initialized using curly braces (`{}`) and the `:` operator:
```Python
d = {
    'key1': 'value1',
    'key2': 'value2',
    ...
}
```

Two dictionaries can be merged using the `|` operator:
```Python   
d3 = d1 | d2 
```


## Comprehensions
In addition to literals, Python has a convinient way of creating basic data structures: the comprehensions. The basic syntax is:
```Python
<struct var> = 
    <op. brace> <member var expr.> for <member var> in <iterable><cl. brace>
```
As for literals, we use square braces (`[]`) for lists, curly braces (`{}`) for sets, and curly braces with colons for dictionaries. In contrast, we get a generator expression when using round braces (`()`), not a tuple.

We can also use the `if` keyword to filter the elements:
```Python
a = [it for it in range(10) if it % 2 == 0] # [0, 2, 4, 6, 8]
```


## Sorting
[Official Manual](https://docs.python.org/3/howto/sorting.html)

For sorting, you can use the `sorted` function. 

Instead of using comparators, Python has a different concept of *key functions* for custom sorting. The key function is a function that is applied to each element before sorting. For any expected object, the key function should return a value that can be compared.

## Complex sorting using tuples
If we need to apply some complex sorting, we can use tuples as the key function return value. The tuples have comparison operator defined, the implementation is as follows:

- elements are compared one by one
- on first non-equal element, the comparison result is returned

This way, we can implement a complex sorting that would normaly require several conditions by storing the condition results in the tuple.


## Slices
Many Python data structures support slicing: selecting a subset of elements. The syntax is:
```Python
<object>[<start>:<end>:<step>]
```
The `start` and `end` are inclusive. 

The `step` is optional and defaults to 1. The start is also optional and defaults to 0. 

Instead of omitting the `start` and `end`, we can use the `None` keyword:
```Python
a = [1, 2, 3, 4, 5]
a[None:3] # [1, 2, 3]
```

Sometimes, it is not possible to use the slice syntax:

- when we need to use a variable for the step or,
- when the object use the slice syntax for something else, e.g., for selecting columns in a Pandas dataframe.

In such cases, we can use the `slice` object:
```Python
a[0:10:2] 
s = slice(0, 10, 2)
a[s] # equivalent
```

Here, the parameters can be ommited as well. We can select everything by using `slice(None)`, which is equivalent to `slice(None, None, None)`.



## Named tuples
Apart from the standard tuple, Python has a named tuple class that can be created using the [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) function. In named tuple, each member has a name and can be accessed using the dot operator:
```Python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x) # 1
```


# Importing
In python, we can import whole modules as:
```Python
import <module>
```

Also, we can import specific functions, classes, or variables from the module:
```Python
from <module> import <name>
```

Note that when importing variable, we import the reference to the variable. Therefore, it will become out of sync with the original variable if the original variable is reassigned. Therefore, **importing non-constant variables is not recommended.**



# Exceptions
[documentation](https://docs.python.org/3/tutorial/errors.html)

Syntax:
```Python
try:
    <code that can raise exception>
except <ERROR TYPE> as <ERROR VAR>:
    <ERROR HANDELING>
```



# Date and time
[Python documentation](https://docs.python.org/3/library/datetime.html)

The base object for date and time is [`datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects)

## `datetime` construction
The `datetime` object can be directly constructed from the parts:
```python
from daterime import datetime

d = datetime(2022, 12, 20, 22, 30, 0) # 2022-12-20 22:30:00
```

The time part can be ommited.

We can load the datetime from string using the [`strptime`](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) function:
```python
d = datetime.strptime('2022-05-20 18:00', '%Y-%m-%d %H:%M')
```
For all possible time formats, check the [`strftime` cheatsheet](https://strftime.org/)


## Accessing the parts of `datetime`
The `datetime` object has the following attributes:

- `year`
- `month`
- `day`
- `hour`
- `minute`
- `second`

We can also query the day of the week using the `weekday()` method. The day of the week is represented as an integer, where Monday is 0 and Sunday is 6.


## Intervals
There is also a dedicated object for time interval named [`timedelta`](https://docs.python.org/3/library/datetime.html#timedelta-objects). It can be constructed from parts (seconds to days), all parts are optional.

We can obtain a timedelta by substracting a `datetime` from another `datetime`:
```python
d1 = datetime.strptime('2022-05-20 18:00', '%Y-%m-%d %H:%M')
d2 = datetime.strptime('2022-05-20 18:30', '%Y-%m-%d %H:%M')
interval = d2 - d1 # 30 minutes
```

We can also add or substract a `timedelta` object from the `datetime` object:
```python
d = datetime.strptime('2022-05-20 18:00', '%Y-%m-%d %H:%M')
interval = timedelta(hours=1)
d2 = d + interval # '2022-05-20 19:00'
```


## Converting to Unix timestamp
To convert a `datetime` object to unix timestamp, we can use the `timestamp` method. It returns the number of seconds since the epoch (1.1.1970 00:00:00). Note however, that **the timestamp is computed based on the `datetime` object's timezone, or your local timezone if the `datetime` object has no timezone information.**



# Filesystem
There are three ways commonlz used to work with filesystem in Python:

- manipulate paths as strings
- [`os.path`](https://docs.python.org/3/library/os.path.html)
- [`pathlib`](https://docs.python.org/3/library/pathlib.html)

The folowing code compares both approaches for path concatenation:
```Python
# string path concatenation
a = "C:/workspace"
b = "project/file.txt"
c = f"{a}/{b}"

# os.path concatenation
a = "C:/workspace"
b = "project/file.txt"
c = os.path.join(a, b)

# pathlib concatentation
a = Path("C:/workspace")
b = Path("project/file.txt")
c = a / b 
``` 

As the `pathlib` is the most modern approach, we will use it in the following examples. Appart from `pathlib` documentation, there is also a [cheat sheet available on github](https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf).

## Path editing
### Computing relative path
To prevent misetakes, it is better to compute relative paths beteen directories than to hard-code them. Fortunately, there are methods we can use for that.

If the desired relative path is a child of the start path, we can simply use the `relative_to` method of the Path object:
```Python
a = Path("C:/workspace")
b = Path("C:/workspace/project/file.txt")
rel = b.relative_to(a) # rel = 'project/file.txt'
```

However, **if we need to go back in the filetree, we need a more sophisticated method from `os.path`**:
```Python
a = Path("C:/Users")
b = Path("C:/workspace/project/file.txt")
rel = os.path.relpath(a, b) # rel = '../Workspaces/project/file.txt'
```


### Get parent directory
We can use the `parent` property of the `Path` object:
```Python
p = Path("C:/workspace/project/file.txt")
parent = p.parent # 'C:\\workspace\\project'
```


### Absolute and canonical path
We can use the `absolute` method of the `Path` object to get the *absolute* path. To get the *canonical* path, we can use the `resolve` method.



### Splitting paths and working with path parts
To read the **file extension**, we can use the `suffix` property of the `Path` object. The property returns the extension **with the dot**.

To **change the extension**, we can use the `with_suffix` method:
```Python
p = Path("C:/workspace/project/file.txt")
p = p.with_suffix('.csv') # 'C:\\workspace\\project\\file.csv'
```

To **remove the extension**, just use the `with_suffix` method with an empty string.


We can split the path into parts using the `parts` property:
```Python
p = Path("C:/workspace/project/file.txt")
parts = p.parts # ('C:\\', 'workspace', 'project', 'file.txt')
```

To find the index of some specific part, we can use the `index` method:
```Python
p = Path("C:/workspace/project/file.txt")
index = p.parts.index('project') # 2
```

Later, we can use the index to manipulate the path:
```Python
p = Path("C:/workspace/project/file.txt")
index = p.parts.index('project') # 2
p = Path(*p.parts[:index]) # 'C:\\workspace'
```

### Changing path separators
To change the path separators to forward slashes, we can use the `as_posix` and 
method:
```Python
p = Path(r"C:\workspace\project\file.txt")
p = p.as_posix() # 'C:/workspace/project/file.txt'
```

### Using `~` as the home directory in paths
Normally, the `~` character is not recognized as the home directory in Python paths. To enable this, we can use the `expanduser` method:
```Python
p = Path("~/project/file.txt")
p = p.expanduser() # 'C:\\Users\\user\\project\\file.txt'
```



## Working directory

- `os.getcwd()` - get the current working directory
- `os.chdir(<path>)` - set the current working directory


## Iterating over files
The `pathlib` module provides a convenient way to iterate over files in a directory. The particular methods are:

- `iterdir` - iterate all files and directories in a directory
- `glob` - iterate over files in a single directory, using a filter
- `rglob` - iterate over files in a directory and all its subdirectories, using a filter

In general, the files will be sorted alphabetically. 

### Single directory iteration
Using pathlib, we can iterate over files using a filter with the `glob` method:
```Python
p = Path("C:/workspace/project")
for filepath in p.glob('*.txt') # iterate over all txt files in the project directory
```

The old way is to use the `os.listdir` method:
```Python
p = Path("C:/workspace/project")
for filename in os.listdir(p):
    if filename.endswith('.txt'):
        filepath = p / filename
```

### Recursive iteration
Using pathlib, we can iterate over files using a filter with the `rglob` method:
```Python
p = Path("C:/workspace/project")
for filepath in p.rglob('*.txt') # iterate over all txt files in the project directory and all its subdirectories
```

The old way is to use the `os.walk` method:
```Python
p = Path("C:/workspace/project")
for root, dirs, files in os.walk(p):
    for filename in files:
        if filename.endswith('.txt'):
            filepath = Path(root) / filename
```


### Iterate only directories/files
There is no specific filter for files/directories, but we can use the `is_file` or `is_dir` method to filter out directories:
```Python
p = Path("C:/workspace/project")
for filepath in p.glob('*'):
    if filepath.is_file():
        # do something
```


### Use more complex filters
Unfortunately, the `glob` and `rglob` methods do not support more complex filters (like regex). However, we can easily apply the regex filter manually:
```Python
p = Path("C:/workspace/project")
for filepath in p.glob('*'):
    if not re.match(r'^config.yaml$', filepath.name):
        # do something
```



## Get the path to the current script
```Python
Path(__file__).resolve().parent
```

## Checking write permissions for a directory
Unfortunatelly, most of the methods for checking write permissions are not reliable outside Unix systems. The most reliable way is to try to create a file in the directory:
```Python
p = Path("C:/workspace/project")
try:
    with open(p / 'test.txt', 'w') as f:
        pass
    p.unlink()
    return True
except PermissionError:
    return False
except:
    raise # re-raise the exception
``` 

Other methods like `os.access` or using `tempfile` module are not reliable on Windows (see e.g.: https://github.com/python/cpython/issues/66305).


## Deleting files and directories
To delete a file, we can use the `unlink` method of the `Path` object:
```Python
p = Path("C:/workspace/project/file.txt")
p.unlink()
```

for deleting directories, we can use the `rmdir` method:
```Python
p = Path("C:/workspace/project")
p.rmdir()
```

However, the `rmdir` method can delete only empty directories. To delete a directory with content, we can use the `shutil` module:
```Python
p = Path("C:/workspace/project")
shutil.rmtree(p)
```

### Deleting Windows read-only files (i.e. Access Denied error)
On Windows, all the delete methods can fail because lot of files and directories are read-only. This is not a problem for most application, but it breaks Python delete methods. One way to solve this is to handle the error and change the attribute in the habdler. Example for shutil:
```Python
import os
import stat
import shutil

p = Path("C:/workspace/project")
shutil.rmtree(p, onerror=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path)))
```




# I/O

## CSV
[Official Manual](https://docs.python.org/3/library/csv.html)

The `csv` module provides a Python interface for working with CSV files. The basic usage is:
```Python
import csv

with open('file.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # do something
```

Reader parameters:

- `delimiter` - the delimiter character


## HDF5
HDF5 is a binary file format for storing large amounts of data. The `h5py` module provides a Python interface for working with HDF5 files.

[An example of reading a dataset from an HDF5 file on SO](https://stackoverflow.com/questions/28170623/how-to-read-hdf5-files-in-python)



# Command line arguments
The `sys` module provides access to the command line arguments. They are stored in the `argv` list with the first element being the name of the script.



# Logging
[Official Manual](https://docs.python.org/3/howto/logging.html)

A simple logging configuration:
```Python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)
```

The logging itself is then done using the `logging` module methods:
```Python
logging.info("message")
logging.warning("message %s", "with parameter")
```



# Type hints
[Official Manual](https://docs.python.org/3/library/typing.html)

Type hints are a useful way to help the IDE and other tools to understand the code so that they can provide better support (autocompletion, type checking, refactoring, etc.). The type hints are not enforced at runtime, so they do not affect the performance of the code.

We can specify the type of a variable using the `:` operator:
```Python
a: int = 1
```
Apart from the basic types, we can also use the `typing` module to specify more complex types:
```Python
from typing import List, Dict, Tuple, Set, Optional, Union, Any

a: List[int] = [1, 2, 3]
```

We can also specify the type of a function argument and return value:
```Python
def foo(a: int, b: str) -> List[int]:
    return [a, b]
```

## Type hints in loops
The type of the loop variable is usually inferred by IDE from the type of the iterable. However, this sometimes fails, e.g., for zip objects. In such cases, we need to specify the type of the loop variable. However, **we cannot use the `:` directly in the loop, but instead, we have to declare the variable before the loop**:
```Python
for a: int in ... # error

a: int
for a in ... # ok
```



# Numpy

## Initialization
We can create the new array as:

- zero-filled: `np.zeros(<shape>, <dtype>)`
- ones-filled: `np.ones(<shape>, <dtype>)`
- empty: `np.empty(<shape>, <dtype>)`
- filled with a constant: [`np.full(<shape>, <value>, <dtype>)`](https://numpy.org/doc/stable/reference/generated/numpy.full.html)

## Sorting
for sorting, we use the [`sort`](https://numpy.org/doc/stable/reference/generated/numpy.sort.html) function.

There is no way how to set the sorting order, we have to use a trick for that:
```Python
a = np.array([1, 2, 3, 4, 5])
a[::-1].sort() # sort in reverse order
```

## Export to CSV
To export the numpy array to CSV, we can use the [`savetxt`](https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html) function:
```Python
np.savetxt('file.csv', a, delimiter=',')
```
By default, the function saves values in the mathematical float format, even if the values are integers. To save the values as integers, we can use the `fmt` parameter:
```Python
np.savetxt('file.csv', a, delimiter=',', fmt='%i')
```


## Usefull array properties:

- `size`: number of array items
    - unlike len, it counts all items in the mutli-dimensional array
- `itemsize`: memory (bytes) needed to store one item in the array
- `nbytes`: array size in bytes. Should be equal to `size * itemsize` .


## Usefull functions




# Regular expressions
In Python,  the regex patterns are not compiled by default. Therefore we can use strings to store them.

The basic syntax for regex search is:
```Python
result = re.search(<pattern>, <string>)
if result: # pattern matches
    group = result.group(<group index>)) # print the first group
```

The 0th group is the whole match, as usual.


# Lambda functions
Lambda functions in python have the following syntax:
```Python
lambda <input parameters>: <return value>
```
Example:
```Python
f = lambda x: x**2
```
Only a single expression can be used in the lambda function, so we need standard functions for more complex logic (temporary variables, loops, etc.).


# Decorators
Decorators are a special type of function that can be used to modify other functions. 

When we write an annotation with the name of a function above another function, the annotated function is *decorated*. It means that when we call the annotated function, a *wrapper* function is called instead. The wrapper function is the function returned by the *decorater*: the function with the same name as the annotation.

If we want to also keep the original function functionality, we have to pass the function to the decorator and call it inside the wrapper function. 

In the following example, we create a dummy decorator that keeps the original function functionality:
Example:
```Python
def decorator(func):
    def wrapper():
        result = func()
        return result
    return wrapper

@decorator
def my_func():
    # do something
    return result
```

## Decorator with arguments
If the original function has arguments, we have to pass them to the wrapper function. Example:
```Python
def decorator(func):
    def wrapper(param_1, param_2):
        result = func(param_1, param_2)
        return result
    return wrapper

@decorator
def my_func(param_1, param_2):
    # do something
    return result
```





# Jupyter

## Memory
Most of the time, when the memory allocated by the notebook is larger than expected, it is caused by some library objects (plots, tables...]). However sometimes, it can be forgotten user objects. To list all user objects, from the largest:
```Python
# These are the usual ipython objects, including this one you are creating
ipython_vars = ['In', 'Out', 'exit', 'quit', 'get_ipython', 'ipython_vars']

# Get a sorted list of the objects and their sizes
sorted([(x, sys.getsizeof(globals().get(x))) for x in dir() if not x.startswith('_') and x not in sys.modules and x not in ipython_vars], key=lambda x: x[1], reverse=True)
```

# Plotting
There are several libraries for plotting in Python. The most common are:

- `matplotlib`
- `plotly`

In the table below, we can see a comparison of the most common plotting libraries:
| Functionality | Matplotlib | Plotly |
| --- | --- | --- |
| real 3D plots | no | yes |
| detail legend styling (padding, round corners...) | yes | no |

## Matplotlib
[Official Manual](https://matplotlib.org/stable/contents.html)

### Saving figures
To save a figure, we can use the `savefig` function. The **`savefig` function has to be called before the `show` function, otherwise the figure will be empty**.


# Docstrings
For documenting Python code, we use docstrings, special comments soroudned by three quotation marks: `""" docstring """`

Unlike in other languages, there are multiple styles for docstring content. The most common are:

- [Epytext](https://epydoc.sourceforge.net/manual-epytext.html)
    ```Python
    """
    @param <param name>: <param description>
    @return: <return description>
    """
    ```
- [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    ```Python
    """
    Args:
        <param name>: <param description>
    Returns:
        <return description>
    """
    ```
- [Numpy](https://numpydoc.readthedocs.io/en/latest/format.html)
    ```Python
    """
    Parameters
    ----------
    <param name> : <param type>
        <param description>
    Returns
    -------
    <return type>
        <return description>
    """
    ```
- [reStructuredText](https://docutils.sourceforge.io/docs/user/rst/quickref.html)
    ```Python
    """
    :param <param name>: <param description>
    :return: <return description>
    """
    ```




# Progress bars
For displaying progress bars, we can use the `tqdm` library. It is very simple to use:
```Python
from tqdm import tqdm
for i in tqdm(range(100)):
    ...
```
Important parameters:

- `desc`: description of the progress bar


# PostgreSQL
When working with PostgreSQL databases, we usually use either

- the [psycopg2](https://www.psycopg.org/) adapter or,
- the [sqlalchemy](https://www.sqlalchemy.org/).


## psycopg2
[documentation](https://www.psycopg.org/docs/usage.html)

To connect to a database:
```Python
con = psycopg2.connect(<connection string>)
```
After running this code a new session is created in the database, this session is handeled by the `con` object.

The operation to the database is then done as follows:

1. create a cursor object which represents a database transaction
    ```Python
    cur = con.cursor()
    ```
2. execute any number of SQL commands
    ```Python
    cur.execute(<sql>)
    ```
3. commit the transaction
    ```Python
    con.commit()
    ```


## SQLAlchemy
[Connection documentation](https://docs.sqlalchemy.org/en/20/core/connections.html)

SQLAlchemy works with engine objects that represent the application's connection to the database. The engine object is created using the `create_engine` function:
```Python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost:5432/dbname')
```

A simple **`SELECT`** query can be executed using using the following code:
```Python
with engine.connect() as conneciton:
    result = conneciton.execute("SELECT * FROM table")
    ...
```

With modifying statements, the situation is more complicated as SQLAlchemy uses transactions by default. Therefore we need to commit the transaction. There are two ways how to do that:

- using the `commit` method of the connection object
    ```Python
    with engine.connect() as conneciton:
        conneciton.execute("INSERT INTO table VALUES (1, 2, 3)")
        conneciton.commit()
    ```

- creating a new block for the transaction using the `begin` method of the connection object
    ```Python
    with engine.connect() as conneciton:
        with conneciton.begin():
            conneciton.execute("INSERT INTO table VALUES (1, 2, 3)")
    ```
    - this option has also its shortcut: the `begin` method of the engine object
        ```Python
        with engine.begin() as conneciton:
            conneciton.execute("INSERT INTO table VALUES (1, 2, 3)")
        ```

Note that **the old `execute` method of the engine object is not available anymore** in newer versions of SQLAlchemy. 



### Executing statements without transaction
By default, sqlalchemy executes sql statements in a transaction. However, some statements (e.g., `CREATE DATABASE`) cannot be executed in a transaction. To execute such statements, we have to use the `execution_options` method:
```Python
with sqlalchemy_engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    conn.execute("<sql>")
    conn.commit()
```

## Executing multiple statements at once
To execute multiple statements at once, for example when executing a script, it is best to use the `execute` method of the psycopg2 connection object. Moreover, to safely handle errors, it is best to catch the exceptions and manually rollback the transaction in case of an error:
```Python
conn = psycopg2.connect(<connection string>)
cursor = conn.cursor()
try:
    cursor.execute(<sql>)
    conn.commit()
except Exception as e:
    conn.rollback()
    raise e
finally:
    cursor.close()
    conn.close()
```


# Working with GIS
When working with gis data, we usually change the `pandas` library for its GIS extension called [`geopandas`](https://geopandas.org/en/stable/).

For more, see the pandas manual.

## Geocoding
For geocoding, we can use the [Geocoder](https://geocoder.readthedocs.io/) library. 


# Complex data structures
## KDTree
[documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html)

KDTree can be found in the `scipy` library. 

# Geometry
There are various libraries for working with geometry in Python:

- [`scipy.spatial`](https://scikit-spatial.readthedocs.io/en/stable/index.html): for basic geometry operations
- `shapely`
- `geopandas`: for gis data


