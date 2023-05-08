

C++ Rules, explanations, and more

# Types
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


## Function Type
A function type consist from the function arguments and the return type. The function type is written as `return_type(arg_1_type, ..., arg_n_type)`. Example:

```cpp
int foo(double a, double b);

static_assert(std::is_same_v<decltype(foo), int(double, double)>) // TRUE
```

## Reference to Function and Pointer to Function Types
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
[cppreference](https://en.cppreference.com/w/cpp/language/implicit_conversion)

In some context, an implicit type conversion is aplied, so that operand(s) have compatible types. 

This process can be tricky though, for example, the signess can be changed as a result of type promotion.

Bellow, the promotions are sorted according to the target type.


### Integral Promotion
- `bool` is promoted to `int`: `false` -> `0`, `true` -> `1`


## Show the Type
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
- *xvalue*, meaning expiring value. Exvalue expressions are:
	- function call to functions returning rvalue reference (e.g., `std::move`).
	- member object expression (`a.m`) if `a` is an rvlaue and `m` is a non-reference type
- *glvalue* = *lvalue* `||` *xvalue*. 
- *rvalue* = *prvlaue* `||` *xvalue*. 



# Operators
C++ supports almost all the standard operators known from other languages like Java or C#.

Note that the standard also supports [**alternative tokens**](https://en.cppreference.com/w/cpp/language/operator_alternative) for some operators (e.g., `&&` -> `and`, `||` -> `or`, `!` -> `not`). However, these are not supported by all compilers. In MSVC, the [`/permissive-`](https://docs.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance?view=vs-2019) flag needs to be used to enable these tokens.


# Functions

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
The return type of a function can be automatically deduced if we use the auto keyword. The decision between value and reference return type is made according to the following rules:
- return type `auto` -> return by value
- return type `auto&` -> return by reference
- return type `auto*` -> return by pointer
- return type `decltyype(auto)` -> the return type is `decltype(<RETURN EXPRESSION>)`

See more rules on [cppreference](https://en.cppreference.com/w/cpp/language/function#Return_type_deduction)


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



# Classes and structs
The only difference between a `class` and a `struct` is that in class, all members are private by default.

## Friend declaration
Sometimes, we need to provide an access to privat e members of a class to some other classes. In java, for example, we can put both classes to the same package and set the members as package private (no specifier). In C++, there is an even stronger concept of friend classes.

We put a `friend` declaration to the body of a class whose *private* members should be accessible from some other class. The declaratiton can look as follows:
```cpp
Class To_be_accesssed {
	friend Has_access;
}
```
Now the `Has_access` class has access to the `To_be_accesssed`'s private members.

Note that the **friend relation is not transitive, nor symetric, and it is not inherited.**
  
[cppreference](https://en.cppreferececomfriend)

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
- some types can have arbitrary values when unassigned. This can lead to confusion when debugging the class, i.e., the member can appear as initialized even if it is not.
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

Type | In-place | works for const members
--|
--|--
Constructor body | no | no
Member initializer list | yes | yes
Default member initializer | yes, if we use direct initialization | yes



# Constructors, Destructors, and Related Operators

## Constructor and Destructor Types
- Constructor
-   Copy Constructor
-   Copy Assignment
-   Move Constructor
-   Move assignment
-   Destructor

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

## Copy Constructor
A copy constructor is called if (incomplete list):
-   we use the = operator when creating a new instance, e.g.:
```
Class instance_a;
Class instance_b = instance_a;
```
-  an instance of the class is passed by value to function,
-  an instance of the class is returned by value (except for RVO),
-  we need to call the copy constructor directly,
-  when   we add an instance to vector using `vector.push_back(instance)`

### Default variant:
-   Default copy constructor calls recursively the copy constructor of all base classes and on all members
	-   for a pointer member, the copy object’s member points to the same object as the original object’s member
-   The *implicit* default copy constructor is deleted if
	-  there exists a user-defined move constructor
	- the parent copy constructor is deleted
	- any of the members has a deleted copy construcor

## Copy Assignment
Copy Assignment is needed when  we use the `=` operator with the existing class instances, e.g.:
```
Class instanceA {};
Class instanceB;
instanceB = instance A
```
    
## Move Constructor
Move constructor is typically called when the object is costructed from rvalue.
-   Move constructor is needed:
	-   to cheaply move the object out from function
	-   to store the object in vector (copy constructo e a e ipted instead) e can alat a:
```c

### Implicitely-declared move constructor
The default move constructor for type `T` is implicitely-declared if all of this is true:
- `T` has no declared copy constructors, copy assignment operators, move assignment operators, or destructors
- All members of `T` are movable
- All base classes of `T` are movable and destructiblenen oetli

 r can be implemented instead) nooect slicin

## Move Assignment

## Destructor
We need destructor only if the object owns some resources that needs to be manually deallocated
    
## Rules
-   if you want to be sure, delete everything you don’t need
- most likely, either we need no custom constructors, or we need three (move and destructor), or we need all of them.
    
## Rules for Typical    
## Object Types

### Simple Temporary Object
-   the object should live only in some local context
-   we don’t need anything

### Unique Object
-   usually represents some real object
-   usually, we need constructors for passing the ownership:
	-   move constructor
	-   move assignment noe sin

### Default Object
-   copyable object
-   We need
	-   copy constructor
	-   copy assignment
	-   move constructor
	-   move assignment

# Operators
In C++ there are more operators than in other popular es like Python or Java. Additionally, thsese operator s can be overloaded. See [cppreferencen](https://en.cppreferencempp.com/w/cpp/language/operators) page for detailed description.

## Comparison Operators
### Deafult Comparison Operators
For details, see [cppreferencetassnpneolan](https://en.cppreference.com/w/cpp/language/default_comparisons).

The `!=` is usually not a problem, because it is implicitely generated as a negation of the `==` operator. However, **the `==` is not generated by default, even for simple classes**. To force the generation of a default member-wise comparison operator, we need to write:

```c++
bool operator==(const My_class&) const == default;
```

owever, to do that, all members and base classes have to ae the operator `==` defined, otherwise the default operator will be implicitely deleted.

The comparability can be checked with a `std::equality_comparable<T>` co
 ncptcp
ic_assert(std::equality_comparable<My_class>);
``` 


# Const vs non-const 
The `const` keyword makes the object non-mutable. This means that:
- it cannot be reassigned
- non-const member functions of the object cannot be called

The const keyword is usually used for local variables, function parameters, etc.

**For members, the const keyword should not be used**, as it sometimes breaks the move operations on the object. For example we cannot move f om a const `std::unique_ptr<T>` object. While this is also true for local variable, in members, it can lead to hard to find compilation errors, as a single const `std::unique_ptr<T>`  member deep in the object hierarchy breaks the move semantic for the whole class and all subclasses.

## Avoiding duplication between const and non-const version of the same function
To solve this problem without threathening the const-correctness, we need to implement the *const* version of a function and call it from the non-const one with double type cast:
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

 there are no common supercalss or i## Const/non const overloads and inheritance
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
# Const vs non-const
Use non-const objects if one of the following is true:
-   you want the object to be mutable

## Avoiding duplication between const and non-const version of the same function
To solve this problem without threathening the const-correctness, we need to implement the *const* version of a function and call it from the non-const one with double type cast:
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



# IO and Filesystem

## Standard IO
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

To remove a directory with all its content, we can use `std::filesystem::remove_all(<path>)` function listed on the same page of cppreference.


## Simple line by line IO
### Input
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

## csv
### Input
### Output
For csv output, we can usually use the general line-by-line approach.





# Inheritance
Inheritance in C++ is similar to other languages, here are the important points:
- To enable overiding, a member function needs to be declared as `virtual`. Otherwise, it will be just hidden in a child with a function with the same name, and the `override` specifier cannot be used (see Shadowing).
- Multiple inheritance is possible.
- No interfaces. Instead, you can use abstract class with no data members.
- Virtual functions without implementation needs `= 0` at the end of the declaration (e.g.: `virtual void print() = 0;`)

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

## Shadowing
Members in child with a same name as another members in parent shadows those members. 
This can be counter-intuitive for functions as **the shadowing considers only the name, not the signature**. To use a member function from base that is shadowed by a function with a different signature, we can use the `using` declaration.

## Constructors
Parent constructor is allways called from a child. By default, an empty construcor is called. Alternatively, we can call another constructor in the initializer. When we do not call the parent  constructor in the child's initializer and the parenhas no empty constructor, a compilation error is raised.

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

But when defining destructor, constructor and move operations are not impliciotely  generated. Moreover, the copy operations are generated enabling a polymorphic copy, which results in slicing.  Therefore, **tThe best approach for the base class** is to**herefore to: 
- declare the **virtual destrucor** as default
- declare the **default constructor**. We need a default constructor, unless we use a diferent constructor and we want to disable the default one.
- declare the **copy and move operations as protected**. This way, the polymorpic copy is not possible, but proper copy/move operations are generated for every child class.  


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

# Templates
## Organization rules

 - `*.h`: declarations
 - `*.tpp` template definitions
 - `*.cpp` non-template definitions.

For simplicity, we include the `tpp` files at the end of corresponding header files. If we need to speed up the compilation, we can include the `tpp` files only in the source files that needs the implementations , as described on [SE](https://softwareengineering.stackexchange.com/questions/373916/c-preferred-method-of-dealing-with-implementation-for-large-templates)

To speed up the build it **is also desireble to move any non-template code to source files**, even through inheritance, if needed.

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

Don|t forget to close the file and reopen it after the change to clear the errors.



## Using Complicated Types as Template Arguments
Sometimes, it can be very tricky to determine the template argument we need in order to use the template. The correct argument can be for example a return value of some function,  templete function, or even member function of a template instanciation which has other templates as argument...

To make it easier, we can, istead of suplying the correct arguments, evaluate an expression that returns the correct type and then use the [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) specifier.  For more info, see the *Determining Type from Expressions* section.

## Template Argument Deduction
Details on [cppreference](https://en.cppreference.com/w/cpp/language/template_argument_deduction).

Template argument deduction should work for:
- constructors
- function and operator calls
- storing the function pointer

## Class Template Argument Deduction (CTAD)
Details on [cppreference](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction).

The main difference from the function templete argument deduction is that in CTAD, all the template arguments needs to be specified, or all must not be specified and must be deducible.

Apart from that, there are more subtle differences arising of a prete complex procedure that is behind CTAD. We explain CTAD principle using a new concept (not a C++ concept :) ) called *deduction guides*.

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
The vast majoritz of deduction guidedes used in CTAD are implicit. The ost important implicit deduction guides are:
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

Most of the time, it is not so important and we can just look at the constructor that is chosen by the constructor overload resolution process and see the used deduction guids and consequently, the resulting template arguments. sometimes, however, this simplified understanding can lead to confusing results:
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




# Type Traits
The purpose of type traits is to create predicates involving teplate parameters. Using type traits, we can ask questios about template parameters. With the answer to these questions, we can even implement conditional compilation, i.e., select a correct template based on parameter type. Most of the STL type traits are defined in header [`type_traits`](https://en.cppreference.com/w/cpp/header/type_traits).

A type trate is a template with a constant that holds the result of the predicate, i.e., the answer to the question.

[More about type traits](https://www.internalpointers.com/post/quick-primer-type-traits-modern-cpp)





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

- *Nested requirement*: a require expression inside another requires expression:
```cpp
requires(T a, size_t n)
{
    requires Same<T*, decltype(&a)>; // nested
}
```

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

## Sources
[https://en.cppreference.com/w/cpp/language/constraints](https://en.cppreference.com/w/cpp/language/constraints)

[Requires expression explained](https://akrzemi1.wordpress.com/2020/01/29/requires-expression/)



# Interfaces
In programming, an interface is usualy a set of requirements that restricts the function or template parameters, so that all types fulfiling the requiremnet can be used as arguments.

Therte are two ways how to create an interface in C++:
- using the *polymorphism*
- using *templates argument restriction*

While the polymorphism is easier to implement, the templating is more powerful and it has zero overhead. The most important thing is probably that despite these concepts can be used together in one application, not all "combinations" are allowed especialy when using tamplates and polymorphism in the same type.

The interace can be created for type, using the tepmlate argument restiction, or for functions, using either templete argument restriction or polymorphism. However, we can use polymorphism even in case of templeta argument re## Polymorphism
Polymorphism is a concept for abstriaction.

To demonstrate all possible options, imagine an interface that constraints a using which we can provide a sigle interface for multiple type sos that it must have the following two functions:
```cpp
int get_value();
void set_value(int date);
```
Inshare. In C++, to use the fpollowing sections we will demonstrate all ymorphism, **we need to work withe possible options:

## Interface using polymorfism
Unlike in java, there are no `interface` types in C++. however, we can implement polymorfic interface using abstractinters or references**. Imagine that we have these two class and a method that can process the base class:

```cpp++
class Value_interface{
	virtual int get_value() = 0;
	virtual void set_value(int date) = 0;
}
```

This system works in C++ because it supports multiple inheritance. Do not forget to use the `virtual` keyword, otherwise, the method cannot be overriden.

To use this interface as a fuction argument or return value, follow this example:
```cpp
std::unique_ptr<Value_interface> increment(std::unique_ptr<Value_interface> orig_value){
	return orig_value->set_value(orig_value->get_value() + 1);
}
```
Note that unlike in other languages, **in C++, the polymorphism cannot be directly use as a template (generic) interface.** Therefore, we cannot use the polymorfism alone to restrict a type.

## Using template argument restriction as an interface
We can Base {
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
process_base(derived); // we can calso create an interface by restricting the templl the function thate arguments. Both classes and functions can be restricted in this way. The template parameters can be restricted using type traits and concepts, we will demostrate the system using concepts. The followinfg concept is analogous to the abstract class in the previous sectionccepts a base pointer with a derived pointer
```

We can do the same with smart pointers:

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

## Using concepts and polymorphism together to restrict template parameters with abstract class
We cannot restrict template parameters by polymorphic interface directly, however, we can combine it with concept. The folowing concept can be used together with the interface from the polymorphic interface section:

```cpp
template<class V>
concept Value_interface_concept = requires std::is_base_of<Value_interface,V>
```++
void process_base_sh(std::shared_ptr<Base> base) {
}

std::shared_ptr<Derived> derived_sh = std::make_shared<Derived>();
std::shared_ptr<Base> base_sh = derived_sh;

process_base_sh(base_sh);
process_base_sh(derived_sh);
```

Advanteges:
- easy to implement
- easy to undestand
- similar to what people know from other languages
## Templates as Interface
Advantages
- no need for type cast
- all types check on compile time -> no runtime errors
- zero overhead
- no object slicing

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

## Deciding between template and polymorphism
Frequently, we need some entity(class, function) to accept multiple objects through some interface. We have to decide, whether we use templates, or polymorphism for that interface. Some decision points:
- We need to return the same type we enter to the class/function -> use templates
- We have to access the interface (from outside) without knowing the exact type -> use polymorphism
- We need to restrict the member/parametr type in the child -> use templates for the template parameter
- if you need to fix the relation between method parameters/members or template arguments of thouse, you need to use templates 

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


# Iterators and ranges
If we want to iterate over elements in some programming language, we need to fullfill some interface. In Java, this interface is called `Iterable`. Also, there is usually some interface that formalize the underlying work, in Java, for example, it is called `Iterator`. 

In C++, however,
## Iterators
In C++ there are no common supercalss for iterable and iterator. Instead, the interface is realized using templates. This results in a zero overhead and much more flexibility, nevertheless, implementing an iterable type in C++ is much more complicated compared to other programming languages.

## Terminology 
- *range*: the object we iterate over (Iterable in Java)
- *iterator*: the object which does the real work (Iterator in Java)

Usually, a range is composed from two iterators:
- *begin*: points to the begining of the range, returne by `<range_object>.begin()`
- *end*: points to the end of the object, returned by  `<range_object>.end()` 

Each iterator implements the dereference (`*`) operator that acces the element of the range the iterator is pointing to.

Depending on the iterator type, the iterator also supports other operations: `++`, `--` to iterate along the range, array index operator (`[]`) for random access, etc.

Most of the STL *collections* (vector, set,...) are also ranges.

## STL Ranges
[https://en.cppreference.com/w/cpp/ranges](https://en.cppreference.com/w/cpp/ranges)

In C++ 20 there is a new range library that provides functional operations for iterators. It is similar to functional addon in Java 8.

Unlike in Java, the [range algorithms](https://en.cppreference.com/w/cpp/ranges) (`ranges::<alg name>`) are invoked eagerly. Luckily, each algorithm has it's lazy analogue, a [range adaptor](https://en.cppreference.com/w/cpp/ranges#Range_adaptors) (`ranges::views::<alg name>`). We demonstrate the difference on the iota algorithm/adapter that creates a range of numbers similar to Python range:
```cpp
// numeric algorithm
std::vector<int> vec(10);
std::iota(vec.begin(), vec.end(), 0); // C++11 way

// numeric algorithm
std::vector<int> vec(10);
std::ranges::iota(vec.begin(), vec.end(), 0); // basically the same, but the constructor arguments are constrained with concepts

// same using adaptor
auto range = std::views::iota(0, 10);
std::vector vec{range.begin(), range.end()}; // in-place vector construction
```
Note that the range algorithm cannot produce result without an input, i.e., **we always need a range or collection on which we want to apply our algorithm/adapter.**


### Range functions
- [`std::shuffle`](https://en.cppreference.com/w/cpp/algorithm/random_shuffle) - shuffles the elements in the range (formerly `std::random_shuffle`).

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

## Sequence Range
The `iota` algortihm/adapter is used to create a sequence:
```cpp
auto range = std::views::iota(0, 10);
auto vec = std::vector(range.begin(), range.end());
```
Note that we cannot pass the view directly to the vector, as the vector does not have a range constructor.

## Zip range
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


## Enumerating range
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

The algorithms (but not the view) also supports binary transformations, i.e., create an output range using two input ranges.

Transform view example:
```c++
std::vector<int> in(3, 0); // [0, 0, 0]
auto ad = std::ranges::transform_view(in, [](const auto in){return in + 1;});
std::vector<int> out(ad.begin(), ad.end());
```

The transform *view*  can be only constructed from an object satisfying [`ranges::input_range`](http://en.cppreference.com/w/cpp/ranges/input_range). If we want to use a general range (e.g., vector), we need to call the addapter, which has a same signature like the view constructor itself. The important thing here is that the adapter return type is not a `std::ranges::views::transform<<RANGE>>` but `std::ranges::views::transform<std::ranges::ref_view<RANGE>>>` ([`std::ranges::ref_view`](https://en.cppreference.com/w/cpp/ranges/ref_view)). Supporting various collections is therefore possible only with teplates, but not with inheritance.

## Iterator Concepts
[https://en.cppreference.com/w/cpp/iterator](https://en.cppreference.com/w/cpp/iterator)

C++ 20 has some new iterator concepts, providing various interfaces. However, [range-based for loop (for each)](https://en.cppreference.com/w/cpp/language/range-for) does not require any of the new concepts, nor the legacy iterators, its requirements are smaller.



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

## Other	- number sequence
	- generator


## Resources
-   [How to write a legacy iterator](https://internalpointers.com/post/writing-custom-iterators-modern-cpp)
    
-   [iter_value_t](https://en.cppreference.com/w/cpp/iterator/iter_t)

# Collections
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
The maps has similar requiremnts for keys as the requirements for set value types (see previous section). The hash map type is called [`std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map).

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
There are three options:
1. `map[key] = value;` or
2. `map.insert({key, value});`
3. `map.emplace(key, value);`

There are some considerations with these options:
- 1 inserts the `value` into the map even if the `key` already exists, overwriting the previous value. 2 and 3 do not overwrite the new value, instead, they return the position in the map and the indicator of success (`true` if the insertion happend).
- 1 requires the value to be default *constructible* and *assignable*
- 3 avoids the creation of temporary objects, it sends references to `key` and `value` directly to the map.  

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

There are also factory methods `make_pair`/`make_tuple`. Before C++17, argument deduction did not work for constructors, so there is a dedicated  method for creating tuples. However, now we can just call the constructor and the template arguments are deduced from the constructor arguments. Also, the `make_pair`/`make_tuple` functions can only produce tuples containing values, not references (even if we specify the reference type in the `make_pair`/`make_tuple` template argument, the returned tuple will be value-typed). **TLDR: from C++17, there is no reason to use `make_pair`/`make_tuple`**.


### Accessing tuple members
The standard way to access the tuple/pair mamber is using the [`std::get`](https://en.cppreference.com/w/cpp/utility/tuple/get) function:
```cpp
auto tuple = std::tuple<int, std::string, float>(0, "hello", 1.5);
auto hello = std::get<1>(tuple);
```

### Structured binding - unpacking tuples into variables
If we don't need the whole tuple objects, but only its members, we can use a [*structured binding*](https://en.cppreference.com/w/cpp/language/structured_binding). Example:
```cpp
std::pair<int, int> get_data();

void main(){
	const auto& [x, y] = get_data();
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



# Numbers




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


## [String Literals](https://en.cppreference.com/w/cpp/language/string_literal)
 The standard string literal is writen as `"literal"`. However, we need to escape some characters in such literals, therefore, a *raw string* literal is sometimes more desirable: `R"(literal)"` If our literal contains `(` or `)`, this is stil not enough, however, the delimiter can be extended to any string with a maximum length of 16 characters, for example:
 `R"lit(literal)lit"`.

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
If we want to split the string on patern, the easiest way is to use the split view from the ranges library:
```cpp
auto parts = std::ranges::views::split(str, "-");
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


# Date and time
The date and time structure in C++ is std::tm. We can create it from the date and time string using [`std::get_time`](https://en.cppreference.com/w/cpp/io/manip/get_time) function:
```cpp
std::tm tm;
std::istringstream ss("2011-Feb-18 23:12:34");
ss >> std::get_time(&tm, "%Y-%b-%d %H:%M:%S");
```



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
In C++, exceptions works simillarly as in other languages. Always catch exception by reference!

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
A lot of tamplates in C++ requires functions to be [`noexcept`](https://en.cppreference.com/w/cpp/language/noexcept_spec) which is usually checked by a type trait [`std::is_nothrow_invocable`](https://en.cppreference.com/w/cpp/types/is_invocable). We can easily modify our function to satisfy this by adding a `noexcept` to the function declariaton.

There are no requirements for a `noexcept` function. It can call functions without noexcept or even throw exceptions itself. The only difference it that uncought exceptions from a `noexcept` function are not passed to the caller. Instead the program is terminated by calling [`std::terminate`](https://en.cppreference.com/w/cpp/error/terminate), which otherwise happens only if the `main` function throws.

By default, only constructors, destructors, and copy/move operations are noexcept.


# Usefull STL functions
- [`std::for_each`](https://en.cppreference.com/w/cpp/algorithm/for_each): iterates over iterable objects and call a callable for each iteration
- [`std::bind`](https://en.cppreference.com/w/cpp/utility/functional/bind): Binds a function call to a variable that can be called
	- some parameters of the function can be fixed in the variable, while others can be provided for each call
	- each reference parameter has to be wrapped as a `reference_wrapper`
- [`std:mem_fn`](https://en.cppreference.com/w/cpp/utility/functional/mem_fn): Creates a variable that represents a callable that calls member function
- [`std::copy`](https://en.cppreference.com/w/cpp/algorithm/copy): Copy elements from one range to another.
- [`std::accumulate`](https://en.cppreference.com/w/cpp/algorithm/accumulate): computes the sum of some iterable
- [`std::transform`](https://en.cppreference.com/w/cpp/algorithm/transform): transforms some range and stores it to another. For the output iterator, you can use [`std::back_inserter`](https://en.cppreference.com/w/cpp/iterator/back_inserter).

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



# Conditional Function Execution
W know it from other languages: if the function can be run in two (or more) modes, there is a function parameter that controls the execution. Usually, most of the function is the same (otherwise, we eould create multiple fuctions), and the switch controls just a small part.

Unlike in other langueges. C++ has not one, but three options how to implement this.  They are described below in atable together with theai properties.

| | function parameter | template parameter | compiler directive |
|--|--|--|--|
| good readability | yes| no |no | 
| compiler optimization | no | yes | yes |
| conditional code compilation | no | no | yes |

## Function Parameter
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

## Template Parameter
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

## Compiler Directive
```cpp
void(){
#ifdef SWITCH
    ...
#else
	...
#endif
}
```

# Ignoring warnings for specific line of code
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

# Measuring used resource

## Memory
### MSVC
In MSVC, we can measure the peak used memory using the following code: 
```cpp
#include <psapi.h>

PROCESS_MEMORY_COUNTERS pmc;
K32GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
auto max_mem = pmc.PeakWorkingSetSize
```

# Working with tabular data
Potential libs similar to Python Pandas:
- [Arrow](https://arrow.apache.org/docs/cpp/)
- [Dataframe](https://github.com/hosseinmoein/DataFrame)


# Executing external commands
The support for executing external commands in C++ is unsatisfactory. The most common solution is to use the [`system`](https://en.cppreference.com/w/cpp/utility/program/system) function.
However, the `system` calls are not portable, e.g., the quotes around the command are not supported in Windows

Another option is to use the Boost [Process](https://www.boost.org/doc/libs/1_82_0/doc/html/process.html) library. 

