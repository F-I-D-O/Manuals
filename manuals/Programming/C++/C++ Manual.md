

# Type System and basic types
[cppreference](https://en.cppreference.com/w/cpp/language/type)

*Type* is a property of each:

- object
- reference
- function
- expression

## Arithmetic Types
[cppreference](https://en.cppreference.com/w/cpp/language/types)

### Integers
Integer types varies in the sign and size.

Unfortunatelly, **the minimum sizes guaranteed by the standard are not usable, because the real size is different and it differs even between platforms**. Especially the `long` type. To use an integer with a specific size, or a specific minimal size, we can use [type aliases defined in `cstdint`](https://en.cppreference.com/w/cpp/types/integer)

### Overflow and Underflow
The overflow (and underflow) is a common problem in most programming languages. The problem in C++ is that:

- overflows are **not detected**
- overflows can happen in many unexpected situations

#### Dangerous situations
In addition to the usual suspects like assigning a value to a variable of a smaller type, there are some less obvious situations that can cause overflows. Some examples:

- the result of an arithmetic operation is assigned to a variable of large enough type, but the overflow happens before the assignment itself:
```cpp
short a = 32767;
short b = 1;
int c = a + b; // overflow happens beffore the assignment
```
A solution to this problem is to use a numeric cast of the opperands (even one is enouhg):
```cpp
short a = 32767;
short b = 1;
int c = static_cast<int>(a) + b;
```


#### Detecting overflows
There are some methods how to detect overflows automatically by suppliying arguments to the compiler. These are summarized here:

- **MSVC**: not implemented
- **GCC**: only detectes signed and floating point overflows, as the unsigned overflows are not considered as errors (the behaviour is defined in the standard). All undefined behaviour can be detected using the `-fsanitize=undefined` flag. [Documentation](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
- **Clang**: Both signed and unsigned overflow can be detected. The undefined behaviour can be detected using the `-fsanitize=undefined` flag. Fo all integer overflows, the `-fsanitize=integer` flag can be used. [Documentation](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)

The reasoning behind excluding the unsigned overflows from GCC are described [here](https://gcc.gnu.org/legacy-ml/gcc/2016-07/msg00051.html).


It is also possible to do an ad-hoc overflow check in the code, the possible solutions are described in [this SO question](https://stackoverflow.com/questions/199333/how-do-i-detect-unsigned-integer-overflow)


### Characters
Characters in C++ are represented by the `char` type, which is an integer type. This type can be signed or unsigned, and it is at least 8 bits long. 

Useful functions for working with characters are:

- [`std::isspace`](https://en.cppreference.com/w/cpp/string/byte/isspace): checks if the character is a whitespace (space, tab, newline, etc.)
- [`std::toupper`](https://en.cppreference.com/w/cpp/string/byte/toupper): converts the character to upper case


## Pointers
[cppreference](https://en.cppreference.com/w/cpp/language/pointer)


### Pointers to Functions
Function pointers are declared as:
```cpp
<return_type> (*<pointer_name>)(<arg_1_type>, ..., <arg_n_type>)
```
For example a function `the_function` returning bool and accepting int can be stored to pointer like this:

```C++
bool (*ptr)(int) = &the_function
```

The above example can be then simply called as `bool b = ptr(2)`


### Pointers to Member Objects
Pointers to member objects has a cumbersome syntax

- declaration: `<member type> <class type>::*<pointer name> = ...`
- usage: `<object name>.*<pointer name> = ...`

Example:
```cpp
class My_class{
public:
	int my_member;
}

int main{
	// declaring the pointer
	int My_class::*ptr = &My_class::my_member;

	// creating the instance
	My_class inst;

	// using the pointer to a member object
	inst.*ptr = 2;
}
```


### Pointers to Member Functions
Pointers to member functions are even more scary in C++. We need to use the member object and the function adress and combine it in a obscure way:

```cpp
class My_class{
public:
	bool my_method(int par);	
}

int main{
	// creating the instance
	My_class inst;

	// assigning method address to a pointer
	bool (My_class::*ptr)(int) = &My_class::my_method;

	// using the pointer to a member function
	bool b = (inst.*ptr)(2)
}
```

The first unexpected change is the `My_class` before the name of the pointer. It's because unlike a pointer to function `the_function` which is of type `(*)(int)`, the pointer to `my_method` is of type `(My_class::*)(int)`

The second difference is the call. We have t use the pointer to member binding operator `.*` to access the member of the specific instance  `inst`. But this operator has a lower priority then the function call operator, so we must use the extra parantheses.

## References
[References](https://en.cppreference.com/w/cpp/language/reference) serve as an alias to already existing objects. Standard (*Lvalue*) references works the same way as pointers, with two differences:

- they cannot be NULL
- they cannot be reassigned

The second property is the most important, as the assignment is a common operation, which often happens under do hood. In conslusion, **reference types cannot be used in most of the containers and objets that needs to be copied**.

### Rvalue references
[Rvalue references](https://en.cppreference.com/w/cpp/language/reference#Rvalue_references) are used to refer to temporary objects. They eneable to prevent copying local objets by extending lifetime of temporary objects. They are mostly used as function parameters:

```cpp
void f(int& x){
}

f(3); // 3 needs to be copied to f, because it is a temporary variable
 
// we can add the rvalue overload
void f(int&& x){
}

f(3) // rvalue overload called, no copy
```

### Forwarding references
[Forwarding references](https://en.cppreference.com/w/cpp/language/reference#Forwarding_references) are references that preserves the value category (i.e. r/l-value reference, `const`). They have two forms:

- function parameter forwarding references
- `auto` forwarding references

#### Function parameter forwarding references
In a function template, if we use the rvalue reference syntax for a function parameter of  whose type is a function template parameter, the reference is actually a forwarding reference. Example:
```cpp
template<class T>
void f(T&& arg) // parameter is T& or T&& depending on the supplied argument
```
Important details:

- it works only for non const references
- the reference type has to be a function template argument, not a class template argument 

#### `auto` forwarding reference
When we assign to `auto&&, it is a forwarding reference, not rvalue reference:
```cpp
auto&& a = f() // both type and value category depends on the return value of f()

for(auto&& a: g(){ // same
}
```


## Arrays
[cppreference](https://en.cppreference.com/w/cpp/language/array)

There are two types of arrays:

- *static*, i.e., their size is known at compile type, and
- *dynamic*, the size of which is computed at runtime

We can use the array name to access the first elemnt of the array as it is the pointer to that element.

### Static arrays

Declaration:
```cpp
int a[nrows];
int a[nrwows][ncols]; // 2D
int a[x_1]...[x_n]; // ND 
```

Initialization:
```cpp
int a[3] = {1, 2, 5}
int b[3] = {} // zero initialization
int c[3][2] = {{1,5}, {2,9}, {4,4}} // 2D
int d[] = {1,5} // we can skip dimensions if their can be derived from data
```

Note that  the multi-dimensional syntax is just an abstraction for the programmers. The following code blocks are therefore equivalent:

Matrix syntax
```cpp
const int rowns = 5;
const int cols =  3;
int matrix[rows][cols];

int main(){
	for(int n = 0; n < rows; ++n){
		for(int m = 0; m < cols; ++m){  
			Table[n][m] = (n + 1) * (m + 1);
		}
	}
}
```

Flat syntax
```cpp
const int rowns = 5;
const int cols =  3;
int matrix[rows * cols];

int main(){
	for(int n = 0; n < rows; ++n){
		for(int m = 0; m < cols; ++m){  
			Table[n * cols + m] = (n + 1) * (m + 1);
		}
	}
}
```

Using the matrix syntax adds the possibility to access the element of the array using multiple dimensions. But the underlying memory is the same.

### Dynamic arrays
Declaration:
```cpp
int* a = new int[size]
```
For multiple dimensions, this syntax does not scale, i.e, only one dimension can be dynamic:

```cpp
int(*a)[4] = new int[rows][4] // static column count
int(*b)[cols] = new int[rows][cols] // does not compile unless cols is a constant!
```


### Array to pointer implicit conversion
When we use the array name in an expression, it can be implicitly converted to a pointer to the first element of the array. This is true for both static and dynamic arrays. Example:
```cpp
int a[3] = {1, 2, 5}
int* ptr = a; // ptr points to the first element of a
```
This implicit conversion is called *array-to-pointer decay*.


### Mutli-dimensional dynamic arrays
To simulate multi-dimensional dynamic arrays, we have two options:

- use the flat syntax, as demonstrated on static arrays
- use aray of pointers to arrays 

Method | Pros | Cons

--|--|--
Flat Syntax | Fast: single continuous allocations | different access syntax than static 2D arrays
Array of pointers | Slow: one allocation per row, unrelated memory addresses between rows | same access syntax as static 2D arrays

#### Flat array
```cpp
int* a = new int[rows * cols]
```

Then we can access the array as:
```cpp
a[x * cols + y] = 5
```


#### Array of pointers to array
Declaration and Definition
```cpp
int** a= new int*[rows]

for(int i = 0; i < rows; ++i){
	a[i] = new int[cols]
}
```
Access is than like for static 2D array: `a[x][y] = 5`. This works because the pointers can be also accessed using the array index operator (`[]`). In other words, it works "by coincidence", but we have not created a real 2D array.

### Auto dealocation of dynamic arrays
We can replace the error-prone usage of `new` and `delete` by wraping the array into unique pointer:
```cpp
std:unique_ptr<int[]> a;
a = std::make_unique<int[]>(size)
```


## References and Pointers to arrays
[cppreference](https://en.cppreference.com/w/cpp/language/pointer)

The pointer to array is declared as `<type> (*<pointer_name>)[<size>]`:
```cpp
int a[5];
int (*ptr)[5] = &a;
```
Analogously, the reference to array is declared as `<type> (&<reference_name>)[<size>]`:
```cpp
int a[5];
int (&ref)[5] = a;
```


## Function Type
A function type consist from the function arguments and the return type. The function type is written as `return_type(arg_1_type, ..., arg_n_type)`. Example:

```cpp
int foo(double a, double b);

static_assert(std::is_same_v<decltype(foo), int(double, double)>) // TRUE
```

## Reference to Function and Pointer to Function Types
[cppreference](https://en.cppreference.com/w/cpp/language/pointer)

A refrence to function has a type `return_type(&)(arg_1_type, ..., arg_n_type)`. Example:

```cpp
int foo(double a, double b);
static_assert(std::is_same_v<decltype(foo)&, int(&)(double, double)>); // TRUE
```

A pointer to function has a type: `return_type(*)(arg_1_type, ..., arg_n_type)`Example:
```cpp
int foo(double a, double b);
static_assert(std::is_same_v<decltype(foo)*, int(*)(double, double)>); // TRUE
```

## Enumerations
[cppreference](https://en.cppreference.com/w/cpp/language/enum)

C++ supports simple enumerations, which are a set of named integer constants. The enumeration can be defined as:
```cpp
enum Color {red, green, blue}; // global scope

enum class Color {red, green, blue}; // scoped, preferred
```

There is no support for enum members like in Python, but we can use a wrapper class for that:
```cpp
class Color{
public:
	enum Value {red, green, blue};

	Color(Value v): value(v){} // non-explicit constructor for easy initialization

	Value get_value() const {return value;}

	std::string to_string() const{
		switch(value){
			case Value::red: return "red";
			case Value::green: return "green";
			case Value::blue: return "blue";
		}
	}

private:
	Value value;
}

Color get_color(){
	return Color::red; // this works due to the non-explicit constructor
}

int main(){
	Color c = get_color();
	std::cout << c.to_string() << std::endl;

	switch(c.get_value()){
		case Color::red: std::cout << "red" << std::endl;
		case Color::green: std::cout << "green" << std::endl;
		case Color::blue: std::cout << "blue" << std::endl;
	}
}
```

For more complex code requireing automatic conversion to string and more, we can consider the [magic_enum library](https://github.com/Neargye/magic_enum). It supports the following features:

- enum to string conversion
- string to enum conversion
- enum iteration
- sequence of possible values


## Complete and Incomplete Types
In many context, we have to supply a type with a requirement of being a complete type. So what types are incomplete?

- The `void` type is always incomplete
- Any structure without definition (e.g. using `struct structure *ps;`, without defining `structure`.)
- An array without dimensions is an incomplete type: `int a[];` is incomplete, while `int a[5];` is complete.
- An array of incomplete elements is incomplete.

 A type trait that can be used to determine whether a type is complete is described [here](https://devblogs.microsoft.com/oldnewthing/20190710-00/?p=102678).

## Aggregate types
Aggregate types are:

- array types
- class types that fullfill the following conditions
	- no private or protected members
	- no constructores declared (including inherited constructors)
	- no private or protected base classes
	- no virtual member functions

The elements of the aggregate types can and are ment to be constructed using the aggregate initialization (see the local variable initialization section).

## Type Conversion
[cppreference: implicit conversion](https://en.cppreference.com/w/cpp/language/implicit_conversion)

In some context, an implicit type conversion is aplied. This happens if we use a value of one type in a context that expects a different type. The conversion is applied automatically by the compiler, but it can be also applied explicitly using the `static_cast` operator. In some cases where the conversion is potentially dangerous, the `static_cast` is the only way to prevent compiler warnings.



### Numeric Conversion
There are two basic types of numeric conversion:

- standard *implicit conversion* that can be of many types: this conversion is applied if we use an expression of type `T` in a context that expects a type `U`. Example:
	```cpp
	void print_int(int a){
		std::cout << a << std::endl;
	}

	int main(){
		short a = 5;
		print_int(a); // a is implicitly converted to int
	}
	```

- *usual arithmetic conversion* which is applied when we use two different types in an arithmetic binary operation. Example:
	```cpp
	int main(){
		short a = 5;
		int b = 2;
		int c = a + b; // a is converted to int
	}
	```

#### Implicit Numeric Conversion

##### Integral Promotion
Integral promotion is a coversion of an integer type to a larger integer type. The promotion should be safe in a sense that it never changes the value. Important promotions are:

- `bool` is promoted to `int`: `false` -> `0`, `true` -> `1`


##### Integral Conversion
Unlike integral promotion, integral conversion coverts to a smaller type, so the value can be changed. The conversion is safe only if the value is in the range of the target type. Important conversions are:
 

#### Usual Arithmetic Conversion
[cppreference](https://en.cppreference.com/w/cpp/language/usual_arithmetic_conversions)

This conversion is applied when we use two different types in an arithmetic binary operation. The purpose of this conversion is convert both operands to the same type before the operation is applied. The result of the conversion is then the type of the operands. 

The conversion has the following steps steps:

1. lvalue to rvalue conversion of both operands
1. special step for enum types
1. special step for floating point types
1. conversion of both operands to the common type

The last step: the conversion of both operands to the common type is performed using the following rules:

1. If both operands have the same type, no conversion is performed.
1. If both operands have signed integer types or both have unsigned integer types, the operand with the type of lesser [integer conversion rank](https://en.cppreference.com/w/cpp/language/usual_arithmetic_conversions#Integer_conversion_rank) (size) is converted to the type of the operand with greater rank.
1. otherwise, we have a mix of signed and unsigned types. The following rules are applied:
	1. If the unsigned type has conversion rank greater or equal to the rank of the signed type, then the unsigned type is used.
	1. Otherwise, if the signed type can represent all values of the unsigned type, then the signed type is used.
	1. Otherwise, both operands are converted to the unsigned type corresponding to the signed type (same rank).

Here **especially the rule 3.1 leads to many unexpected results** and hard to find bugs. Example:
```cpp
int main(){
	unsigned int a = 10;
	int b = -1;
	auto c = b - a; // c is unsigned and the value is 4294967285
}
```
To avoid this problem, **always use the `static_cast` operator if dealing with mixed signed/unsigned types**.


## Show the Type at Runtime
It may be useful to show the type of a variable at runtime:

- for debugging purposes
- for logging
- to compare the types of two variables

Note however, that in C++, there is no reflection support. Therefore, **we cannot retrieve the name of the type at runtime in a reliable way**. Instead, the name retrieved by the methods described below can depend on the compiler and the compiler settings.


### Resolved complicated types
Sometimes, it is useful to print the type, so that we can see the real type of some complicated template code. For that, the following template can be used:

```cpp
#include <string_view>

template <typename T>
constexpr auto type_name() {
  std::string_view name, prefix, suffix;
#ifdef __clang__
  name = __PRETTY_FUNCTION__;
  prefix = "auto type_name() [T = ";
  suffix = "]";
#elif defined(__GNUC__)
  name = __PRETTY_FUNCTION__;
  prefix = "constexpr auto type_name() [with T = ";
  suffix = "]";
#elif defined(_MSC_VER)
  name = __FUNCSIG__;
  prefix = "auto __cdecl type_name<";
  suffix = ">(void)";
#endif
  name.remove_prefix(prefix.size());
  name.remove_suffix(suffix.size());
  return name;
}
```
Usage:

```cpp
std::cout << type_name<std::remove_pointer_t<typename std::vector<std::string>::iterator::value_type>>() << std::endl;

// Prints: class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >
```

[Source on SO](https://stackoverflow.com/a/56766138/1827955)


### Show the user-provided types (std::type_info)
If we want to show the type of a variable provided by the user (e.g., by a function accepting `std::any`), we can use the [`typeid`](https://en.cppreference.com/w/cpp/language/typeid) operator which returns a [`std::type_info`](https://en.cppreference.com/w/cpp/types/type_info) object.  


# Standard Library Types

## Smart Pointers
For managing resources in dynamic memory, *smart pointers* (sometimes called *handles*) should be used. They manage the memory (alocation, dealocation) automatically, but their usage requires some practice.

There are two types of smart pointers:

- `std::unique_ptr` for unique ownership
- `std::shared_ptr` for shared ownership

### Creation
Usually, we create the pointer together with the target object in one call:

- [`std::make_unique<T>(<OBJECT PARAMS>)`](https://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique) for unique pointer
- `std::make_shared<T>(<OBJECT PARAMS>)` for shared pointer

These methods work well for objects, but cannot be used for arbitrary array initialization (only the empty/zero-initialized array can be created using these methods). For arbitrary array initialization, we need to use the smart pointer constructor:
```cpp
std::unique_ptr<int[]> ptr(new int[]{1, 2, 3}); 
```

Counter-intuitively, smart pointers created using the empty constructor of the respective pointer type does not default-construct the target object, but initialize the pointer to null instead:
```cpp
std::unique_ptr<My_class> ptr(std::null_ptr); // ptr is null
std::unique_ptr<My_class> ptr(); // ptr is also null
```


### Shared Pointer
Pointer to object with non-trivial ownership (owned by multiple objects).



## std::reference_wrapper
[cppreference](https://en.cppreference.com/w/cpp/utility/functional/reference_wrapper)
Reference wrapper is a class template that can be used to store references in containers or aggregated objects. The disintinction from normal references is that the reference wrapper can be copied and assigned, so it does not prevent the copy/move operations on the object it belongs to. Otherwise, it behaves like a normal reference: it has to be assigned to a valid object and it cannot be null.

## Strings
In C++, there are two types of strings:

- [`std::string`](https://en.cppreference.com/w/cpp/string/basic_string) is an owning class for a string.
- [`std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view) is a non-owning class for a string.

Also, there is a C-style string (`char*`), but it is not recommended to use it in modern C++.

The difference between `std::string` and `std::string_view` is best explained by a table below:

| | `std::string` | `std::string_view` |
| --- | --- | --- |
| **Owning** | Yes | No |
| **Null-terminated** | Yes | No |
| **Size** | Dynamic | Static |
| **Lifetime** | Managed by the string | Managed by the underlying char sequence |
| **Can be `constexpr`** | No | Yes |

and the following code:
```cpp
std::string_view sv = "hello"; // sv is a view of the string literal "hello"
std::string s = "hello"; // s stores a copy of the string literal "hello"
```


### String Literals
[cppreference]](https://en.cppreference.com/w/cpp/language/string_literal)

 The standard string literal is writen as `"literal"`. However, we need to escape some **special characters** in such literals, therefore, a *raw string* literal is sometimes more desirable: `R"(literal)"`.
 
 If our literal contains `(` or `)`, this is stil not enough, however, the delimiter can be extended to any string with a maximum length of 16 characters, for example:
 `R"lit(literal)lit"`. 
 
 Raw string literals also useful for **multi-line string literals**.

### Formatting strings
The usage of modern string formating is either

- [`std::format`](https://en.cppreference.com/w/cpp/utility/format/format) from the `<format>` header if the compiler supports [C++20 string formatting](https://en.cppreference.com/w/cpp/utility/format) ([compiler support](https://en.cppreference.com/w/cpp/compiler_support)) or
- `fmt::format` from the [`fmt`](https://github.com/fmtlib/fmt) library if not.

Either way, the usage is the same:
```cpp
format(<literal>, <arguments>)
```
where the literal is a string literal with `{}` placeholders and the arguments are the values to be inserted into the placeholders. 

The placeholders can be filled width  

- argument identification, if we want to use the same argument multiple times or change the order in the string while keep the order of arguments in the function call or
- format specification.

These two parts are separated by `:`, both of them are optional.

The most common format specifications are:

- data type:
	- `d` for decimal integer
	- `f` for floating point number
	- `s` for string
- width and precision, in the format `<width>.<precision>`. Both values can be dynamic: `std::format("{:{}.{}f}", a, b, c)` formats a float number `a` with width `b` and precision `c`.


 The formating reference can be found in the [cppreference](https://en.cppreference.com/w/cpp/utility/format/formatter#Standard_format_specification) 
 

### Spliting the string into tokens
Unfortunately, the STL does not provide a simple way to split the string into tokens like Python's `split` method or PHP's `explode` function. It is not even planned for the future.  

If we want to split a string on a character or pattern, the easiest way is to use the [split view](https://en.cppreference.com/w/cpp/ranges/split_view) from the ranges library, which has a [`std::ranges::subrange`](https://en.cppreference.com/w/cpp/ranges/subrange) as its element type: 
```cpp
// get a range of character subranges
auto parts = std::ranges::views::split(str, '-');

// iterate over the parts
for (auto part : parts) {
	std::cout << part << std::endl; // prints the part

	// convert part to string
	std::string s(part.begin(), part.end());

	// convert part to string (C++23)
	std::string s(std::from_range, part);
}
```
The last [string constructor](https://en.cppreference.com/w/cpp/string/basic_string/basic_string) is only available in C++23, and moreover, it requires the [`stl::from_range`](https://en.cppreference.com/w/cpp/ranges/from_range) tag. The `std::string_view` is equiped with a range constructor which does not require the tag in C++23. However, it is explicit, so its usage is limited:

```cpp
std::string_view s(part) // invalid
std::string_view s = std::string_view(part) // valid in C++23
```


### Converting string to int
There are simple functions for converting `std::string` to numbers, named `std::stoi`, `std::stoul`, etc. See [cppreference](https://en.cppreference.com/w/cpp/string/basic_string) for details.

For C strings, the situation is more complicated.

### Substring
A substring can be obtained using a member function `substr`:
```cpp
str.substr(str.size() - 1, 1)) // returns the last character as a string
```
### change the case
Unfortunatelly, the STL has case changing functions only for characters, so we need to iterate over the string ourselfs. The boost has a solution, however:
```cpp
#include <boost/algorithm/string.hpp>

auto upper = boost::to_upper(str);
``` 


### Building strings
Unlike other languages, in C++, strings are mutable, so we can build them using the `+` operator without performance penalty. Alternatively, we can use the `std::stringstream` class.


### Testting for whitespace
To test if a string contains only whitespace characters, we can use the `std::all_of` algorithm:
```cpp
std::all_of(str.begin(), str.end(), [](char c){return std::isspace(c);})
```


## Date and time
The date and time structure in C++ is [`std::tm`](https://en.cppreference.com/w/cpp/chrono/c/tm). We can create it from the date and time string using [`std::get_time`](https://en.cppreference.com/w/cpp/io/manip/get_time) function:
```cpp
std::tm tm;
std::istringstream ss("2011-Feb-18 23:12:34");
ss >> std::get_time(&tm, "%Y-%b-%d %H:%M:%S");
```



## Collections
In C++, the collections are implemented as templates, so they can store any type. The most common collections are:

- [std::array](https://en.cppreference.com/w/cpp/container/array)
- [std::vector](https://en.cppreference.com/w/cpp/container/vector)
- [std::unordered_set](https://en.cppreference.com/w/cpp/container/unordered_set)
- [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map)
- [std::pair](https://en.cppreference.com/w/cpp/utility/pair) and [std::tuple](https://en.cppreference.com/w/cpp/utility/tuple)

Currently, the collection semantic requirmenets are not imposed on the whole connection, bu on its member functions instead. Depending on the function used, there are different requirements for the stored types. This adds a lot of flexibility, as we can, for example, use move only types in collections when we refrain from using functions that require copying. On the other hand, it can make the debugging harder, as the compiler usually does not recognize the methods that caused the template to have stricter requirements but instead complains on the place where the template is instantiated.


### Sets
Normal set collection for C++ is [`std::unordered_set`](https://en.cppreference.com/w/cpp/container/unordered_set). By default, the set uses a `Hash`, `KeyEqual` and `Allocator` template params provided by std functions. However, they need to exist, specifically:

- [`std::hash<Key>`](https://en.cppreference.com/w/cpp/utility/hash)
- `std::equal_to<Key>`
- `std::allocator<Key>`

So either those specializations needs to be provided by the snadard library (check cppreference), or you have to provide it. 

#### Providing custom hash function
There are two options for providing custom hash function for a type `T`s:

- implementing an *explicit specialization* of the template function  `std::hash<T>`
- providing the `Hash` template param when constructing the hash

The first method is prefered if we want to provide a default hash function for some type for which there is no hash function specialization in the standard library. The second method is prefered only when we want some special hash function for a type `T` for which `std::hash<T>` is already defined.

#### Implementing custom hash function
First check whether the hash function is not provide by STL on [cppreference](https://en.cppreference.com/w/cpp/utility/hash). Then, many other hash specializations are implemented by boost, check the [reference](https://www.boost.org/doc/libs/1_78_0/doc/html/hash/reference.html). 

If there is no implementation, we can implement the hash function as follows (example for set):
```cpp
template<>
struct std::hash<std::unordered_set<const Request*>> {
    size_t operator()(const std::unordered_set<const Request*>& set) const {
        std::hash<const Request> hash_f;
        size_t sum{0};
        for (const Request* r : set) {
            sum += hash_f(*r);
        }
        return sum;
    }
};
```

Important implementation details:

- the function needs to be implemented inside `std` or annonymous namespace, not inside a custom namespace
- do not forget to add `template<>` above the function, this indicates that it is a template specialization.

### Maps
The maps has similar requiremnts for keys as the requirements for set value types (see previous section). The hash map type is called [`std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map). Note that [maps require the stored types to be complete](https://stackoverflow.com/a/74965248/1827955).

#### Geeting value by key
To access the map element, the array operator (`[]`) can be used. Note however, that this operator does not check the existence of the key, even if we do not provide a value. Example:
```cpp
std::unordered_map<int,std::string> map;
map[0] = "hello"
map[0] = "world" // OK, tha value is overwritten
a = map[1] // a == map[1] == "" unintuitively, the default value is inserted if the key does not exist
```

Therefore, **if we just read from the map, it is safer to use the `at()`** member function.

#### Inserting into map
There are five options:

1. [`map[key] = value;`](https://en.cppreference.com/w/cpp/container/unordered_map/operator_at) or
2. [`map.insert({key, value})`](https://en.cppreference.com/w/cpp/container/unordered_map/emplace)
3. [`map.emplace(key, value);`](https://en.cppreference.com/w/cpp/container/unordered_map/emplace)
4. [`map.try_emplace(key, value);`](https://en.cppreference.com/w/cpp/container/unordered_map/try_emplace)
5. [`map.insert_or_assign(key, value);`](https://en.cppreference.com/w/cpp/container/unordered_map/insert_or_assign)

The following table summarizes the differences:

| Method | If key exists | constructs in place | returns value |
| --- | --- | --- | --- |
| `map[key] = value;` | overwrites | no | a reference to the value |
| `map.insert({key, value});` | does not overwrite | no | a pair of iterator to value and bool set to true if insertion took place |
| `map.emplace(key, value);` | does not overwrite | yes | a pair of iterator to value and bool set to true if insertion took place |
| `map.try_emplace(key, value);` | does not overwrite | yes | same as emplace |
| `map.insert_or_assign(key, value);` | overwrites | yes | a pair of iterator to value and bool set to true if insertion took place |

There is only a small difference between `emplace` and `try_emplace`: the `try_emplace` does not create a new value if the key already exists, while the `emplace` can create a new value even if the key already exists (in which case, the value is then discarded).


### Tuples
We have two standard class templates for tuples:

- [`std::pair`](https://en.cppreference.com/w/cpp/utility/pair) for pairs
- [`std::tuple`](https://en.cppreference.com/w/cpp/utility/tuple) for tuples with unlimited size

Although named differently, these class templates behaves mostly the same.

#### Creating tuples
There are two ways of creating a tuple:

- constructor (`auto p = std::pair(...)`)
- initializer (`auto p = {}`)

Beware that **by default**, the deduced types are decayed, i.e., const and references are removed and the **tuple stores value types**. If you need to store the reference in a tuple, you have to specify the type: 
```cpp
auto p = std::pair<int, constr std::string&>(...)
```

Also, beware that the RVO does not apply for tuple members. **This means that if we store values types in the tuple, the types are copied/moved, and in conclusion, they have to by copyable/movable!** This is the reason why we frequently use smart pointers in tuples even though we would reurn directly by value if we returned a single value.

##### Creating tuples with `std::make_pair` or `std::make_tuple`
**TLDR: from C++17, there is no reason to use `make_pair`/`make_tuple`**.

There are also factory methods `make_pair`/`make_tuple`. Before C++17, argument deduction did not work for constructors, so there is a dedicated  method for creating tuples. However, now we can just call the constructor and the template arguments are deduced from the constructor arguments. Also, the `make_pair`/`make_tuple` functions can only produce tuples containing values, not references (even if we specify the reference type in the `make_pair`/`make_tuple` template argument, the returned tuple will be value-typed). 


#### Accessing tuple members
The standard way to access the tuple/pair mamber is using the [`std::get`](https://en.cppreference.com/w/cpp/utility/tuple/get) function:
```cpp
auto tuple = std::tuple<int, std::string, float>(0, "hello", 1.5);
auto hello = std::get<1>(tuple);
```

#### Unpacking tuples into variables
There are two scenarios of unpacking tuples into variables:

- unpacking into **new variables**: for that, we use *structured binding*.
- unpacking into **existing variables**: for that, we use `std::tie` function.

##### Structured binding 
If we don't need the whole tuple objects, but only its members, we can use a [*structured binding*](https://en.cppreference.com/w/cpp/language/structured_binding). Example:
```cpp
std::pair<int, int> get_data();

void main(){
	const auto& [x, y] = get_data();
}
```

##### `std::tie`
If we want to unpack the tuple into existing variables, we can use the [`std::tie`](https://en.cppreference.com/w/cpp/utility/tuple/tie) function:
```cpp
std::pair<int, int> get_data();

void main(){
	int x, y;
	std::tie(x, y) = get_data();
}
```	

#### Unpacking tuples to constructor params with `std::make_from_tuple`
We cannot use structured binding to unpack tuple directly into function arguments. For normal functions, this is not a problem, as we can first use structured binding into local variables, and then we use those variables to call the function. However, it is a problem for parent/member initializer calls, as we cannot introduce any variables there. Luckily, there is a [`std::make_from_tuple`](https://en.cppreference.com/w/cpp/utility/make_from_tuple) template function prepared for this purpose. Example:

```cpp
std::tuple<int,float> get_data(){
...
}

class Parent{
public:
	Parent(int a, float b){...}
{

class Child: public Parent{
public:
	Child(): Parent(std::make_from_tuple<Parent>(get_data())){}
}
```


## `std::optional`
[cppreference](https://en.cppreference.com/w/cpp/utility/optional)

`std::optional<T>` is a class template that can be used to store a value of type `T` or nothing. The advantage over other options like null pointers or is that the `std::optional` is a value type, so it can wrap stack objects as well.

The **type `T` must satisfy `std::is_move_constructible_v<T>`** (must be either movable or copyable).

The usage is easy as the class has a value constructor from `T` and a default constructor that creates an empty optional. Also, the type `T` is convertible to `std::optional<T>`, and `std::nullopt` is convertible to an empty optional. Finally, `std::optional<T>` is convertible to `bool`, so it can be used in `if` statements.

A typical usage is:
```cpp
class My_class{
public:
	My_class(int a, int b);
}

std::optional<My_class> f(){
	...
	return My_class(a, b);
	// or 
	return {a, b};

	// or, in case of fail
	return std::nullopt; 
}
std::optional<int> a = f();
if(a){
	// a has a value
}
```


## Unions and Variants
The idea of a union is to store multiple types in the same memory location. Compared to the polymorphism, when we work with pointers and to templates, where the actual type is determined at compile time, the union actually has a shared memory for all the types.

The union can be therefore used in cases where nor polymorphism neither templates are suitable. One example can be storing different unrelated types (e.g., `std::string` and `int`) in a container. We cannot use templates as that require a single type. Nor we can use polymorphism, as the types are unrelated. 

The big disadvantage of unions is that they are not type safe. The compiler cannot check if the type we are accessing is the same as the type we stored. Therefore, we have to be very careful when using unions. Therefore, unless some special case, **we should use [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant) instead of unions**.

### `std::variant`
The declaration of `std::variant` is similar to the declaration of `std::tuple`:
```cpp
std::variant<int, double> v;
```
The `std::variant` can store any of the types specified in the template parameters. The only requirement is that the types are default constructible. Also, incompatible types cannot be stored in `std::variant`, as we cannot use them as template arguments. However, we can use pointers or references to incompatible types instead.

The **type** of the stored value can be obtained using:

- [`std::holds_alternative`](https://en.cppreference.com/w/cpp/utility/variant/holds_alternative) method that returns a boolean value if the variant stores the type specified in the template parameter or
- [`std::variant::index`](https://en.cppreference.com/w/cpp/utility/variant/index) method that returns the index of the stored value.
	- this method can be used also in a **switch statement** as the index is integral

The **value** can be accessed using:

- the [`std::get`](https://en.cppreference.com/w/cpp/utility/variant/get) function, if we know the type stored in the variant or
- the [`std::get_if`](https://en.cppreference.com/w/cpp/utility/variant/get_if) function if we are guesing the type.

Both functions return a pointer to the stored value. Example:
```cpp
std::variant<int, double> v = 1;
std::cout << v.index() << std::endl; // prints 0
std::cout << *std::get_if<int>(&v) << std::endl; // prints 1
```

A really usefull feature of `std::variant` is the `std::visit` method, which allows us to call a function on the stored value. The function is selected based on the type of the stored value. Example:
```cpp
std::variant<int, double> v = 1;
std::visit([](auto&& arg) { std::cout << arg << std::endl; }, v); // prints 1
```

More on variants:

- [cppreference](https://en.cppreference.com/w/cpp/utility/variant)
- [cppstories](https://www.cppstories.com/2018/06/variant/)



# Value Categories
[cppreferencepreerecege/value_category).
In many contexts, the value category of an expression is important in deciding whether the code compiles or not, or which function or template overload is chosen. Therefore, it is usefull to be able to read value categories.

expression value types:

- *lvalue*, meaning left-value. An expression typically on the left side of compound expression a statement, e.g. variable, member, or function name. Also, lvalues expressions are are:
	- function ratoalls to fuctions returning lvalue
	- assignments
	-  `++a`, `--a` and similar pre operators
	- `*a` indirection
	- string literal
	- cast
- *prvalue*, meaning pure rvalue. It is either a result of some operand (`+`, `/`) or a constructor/initializer result. The foloowing expressions are prvalues:
	- literals with exception of string literals, e.g.: `4`, `true`, `nullptr`
	- function or operator calls that return rvalue (non-reference)
	- `a++`, `a--` and other post operators
	- arithmetic and logical expressions
	- `&a` address of expression
	- `this`
	- non-type template parameters, unless they are references
	- lambda expressions
	- requires expressions and concept spetializations
- *xvalue*, meaning expiring value. These valaues usually represent lvalues converted to rvalues. Xvalue expressions are:
	- function call to functions returning rvalue reference (e.g., [`std::move`](https://en.cppreference.com/w/cpp/utility/move)).
	- member object expression (`a.m`) if `a` is an rvlaue and `m` is a non-reference type
- *glvalue* = *lvalue* `||` *xvalue*. 
- *rvalue* = *prvlaue* `||` *xvalue*. 



# Operators
[cppreferencen](https://en.cppreferencempp.com/w/cpp/language/operators)

C++ supports almost all the standard operators known from other languages like Java, Python, or C#. Additionally, thsese operators can be overloaded. 

Note that the standard also supports [**alternative tokens**](https://en.cppreference.com/w/cpp/language/operator_alternative) for some operators (e.g., `&&` -> `and`, `||` -> `or`, `!` -> `not`). However, these are not supported by all compilers. In MSVC, the [`/permissive-`](https://docs.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance?view=vs-2019) flag needs to be used to enable these tokens.

## User-defined Operators
In C++ there are more operators than in other popular es like Python or Java. Additionally, these operators can be overloaded. See [cppreferencen](https://en.cppreferencempp.com/w/cpp/language/operators) page for detailed description.


## Comparison Operators
### Default Comparison Operators
[cppreference](https://en.cppreference.com/w/cpp/language/default_comparisons).

The `!=` is usually not a problem, because it is implicitely generated as a negation of the `==` operator. However, **the `==` is not generated by default, even for simple classes**. To force the generation of a default member-wise comparison operator, we need to write:

```c++
bool operator==(const My_class&) const = default;
```

However, to do that, all members and base classes have to ae the operator `==` defined, otherwise the default operator will be implicitely deleted.

The comparability can be checked with a `std::equality_comparable<T>` concept:
```cpp
staic_assert(std::equality_comparable<My_class>);
``` 


# Control Structures
C++ supports the control structures known from other languages like Java, Python, or C#. Here, we focus on the specifics of C++.


## Switch Statement
[cppreference](https://en.cppreference.com/w/cpp/language/switch)

In C++, we can switch on integer types or enumeration types. Also, we can use classes that are implicitely convertible to integers or enums. Switch on string is not possible.

The switch statement has the following syntax:
```cpp
switch(expression){
	case value1:
		// code
		break;
	case value2:
		// code
		break;
	default:
		// code
}
```
However, it is usually a good idea to wrap each case in a block to create a separate scope for each case. Without it, the whole switch is a single block (contrary to if/else statements). The swich statements just jump to a case that matches the value, similarly to a `goto` statement. This can create problems, as for example variable initialization cannot be jumped over. The safe case statement looks like:
```cpp
switch(expression){
	case value1:{
		// code
		break;
	}
	case value2:{
		// code
		break;
	}
	default:{
		// code
	}
}
```




# Functions
[cppreference](https://en.cppreference.com/w/cpp/language/functions)

## Function Declaration and Definition
In C and C++, functions must have a:
- **declaration** (signature) that specifies the function name, return type, and parameters
- **definition** that specifies the function body

The declaration has to be provided before the first use (call) of the function. The definition can be provided later.

The declaration is typically provided in a header file, so that the function can be used outside the translation unit. The definition is typically provided in a source file.

### Merged Declaration and Definition
If the function is not used outside the translation unit, the declaration and definition can be merged, i.e., the definition is itself a declaration. However, this is not recommended because after adding a corresponding declaration to one of the included headers (including libraries), the merged declaration/definition will become a definition of that function, which will be manifested as a linker error (multiple definitions of the function). Therefore, to control the visibility of the function, it is better to use other methods, provides in Section [Visibility of Functions](#function-visibility).


## Deciding between free function, member function and static member function
Basically, you should decide as follows:

1. Function needs access to instance -> **member function**
2. Function 
	- should be called only by class members (i.e., member functions), so we want to limit its visibility, or
	- we need to access static members of the class -> **static member function**
1. Otherwise -> **free function**

## Argument-parameter Conversions
Arg/param | value | reference | rvalue

-- |--|--|--
value | - | - | `std::move` 
reference | implicit copy | - | copy constructor
rvalue | - | not possible | -


## Default Parameters
Default function parameters  in C++ works similarly to other languages:
```c++
int add(int a, int b = 10);

add(1, 2) // 3
add(1) // 11
```

However, the default parameters works only if we call the function by name. Therefore, we cannot use them in std::function and similar contexts. Example:

```c++
std::function<int(int,int)> addf = add;
std::function<int(int)> addf = add; // does not compile

addf(1) // does not compile
```

Also, the default parameters need to be values, not references or pointers. For references and pointers, we should use function overloading.

### Default Parameters and Inheritance
TLDR: do not use default parameters in virtual functions.

The default parameters are resolved at compile time. Therefore, the value does not depend on the actual type of the object, but on the declared type of the variable. This have following consequences:

- the default parameters are not inherited
- `A* a = new B(); a->foo()` will call `B::foo()`, with the default parameters of `A::foo()`

To prevent confusion with inheritence we should use function overloading instead of default parameters in virtual functions (like in Java).


## Return values and NRVO
For deciding the return value format, refer to the [return value decision tree](https://drive.google.com/file/d/1Ml6g63_mbgjmRRByIItayAuEnhDymnH_/view?usp=sharing).

Especially, note that [NRVO](https://en.wikipedia.org/wiki/Copy_elision#RVO) is used in modern C++ and therefore, we can return all objects by value with no overhead most of the time.

The NRVO works as follows:

1. compiler tries to just tranfer the object to the parent stack frame (i. e. to the caller) without any move or copy
2. if the above is not possible, the move constructor is called.
3. if the above is not possible, the copy constructor is called.

From C++17, the RVO is mandatory, therefore, it is unlikely that the compiler use a move/copy constructor.
Consequently, most of the times, we can just return the local variable and let the rest to the compiler:
```cpp
unique_ptr<int> f(){
  auto p = std::make_unique<int>(0);

  return p; // works, calls the move constructor automatically in the worst case (pre C++17 compiler)
  // return move( p ); // also works, but prevents NRVO
}
```

The NRVO is described also on [cppreference](https://en.cppreference.com/w/cpp/language/copy_elision) together with initializer copy elision.

## Function Overlaoding
Both normal and member funcions in C++ can be overloaded. The oveload mechanic, however, is quite complicated. There can be three results of overload resolution of some function call:

- no function fits -> error
- one function fits the best
- multiple functions fits the best -> error

The whole algorithm of overload resolution can be found on [cppreference](https://en.cppreference.com/w/cpp/language/overload_resolution).

First, *viable* funcions are determined as functions with the same name and:

- with the same number of parameters
- with a greater number of parameters if the extra parameters has default arguments

If there are no viable functions, the compilation fails. Otherwise, all viable functions are compared to get the best fit. The comparison has multiple levels. The basic principle is that if only one function fits the rules at certain level, it is chosen as a best fit. If there are multiple such functions, the compilation fails. Levels:

1. Better *conversion* priority (most of the time, the best fit is found here, see conversion priority and ranking bellow)

12. non-template constructor priority

### Conversion prioritiy and ranking
[cppreference](https://en.cppreference.com/w/cpp/language/overload_resolution#Ranking_of_implicit_conversion_sequences)

When the conversion takes priority during the best viable function search, we say it is *better*. The (incomplete) algorithm of determining *better* conversion works as follows:

1. standard conversion is better than user defined conversion
2. user defined conversion is better then elipsis (`...`) conversion
3. comparing two standard conversions:
	1. if a conversion sequence S1 is a subsequence of conversion sequence S2, S1 is better then S2
	2. lower rank priority
	3. rvalue over lvalue if both applicable
	4. ref over const ref if both applicable

#### Conversion sequence ranks

1. **exact match**
2. **promotion**
3. **conversion**: includes class to base conversion



### Constructor argument type resolution in list initialization
When we use a list initailization **and** it results in a constructor call, it is not immediatelly clear which types will be used for arguments as the initialization list is not an expression. These types are, however, critical for the finding of best viable constructor. The following rules are used to determine the argument types (simplified):

1. 


## `auto` return type
For functions that are defined inside declaration (template functions, lambdas), the return type can be automatically deduced if we use the `auto` keyword. 

The decision between value and reference return type is made according to the following rules:

- return type `auto` -> return by value
- return type `auto&` -> return by reference
- return type `auto*` -> return by pointer
- return type `decltyype(auto)` -> the return type is `decltype(<RETURN EXPRESSION>)`

See more rules on [cppreference](https://en.cppreference.com/w/cpp/language/function#Return_type_deduction)

Note that **the `auto` return type is not allowed for functions defined outside the declaration** (unless using the trailing return type).


## Function visibility
The **member function** visibility is determined by the access specifier, in the same manner as the member variable visibility. 

For **free functions**, the visibility is determined by the *linkage specifier*. Without the specifier, the function is visible. To make it visible only in the current translation unit, we can use the `static` specifier. 

An equivalent way to make a function visible only in the current translation unit is to put it into an *anonymous namespace*:
```cpp
namespace {
	void f() {}
}
```
This way, the function is visible in the current translation unit, as the namespace is implicitly imported into it, but it is not visible in other translation units, because anonymous namespaces cannot be imported.

One of the other approches frequently used in C++ is to **put the function declaration into the source file** so it cannot be included from the header. This solution is, however, flawed, unsafe, and therefore, **not recommended**. The problem is that this way, the function is still visible to the linker, and can be mistakenly used from another translation unit if somebody declare a function with the same name.



## Deleting functions
[cppreference](https://en.cppreference.com/w/cpp/language/function#Deleted_functions)

We can delete functions using the `delete` keyword. This is mostly used for preventing the usage of copy/move constructors and assignment operators. However, it can be used for any function, as we illustrate in the following example:
```cpp
class My_class{
	print_integer(int a){
		std::cout << a << std::endl;
	}
	// we do not want to print doubles even they can be implicitly converted to int
	print_integer(double a) = delete; 
}
```


# Classes and structs
The only difference between a `class` and a `struct` is that in class, all 
members are private by default.

## Class Constants
Class constants can be defined in two ways:

- `static constexpr` member variable if the constant type supports `constexpr` specifier, or
- `static const` member variable 

In the second case, we have to split the declaration and definition of the variable to avoid multiple definitions:
```cpp
// in the header file
class My_class{
	static const int a;
}

// in the cpp file
const int My_class::a = 5;
```

## Friend declaration
[cppreference](https://en.cppreferececom/friend)

Sometimes, we need to provide an access to privat e members of a class to some other classes. In java, for example, we can put both classes to the same package and set the members as package private (no specifier). In C++, there is an even stronger concept of friend classes.

We put a `friend` declaration to the body of a class whose *private* members should be accessible from some other class. The declaratiton can look as follows:
```cpp
Class To_be_accesssed {
	friend Has_access;
}
```
Now the `Has_access` class has access to the `To_be_accesssed`'s private members.

Note that the **friend relation is not transitive, nor symetric, and it is not inherited.**


### Template friends
If we want a template to be a friend, we can modify the code above:
```cpp
class To_be_accesssed {
	template<class T>
	friend class Has_access;
}
```
Now every `Has_access<T>` is a friend of `To_be_accesssed`. Note thet we need to use keyword `class` next to `friend`.

We can also use only a template spetialization: 

```cpp
class To_be_accesssed {
	friend class Has_access<int>;
}
```

or we can bound the allowed types of two templates togehter if both `Has_access` and of `To_be_accesssed` are templates:
```cpp
template<class T>
class To_be_accesssed {
	friend class Has_access<T>;
}
```



# Initialization and Assignment

## Loacal variables initialization/assignment
[Initialization](https://en.cppreference.com/w/cpp/language/initialization) happens in many **contexts**:

- in the declaration
- in `new` expression
- function parameter initialization
- return value initialization

The **syntax** can be:

- `(<expression list>)`
- ` = expression list`
- `{<initializer list>}`

Finally, there are multiple initialization types, the resulting **initialization type** depends on both context and syntax:

- Value initialization: `std::string s{};`
- Direct initialization: `std::string s{"value"}`
- Copy initialization: `std::string s = "value"`
- List initialization: `std::string s{'v', 'a', 'l', 'u', 'e'}`
- Aggregate initialization: `char a[3] = {'a', 'b'}`
- Reference initialization: `char& c = a[0]`
- Default initialization: `std::string s`

### List initialization
[List initialization](https://en.cppreference.com/w/cpp/language/list_initialization) initializes an object from a list. he list initialization has many forms, including:

- `My_class c{arg_1, arg_2}` 
- `My_class c = {arg_1, arg_2}`
- `my_func({arg_1, arg_2})`
- `return {arg_1, arg_2}`

The list initialization of a type `T` can result in various initializations/constructios depending on many aspects. Here is the simplified algorithm:
 1. `T` is aggregate -> aggregate initialization
 2. The initializer list is empty and `T` has a default constructor -> value initialization
 3. `T` has an constructor accepting `std::initializer_list` -> this constructor is called
 4. other constructors of `T` are considered, excluding explicit constructors

### Value initialization
[cppreference](https://en.cppreference.com/w/cpp/language/value_initialization)

This initializon is performed when we do not porvide any parameters for the initialization. Depending on the object, it results in either defualt or zero initialization.

### Aggregate initialization
[Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) is an initialization for aggregate types. It is a form of list initialization. Example:

```cpp
My_class o1{arg_1, arg_2};
My_class o2 = {arg_1, arg_2}; // equivalent
```

The list initialization of type `T` from an initializer list results in aggregate initialization if these conditions are fullfilled:

- the initializer list contains more then one element
- T is an aggregate type

### Nested initialization
**It is not possible to create nested initializatio statements** like:
```cpp
class My_class{
	int a,
	float b;

public:
	My_class(ina a, float b): a(a), b(b)
}

std::tuple<int, My_class>{2, {3, 2.5}} // does not compile
std::tuple<int, My_class>{2, My_class{3, 2.5}} // correnct version
```


## Member Initialization/Assignment
There are two ways of member initialization:

- **default member initialization**
- initialization using **member initializer list**

And then, there is an assignment option in  **constructor body** .

Reference:

- [default member initialization](https://en.cppreference.com/w/cpp/language/data_members#Member_initialization)
- [constructor and initializer list](https://en.cppreference.comwcplng/w/cpp/language/constructor)

One way or another, **all members should be initialized at the constructor body at latest**, even if we assign them again during all possible use cases. Reason:

- some types (numbers, enums, ...) can have arbitrary values when unassigned. This can lead to confusion when debugging the class, i.e., the member can appear as initialized even if it is not.
- easy support for overloading constructors, we can sometimes skip the call to the constructor with all arguments
- we can avoid default arguments in the constructor


It is important to **not use virtual functions in member initialization or constructor body**, because the function table is not ready yet, so the calls are hard wired, and the results can be unpredictable, possibly compiler dependent.

### Default Member Initialization 
Either a **brace initializer**:
```C++
My_class{
	int member{1} 
}
```
or an **equals initializer**:
```C++
My_class{
	int member = 1 
}
```


### Member Initializer List
Either using [**direct initialization**](https://en.cppreference.com/w/cpp/language/direct_initialization) (calling constructor of `member`):
```C++
My_class{
	My_class(): member(1){
	}
```
or [**list initialization**](https://en.cppreference.com/w/cpp/language/list_initialization):
```C++
My_class{
	My_class(): member{1}{
	}
```

### Constructor Body
```C++
My_class{
	My_class(){
		member = 1
	}
}
```

### Comparison Table
Ordered by priority, i.e., each method makes the methods bellow ignored/ovewritten if applied to the same member.

| Type | In-place | works for const members |
|--|--|--|
| Constructor body | no | no |
| Member initializer list | yes | yes |
| Default member initializer | yes, if we use direct initialization | yes |



# Constructors and Special Member Functions
[cppreference](https://en.cppreference.com/w/cpp/language/member_functions#Special_member_functions)

Special member functions are member functions that are someetimes defined implicitely by the compiler. The special member functions are:

- default (no parameter) constructor
- copy constructor
- copy assignment
- move constructor
- move assignment
- destructor

These functions can be:

- defined implicitely by the compiler
- deleted implicitely by the compiler
- *defaulted*, i.e., defined by the compiler on our request
	```cpp
	My_class() = default;
	```
	- Along with the comparison operators, these are the only functions that can be  (see below).
- *deleted*, i.e., disabled by the compiler on our request
	```cpp
	My_class(const My_class&) = delete;
	```

By default, all special member functions are defined implicitely if the members satisfy the requirements (see below). However, if we define any of the special member functions, the implicit definition is disabled. Therefore, **typically, we define all special member functions or none of them.**

## Constructor

### Defualt Variant
The default constructor just create an empty object. The default constructor is not implicitly generated if:

- there is anothe constructor declared, including copy and move constructor
- there is some member that cannot be defaulty initialized

### Explicit constructor
Sometimes, a normal constructor can lead to unexpected results, especially if it has only a single argument:
```cpp
class My_string {
public:
	String(std::string string); // convert from std::string
   	String(int length);   // construct empty string with a preallocated size
};

String s = 10;   // surprise: empty string of size 10 istead of "10"
```    

To prevent these surprising conversion, we can mark the constructor `explicit`. The `explicit` keyword before the constructor name prevents the assigment using this constructor. The explicit constructor has to be explicitelly called.    


### Call one constructor from another
We can call one constructor from another using the *[delegating constructor](https://en.cppreference.com/w/cpp/language/constructor#Delegating_constructor)*. The syntax is:
```cpp
class My_class{
public:
	My_class(int a, int b): a(a), b(b){}
	My_class(int a): My_class(a, 0){} // delegating constructor
}
```
This way, we can call another constructor of the same class, or of the base class. 


## Copy Constructor
[cppreference](https://en.cppreference.com/w/cpp/language/copy_constructor)

A copy constructor is called if an object is initialized from another object unless the move constructor is called as a better fit or the call is optimized out by [copy elision](https://en.cppreference.com/w/cpp/language/copy_elision). Some examples:

- initializing a new object from an existing object:
```cpp
My_class a;

My_class b = a;  // copy constructor called
My_class c(a);  // copy constructor called
```

- passing an object to a function by value:
```cpp
void f(My_class a){...}

My_class a;
f(a); // copy constructor called
```

- returning an object by value where the type is not movable and the compiler cannot optimize the call out.
-  we call the copy constructor directly


### Implicit declaration and implicit deletion
The copy constructor for type `T` is implicitely-declared if `T` has no declared user-defined copy constructors. 

If some there are some user-defined copy constructors, we can still force the implicit declaration of the copy constructor using the `default` keyword

However, the implicit declaration does not mean that the copy constructor can be used! This is because the **copy constructor can be implicitely defined as deleted**. This happens if any of the following conditions is true:

1. T has a non-static data member that cannot be copied. This can happen if any of the following is true:
	- it has a deleted copy constructor,
	- the copy constructor is inaccessible (**protected, private**)
	- the copy constructor is ambiguous (e.g., multiple inheritance)
1. T has a base class that cannot be copied, i.e., 1, 2, or 3 applies to at least one base class
1. T has a non-static data member or base class with inaccessible destructor
1. T has a rvlaue data member
1. T has a user-defined move constructor or move assignment operator (this rule does not apply for defaulted copy constructor)

The default implementationof copy constructor calls recursively the copy constructor of all base classes and on all members. For a pointer member, the copy object’s member points to the same object as the original object’s member


### Checking if a class is copy constructible
We can check if a class is copy constructible using the [`std::is_copy_constructible`](https://en.cppreference.com/w/cpp/types/is_copy_constructible) type trait. 


## Copy Assignment
Copy Assignment is needed when  we use the `=` operator with the existing class instances, e.g.:
```cpp
Class instanceA {};
Class instanceB;
instanceB = instance A
```
    

## Move Constructor
[cppreference](https://en.cppreference.com/w/cpp/language/move_constructor)

Move constructor semantic is that the new object takes the ownership of the resources of the old object. The state of the old object is unspecified, but it should not be used anymore. 

Move constructor is typically called when the object is initaialized from xvalue (but not prvalue!) of the same type. Examples:

- returning xvalue: 
```cpp
Type f(){
	Type t;
	return std::move(t);
}
```

- passing argument as xvalue:
```cpp
f(Type t){
	...
}
Type t
f(std::move(t)); 
```

- initializing from xvalue:
```cpp
Type t;
Type t2 = std::move(t);
```

Note that for prvalues, the move call is eliminated by [copy elision](https://en.cppreference.com/w/cpp/language/copy_elision). Therefore, some calls that suggest move constructor call are actually optimized out:
```cpp
Type f(){
	Type t;
	return t; // no move constructor call, copy elision
}

Type t = T(f()) // no move constructor call, copy elision
```

Move constructor is needed:

- to cheaply move the object out from function if RVO is not possible
- to store the object in vector without copying it

Note that a single class can have multiple move constructors, e.g.: both `Type(Type&&)` and `Type(const Type&&)`.


### Implicit declaration and implicit deletion
The move constructor for type `T` is implicitely-declared if `T` has no declared copy constructors, copy assignment operators, move assignment operators, or destructors.

If some of the above is declared, we can still force the implicit declaration of the move constructor using the `default` keyword

However, that does not mean that the move constructor can be used! This is because the **move constructor can be implicitely defined as deleted**. This happens if any of the following conditions is true:

1. T has a non-static data member that cannot be moved. A member cannot be moved if any of the following is true:
	- it has a deleted, inaccessible (protected, private), or ambiguous move constructor,
	- it is a reference,
	- it is **const**-qualified
1. T has a base class that cannot be moved, i.e., 1, 2, or 3 applies to at least one base class
1. T has a non-static data member or base class with inaccessible destructor


### Checking if a class is move constructible
We can check if a class is move constructible using the [`std::is_move_constructible`](https://en.cppreference.com/w/cpp/types/is_move_constructible) type trait. However, **the `std::is_move_constructible` does not check if the move constructor is accessible!** Instead it checks if the call to the move constructor is valid (can success, compiles). The call can success if the move constructor is accessible, but it can also success if it is not accessible, but the class has a copy constructor, which is used instead. 

To check if the move constructor is accessible, we have to manually check the conditions, or disable the copy constructor. 



## Move Assignment


## Trivial special member functions
The special member functions are called trivial if they contain no operations other then copying/moving the members and base classes. For a special member function of type `T` to be trivial, all of the following conditions must be true:

- it is implicitly-declared or defaulted
- `T` has no virtual functions
- `T` has no virtual base classes
- the constructor for all direct base classes is trivial
- the constructor for all non-static data members is trivial


## Destructor
We need destructor only if the object owns some resources that needs to be manually deallocated


## Typical usage
It's mostly better to delete everything you don’t need. Most likely, either
- we need no custom constructors, or we need three (move and destructor), or we need all of them.

### Simple Temporary Object

- the object should live only in some local context
- we don’t need anything

### Unique Object

- usually represents some real object
- usually, we need constructors for passing the ownership:
	- move constructor
	- move assignment

### Default Object

- copyable object
- We need
	- copy constructor
	- copy assignment
	- move constructor
	- move assignment


# Const vs non-const 
The `const` keyword makes the object non-mutable. This means that:

- it cannot be reassigned
- non-const member functions of the object cannot be called

The const keyword is usually used for local variables, function parameters, etc.

**For members, the const keyword should not be used**, as it sometimes breaks the move operations on the object. For example we cannot move from a const `std::unique_ptr<T>` object. While this is also true for local variable, in members, it can lead to hard to find compilation errors, as a single const `std::unique_ptr<T>`  member deep in the object hierarchy breaks the move semantic for the whole class and all subclasses.

## Avoiding duplication between const and non-const version of the same function
To solve this problem without threatening the const-correctness, we need to implement the *const* version of a function and call it from the non-const one with double type cast:

- one that converts *this* to const, so we can call the const version of the function
- another one that removes const from the return value

Example:
```cpp
const Content& get_content(unsigned index) const {
	Content content = ... // complicated code to get the right content
	return content;
}

Content& get_content(unsigned index){
	return const_cast<Content&>(std::as_const(this*).get_content());
}

```

## Const/non const overloads and inheritance
Normally, the compiler can safely choose the best match between const and non-const overloads. The problem can happen when each version is in a different place in the class hierarchy. Example:
```cpp
class Base {
public:
	const int& get() const {
    return some;
  }
protected:
  int some;
};

class A : public virtual Base {
public:
  int& get() {
    return some;
  }
};

class B : public A {};

B test;
test.get(); // ambiguous function error
```
The problem is that the overload set is created for each class in the hierarchy separately. So if the overload was resolved prior the virtual function resolution, we would have only one version (non-const), which would be chosen, despite not being the best overload match in both overload sets. To prevent such unexpected result, some compilers (GCC) raise an ambiguous function error in such situations.

To resolve that, we can merge the overload sets in class `B`:
```cpp
class B : public A {
	using Base:get;
	using A:get;
};
```



# IO and Filesystem
The simple way to print to standard input is:
```cpp
std::cout << "Hello world" << std::endl;
```

To return to the begining of the line and overwrite the previous output, we can use the `'\r'` character:
```cpp
std::cout << "Hello world" << '\r' << std::flush;
```


## File path manipulation
Although we can use strings to work with file paths in C++, the standard format which is also easy to use is [`std::filesystem::path`](https://en.cppreference.com/w/cpp/filesystem/path) from the [filesystem library](https://en.cppreference.com/w/cpp/filesystem).

Basic operations:

- To **create a path**, we jusct call `std::filesystem::path(<string path>)`.
- We can easily **join two paths** by `auto full_path = <path 1> / <path 2>`;
- To get the **asolute path**, we call
	- [`std::filesystem::absolute(<path>)`](https://en.cppreference.com/w/cpp/filesystem/absolute) to get the path as `CWD/<path>`
	- [`std::filesystem::canonical(<path>)`](https://en.cppreference.com/w/cpp/filesystem/canonical) to get the dots resolved. Note that this method throws exception if the path does not exists.
- The path to the **current working directory** can be obtained by calling `std::filesystem::current_path()` and set using `std::filesystem::current_path(<path>)`.
- To change the file extension (in the C++ representation, not in the filesystem), we can call the [`replace_extension`](https://en.cppreference.com/w/cpp/filesystem/path/replace_extension) method.



## Filesystem manipulation
[cppreference](https://en.cppreference.com/w/cpp/filesystem) 

### Copying
To copy, we can use [`std::filesystem::copy(<source path>, <destination path>[, <options>])`](https://en.cppreference.com/w/cpp/filesystem/copy) function.

The options parameter type is [`std::filesystem::copy_options`](https://en.cppreference.com/w/cpp/filesystem/copy_options). This enum is a bitmask type, therefore, multiple options can be combined using the `|` operator. Example:
```cpp
auto options = std::filesystem::copy_options::recursive | std::filesystem::copy_options::overwrite_existing;

std::filesystem::copy("C:/temp/data", "c:/data/new", options);
```

Note that **unlike the unix `cp` command, the `copy` function does not copy the directoy itself**, even if the destination directory exists. Suppose we have two direcories:

- `C:/temp/new` 
- `C:/data/`

And we want to copy the `new` folder, so that the result is: `C:/data/new/`. In bash, this will be:
```bash
cp -r C:/temp/new C:/data/
```
While in C++, we need to do:
```cpp
std::filesystem::copy("C:/temp/new", "C:/data/new",  std::filesystem::copy_options::recursive);
```


### Creating directories
To create a directory, we can use [`std::filesystem::create_directory(<path>)`](https://en.cppreference.com/w/cpp/filesystem/create_directory) function. 

This function fails if the parent directory does not exist. To create the parent directories as well, we can use [`std::filesystem::create_directories(<path>)`](https://en.cppreference.com/w/cpp/filesystem/create_directory) function.


### Removing files and directories
To remove a file or an empty directory, we can use [`std::filesystem::remove(<path>)`](https://en.cppreference.com/w/cpp/filesystem/remove) function.

To remove a content of a directory we can use `std::filesystem::remove_all(<path>)` function listed on the same page of cppreference.


### Other useful functions

- [`std::filesystem::exists(<path>)`](https://en.cppreference.com/w/cpp/filesystem/exists)
- [`std::filesystem::is_directory(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_directory)
- [`std::filesystem::is_regular_file(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_regular_file)
- [`std::filesystem::is_empty(<path>)`](https://en.cppreference.com/w/cpp/filesystem/is_empty)


## Manual text IO

### Input
For input, we can use [`std::ifstream`](https://en.cppreference.com/w/cpp/io/basic_ifstream):
```cpp
std::ifstream file;
file.open(<path>);
...
file.close();
```
The important thing is that we need to check whether the `open` call was successful. **The `open` function never throws an exception, even if the file does not exist**, which is a common case. Instead, it only sets the `failbit` of the stream. Without some check, the failure is hidden as an ifstream  in a fail state behaves as if it was empty.

For reading **line by line**, we can use the `std::getline` function:
```cpp
std::string line;
while (std::getline(file, line)) {
	// do something with the line
}
```

However, processing the line is currently not very convenient in C++ because functions from other languages like `split` are missing.

For **reading whitespace delimited tokens** we can instead use the [`>>` operator](https://en.cppreference.com/w/cpp/io/basic_istream/operator_gtgt) on the stream:
```cpp
// file content: "01 Smith"

int id;
std::string name;

file >> id >> name;
```

If we need to skip some tokens, its best to introduce a dummy string variable:
```cpp
// file content: "01 2021-01-01 active Smith"

int id;
std::string dummy;
std::string name;

file >> id >> dummy >> dummy >> name;
```

Conveniently, the input streams have a `bool` operator that states whether the stream is in a state ready for reading. This way, we can easily stop the loop when the file is read, because the `>>` operator returns the stream itself:
```cpp
// read the whole file
while (file >> id >> name) {
	...
}
```





### Output
For line by line output, we use `std::ofstream`:
```cpp
std::ofstream file;
file.open(<path>);
batch_file << "first line" << std::endl;
batch_file << "second line" << std::endl;
...
batch_file.close();
```


## Load whole file into string
Again, we use the `std::ifstream`, but this time, we also use the `std::istreambuf_iterator` to read the whole file into a string:
```cpp
std::ifstream file(<path>);
std::string content(std::istreambuf_iterator<char>{file}, {});
```
Here, the `std::istreambuf_iterator<char>` is created using initialization instead of the constructor so that the local variable is not confused with function declaration. The `{}` is used to create an empty string, which is the end of the range for the iterator.

## csv
### Input
### Output
For csv output, we can usually use the general line-by-line approach.


## YAML
For YAML, we can use the [yaml-cpp](https://github.com/jbeder/yaml-cpp/) library.

To test whether a `YAML::Node` **contains a certain key**, we may use the `[]` operator, as it does not create a new node (unlike the stl containers):
```cpp
YAML::Node node;
if (node["key"]) {
	// do something
}
```
The **iteration** over the keys is done using `YAML::const_iterator`:
```cpp
for (YAML::const_iterator it = node.begin(); it != node.end(); ++it) {
	std::string key = it->first.as<std::string>();
	YAML::Node value = it->second;
}
```



# Inheritance
Inheritance in C++ is similar to other languages, here are the important points:

- To enable overiding, a member function needs to be declared as `virtual`. Otherwise, it will be just hidden in a child with a function with the same name, and the `override` specifier cannot be used (see Shadowing).
- Multiple inheritance is possible.
- No interfaces. Instead, you can use abstract class with no data members.
- Virtual functions without implementation needs `= 0` at the end of the declaration (e.g.: `virtual void print() = 0;`)
- a type is polymorphic if it has at least one virtual function. I.e., the inheritance itself does not make the type polymorphic.

## Polymorphism
Polymorphism is a concept for abstraction using which we can provide a single interface for multiple types that share the same parent. In C++, to use the polymorphism, **we need to work with pointers or references**. Imagine that we have these two class and a method that can process the base class:

```c++
class Base {
};

class Derived: public Base {
};

void process_base(Base* base) {
}
```

Now we can use it lake this:
```c++
Derived* derived = new Derived(); 
Base* base = derived; // we easilly can convert derived to base
process_base(base);
process_base(derived); // we can call the function that accepts a base pointer with a derived pointer
```
We can do the same with smart pointers:
```c++
void process_base_sh(std::shared_ptr<Base> base) {
}

std::shared_ptr<Derived> derived_sh = std::make_shared<Derived>();
std::shared_ptr<Base> base_sh = derived_sh;

process_base_sh(base_sh);
process_base_sh(derived_sh);
```

## Shadowing/Hiding: why is a function from parent not available in child?
Members in child with a same name as another members in parent shadows those members (except the case when the parent member is virtual). When a member is shadowed/hiden, it is not available in the child class and it cannot be called using the child class instance. 

This can be counter-intuitive for functions as **the shadowing considers only the name, not the signature**. Example:

```c++
class Base {
public:
	void print() {
		printf("Base\n");
	}
};

class Child: public Base {
public:
	void print(std::string type) {
		printf("Child " + type + "\n");
	}
};

int main()
{
	Child child;
	child.print(); // does not compile, as the print() is hidden by print(std::string)
	return 0;
}
```


### How to call a hidden function?
There are two ways how to call a hideen function:

1. we can use the `using` declaration in the child to introduce the hidden function:
	```c++
	class Child: public Base {
	public:
		using Base::print; // now the print() is available in Child
		void print(std::string type) {
			printf("Child " + type + "\n");
		}
	};
	```

2. Usiang a *fully qualified name* of the method:
	```c++
	int main()
	{
		Child child;
		child.Base::print(); 
		return 0;
	}
	```


## Constructors
Parent constructor is always called from a child. By default, an empty constructor is called. Alternatively, we can call another constructor in the initializer. When we do not call the parent constructor in the child's initializer and the parent has no empty constructor, a compilation error is raised.

### Enablinging Parent Constructors in Child
Implicitly, all methods from parent classes are visible in child, with exception of constructors. Constructors can be inherited manually with a `using` declaration, but only all at once.
To enable only some constructors, we need to repeat them manually as child constructors and call parent construcors from them.

### Inheritance and Constructors/Destructors
To prevent the future bugs with polymorphic destruction calls, **it's a good habit to declare a public virtual destructor in each base class**:
```C++
class Base{
public:
	virtual ~Base() = default;
}
```

Otherwise, the following code will not call the child destructor:

```C++
Child* child = new Child();
Base* base = (Base) child;
delete base;
```

But when defining destructor, constructor and move operations are not impliciotely  generated. Moreover, the copy operations are generated enabling a polymorphic copy, which results in slicing.  Therefore, **the best approach for the base class** is to: 

- declare the **virtual destrucor** as default
- declare the **default constructor**. We need a default constructor, unless we use a diferent constructor and we want to disable the default one.
- declare the **copy and move operations as protected**. This way, the polymorpic copy is not possible, but proper copy/move operations are generated for every child class.  


### Initializing base class members
The base class members cannot be initialized in the child constructor initializer. Instead, we need to create a constructor in the base class and call it from the child constructor initializer.


## Slicing
Polymorphism does not go well with value types. When a value type is copied, the only part that remains is the part writen in the code. That means that copying `base_2 = base_1` result in a new `Base` object in `base_2`, even if `base_1` is an instance of child. **Abstract classes therefore cannot be used as function value arguments at all**.

To pass a polymorphic type as a value to a library function, we need a copyable wrapper that forwards all calls to the undelying polymorphic type.

## Checking the Type
There is no equivalent of Java's `instanceof` in C++. To check the type. it is possible to use dynamic cast:

```C++
Child& child = dynamic_cast<Child&>(parent)
```
In case of failure, `std::bad_cast` is thrown. To prevent exceptions (i.e., we need the type check for branching), we can use pointers:

```C++
Child* child = dynamic_cast<Child*>(&parent)
```
In this case, if the cast fails, then `child == nullptr`.

**Note that to use the `dynamic_cast` on a type, the type, the type needs to have at least one virtual method**. However, this should not be an issue as the type should have at least a virtual destructor.

## Covariant Return Type
Covariant return type is a concept of returning a narower type id derived class than the return type specified in base. Example:
```c++
class Base {
public:
	virtual Base& get() = 0;
};

class Derived: public Base{
public:
	Derived& get() override {
		return *this;
	}
};
```

It works with template classes too:
```c++
template<class T>
class Derived_template: public Base {
public:
	Derived_template<T>& get() override {
		return &this;
	}
};
```

## Use Method from Parent to Override a Method from Other Parent
Unlike in java, **a parent method cannot be used to implement an interface of a child**. Example:
```c++
class Interface {
public:
	virtual void print() = 0;
};

class Base {
public:
	virtual void print() {
		printf("Base\n");
	}
};

class Child: public Base, public Interface {
public:

};

int main()
{
	Child child; // does not compile, as Child is an abstract class

	child.print();
	return 0;
}
```
The above code does not compile as in C++, the parent `print()` method is not used as an impementation of `print()` from the interface (like it works e.g. in Java).

There simplest solution to this problem is to override the method in `Child` and call the parent method staticaly:

```c++
class Child: public Base, public Interface {
public:
	void print() override {
		Base::print();
	}
};
```


## Multiple inheritance and virtual base classes
[wiki](https://en.wikipedia.org/wiki/Virtual_inheritance)

[cppreference](https://en.cppreference.com/w/cpp/language/derived_class#Virtual_base_classes)

Multiple inheritance is possible in C++. However, it can lead to some problems.
Consider the following example:
```c++
class A {
public:
	int a;
};

class B: public A {};

class C: public A {};

class D: public B, public C {};
```
It may not be obvious, but the **class `D` has two instances of `A`** in it. This is because the `B` and `C` both have their own instance of `A`. This is certainly not what we want as this way, we have two copies of `A::a` in `D`, which are only accessible using qualified names (`D::B::a` and `D::C::a`) and which can have different values. 


### Virtual Inheritance
To mitigate this problem, we can use the *virtual inheritance*. The virtual inheritance is used when we want to have only one instance of a base class in a child class, even if the base class is inherited multiple times. To use the virtual inheritance, we need to declare the base class as virtual in all child classes:
```c++
class A {
public:
	int a;
};

class B: public virtual A {};

class C: public virtual A {};

class D: public B, public C {};
```

### Multiple copy/move calls with virtual inheritance
However, this solves only the problem of having multiple instances of the same base class. But there are also problems with the copy and move operations. In the above example, if the class `D` is copied or moved, it calls the copy/move operations of `B` and `C`, which in turn call the copy/move operations of `A`. **This means that the `A` is copied/moved twice**, which is not what we want.

To solve this we need to manually define the copy/move operations of classes in the hierarchy so that the copy/move operations of the base class are called only once. However this can be a complex task. Also, it can backfire later when we extend the hierarchy.

### Other sources

- [SO answer](https://stackoverflow.com/questions/406081/why-should-i-avoid-multiple-inheritance/407928#407928)
- [SO answer 2](https://stackoverflow.com/questions/21558/in-c-what-is-a-virtual-base-class/21607#21607)

# Templates
The templates are a powerful tool for:

- generic programming,
- zero-overhead interfaces,
- and metaprogramming.

Although they have similar syntax as generics in Java, they are principialy different both in the way they are implemented and in the way they are used.

There are two types of templates:

- function templates
- class templates

## Syntax
### Template Declaration
Both for classes and functions, the template declaration has the following form:
```cpp
template<<template parameters>>
```
The template parameters can be:

- type parameters: `class T`
- value parameters: `int N`
- concept parameters: `std::integral T`


### Template definition
The definition of template functions or functions fo the template class requires the template declaration to be present. The definition has the following form:
```cpp
template<<template parameters>>
<standard function definition>
```
Here, the template parameters are the function template parameters if we define a template function, or the class template parameters if we define a function of a template class.

If the template function is a member of a template class, we have to specify both the template parameters of the function and the template parameters of the class:
```cpp
template<<class template parameters>>
template<<function template parameters>>
<standard class function definition>
```

Note that the **template definition has to be in the header file**, either directly or included from another header file. This includes the member function definitions of a template class, even if they are not templated themselves and does not use the template parameters of the class.


## Organization rules

 - `*.h`: declarations
 - `*.tpp` template definitions
 - `*.cpp` non-template definitions.

For simplicity, we include the `tpp` files at the end of corresponding header files. If we need to speed up the compilation, we can include the `tpp` files only in the source files that needs the implementations , as described on [SE](https://softwareengineering.stackexchange.com/questions/373916/c-preferred-method-of-dealing-with-implementation-for-large-templates)

To speed up the build it **is also desireble to move any non-template code to source files**, even through inheritance, if needed.


## Providing Template Arguments
A template can be instantiated only if all the template arguments are provided.

The **templete arguments need to be complete types**.

Arguments can be

- provided explicitly: `std::vector<int> v;` or `sum<int>(1,2)`,
- deduced
	- from the initialization (classes): `std::vector v = {1,2,3};`
	- from the context (functions): `sum(1,2);`, or
- defaulted

	```cpp
	template<class T = int>
	class A {};

	template<class T = int>
	int sum<T>(T a, T b = 0) {
		return a + b;
	}

	auto s = sum(1, 2);

	A a();
	```


If we want the template arguments to be deduced or defaulted, we usually  use the `<>`:
```cpp
template<class T = int>
class A {};

A<> a(); // default argument is used
std::vector<A<>> v; // default argument is used 
```
In some cases, the `<>` can be ommited, e.g., when declaring a variable:
```cpp
A a; // default argument is used

// but
std::vector<A> v; // error, the A is considered a template here, not the instantiation
```

The rules for omitting the `<>` are quite complex. Therefore, **it is better to always use the `<>`** when we want to use the default arguments.


### Rules for omitting the `<>`
We can ommite the `<>` in the following cases:

- when declaring a variable: `A a;`
- when using the type in a function call: `f(A());`
- when instantiating a template class: `class B: public A {};`

We cannot ommite the `<>` in the following cases:

- When we use the template as a nested type: `std::vector<A<>> v;`, not `std::vector<A> v;`
- in the return type of a function: `A<> f()`, not `A f()`
- When declaring an alias: `using B = A<>` not `using B = A`
- for template template parameters.




### Default Template Arguments
Default template arguments can be used to provide a default value for any template parameter except parameter packs. 

For template classes, there is a restriction that after a default argument is used, all the following parameters must have a default argument as well, except the last one wchich can be parameter pack. 


## Template Argument Deduction
Details on [cppreference](https://en.cppreference.com/w/cpp/language/template_argument_deduction).

Template argument deduction should work for:

- constructors
- function and operator calls
- storing the function pointer


## Class Template Argument Deduction (CTAD)
Details on [cppreference](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction).

The main difference from the function templete argument deduction is that in CTAD, all the template arguments needs to be specified, or all must not be specified and must be deducible.

Apart from that, there are more subtle differences arising of a complex procedure that is behind CTAD. We explain CTAD principle using a new concept (not a C++ concept :) ) called *deduction guides*.

### Deduction Guides
The CTAD use so called *deductione guides* to deduce the template parameters. Deduction guides can be either implicit or explicit. To demonstrate the principle, let's first start with user-defined deduction guides.

#### User defined deduction guides
 Let's have an iterator wrapper class below:

```cpp
template<class E, Iterator<E> I>
class Iter_wrapper{
public:
	explicit Iter_wrapper(I iterator){
	...
	}
	...
};
```
Here, the argument `E` cannot be deduced from argument `I`, despite the use of the `Iterator` concept may indicate otherwise. We can still enable the deduction by adding the following deduction guide:

```cpp
template<class I> Iter_wrapper(I iterator) -> Iter_wrapper<decltype(*iterator),I>;
``` 
Here, the part left from `->` represents the constructor call that should be guided, and the part right from `->` defines the argument types we want to deduce.

Some more details about user defined deduction guides are also on the [Microsoft Blog](https://devblogs.microsoft.com/cppblog/how-to-use-class-template-argument-deduction/).


#### Implicit deduction guides
The vast majority of deduction guidedes used in CTAD are implicit. The most important implicit deduction guides are:

- constructor deduction guides
- copy deduction guides

The **copy** deduction guide has the following form:
```
template<<class template parameters>> <class>(<class><class template parameters> obj) -> <class><class template parameters>;
```
For a simple wrapper class:
```cpp
template<class C>
class Wrapper{
	...
}

template<class C> Wrapper(Wrapper<C> obj) -> Wrapper<C>; // implicitelly defined copy deduction guide
```

The constructor deduction guides has the following form:
```
template<<class template parameters>> <class>(<constructor arguments>) -> <class><class template parameters>;
```

For a simple wrapper class:
```cpp
template<class C>
class Wrapper{
	Wrapper(T&& ref);
}

template<class C> Wrapper(C&&) -> Wrapper<C>; // implicitelly defined constructor deduction guide
```


#### Deduction guides resolution
**Note that CTAD is a process independent of the constructor overload!**. First an appropriate deduction guide is used to deduce the class template argumnets, this process can fail if there is no guide. Only then, the overload resolution begins. 

Most of the time, it is not so important and we can just look at the constructor that is chosen by the constructor overload resolution process and see the used deduction guids and consequently, the resulting template arguments. Sometimes, however, this simplified understanding can lead to confusing results:
```cpp
template<class C>
class Wrapper{
	Wrapper(T&& ref);

	Wrapper(double&& ref); // special overload for double
}

auto w1 = Wrapper(1.5) // the double overload is called
```
In the above example, it may be surprising that the second constructor can be called, as it does not have the class argument present, so the implicit deduction guide cannot work:
```cpp
template<class C> Wrapper(double&&) -> Wrapper<C>; // C unknown! 
```

However, it compiles and works, because the deduction guide from the first constructor is used for CTAD, and then, the second constructor is chosen by the constructor overload.


## Template Specialization
Template specialization is a way to provide a different implementation of a template for a specific type. For example, we can provide a different implementation of a template for a `std::string` type. Imagine following class:

```cpp
// declaration
template<class T>
class Object{
public:
	void print(T value)
};

// definition
template<class T>
void Object<T>::print(T value){
	std::cout << value << std::endl;
}
```

Now, we can provide a different implementation for `std::string`:

```cpp
// declaration
template<>
class Object{
public:
	void print(std::string value)
};

template<>
void Object<std::string>::print(std::string value){
	std::cout << value << std::endl;
}
```

There are two types of template specialization:

- **full specialization**: exact specification for all template arguments
- [**partial specialization**](https://en.cppreference.com/w/cpp/language/partial_specialization): exact specification for a subset of template arguments and/or non-type template arguments

To demonstrate the difference, let's have a look at the following example:
```cpp
// declaration
template<class T, class C>
class Object{}; // primary template

// full specialization
template<>
class Object<int, std::string>{}; // full specialization

// partial specializations
template<class C>
class Object<int, C>{}; // not a full specialization, as C is not specified

template<std::integral T, My_concept C>
class Object<T, C>{}; // not a full specialization, types are not exactly specified
```

While behaving similarly, there are some important differences between the two types:

- **Full specialization is a new type. Therefore, it must be defined in the source file (`.cpp`), just like any other class or function and it must have a separate declaration.** On the other hand, partial specialization is still just a template, so it must be defined in the header file (`.h` or `.tpp`).
- **For functions, we cannot provide a partial specialization**. For member functions we can solve this by specializing the whole class. The solution for any function is to alloow all types in the function and use `if constexpr` to select the correct implementation:
	```cpp
	template<class T, class C>
	class Object{
	public:
		bool process(T value, C config){
			if constexpr (std::is_same_v<T, std::string>){
				return process_string(value, config);
			} 
			else {
				return process_value(value, config);
			}
		}
	};
	```
	- Note that here, the `if constexpr` requires the corresponding `else` branch. Otherwise, the code cannot be discarded during the compilation. Example:
		```cpp
		template<class T, class C>
		class Object{
		public:
			bool process(T value, C config){
				if constexpr (std::is_same_v<T, std::string>){
					return process_string(value, config);
				} 

				return process_value(value, config); // this compiles even if T is std::string
			}
		};
		```


## Templates and Namespaces
If the templated code resides in a namespace, it can be tempting to save few lines of code by sorrounding both `.h` and `.tpp` files using one namespace expression:
```cpp
// structs.h hile
namespace my_namespace {
	// declarations...

	#include 'structs.tpp'
}

// structs.tpp
	// definitions

```
However, this can confuse some IDEs (e.g., false positive errors in IntelliSense), so it is better to introduce the namespace in both files:
```cpp
// structs.h hile
namespace my_namespace {
	// declarations...
}

#include 'structs.tpp'

// structs.tpp
namespace my_namespace {
	// definitions
}
```

Don't forget to close the file and reopen it after the change to clear the errors.



## Using Complicated Types as Template Arguments
Sometimes, it can be very tricky to determine the template argument we need in order to use the template. The correct argument can be for example a return value of some function,  templete function, or even member function of a template instanciation which has other templates as argument...

To make it easier, we can, istead of suplying the correct arguments, evaluate an expression that returns the correct type and then use the [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) specifier.  For more info, see the *Determining Type from Expressions* section.





# Type Traits
The purpose of type traits is to create predicates involving teplate parameters. Using type traits, we can ask questios about template parameters. With the answer to these questions, we can even implement conditional compilation, i.e., select a correct template based on parameter type. Most of the STL type traits are defined in header [`type_traits`](https://en.cppreference.com/w/cpp/header/type_traits).

A type trate is a template with a constant that holds the result of the predicate, i.e., the answer to the question.

[More about type traits](https://www.internalpointers.com/post/quick-primer-type-traits-modern-cpp)


## Usefull Type Traits

- [`std::is_same`](https://en.cppreference.com/w/cpp/types/is_same)
- [`std::is_base_of`](https://en.cppreference.com/w/cpp/types/is_base_of)
- [`std::is_convertible`](https://en.cppreference.com/w/cpp/types/is_convertible)
- [`std::conditional`](https://en.cppreference.com/w/cpp/types/conditional): enables if-else type selection


## Replacement for old type traits
Some of the old type traits are no longer needed as they can be replaced by new language features, which are more readable and less error prone. Some examples:

- [`std::enable_if`](https://en.cppreference.com/w/cpp/types/enable_if) can be replaced by concepts:
```cpp

// old: enable_if
template<class T>
void f(T x, typename std::enable_if_t<std::is_integral_v<T>, void> = 0) {
	std::cout << x << '\n';
}

// new: concepts
template<std::integral T>
void f(T x) {
	std::cout << x << '\n';
}
```


# Concepts
[cppreference](https://en.cppreference.com/w/cpp/language/constraints)

Concepts are named sets of requiremnets. They can be used instead of `class`/`typename` keywords to restrict the template types.

The syntax is:
```cpp
template<class T, ....>
concept concept-name = constraint-expression
```

The concept can have multiple template parameters. The first one in the declaration stands for the concept itself, so it can be refered in the constraint expression. More template parameters can be optionally added and their purpose is to make the concept generic.

## Constraints
Constraints can be composed using `&&` and `||` operatos. For atomic constaints declaration, we can use:

- Type traits:
```cpp
template<class T>
concept Integral = std::is_integral<T>::value;
```

- Concepts: 
```cpp
template<class T>
concept UnsignedIntegral = Integral<T> && !SignedIntegral<T>;
```

- Requires expression:
```cpp
template<typename T>
concept Addable = requires (T x) { x + x; };
```

Either form we chose, the atomic constraint have to always evaluate to bool. 

## Requires Expression
Requires expressions ar ethe most powerfull conctraints. The syntax is:
```cpp
requires(parameter list){requirements}
```

There are four types of requirements that can appear in the requires expression:

- *simple requiremnet*: a requirement that can contain any expression. Evaluates to true if the expression is valid.
	```cpp
	requires (T x) { x + x; };
	```

- *type requirement*: a requiremnt checking the validity of a type:
	```cpp
	requires
	{
		typename T::inner; // required nested member name
		typename S<T>;     // required class template specialization
		typename Ref<T>;   // required alias template substitution
	};
	```

- *compound requirement*: Checks the arguments and the return type of some call. It has the form: `{expression} -> return-type-requirement;`
	```cpp
	requires(T x)
	{
		{*x} -> std::convertible_to<typename T::inner>;
	}
	```

	- other [useful type traits](#usefull-type-traits) can be used instead of `std::convertible_to`.

- *Nested requirement*: a require expression inside another requires expression:
	````cpp
	requires(T a, size_t n)
	{
		requires Same<T*, decltype(&a)>; // nested
	}
	````

## Auto filling the first template argument
Concepts have a special feature that their first argument can be autoffiled from outer context. Consequentlly, you then fill only the remaining arguments. Examples:

```cpp
//When using the concept
template<class T, class U>
concept Derived = std::is_base_of<U, T>::value;
 
template<Derived<Base> T>
void f(T); // T is constrained by Derived<T, Base>

// When defining the concept
template<typename S>
concept Stock = requires(S stock) {
	// return value is constrained by std::same_as<decltype(stock), double>
	{stock.get_value()} -> std::same_as<double>; 
}
```

## STL Concepts

- [iterator concepts](https://en.cppreference.com/w/cpp/header/iterator)

## Usefull Patterns
### Constrain a Template Argument
Imagine that you have a template function `load` and an abstract class `Loadable_interface` that works as an interface:
```c++
class Loadable_interface{
	virtual void load() = 0;
};

template<class T>
void load(T to_load){
	...
	to load.load()
	...
};
```

Typically you want to constraint the template  argument `T` to the `Loadable_interface` type, so that other developer clearly see the interface requirement, and receives a clear error message if the requirement is not met. 

In Java, we have an `extend` keyword for this purpose that can constraint the template argument. In C++, this can be solved with concepts. First we have to define a concept that requires the interface:
```c++
template<typename L>
concept Loadable =
std::is_base_of_v<Loadable_interface, L>;
```
Than we can use the concept like this:
```c++
template<Loadable T>
void load(T to_load){
	...
	to load.load()
	...
};
```

## Constraint a Concept Argument
Imagine that you have a concept `Loadable` that requires a method `load` to return a  type `T` restricted by a concept `Loadable_type`. One would expect to write the `loadable` concept like this:
```c++
template<typename L, Loadable_type LT>
concept Loadable = 
requires(L loadable) {
	{loadable.load()} -> LT;
};
```
However, this is not possible, as there is a rule that **concept cannot not have associated constraints**. The solution is to use an unrestricted template argument and constrain it inside the concept definition:
```c++
template<typename L, typename LT>
concept Loadable =
Loadable_type<LT> &&
requires(L loadable) {
	{loadable.load()} -> LT;
};
```


## Sources
[https://en.cppreference.com/w/cpp/language/constraints](https://en.cppreference.com/w/cpp/language/constraints)

[Requires expression explained](https://akrzemi1.wordpress.com/2020/01/29/requires-expression/)



# Interfaces
In programming, an interface is usualy a set of requirements that restricts the function or template parameters, so that all types fulfiling the requiremnet can be used as arguments.

Therte are two ways how to create an interface in C++:

- using the *polymorphism*
- using *templates argument restriction*

While the polymorphism is easier to implement, the templating is more powerful and it has zero overhead. The most important thing is probably that despite these concepts can be used together in one application, not all "combinations" are allowed especialy when using tamplates and polymorphism in the same type.

**Note that in C++, polymorphism option work only for function argument restriction, but we cannot directly use it to constrain template arguments** (unlike in Java). 

To demonstrate all possible options, imagine an interface that constraints a type that it must have the following two functions:
```cpp
int get_value();
void set_value(int date);
```
The following sections we will demonstrate how to achieve this using multiple techniques. 


## Interface using polymorfism
Unlike in java, there are no `interface` types in C++. However, we can implement polymorfic interface using abstract class. The following class can be used as an interface:

```cpp
class Value_interface{
	virtual int get_value() = 0;
	virtual void set_value(int date) = 0;
}
```

To use this interface as a fuction argument or return value, follow this example:
```cpp
std::unique_ptr<Value_interface> increment(std::unique_ptr<Value_interface> orig_value){
	return orig_value->set_value(orig_value->get_value() + 1);
}
```
This system works in C++ because it supports multiple inheritance. Do not forget to use the `virtual` keyword, otherwise, the method cannot be overriden.
Note that unlike in other languages, **in C++, the polymorphism cannot be directly use as a template (generic) interface.** Therefore, we cannot use the polymorfism alone to restrict a type.


## Using template argument restriction as an interface
To use template argument restriction as an interface, we can use concepts. The following concept impose the same requirements as the interface from the polymorphism section:
To use template argument restriction as an interface, we can use concepts. The following concept impose the same requirements as the interface from the polymorphism section:

```cpp
template<class V>
concept Value_interface = 
	requires(V value_interface){{value_interface.get_value()} -> std::same_as<int>; }
	&& requires(V value_interface, int value){{value_interface.set_value(value)} -> std::same_as<void>; }
```

Remember that **the return type of the function has to defined by a concept**,  the type cannot be used directly. Therefore, the following require statement is invalid:
```cpp
requires{(V value_interface){value_interface.get_value()} -> int; }
```

To use this interface as an template argument in class use:
```cpp
template<Value_interface V>
class ...
```

And in function arguments and return types:

```cpp
template<Value_interface V> V increment(V orig_value){
	return orig_value.set_value(orig_value.get_value() + 1);
```


### Restricting the member function to be const
To restrict the member function to be const, we neet to make the type value const in the requires expression:
```cpp
template<class V>
concept Value_interface = requires{(const V value_interface) 
	{valvalue_interfaceue.get_value() -> std::same_as<int>;};
};
```



## Using concepts and polymorphism together to restrict template parameters with abstract class
We cannot restrict template parameters by polymorphic interface directly, however, we can combine it with concept. The folowing concept can be used together with the interface from the polymorphic interface section:

```cpp
template<class V>
concept Value_interface_concept = requires std::is_base_of<Value_interface,V>
```

**Neverthless, as much as this combination can seem to be clear and elegent, it brings some problems.**. We can use concepts to imposed many interfaces on a single type, but with this solution, it can lead to a polymorphic hell. While there is no problem with two concepts that directly requires the same method to be present with abstract classes, this can be problematic.
Moreover, we will lose the zero overhead advantage of the concepts, as the polymorphism will be used to implement the interface.



## The Conflict Between Templates and Polymorphism
As described above, messing with polymorphism and templates together can be tricky. Some examples:

### No Virtual Member Function with Template Parameters
An example: a virtual (abstract) function cannot be a template function ([member template function](https://en.cppreference.com/w/cpp/language/member_template) cannot be virtual), so it cannot use template parameters outside of those defined by the class template.

### Polymorphism cannot be used inside template params
If the functin accepts `MyContainer<Animal>` we cannot call it with `MyContainer<Cat>`, even if `Cat` is an instance of Animal.

### Possible solutions for conflicts

-   do not use templates -> more complicated polymorphism (*type erasure* for members/containers)
-   do not use polymorphism -> use templates for interfaces
-   an [adapter](https://www.sciencedirect.com/science/article/pii/S0167642309000021) can be used


## Polymorphic members and containers
When we need to store various object in the same member or container, we can use both templates and polymorphism. However, both techniques has its limits, summarized in the table below:
| | Polymorphism | Templates |
| -- | -- | -- |
| The concrete type has to be known at compile time | `No` | `Yes`
| For multiple member initializations, the member can contain any element. | `No`, the elements have to share base class. | `Yes` |
| For a single initialization, the containar can contain multiple types of objects | `Yes`, if they have the same base class | `No` 
| We can work with value members | `No` | `Yes`
| When using the interface, we need to use downcasting and upcasting | `Yes` | `No`

## Deciding between template and polymorphism
Frequently, we need some entity(class, function) to accept multiple objects through some interface. We have to decide, whether we use templates, or polymorphism for that interface. Some decision points:

- We need to return the same type we enter to the class/function -> use templates
- We have to access the interface (from outside) without knowing the exact type -> use polymorphism
- We need to restrict the member/parametr type in the child -> use templates for the template parameter
- if you need to fix the relation between method parameters/members or template arguments of thouse, you need to use templates 
- If there are space considerations, be aware that every parent class adds an 8 byte pointer to the atribute table

In general, the polymorphic interface have the following adventages:

- easy to implement
- easy to undestand
- similar to what people know from other languages

On the other hand, the interface using concepts has the following adventages:

- no need for type cast
- all types check on compile time -> no runtime errors
- zero overhead
- no object slicing -> you don't have to use pointers when working with this kind of interface
- we can save memory because we don't need the vtable pointers


# Iterators, STL algorithms, and ranges
If we want to iterate over elements in some programming language, we need to fulfill some interface. In Java, this interface is called `Iterable`. Also, there is usually some interface that formalize the underlying work, in Java, for example, it is called `Iterator`. 

In C++, however, the interface for iteration is not handled by polymorphism. Instead, it is handled using type traits and concepts. On top of that, there are multiple interfaces for iteration:

- legacy iteration, e.g., `for (auto it = v.begin(); it != v.end(); ++it)`
- STL algorithms, e.g., `std::find(v.begin(), v.end(), 42)`
- STL range algorithms, e.g., `std::ranges::find(v, 42)`
- STL range views, e.g., `std::ranges::views::filter(v, [](int x){return x > 0;})`

The following table summarizes the differences between the interfaces:
|---| Plain iteration | STL algorithms | STL range algorithms | STL range views |
|---|---|---|---|---|
| **Interface** | type traits | type traits | concepts | concepts |
| **Iteration** | eager | eager | eager | lazy |
| **Modify the underlying range*** | no | yes | yes | no |
| **Can work on temporaries** | yes | yes | yes | no |

*If the operation modifies the data, i.e., sorting, shuffling, transforming, etc.

The examples below demonstrate the differences between the interfaces on the following task: create a vector of 10 elements with values 0,1,2,...,9, i.e., the same as Python `range(10)`.
```cpp
// plain iteration
std::vector<int> vec(10);
int i = 0;
for (auto it = vec.begin(); it != vec.end(); ++it) {
	*it = i;
	++i;
}

// legacy algorithm
std::vector<int> vec(10);
std::iota(vec.begin(), vec.end(), 0); // C++11 way, legacy interface using type traits

// range algorithm
std::vector<int> vec(10);
std::ranges::iota(vec.begin(), vec.end(), 0); // basically the same, but the constructor arguments are constrained with concepts

// same using adaptor
auto range = std::views::iota(0, 10);
std::vector vec{range.begin(), range.end()}; // in-place vector construction
```


## Terminology 

- *range*: the object we iterate over (Iterable in Java)
- *iterator*: the object which does the real work (Iterator in Java)

Usually, a range is composed of two iterators:

- *begin*: points to the beginning of the range, returned by `<range_object>.begin()`
- *end*: points to the end of the object, returned by  `<range_object>.end()` 

Each iterator implements the dereference (`*`) operator that acces the element of the range the iterator is pointing to.

Depending on the iterator type, the iterator also supports other operations: `++`, `--` to iterate along the range, array index operator (`[]`) for random access, etc.

Most of the STL *collections* (vector, set,...) are also ranges.


## How to choose the correct interface?
when deciding which interface to use, we can use the following rules:

1. **If the number of tasks and the complexity of the tasks is high, use the legacy iteration**. It is hard to write a 20 line for loop with various function calls as algorithm or adaptor and the result would be hard to read.
1. Otherwise, **if you need to preserve the original range as it is or you need to compose multiple operations, use the STL range adaptors**. 
1. Otherwise, **use the STL range algorithms**.

Note that the in this guide, we do not consider the legacy STL algorithms. With the availability of the STL *range* algorithms, there is no reason to use the legacy algorithms, except for the backward compatibility or for the algorithms that are not yet implemented in the STL.

Also note that some STL algorithms are principially non-modifying, e.g., `std::ranges::find` or `std::ranges::count`. These algorithms logically do not have the adaptor equivalent.


## STL ranges and views
[https://en.cppreference.com/w/cpp/ranges](https://en.cppreference.com/w/cpp/ranges)

In C++ 20 there is a new range library that provides functional operations for iterators. It is similar to functional addon in Java 8.

As explained in the beginning of this chapter, there are two ways how to use the STL ranges:

- using the [range algorithms](https://en.cppreference.com/w/cpp/ranges) (`ranges::<alg name>`) that are invoked eagerly.
- using the [range views](https://en.cppreference.com/w/cpp/ranges/views) (`ranges::views::<view name>`) that are invoked lazily.

Note that the range algorithms and adaptors cannot produce result without an input, i.e., **we always need a range or collection on which we want to apply our algorithm/view.**

### STL range views
The difference of range view to range algorithms is that the views are lazy, i.e., they do not produce any result until they are iterated over. This is similar to the Python generators. The advantage is that we can chain multiple views together and the result is computed only when we iterate over the final view.

Note that due to the lazy nature of the views, **the underlying range has to be alive during the whole iteration**. Therefore, we cannot use the views on temporaries, e.g., we cannot useviews directly in the constructor of a vector, or we cannot use the views on a temporary range returned by a function.

A custom view can be created so that it can be chained with STL views. However, it has to satisfy the [view concept](https://en.cppreference.com/w/cpp/ranges/view), and more importantly, it should satisfy the view semantic, i.e., it should be cheap to copy and move (without copying the underlying data).

#### Usefull views

- [`std::views::iota`](https://en.cppreference.com/w/cpp/ranges/iota_view): generates a sequence of numbers
- [`std::views::filter`](https://en.cppreference.com/w/cpp/ranges/filter_view): filters the elements of the range


### Projections
Unlike in Java, we cannot refer to member functions when lambda functions are required. However, we can use these member functions when the algorithm or adaptor has a *projection* parameter. Example:
```cpp
struct Data {
	int a;
	std::string b;
	...
};

std::vector<Data> data = get_data();

std::sort(data, {}, &Data::b);
```
The trick here is that we can only provide the member that we want to use for sorting, but the sorting logic (`first < second`...) is handeled by a standard comparator (the second argument initialized with `{}`).

We can have even more complicated projections that are not just references to member functions:
```cpp
std::vector<My_class> objects = get_objects();
std::vector<unsigned> indexes = get_indexes(objects);
auto proj = [&objects](std::size_t i) -> const std::string& { 
	return objects[i].get_name(); 
};
std::ranges::sort(indexes, {}, proj) // sort indexes using the property of objects
```


### Useful range algorithms
Note that the most frequently used algorithms have a separate section in the Iterators chapter.

- [`std::shuffle`](https://en.cppreference.com/w/cpp/algorithm/random_shuffle) : shuffles the elements in the range (formerly `std::random_shuffle`).
- [`std::adjacent_find`](https://en.cppreference.com/w/cpp/algorithm/adjacent_find) : finds the first two adjacent elements that are equal. Can be used to find duplicates if the range is sorted.
- [`std::ranges::unique`](https://en.cppreference.com/w/cpp/ranges/unique): moves the duplicates to the end of the range and returns the iterator to the first duplicate. Only consecutive duplicates are found.
- [`std::ranges::min`](https://en.cppreference.com/w/cpp/algorithm/ranges/min) : finds the smallest element in the range. We can use either natural sorting, or a comparator, or a projection. If the range is empty, the behavior is undefined.
- [`std::ranges::min_element`](https://en.cppreference.com/w/cpp/algorithm/ranges/min_element) : finds the smallest element in the range. Unlike `std::ranges::min`, this function returns an iterator to the smallest element. 
- [`std::ranges::empty`](https://en.cppreference.com/w/cpp/algorithm/ranges/empty) : checks whether the range is empty. 


### Other Resources

-   [https://www.modernescpp.com/index.php/c-20-the-ranges-library](https://www.modernescpp.com/index.php/c-20-the-ranges-library) 



## Boost ranges
In addition to the STL range algorithms and adaptors, boost has it's own [range library](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/index.html) with other more complex algorithms and adaptors.

### Boost range requirements
Sometimes, it is hard to say why a type does not satisfy some of the requirements for boos ranges. Fortunatelly, the boost provides concepts for checking whether a type satisfy each specific range model. Example:
```cpp
BOOST_CONCEPT_ASSERT((
	boost::SinglePassRangeConcept<std::vector<int>>
)); // true
```

Also, it is necessary to check whether the value of the iterator can be accessed:
```cpp
BOOST_CONCEPT_ASSERT((
	boost_concepts::ReadableIteratorConcept<
		typename boost::range_iterator<std::vector<int>>::type
	>
)); // true
```

Most likely, the compiler will complain that `boost::range_iterator<R>::type` does not exist for your range `R` . The boost range library generate this type by a macro from the `R::iterator` type. Therefore, make sure that your range has an iterator type defined, either as:

- a type alias to an existing iterator
- an iterator nested class
 
Note that **`<RANGE CLASS>::iterator` and `<RANGE CLASS>::const_iterator` has to be accessible (public).**

## Sequences
The `iota` algortihm/adapter is used to create a sequence:
```cpp
auto range = std::views::iota(0, 10);
auto vec = std::vector(range.begin(), range.end());
```
Note that we cannot pass the view directly to the vector, as the vector does not have a range constructor.

## Zip
The classical Python like zip iteration is available using the [zip adapator](https://en.cppreference.com/w/cpp/ranges/zip_view), which is not yet supported in MSVC.

However, boost provides a similar functionality `boost::combine`.

### `boost::combine`
[`boost::combine`](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/range/reference/utilities/combine.html) example: 
```cpp
std::vector<int> va{1, 2, 3};
std::vectro<float> vb{0.5, 1, 1.5};
for(const auto& [a, b]: boost::combine(va, vb)){
	...
}
```
Each argument of combine must satisfy [boost::SinglePassRange](https://www.boost.org/doc/libs/1_80_0/libs/range/doc/html/range/concepts/single_pass_range.html)


## Enumerating
There is no function in standard library equivalent to the python enumerate. We can use a similar boost solution:
```cpp
#include <boost/range/adaptor/indexed.hpp>

for(auto const& el: <range> | boost::adaptors::indexed(0)){
	std::cout << el.index() << ": " << el.value() << std::endl;
}
```
However, inside the loop, we have to call the `index` and `value` functions, so it is probably easier to stick to the good old extra variable:
```cpp
size_t i = 0;
for(auto const& el: <range>) {
  std::cout << i << ": " << el << std::endl;
  ++i;
}
```


## Sorting
There is no sorted view or something simmiler, so in order to sort a range, we need to:

- really sort the object in the range
- create an adaptor/view from the range, and then sort the view

There are two functions for sorting in the STL algorithm library:

- [`std::sort`](https://en.cppreference.com/w/cpp/algorithm/sort): old
	- supports parallelization directly by the policy param
- [`std::ranges::sort`](https://en.cppreference.com/w/cpp/algorithm/ranges/sort): new
	- supports comparison using projections

There are three types of sorting:

- natural sorting using the `<` operator of `T` : `std::sort(<RANGE<T>>)`
- sorting using a comparator: `std::sort(<RANGE>, <COMPARATOR>)`, where comparator is a fuction with parameters and return value analogous to the natural sorting operator.
- sorting using projection (only availeble in `std::ranges::sort`): `std::ranges::sort(<RANGE>, <STANDARD GENERIC COMPARATOR>, <PROJECTION>`

### Sorting using projection
When we want to sort the objects by a single property different then natural sorting, the easiest way is to use projection. Example:
```cpp
struct Data {
	int a;
	std::string b;
	...
};

std::vector<Data> data = get_data();

std::sort(data, {}, &Data::b);
```
The trick here is that we can only provide the member that we want to use for sorting, but the sorting logic (`first < second`...) is handeled by a standard comparator (the second argument initialized with `{}`).

We can have even more complicated projections:
```cpp
std::vector<My_class> objects = get_objects();
std::vector<unsigned> indexes = get_indexes(objects);
auto proj = [&objects](std::size_t i) -> const std::string& { 
	return objects[i].get_name(); 
};
std::ranges::sort(indexes, {}, proj) // sort indexes using the property of objects
```


## Transformation
Transformation alg/views transforms an input range according to a callable. As with other operation, there are thre options:

- classical algorithm: [`std::transform`](https://en.cppreference.com/w/cpp/algorithm/transform) with a direct paralellization using the policy parameter
- range algorithm: [`std::ranges::transform`](https://en.cppreference.com/w/cpp/algorithm/ranges/transform) with a support for projections
- range view: [`std::ranges::views::transform`](https://en.cppreference.com/w/cpp/ranges/transform_view) - a lazy variant

The algorithms (but not the view) also supports **binary transformations**, i.e., create an output range using two input ranges.

Transform view example:
```c++
std::vector<int> in(3, 0); // [0, 0, 0]
auto ad = std::ranges::transform_view(in, [](const auto in){return in + 1;});
std::vector<int> out(ad.begin(), ad.end());
```

The transform *view*  can be only constructed from an object satisfying [`ranges::input_range`](http://en.cppreference.com/w/cpp/ranges/input_range). If we want to use a general range (e.g., vector), we need to call the addapter, which has a same signature like the view constructor itself. The important thing here is that the adapter return type is not a `std::ranges::views::transform<<RANGE>>` but `std::ranges::views::transform<std::ranges::ref_view<RANGE>>>` ([`std::ranges::ref_view`](https://en.cppreference.com/w/cpp/ranges/ref_view)). Supporting various collections is therefore possible only with teplates, but not with inheritance.

**Note that unlike in Java, it is not possible to use a member reference as a transformation function (e.g.: `&MyClass::to_sting()`).** We have to always use lambda functions, `std::bind` or similar to create the callable.


## Aggregating (sum, product, etc.)
These operations can be done using the [`std::accumulate`](https://en.cppreference.com/w/cpp/algorithm/accumulate) algorithm. This algorithm is about to be replaced by the `std::ranges::fold` algorithm, but it is not yet implemented in Clang. Examples:
```cpp
// default accumulation -> sum
std::vector<int> vec{1, 2, 3, 4, 5};
int sum = std::accumulate(vec.begin(), vec.end(), 0);

// product
int product = std::accumulate(vec.begin(), vec.end(), 1, std::multiplies<int>());
```


## Implementing a custom range
There are different requirements for different types of ranges. Moreover, there are different requirements for the [range-based for loop (for each)](https://en.cppreference.com/w/cpp/language/range-for), or the legacy STL algorithms. 

Here we focus on requirements for ranges. Not however, that the range requirements are more strict than the requirements for the range-based for loop or the legacy STL algorithms. Therefore, the described approach should work for all three cases.

Usually, we proceed as follows:

1. Choose the right range (Iterable) concept for your range from the [STL range concepts](https://en.cppreference.com/w/cpp/ranges).
	- The most common is the [`std::ranges::input_range`](https://en.cppreference.com/w/cpp/ranges/input_range) concept.
1. Implement the range concept for the range.
	- Either, we can do it by using the interface of the undelying range we usein our class (i.e, we just forward the calls to the methods of `std::vector` or `std::unordered_map`) or
	- implement the interface from scratch. For that, we also need to implement the iterator class that fulfills the corresponding [iterator concept](https://en.cppreference.com/w/cpp/iterator) (e.g., [`std::input_iterator`](https://en.cppreference.com/w/cpp/named_req/InputIterator) for the `std::ranges::input_range`).


### Implementing an input range
The input range is the most common range type. The only requirement for the input range is that it has to have the `begin` and `end` methods that return the input iterator. Example:
```cpp
class My_range {
	private:
		std::vector<int> data;
	public:
		My_range(std::vector<int> data): data(data) {}
		auto begin() {return data.begin();}
		auto end() {return data.end();}

		// usually, we also want a const version of the range
		auto begin() const {return data.begin();}
		auto end() const {return data.end();}
};
```

## Boost Iterator Templates
The [boost.iterator library](https://www.boost.org/doc/libs/1_77_0/libs/iterator/doc/index.html) provides some templates to implement iteratores easily, typically using some existing iterators and modifying just a small part of it:

- for pointer to type (dereference) iterator, you can use [boost indirect iterator](https://www.boost.org/doc/libs/1_54_0/libs/iterator/doc/indirect_iterator.html)
- [zip iterator](https://www.boost.org/doc/libs/1_80_0/libs/iterator/doc/zip_iterator.html) for Python like iteration over multiple collections
- [transform iteratorather useful iterators are also included in [the boost.iterator library](https://www.boost.org/doc/libs/1_787_0/libs/iterator/doc/transform_iterator.html) for using another iterator and just modify the access (`*`) opindex.html). including:
	- zip iterator.
	- [counting_iterator](https://live.boost.org/doc/libs/1_78_0/libs/iterator/doc/counting_iterator.html) to create number sequence like Python range
- [gentransform iterator](https://livewww.boost.org/doc/libs/1_787_0/libs/iterator/doc/generattransform_iterator.html)

There are also two general (most powerfull) classes:

- [iterator adapter](https://live.boost.org/doc/libs/1_78_0/libs/iterator/doc/iterator_adaptor.html)
- iterator facade


## Resources

-   [How to write a legacy iterator](https://internalpointers.com/post/writing-custom-iterators-modern-cpp)
    
-   [iter_value_t](https://en.cppreference.com/w/cpp/iterator/iter_t)



# Lambda Functions
In c++ [lambda functions](https://en.cppreference.com/w/cpp/language/lambda) are defined as:
```cpp
[<capture>](<params>) -> <return_type> { <code> }
```

The rerurn type is optional, but sometimes required (see below). 

Since C++23, the parantheses are optional if there are no functon parameters.

## Captures
Anything that we want to use from outside has to appear in capture. To prevent copying, we should capture by reference, using `&` before the name of the variable.
```cpp
[&var_1] // capture by reference
[var_1] // capture by value
[&] // default capture by reference
```

For the detailed explanation of the captures, see [cppreference](https://en.cppreference.com/w/cpp/language/lambda#Lambda_capture).

## Return type
The return type of lambda functions can be set only using the trailing return type syntax (`-> <RETURN TYPE>` after the function params). The return type can be omited. Note however, that **the default return type is `auto`**, so in case we want to return by reference, we need to add at least `-> auto`, or even a more specific return type.


## Specifiers
Lambda functions can have special specifiers:

- `mutable`: lambda can modify function parameters capture by copy




# Exceptions
In C++, exceptions works simillarly as in other languages. 

Standard runtime error can be thrown using the [`std::runtime_error`](https://en.cppreference.com/w/cpp/error/runtime_error) class:
```cpp
throw std::runtime_error("message");
```

Always catch exception by reference! 

Note that unlike in Java or Python, there is no default exception handler in C++. Therefore, if an exception is not caught and, in conclusion, the program is terminated, there is no useful information about the exception in the standard output. Instead, we only receive the exit code. For this reason, it is a good practice to catch all exceptions in the main function and print the error message. Example:
```cpp
int main() {
	try {
		<the code of the whole program here>
	} catch(...) {
		const std::exception_ptr& eptr = std::current_exception()
		if (!eptr) {
        	throw std::bad_exception();
		}

		/*char* message;*/
		std::string message;
		try {
			std::rethrow_exception(eptr);
		}
		catch (const std::exception& e) {
			message = e.what();
		}
		catch (const std::string& e) {
			message = e;
		}
		catch (const char* e) {
			message = e;
		}
		catch(const GRBException& ex) {
			message = fmt::format("{}: {}", ex.getErrorCode(), ex.getMessage());
		}
		catch (...) {
			message = "Unknown error";
		}

		spdlog::error(message);
		return message;
	}
}
```


## Rethrowing Exceptions
We can rethrow an exception like this:
```cpp
catch(const std::exception& ex){
	// do ssomething
	...
	throw;
}
```

Note that **in parallel regions, the exception have to be caught before the end of the parallel region**, otherwise the thread is killed.

## How to Catch Any Exception
In C++, we can catch any exception with:
```cpp
catch (...) {
    
}
```
However, this way, we cannot access the exception object. As there is no base class for exceptions in C++, there is no way to catch all kind of exception objects in C++.

## `noexcept` specification
A lot of templates in C++ requires functions to be [`noexcept`](https://en.cppreference.com/w/cpp/language/noexcept_spec) which is usually checked by a type trait [`std::is_nothrow_invocable`](https://en.cppreference.com/w/cpp/types/is_invocable). We can easily modify our function to satisfy this by adding a `noexcept` to the function declariaton.

There are no requirements for a `noexcept` function. It can call functions without noexcept or even throw exceptions itself. The only difference it that uncought exceptions from a `noexcept` function are not passed to the caller. Instead the program is terminated by calling [`std::terminate`](https://en.cppreference.com/w/cpp/error/terminate), which otherwise happens only if the `main` function throws.

By default, only constructors, destructors, and copy/move operations are noexcept.


## Stack traces
Unlike most other languages, C++ does not print stack trace on program termination. The only way to get a stack trace for all exceptions is to set up a custom terminate handler an inside it, print the stack trace. 

**However, as of 2023, all the stack trace printing/generating libraries requires platform dependent configuration and fails to work in some platforms or configurations.**

Example:
```cpp
 void terminate_handler_with_stacktrace() {
    try {
        <stack trace generation here>;
    } catch (...) {}
    std::abort();
}

std::set_terminate(&terminate_handler_with_stacktrace);
```

To create the stacktrace, we can use one of the stacktrace libraries:

- [stacktrace](https://en.cppreference.com/w/cpp/header/stacktrace) header from the standard library if the compiler supports it (C++ 23)
	- as of 2024-04, only MSVC supports this functionality
- [cpptrace](https://github.com/jeremy-rifkin/cpptrace)
- [boost stacktrace](https://github.com/boostorg/stacktrace/)



# Logging
There is no build in logging in C++. However, there are some libraries that can be used for logging. In this section we will present logging using the [spdlog](https://github.com/gabime/spdlog) library.

We can log using the `spdlog::<LEVEL>` functions:
```cpp
spdlog::info("Hello, {}!", "World");
```

By default, the log is written to console. In order to write also to a file, we need to create loggers manually and set the list of sinks as a default logger:
```cpp
const auto console_sink = std::make_shared<spdlog::sinks::stdout_sink_st>();
console_sink->set_level(spdlog::level::info); // log level for console sink

auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_st>(<log filepath>, true);

std::initializer_list<spdlog::sink_ptr> sink_list{console_sink, file_sink};
const auto logger = std::make_shared<spdlog::logger>(<LOGGER NAME>, sink_list);
logger->set_level(spdlog::level::debug); //log level for the whole logger

spdlog::set_default_logger(logger);
```

To save performance in case of an intensive logging, we can set an extended flushing period:
```cpp
spdlog::flush_every(std::chrono::seconds(5));
```

## Levels
The log levels are defined in the [`spdlog::level::level_enum`](https://github.com/gabime/spdlog/blob/v1.x/include/spdlog/common.h#L231). The levels are:

- `trace`
- `debug`
- `info`
- `warn`
- `error`
- `critical`

## Colors
By default, the logger uses colors for different log levels. However, this capability is lost when:

- using custom sinks or
- using custom formatters

To keep the colors, we need to a) use the color sink and b) explicitly set the usage of the color in the formatter:
```cpp
auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();

auto logger = std::make_shared<spdlog::logger>("console", console_sink);
logger->set_pattern("[%^%l%$] %v");
```
Here `%^` and `%$` are the color start and end markers.





# Type Aliases
Type aliases are short names bound to some other types. We can introduce it either with `typedef` or with `using` keyword. Examples (equvalent):

```cpp
typedef int number;
using number = int;

typedef void func(int,int);
using func = void(int, int)
```

The `using`new syntax is more readable, as the alias is at the begining of the expression. But why to use type aliases? Two strong motivations can be:

- **iImprove the readebility**: When we work with a type with a very long declaration, it is wise to use an alias. We can partialy solve this issue by using auto, but that is not a complete solution
- **Make the refactoring easier**: When w work with aliases, it is easy to change the type we work with, just by redefining the alias. 

Note that **type aliases cannot have the same name as variables in the same scope**. So it is usually safer to name type aliases with this in mind, i.e., `using id_type = ..` insted of `using id = ..`

## Template Aliasis
We can also create template aliases as follows:
```cpp
template<class A, typename B> 
class some_template{ ... };

template<class T>
using my_template_alias = some_template<T, int>; 
```


## Aliases inside classes
The type alias can also be  placed inside a class. From outside the class, it can be accessed as `<CLASS NAME>::<ALIAS NAME>`:
```cpp
class My_class{
public:
	using number = unsigned long long
	
	number n = 0;
}

My_class::number number = 5;
```

# Constant Expressions
A constant expression is an expression that can be evaluated at compile time. The result of constant expression can be used in static context, i.e., it can be:

- assigned to a `constexpr` variable,
- tested for true using `static_assert`

Unfortunatelly, [there is no universal way how to determine if an expression is a constant expression](https://stackoverflow.com/a/47538175/1827955).

More on [cppreference](https://en.cppreference.com/w/cpp/language/constant_expression).

# Regular expressions
The regex patern is stored in a `std::regex` object:
```cpp
const std::regex regex{R"regex(Plan (\d+))regex"};
```
Note that **we use the raw string** so we do not have to escape the pattern. Also, note that `std::regex` cannot be `constexpr`

## Matching the result
We use the [`std::regex_search`](https://en.cppreference.com/w/cpp/regex/regex_search) to search for the occurence of the pattern in a string. The result is stored in a `std::smatch` object which contains the whole match on the 0th index and then the macthed groups on subsequent indices.
A typical operation:
```cpp
std::smatch matches;
const auto found = std::regex_search(string, matches, regex);
if(found){
	auto plan_id = matches[1].str(); // finds the first group
}
```

**Note that `matches[0]` is not the first matched group, but the whole match.** 

# Namespaces
[cppreference](https://en.cppreference.com/w/cpp/language/namespace)

Namespace provides duplicit-name protection, it is a similar concept to Java packages. Contrary to java packages and modules, the C++ namespaces are unrelated to the directory structure.
```cpp
namespace my_namespace {
	...
}
```
The namespaces are used in both declaration and definition (both in header and source files). 

The inner namespace has access to outer namespaces. For using some namespace inside our namespace without full qualification, we can write:
```cpp
using namespace <NAMESPACE NAME>
```


## Anonymous namespaces
Anonymous namespaces are declared as:
```cpp
namespace {
	...
}
```
Each anonnymous namespaces has a different and unknown ID. Therefore, the content of the annonymous namespace cannot be accessed from outside the namespace, with exception of the file where the namespace is declared which has an implicit access to it.


## Namespace aliases
We can create a [namespace alias](https://en.cppreference.com/w/cpp/language/namespace_alias) using the `namespace` keyword to short the nested namespace names. Typicall example:
```cpp
namespace fs = std::filesystem;
```



# `decltype`: Determining Type from Expressions
Sometimes, it is usefull to declare a type from expression, instead of do it manualy. Using  [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) specifier, we can get the resulting type of an expression as if it was evaluated. Examples:

```cpp
struct A { double x; };
const A* a;

decltype(a->x) // evaluates to double

decltype(std::accumulate(a, [](double sum, double val){return sum + val;})) // evalutes to double
```
We can use the `decltype` in any context where type is required. Examples:
```cpp
int i = 1
decltype(i) j = 3

std::vector<decltype(j)> numbers;
```
## The Value Category of `decltype`
The value category of `decltype` is resolved depending on the value category of an expression inside it:

- `deltype(<XVALUE>)` -> `T&&`
- `deltype(<LVALUE>)` -> `T&`
- `deltype(<RVALUE>)` -> `T`

The rvalue conversion can lead to unexpected results, in context, where the value type matters:
```cpp
static_assert(std::is_same_v<decltype(0), decltype(std::identity()(0))>); // error
```
The above expressions fails because:

- `decltype(0)`, `0` is an rvalue `->` the `decltype` result is `int`
- `decltype(std::identity()(0))` result of [`std::identity()`](https://en.cppreference.com/w/cpp/utility/functional/identity) is an xvalue `->` the `decltype` result is `int&&`. Determining Type from Expressions
Sometimes, it is usefull to declare a type from expression, instead of do it manualy. Using  [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) specifier, we can get the resulting type of an expression as if it was evaluated. Examples:

```cpp
struct A { double x; };
const A* a;

decltype(a->x) // evaluates to double

decltype(std::accumulate(a, [](double sum, double val){return sum + val;})) // evalutes to double
```
We can use the `decltype` in any context where type is required. Examples:
```cpp
int i = 1
decltype(i) j = 3

std::vector<decltype(j)> numbers;
```

### Determining the Return Value Type of a Function
As we can see above, we can use `decltype` to determine the return value type. But also, there is a *type trait* for that: [`std::invoke_result_t`](https://en.cppreference.com/w/cpp/types/result_of) (formerly `std::result_of`). The `std::invoke_result_t` should vbe equal to `decltype` when aplied to return type, with the following limitations:

- we cannot use abstract classes as arguments of `std::invoke_result_t`, while we can use them inside `decltype` (using `std::declval`, see below).
- 


### Construct object inside `decltype` with `std::declval`
[`std::declval`](https://en.cppreference.com/w/cpp/utility/declval) is a usefull function designed to be used only in static contexts, inside `decltype`. It enables using member functions inside decltype without using constructors.  Without `std::declval`, some type expressions are hard or even impossible to costruct. Example:
```cpp
class Complex_class{
	Complex_class(int a, bool b, ...)
	...

	int compute()
}

// without declval
decltype<Complex_class(1, false, ...).compute()> 

// using declval
decltype(std::declval<Complex_class>().compute())
```

### `decltype` and Overloading
in static context, there is no overloading, the vtable is not available. Therefore, we have to hint the compiler which specific overloaded function we want to evaluate. This also applies to const vs non const overloading. The following example shows how to get the const iterator type of a vector:

```cpp
std::vector<anything> vec

// non const iter
decltype(vec.begin())

// const iter
decltype<std::declval<const decltype(vec)>().begin()>
```

Another example shows how to use the const overload inside `std::bind`:

```cpp
decltype(std::bind(static_cast<const ActionData<N>&(std::vector<ActionData<N>>::*)(size_t) const>(&std::vector<ActionData<N>>::operator[]), action_data)),
```
Above, we used static cast for choosing the const version of the vector array operator. Instead, we can use explicit template argument for `std::bind`:

```cpp
decltype(std::bind<const ActionData<N>& (std::vector<ActionData<N>>::*)(size_t) const>(&std::vector<ActionData<N>>::operator[], action_data)),
```








# Parallelization
While there wa no support of parallelization i earlier versions of C++ , now there are many tools.

## Standard Threads

## For-each with Parallel Execution Policy
The function [`std::for_each`](https://en.cppreference.com/w/cpp/algorithm/for_each) can be run with a parallel execution policy to process the loop in parallel.

## Async tasks
Tasks for asznchronous execution, like file downloads, db queries, etc. The main function is [`std::async`](https://en.cppreference.com/w/cpp/thread/async).

## Open-MP
In MSVC, the Open MP library is automatically included and linked. In GCC, we need to find the libs in `CmakeLists.txt`:
```cmake
find_package(OpenMP REQUIRED)
```



# Standard Templates for Callables
## Using std::invoke to call the member function
using [`std::invoke`](https://en.cppreference.com/w/cpp/utility/functional/invoke), the cal syntax `bool b = (inst.*ptr)()` can be replaced with longer but more straighforward call:
```cpp
bool b = std::invoke(ptr, inst, 2) 
```

## Using std::mem_fn to Store a Pointer to Member Function in a Callable
With [`std::mem_fn`](https://en.cppreference.com/w/cpp/utility/functional/mem_fn), we can store the pointer to a member function in a callable object. Later, we can call the object without the pointer to the member function. Example:
```c++
auto mem_ptr = std::mem_fn(&My_class::my_method)
bool b = mem_ptr(inst, 2)
```

## Using a Pointer to Member Function as a Functor
A normal function can be usually send instead of functor, as it can be invoked in the same way. However, in case of  member function, we usually need to somehow bind the function pointer to the instance. We can use the [`std::bind`](https://en.cppreference.com/w/cpp/utility/functional/bind) function exactly for that:
```cpp
auto functor = std::bind(&My_class::my_method, inst);
bool b = functor(2)
```

Advanteges:

- we do not need an access to instance in the context from which we call the member function
- we do not have to remember the complex syntax of a pointer to a member function declaration
- we receive a callable object, which usage is even simpler than using `std::invoke`

Note that in case we want to bind only some parameters, we need to supply placeholders for the remaining parameters (`std::placeholders`).

## Using Lambdas Instead of std::bind
For more readable code and better compile error messages, it is usefull to replace `std::bind` callls with labda functions. The above example can be rewritten as:
```cpp
auto functor = [inst](int num){return inst.my_method(num););
bool b = functor(2)
```

## Store the Result of std::bind
Sometimes, we need to know the return type of the `std::bind`. In many context, we need to provide the type instead of using `auto`. But luckily, there is a type exactly for that: [`std::function`](https://en.cppreference.com/w/cpp/utility/functional/function). Example:

```cpp
std::function<bool(int)> functor = std::bind(&My_class::my_method, inst);
bool b = functor(2)
```

A lambda can also be stored to `std::function`. But be carefull to add an explicit return type to it, if it returns by a reference. Example:

```cpp
My_class{
public:
	int my_member
}

My_class inst;

std::function f = [inst](){return &inst.my_member; } // wrong, reference to a temporary due to return type deduction
std::function f = [inst]() -> const int& {return &inst.my_member; } // correct

```

[More detailed information about pointers to member functions](https://isocpp.org/wiki/faq/pointers-to-members)


## std::mem_fn and Data Members
Data member pointers can be aslo stored as [`std::mem_fn`](https://en.cppreference.com/w/cpp/utility/functional/mem_fn). A call to this object with an instance as the only argument then return the data member value.

The plain syntax is `<type> <class name>.*<pointer name> = <class name>.<member name>`, and the pointer is then accessed as `<instance>.*<pointer name>`. Example:

```cpp
int Car::*pSpeed = &Car::speed;
c1.*pSpeed = 2;
```
Usefull STL functions

- [`std::for_each`](https://en.cppreference.com/w/cpp/algorithm/for_each): iterates over iterable objects and call a callable for each iteration
- [`std::bind`](https://en.cppreference.com/w/cpp/utility/functional/bind): Binds a function call to a variable that can be called
	- some parameters of the function can be fixed in the variable, while others can be provided for each call
	- each reference parameter has to be wrapped as a `reference_wrapper`
- [`std:mem_fn`](https://en.cppreference.com/w/cpp/utility/functional/mem_fn): Creates a variable that represents a callable that calls member function

## std::function
The [`std::function`](https://en.cppreference.com/w/cpp/utility/functional/function) template can hold any callable. It can be initialized from:

- function pointer/reference, 
- member function pointer/reference, 
- lambda function 
- functor

It can be easily passed to functions, used as template parameter, etc. The template parameters for `std::function` has the form of `std::function<<RETURN TYPE>(<ARGUMENTS>)>`. Example:
```cpp
auto lambda = [](std::size_t i) -> My_class { return My_class(i); };

std::function<My_class(std::size_t)> f{lambda}
```

### std::function and overloading
one of the traps when using `std::function` is the ambiguity when using an overloade function:
```c++
int add(int, int);
double add(double, double);

std::function<int(int, int)> func = add; // fails due to ambiguity.
```

The solution is to cant the function to its type first and then assign it to the template:
```
std::function<int(int, int)> func = static_cast<int(*)(int, int)>add;
```


# Preprocessor Directives
The C language has a [preprocessor](https://en.wikipedia.org/wiki/C_preprocessor) that uses a specific syntax to modify the code before the compilation. This preprocessor is also used in C++. The most used tasks are:

- including files (`#include`): equivalent to Java or Python `import` statement
- conditional compilation based on OS, compiler, or other conditions

Also, preprocessor had some other purposes, now replaced by other tools:

- defining constants (`#define`): replaced by `const` and `constexpr`
	- A simple constant can be defined as: `#define PI 3.14159`. The variable can be used in the code as `PI`.
- metaprogramming: replaced by templates

# Include
There are two types of include directives. For both types, the behavior is implementation dependent. However, the most common behavior is:

- `#include <file>`: the file is searched in the system directories
- `#include "file"`: the file is searched relative to the current file

## Control structures
```cpp
#ifdef <MACRO>
	...
#elif <MACRO>
	...
#else
	...
#endif
```

Instead of `#ifdef <MACRO>`, we can use `#if defined(<MACRO>)`. In this case, we can use multiple conditions in one `#if` directive:
```cpp
#if defined(MACRO_1) && defined(MACRO_2)
	...
#endif
```

## Predefined macros for detecting compiler, OS, etc.
To detect the **Operating system**, use:

- `#ifdef _WIN32` for Windows
- `#ifdef __linux__` for Linux
- `#ifdef unix` for Unix-like systems (but not MacOS)
- `#ifdef __APPLE__` for MacOS



# Resources
In C++, there is no facility for resource management like in Java or Python. Instead, resources have to be loaded like standard files. 

Moreover, there is no built-in way how to determine the localtion of the running executable so that we can load the resources from the same directory. Typically, this has to be implemented for each platform separately:

```cpp
#include <iostream>
#include <filesystem>
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

std::string get_executable_path() {
    char buffer[1024];
#ifdef _WIN32
    GetModuleFileNameA(NULL, buffer, sizeof(buffer));
#else
    ssize_t count = readlink("/proc/self/exe", buffer, sizeof(buffer));
    if (count == -1) throw std::runtime_error("Failed to get executable path");
    buffer[count] = '\0';
#endif
    return std::filesystem::path(buffer).parent_path().string();
}
```



# Testing with Google Test

## Private method testing
The testing of private method is not easy with Google Test, but that is common also for other tets frameworks or even computer languages (see the common manual). Some solutions are described in [this SO question](https://stackoverflow.com/questions/47354280/what-is-the-best-way-of-testing-private-methods-with-googletest).

Usually, the easiest solution is to aplly some naming/namespace convention and make the function accessible.

For free functions:
```cpp
namespace internal {
	void private_function(){
		...
	}
}
```

For member functions:
```cpp
class MyClass{
public:
	void _private_function();
```


# specific tasks

## Conditional Function Execution
W know it from other languages: if the function can be run in two (or more) modes, there is a function parameter that controls the execution. Usually, most of the function is the same (otherwise, we eould create multiple fuctions), and the switch controls just a small part.

Unlike in other langueges. C++ has not one, but three options how to implement this.  They are described below in atable together with theai properties.

| | function parameter | template parameter | compiler directive |
|--|--|--|--|
| good readability | yes| no |no | 
| compiler optimization | no | yes | yes |
| conditional code compilation | no | no | yes |

### Function Parameter
```cpp
void(bool switch = true){
	if(switch){
		...
	}
	else{
		...
	}
}
```

### Template Parameter
```cpp
template<bool S = true>
void(){
	if(S){
		...
	}
	else{
		...
	}
}
```

### Compiler Directive
```cpp
void(){
#ifdef SWITCH
    ...
#else
	...
#endif
}
```

## Ignoring warnings for specific line of code
Sometimes, we want to suppress some warnings, mostly in libraries we are including. The syntax is, unfortunatelly, different for each compiler. Example:
```cpp
#if defined(_MSC_VER)
	#pragma warning(push)
	#pragma warning(disable: <WARNING CODE>)
#elif defined(__GNUC__)
	#pragma GCC diagnostic push
	#pragma GCC diagnostic ignored "<WARNING TYPE GCC>"
#elif defined(__clang__)
	#pragma clang diagnostic push
	#pragma clang diagnostic ignored "<WARNING TYPE CLANG>"
#endif
.. affected code...
#if defined(_MSC_VER)
	#pragma warning(pop)
#elif defined(__GNUC__)
	#pragma GCC diagnostic pop
#elif defined(__clang__)
	#pragma clang diagnostic pop
#endif
```

**Note that warnings related to the preprocessor macros cannot be suppressed this way in GCC** due to a [bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53431) (fixed in GCC 13). The same is true for conditions:
```cpp
#if 0
	#pragma sdhdhs // unknown pragma raises warning, despite unreachcable
#endif
```

## Measuring used resource

### Memory

#### MSVC
In MSVC, we can measure the peak used memory using the following code: 
```cpp
#include <psapi.h>

PROCESS_MEMORY_COUNTERS pmc;
K32GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
auto max_mem = pmc.PeakWorkingSetSize
```

## Working with tabular data
Potential libs similar to Python Pandas:

- [Arrow](https://arrow.apache.org/docs/cpp/)
- [Dataframe](https://github.com/hosseinmoein/DataFrame)


## Executing external commands
The support for executing external commands in C++ is unsatisfactory. The most common solution is to use the [`system`](https://en.cppreference.com/w/cpp/utility/program/system) function.
However, the `system` calls are not portable, e.g., the quotes around the command are not supported in Windows

Another option is to use the Boost [Process](https://www.boost.org/doc/libs/1_82_0/doc/html/process.html) library. 


## Command Line Interface
For CLI, please follow the [CLI manual](../Common.md#command-line-interface). Here we focus on setting up the [TCLAP](http://tclap.sourceforge.net/manual.html) library.

TCLAP use


## Jinja-like Templating
For working with Jinja-like templates, we can use the [Inja](https://github.com/pantor/inja) template engine. 


### Exceptions
There are the following exceptions types:

- `ParserError` thrown on `parse_template` method
- `RenderError` thrown on `write` method

#### Render Errors

- `empty expression`: this signalize that some expression is empty. Unfortunatelly, the line number is incorrect (it is always 1). Look for empty conditions, loops, etc. (e.g., `{% if %}`, `{% for %}`, `{% else if %}`).



