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

# Checking the type
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

The base object for date and time is [`datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects), which can be directly constructed from the parts:
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



# Working with paths
We can use strings to manipulate with pths in Python, however, it is easier to manipulate the `Path` or `PurePath` objects from [`pathlib`](https://docs.python.org/3/library/pathlib.html#methods-and-properties) for complicated situations. The folowing code compares both approaches for path concatenation:
```Python
a = "C:/workspace"
b = "project/file.txt"

# string path concatenation
c = f"{a}/{b}"

# pathlib concatentation
a = Path("C:/workspace")
b = Path("project/file.txt")
c = a / b 
``` 


## Computing relative path
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

## iterating over files
There are different method available, depending what we need
- standard iteration
- recursive iteration: `os.walk(<path>)`, see [example on SO](https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python)



# Built-in data structures
Python has several built-in data structures, most notably `list`, `tuple`, `dict`, and `set`. These are less efficient then comparable structures in other languages, but they are very convenient to use.

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




# Numpy
## Usefull array properties:
- `size`: number of array items
    - unlike len, it counts all items in the mutli-dimensional array
- `itemsize`: memory (bytes) needed to store one item in the array
- `nbytes`: array size in bytes. Should be equal to `size * itemsize` .


## Usefull functions
- [`sort`](https://numpy.org/doc/stable/reference/generated/numpy.sort.html)



# Regular expressions




# Jupyter

## Memory
Most of the time, when the memory allocated by the notebook is larger than expected, it is caused by some library objects (plots, tables...]). However sometimes, it can be forgotten user objects. To list all user objects, from the largest:
```Python
# These are the usual ipython objects, including this one you are creating
ipython_vars = ['In', 'Out', 'exit', 'quit', 'get_ipython', 'ipython_vars']

# Get a sorted list of the objects and their sizes
sorted([(x, sys.getsizeof(globals().get(x))) for x in dir() if not x.startswith('_') and x not in sys.modules and x not in ipython_vars], key=lambda x: x[1], reverse=True)
```

# Docstrings
For documenting Python code, we use docstrings, special comments soroudned by three quotation marks: `""" docstring """`

Unlike in other languages, there are multiple styles for docstring content.

# PostgreSQL
When working with PostgreSQL databases, we usually use either
- the [psycopg2](https://www.psycopg.org/) adapter or,
- the [sqlalchemy](https://www.sqlalchemy.org/).

## SQLAlchemy
Simple query:
```Python
sqlalchemy_engine.execute("<sql>")
```


# Working with GIS
when working with gis data, we usually change the `pandas` library for its GIS extension called [`geopandas`](https://geopandas.org/en/stable/).

For more,, see the pandas manual.

