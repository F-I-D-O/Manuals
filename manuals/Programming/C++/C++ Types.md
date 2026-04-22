# Arithmetic Types
[cppreference](https://en.cppreference.com/w/cpp/language/types)

## Integers
Integer types varies in the sign and size.

Unfortunatelly, **the minimum sizes guaranteed by the standard are not usable, because the real size is different and it differs even between platforms**. Especially the `long` type. To use an integer with a specific size, or a specific minimal size, we can use [type aliases defined in `cstdint`](https://en.cppreference.com/w/cpp/types/integer)

## Overflow and Underflow
The overflow (and underflow) is a common problem in most programming languages. The problem in C++ is that:

- overflows are **not detected**
- overflows can happen in many unexpected situations

### Dangerous situations
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


### Detecting overflows
There are some methods how to detect overflows automatically by suppliying arguments to the compiler. These are summarized here:

- **MSVC**: not implemented
- **GCC**: only detectes signed and floating point overflows, as the unsigned overflows are not considered as errors (the behaviour is defined in the standard). All undefined behaviour can be detected using the `-fsanitize=undefined` flag. [Documentation](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
- **Clang**: Both signed and unsigned overflow can be detected. The undefined behaviour can be detected using the `-fsanitize=undefined` flag. Fo all integer overflows, the `-fsanitize=integer` flag can be used. [Documentation](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)

The reasoning behind excluding the unsigned overflows from GCC are described [here](https://gcc.gnu.org/legacy-ml/gcc/2016-07/msg00051.html).


It is also possible to do an ad-hoc overflow check in the code, the possible solutions are described in [this SO question](https://stackoverflow.com/questions/199333/how-do-i-detect-unsigned-integer-overflow)


## Characters
Characters in C++ are represented by the `char` type, which is an integer type. This type can be signed or unsigned, and it is at least 8 bits long. 

Useful functions for working with characters are:

- [`std::isspace`](https://en.cppreference.com/w/cpp/string/byte/isspace): checks if the character is a whitespace (space, tab, newline, etc.)
- [`std::toupper`](https://en.cppreference.com/w/cpp/string/byte/toupper): converts the character to upper case


# Pointers
[cppreference](https://en.cppreference.com/w/cpp/language/pointer)


## Pointers to Functions
Function pointers are declared as:
```cpp
<return_type> (*<pointer_name>)(<arg_1_type>, ..., <arg_n_type>)
```
For example a function `the_function` returning bool and accepting int can be stored to pointer like this:

```C++
bool (*ptr)(int) = &the_function
```

The above example can be then simply called as `bool b = ptr(2)`


## Pointers to Member Objects
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


## Pointers to Member Functions
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

# References
[References](https://en.cppreference.com/w/cpp/language/reference) serve as an alias to already existing objects. Standard (*Lvalue*) references works the same way as pointers, with two differences:

- they cannot be NULL
- they cannot be reassigned

The second property is the most important, as the assignment is a common operation, which often happens under do hood. In conslusion, **reference types cannot be used in most of the containers and objets that needs to be copied**.

## Rvalue references
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

## Forwarding references
[Forwarding references](https://en.cppreference.com/w/cpp/language/reference#Forwarding_references) are references that preserves the value category (i.e. r/l-value reference, `const`). They have two forms:

- function parameter forwarding references
- `auto` forwarding references

### Function parameter forwarding references
In a function template, if we use the rvalue reference syntax for a function parameter of  whose type is a function template parameter, the reference is actually a forwarding reference. Example:
```cpp
template<class T>
void f(T&& arg) // parameter is T& or T&& depending on the supplied argument
```
Important details:

- it works only for non const references
- the reference type has to be a function template argument, not a class template argument 

### `auto` forwarding reference
When we assign to `auto&&`, it is a forwarding reference, not rvalue reference:
```cpp
auto&& a = f() // both type and value category depends on the return value of f()

for(auto&& a: g(){ // same
}
```


# Arrays
[cppreference](https://en.cppreference.com/w/cpp/language/array)

There are two types of arrays:

- *static*, i.e., their size is known at compile type, and
- *dynamic*, the size of which is computed at runtime

We can use the array name to access the first element of the array as it is the pointer to that element.

## Static arrays

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


## Dynamic arrays
Declaration:
```cpp
int* a = new int[size]
```
For multiple dimensions, this syntax does not scale, i.e, only one dimension can be dynamic:

```cpp
int(*a)[4] = new int[rows][4] // static column count
int(*b)[cols] = new int[rows][cols] // does not compile unless cols is a constant!
```


## Array to pointer implicit conversion
When we use the array name in an expression, it can be implicitly converted to a pointer to the first element of the array. This is true for both static and dynamic arrays. Example:
```cpp
int a[3] = {1, 2, 5}
int* ptr = a; // ptr points to the first element of a
```
This implicit conversion is called *array-to-pointer decay*.


## Mutli-dimensional dynamic arrays
To simulate multi-dimensional dynamic arrays, we have two options:

- use the flat syntax, as demonstrated on static arrays
- use aray of pointers to arrays 

Method | Pros | Cons
--|--|--
Flat Syntax | Fast: single continuous allocations | different access syntax than static 2D arrays
Array of pointers | Slow: one allocation per row, unrelated memory addresses between rows | same access syntax as static 2D arrays

### Flat array
```cpp
int* a = new int[rows * cols]
```

Then we can access the array as:
```cpp
a[x * cols + y] = 5
```


### Array of pointers to array
Declaration and Definition
```cpp
int** a = new int*[rows]

for(int i = 0; i < rows; ++i){
	a[i] = new int[cols]
}
```
Access is like for static 2D array: `a[x][y] = 5`. This works because the pointers can be also accessed using the array index operator (`[]`). In other words, it works "by coincidence", but we have not created a real 2D array.

## Auto dealocation of dynamic arrays
We can replace the error-prone usage of `new` and `delete` by wraping the array into unique pointer:
```cpp
std:unique_ptr<int[]> a;
a = std::make_unique<int[]>(size)
```


# References and Pointers to arrays
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


# Function Type
A function type consist from the function arguments and the return type. The function type is written as `return_type(arg_1_type, ..., arg_n_type)`. Example:

```cpp
int foo(double a, double b);

static_assert(std::is_same_v<decltype(foo), int(double, double)>) // TRUE
```

# Reference to Function and Pointer to Function Types
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

# Enumerations
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

# Smart Pointers
For managing resources in dynamic memory, *smart pointers* (sometimes called *handles*) should be used. They manage the memory (alocation, dealocation) automatically, but their usage requires some practice.

There are two types of smart pointers:

- `std::unique_ptr` for unique ownership
- `std::shared_ptr` for shared ownership

## Creation
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


## Shared Pointer
Pointer to object with non-trivial ownership (owned by multiple objects).



# std::reference_wrapper
[cppreference](https://en.cppreference.com/w/cpp/utility/functional/reference_wrapper)
Reference wrapper is a class template that can be used to store references in containers or aggregated objects. The disintinction from normal references is that the reference wrapper can be copied and assigned, so it does not prevent the copy/move operations on the object it belongs to. Otherwise, it behaves like a normal reference: it has to be assigned to a valid object and it cannot be null.

# Strings
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


## String Literals
[cppreference](https://en.cppreference.com/w/cpp/language/string_literal)

 The standard string literal is writen as `"literal"`. However, we need to escape some **special characters** in such literals, therefore, a *raw string* literal is sometimes more desirable: `R"(literal)"`.
 
 If our literal contains `(` or `)`, this is stil not enough, however, the delimiter can be extended to any string with a maximum length of 16 characters, for example:
 `R"lit(literal)lit"`. 
 
 Raw string literals also useful for **multi-line string literals**.

## Formatting strings
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
 

## Spliting the string into tokens
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


## Converting string to int
There are simple functions for converting `std::string` to numbers, named `std::stoi`, `std::stoul`, etc. See [cppreference](https://en.cppreference.com/w/cpp/string/basic_string) for details.

For C strings, the situation is more complicated.

## Substring
A substring can be obtained using a member function `substr`:
```cpp
str.substr(str.size() - 1, 1)) // returns the last character as a string
```
## change the case
Unfortunatelly, the STL has case changing functions only for characters, so we need to iterate over the string ourselfs. The boost has a solution, however:
```cpp
#include <boost/algorithm/string.hpp>

auto upper = boost::to_upper(str);
``` 

Alternatively, we can use the [`std::transform`](https://en.cppreference.com/w/cpp/algorithm/transform) algorithm and the [`std::toupper`](https://en.cppreference.com/w/cpp/string/byte/toupper) or [`std::tolower`](https://en.cppreference.com/w/cpp/string/byte/tolower) functions:
```cpp
std::transform(str.begin(), str.end(), str.begin(), std::toupper);
```


## Building strings
Unlike other languages, in C++, strings are mutable, so we can build them using the `+` operator without performance penalty. Alternatively, we can use the `std::stringstream` class.


## Testting for whitespace
To test if a string contains only whitespace characters, we can use the `std::all_of` algorithm:
```cpp
std::all_of(str.begin(), str.end(), [](char c){return std::isspace(c);})
```


# Date and time
The date and time structure in C++ is [`std::tm`](https://en.cppreference.com/w/cpp/chrono/c/tm). We can create it from the date and time string using [`std::get_time`](https://en.cppreference.com/w/cpp/io/manip/get_time) function:
```cpp
std::tm tm;
std::istringstream ss("2011-Feb-18 23:12:34");
ss >> std::get_time(&tm, "%Y-%b-%d %H:%M:%S");
```


# Collections
In C++, the collections are implemented as templates, so they can store any type. The most common collections are:

- [std::array](https://en.cppreference.com/w/cpp/container/array)
- [std::vector](https://en.cppreference.com/w/cpp/container/vector)
- [std::unordered_set](https://en.cppreference.com/w/cpp/container/unordered_set)
- [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map)
- [std::pair](https://en.cppreference.com/w/cpp/utility/pair) and [std::tuple](https://en.cppreference.com/w/cpp/utility/tuple)

Currently, the collection semantic requirements are not imposed on the whole connection, but on its member functions instead. Depending on the function used, there are different requirements for the stored types. This adds a lot of flexibility, as we can, for example, use move only types in collections when we refrain from using functions that require copying. On the other hand, it can make the debugging harder, as the compiler usually does not recognize the methods that caused the template to have stricter requirements but instead complains on the place where the template is instantiated.


## Sets
Normal set collection for C++ is [`std::unordered_set`](https://en.cppreference.com/w/cpp/container/unordered_set). By default, the set uses a `Hash`, `KeyEqual` and `Allocator` template params provided by std functions. However, they need to exist, specifically:

- [`std::hash<Key>`](https://en.cppreference.com/w/cpp/utility/hash)
- `std::equal_to<Key>`
- `std::allocator<Key>`

So either those specializations needs to be provided by the snadard library (check cppreference), or you have to provide it. 

### Providing custom hash function
There are two options for providing custom hash function for a type `T`s:

- implementing an *explicit specialization* of the template function  `std::hash<T>`
- providing the `Hash` template param when constructing the hash

The first method is prefered if we want to provide a default hash function for some type for which there is no hash function specialization in the standard library. The second method is prefered only when we want some special hash function for a type `T` for which `std::hash<T>` is already defined.

### Implementing custom hash function
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

## Maps
The maps has similar requiremnts for keys as the requirements for set value types (see previous section). The hash map type is called [`std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map). Note that [maps require the stored types to be complete](https://stackoverflow.com/a/74965248/1827955).

### Geeting value by key
To access the map element, the array operator (`[]`) can be used. Note however, that this operator does not check the existence of the key, even if we do not provide a value. Example:
```cpp
std::unordered_map<int,std::string> map;
map[0] = "hello"
map[0] = "world" // OK, tha value is overwritten
a = map[1] // a == map[1] == "" unintuitively, the default value is inserted if the key does not exist
```

Therefore, **if we just read from the map, it is safer to use the `at()`** member function.

### Inserting into map
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


## Tuples
We have two standard class templates for tuples:

- [`std::pair`](https://en.cppreference.com/w/cpp/utility/pair) for pairs
- [`std::tuple`](https://en.cppreference.com/w/cpp/utility/tuple) for tuples with unlimited size

Although named differently, these class templates behaves mostly the same.

### Creating tuples
There are two ways of creating a tuple:

- constructor (`auto p = std::pair(...)`)
- initializer (`auto p = {}`)

Beware that **by default**, the deduced types are decayed, i.e., const and references are removed and the **tuple stores value types**. If you need to store the reference in a tuple, you have to specify the type: 
```cpp
auto p = std::pair<int, constr std::string&>(...)
```

Also, beware that the RVO does not apply for tuple members. **This means that if we store values types in the tuple, the types are copied/moved, and in conclusion, they have to by copyable/movable!** This is the reason why we frequently use smart pointers in tuples even though we would reurn directly by value if we returned a single value.

#### Creating tuples with `std::make_pair` or `std::make_tuple`
**TLDR: from C++17, there is no reason to use `make_pair`/`make_tuple`**.

There are also factory methods `make_pair`/`make_tuple`. Before C++17, argument deduction did not work for constructors, so there is a dedicated  method for creating tuples. However, now we can just call the constructor and the template arguments are deduced from the constructor arguments. Also, the `make_pair`/`make_tuple` functions can only produce tuples containing values, not references (even if we specify the reference type in the `make_pair`/`make_tuple` template argument, the returned tuple will be value-typed). 


### Accessing tuple members
The standard way to access the tuple/pair mamber is using the [`std::get`](https://en.cppreference.com/w/cpp/utility/tuple/get) function:
```cpp
auto tuple = std::tuple<int, std::string, float>(0, "hello", 1.5);
auto hello = std::get<1>(tuple);
```

### Unpacking tuples into variables
There are two scenarios of unpacking tuples into variables:

- unpacking into **new variables**: for that, we use *structured binding*.
- unpacking into **existing variables**: for that, we use `std::tie` function.

#### Structured binding 
If we don't need the whole tuple objects, but only its members, we can use a [*structured binding*](https://en.cppreference.com/w/cpp/language/structured_binding). Example:
```cpp
std::pair<int, int> get_data();

void main(){
	const auto& [x, y] = get_data();
}
```

#### `std::tie`
If we want to unpack the tuple into existing variables, we can use the [`std::tie`](https://en.cppreference.com/w/cpp/utility/tuple/tie) function:
```cpp
std::pair<int, int> get_data();

void main(){
	int x, y;
	std::tie(x, y) = get_data();
}
```	

### Unpacking tuples to constructor params with `std::make_from_tuple`
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


# `std::optional`
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


# Unions and Variants
The idea of a union is to store multiple types in the same memory location. Compared to the polymorphism, when we work with pointers and to templates, where the actual type is determined at compile time, the union actually has a shared memory for all the types.

The union can be therefore used in cases where nor polymorphism neither templates are suitable. One example can be storing different unrelated types (e.g., `std::string` and `int`) in a container. We cannot use templates as that require a single type. Nor we can use polymorphism, as the types are unrelated. 

The big disadvantage of unions is that they are not type safe. The compiler cannot check if the type we are accessing is the same as the type we stored. Therefore, we have to be very careful when using unions. Therefore, unless some special case, **we should use [`std::variant`](https://en.cppreference.com/w/cpp/utility/variant) instead of unions**.

## `std::variant`
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


# Storing individual bits in a sequence
Storing individual bits is a strategy for saving memory in high-performance applications, where each saved bit can have a dramatical impact on the performance. When working with small amounts of objects (less than millions), these strategies are not worth the effort, as we can store information in built-in types like `int`, `char`, or `bool`.

There are multiple strategies for storing individual bits where each bit has its own meaning:

- using built-in arithmetic types and accessing individual bits using bit masks
- [`std::bitset`](https://en.cppreference.com/w/cpp/utility/bitset)
- using [bitfields](https://en.cppreference.com/w/cpp/language/bit_field)
- using `std::vector<bool>`

The best strategy depends on the use case. The following table summarizes the pros and cons of the different strategies:

Feature | built-in arithmetic types | `std::bitset` | bitfields | `std::vector<bool>`
--- | --- | --- | --- | ---
Maximum size per variable | 64 bits | unlimited | 64 bits | unlimited
Dynamic size | no | no | no | yes


## Reading a subsequnece of bits
For reading individual bits or the whole sequence of bits, each strategy has its own way of doing it. However, for reading a subsequence of bits, there is no machinery, so we have to resort to bit operations no matter of the strategy.

For skipping first `n` bits, we use the right shift (`>>`) or the left shift operator, depending on endians. For skipping last `n` bits, we use a bitmask and the and (`&`) operator.

Example:
```cpp
std::bitset<8> b = 0b10101010;
std::cout << b.to_ulong() << std::endl; // prints 170
```


## `std::bitset`
[cppreference](https://en.cppreference.com/w/cpp/utility/bitset)

`std::bitset<N>` is a class template that can store up to `N` bits.

### Reading
To **read a single bit**, we can use:

- the [`test`](https://en.cppreference.com/w/cpp/utility/bitset/test) member function that returns a boolean value
- the [`operator[]`](https://en.cppreference.com/w/cpp/utility/bitset/operator_at) operator that returns a boolean value

To **read more bits at once**, we can use:

- the [`to_ulong`](https://en.cppreference.com/w/cpp/utility/bitset/to_ulong) member function that returns an `unsigned long` value
- the [`to_ullong`](https://en.cppreference.com/w/cpp/utility/bitset/to_ullong) member function that returns an `unsigned long long` value

Both methods convert the whole bitset to an integer value of the corresponding type. If the bitset is larger than the integer type, an exception is thrown.

**There is no function for reading a specified sequence of bits**. One way to overcome this is to read the whole bitset and apply a series of bit operations to get the desired bits (same as we would do with built-in arithmetic types). Another, slower option is to read the bits one by one using for loop.


# `std::any`: storing any type of value
[cppreference](https://en.cppreference.com/w/cpp/utility/any)

`std::any` is a class template that can store any type of value. It is a better alternative to traditional usage of void pointers. If the possible types are known at compile time, we should use `std::variant` instead.

