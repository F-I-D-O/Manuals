# Templates
The templates are a powerful tool for:

- generic programming,
- zero-overhead interfaces,
- and metaprogramming.

Although they have similar syntax as generics in Java, they are principialy different both in the way they are implemented and in the way they are used.

There are two types of templates:

- function templates
- class templates


# Syntax
## Template Declaration
Both for classes and functions, the template declaration has the following form:
```cpp
template<<template parameters>>
```



## Template definition
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


# Template Parameters
[cppreference](https://en.cppreference.com/w/cpp/language/template_parameters)

The template parameters can be:

- type parameters: `class T`
- value parameters: `int T`
- template parameters: `template<class T> class TT`

Template parameters can be restricted by in several ways: 

- `typename T`: any complete type
- `class T`: a class type
- `<Concept> T`: a type constrained by a concept
- by a `requires` expression, e.g.: `template<typename T> requires std::is_integral_v<T>`


# Organization rules

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

Don't forget to close the file and reopen it after the change to clear the errors.


# Providing Template Arguments
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


## Rules for omitting the `<>`
We can ommite the `<>` in the following cases:

- when declaring a variable: `A a;`
- when using the type in a function call: `f(A());`
- when instantiating a template class: `class B: public A {};`

We cannot ommite the `<>` in the following cases:

- When we use the template as a nested type: `std::vector<A<>> v;`, not `std::vector<A> v;`
- in the return type of a function: `A<> f()`, not `A f()`
- When declaring an alias: `using B = A<>` not `using B = A`
- for template template parameters.




## Default Template Arguments
Default template arguments can be used to provide a default value for any template parameter except parameter packs. 

For template classes, there is a restriction that after a default argument is used, all the following parameters must have a default argument as well, except the last one wchich can be parameter pack. 


# Template Argument Deduction
Details on [cppreference](https://en.cppreference.com/w/cpp/language/template_argument_deduction).

Template argument deduction should work for:

- constructors
- function and operator calls
- storing the function pointer


# Class Template Argument Deduction (CTAD)
Details on [cppreference](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction).

The main difference from the function templete argument deduction is that in CTAD, all the template arguments needs to be specified, or all must not be specified and must be deducible.

Apart from that, there are more subtle differences arising of a complex procedure that is behind CTAD. We explain CTAD principle using a new concept (not a C++ concept :) ) called *deduction guides*.

## Deduction Guides
The CTAD use so called *deductione guides* to deduce the template parameters. Deduction guides can be either implicit or explicit. To demonstrate the principle, let's first start with user-defined deduction guides.

### User defined deduction guides
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


### Implicit deduction guides
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


### Deduction guides resolution
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


# Template Specialization
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

While behaving similarly, there are some important **differences between the full and partial specialization**:

- **Declaration and definition:**
	- Full specialization is a new type. Therefore, it must be declared in the header and defined in the source file (`.cpp`).
		- additionaly, if the full specialization is a member of a class, the declaration must be outside the class:
			```cpp
			template<>
			class Object{
			public:
				// member function template
				template<class T>
				void print(T value){
					... // template definition
				}

				// template full specialization declaration - wrong. This will not compile in GCC
				template<>
				void print(std::string value){
					... // template definition
				}
			};

			// template full specialization declaration - correct
			template<>
			void Object::print(std::string value);
			```

	- Partial specialization is still just a template, so it must be defined in the header file (`.h` or `.tpp`).
- **For functions, we cannot provide a partial specialization**. 
	- For member functions we can solve this by specializing the whole class. 
	- For free functions, we have to use other techniques like [compile-time branching](#compile-time-branching).


# Type Erasure
[cppreference](https://en.cppreference.com/w/cpp/language/type_erasure)

When working with templates, one soon realizes that they are contiguous. Once we use a template with a parameter `T`, we have to use `T` in the calling code if we do not know the exact type, and that is also true for the calling code of the calling code, etc, all the way to the point where we know the exact type.

Often times, this is principially unavoidable, because we need to use the template parameter to keep the contract on the template parameter type.
However, there are situation where this is absolutely useless. Imagine this scenario:

```cpp
template<class T>
class Vector_statistic{
	void print_vector_size(const std::vector<T>& vector){
		return vector.size();
	}
};
```
Here, there is no type contract on the template parameter `T` needed. Yet, we have to implement `Vector_statistic` as a template class, otherwise it won't compile. To avoid this, we can use the technic called *type erasure*.

The principle of type erasure is to create a parent class without the template parameter `T` that contain the necessary methods that does not depend on the type `T`. Then, we use this polymorphic interface to avoid the need for the template parameter `T`. For the above example, we also need a wrapper class as we cannot change the `std::vector` class template to inherit from our parent class.

```cpp
class Vector_statistic_wrapper{
public:
	virtual void print_vector_size() = 0;
};

template<class T>
class Vector_statistic_wrapper_impl: public Vector_statistic_wrapper{
public:
	Vector_statistic_wrapper_impl(const std::vector<T>& vector): vector(vector){}
	void print_vector_size() override{
		return vector.size();
	}
private:
	std::vector<T>& vector;
};

class Vector_statistic{
public:
	Vector_statistic(){}

	void print_vector_size(const Vector_statistic_wrapper& wrapper){
		return wrapper.print_vector_size();
	}
};
```

Note that for this example, it is probably simpler to use the class template even though we do not need the template parameter `T`. However, if the call chain independent of the type `T` is complex, the type erasure solution can become much simpler and more readable. 

Also note that the type erasure solution can never be more efficient. We can save a little bit on the compile time and code size, but the runtime performance will be strictly lower (due to the virtual function calls)

Sources
- https://davekilian.com/cpp-type-erasure.html


# Template parameter packs
[cppreference on all parameter packs, but mostly template parameter packs](https://en.cppreference.com/w/cpp/language/parameter_pack)

From many programming languages, ve know the concept of function parameter packs (Java), or variable length argument lists (Python). These are available in C++ as well. However, in C++, we also have a much more complex and powerful concept of template parameter packs.

The differnece from function parameter packs is that template parameter packs are resolved at compile time, efectively creating function or class types with a variable number of arguments.

A practical example can be a template function that measures the time of the execution of a function:
```cpp
template<typename F, typename... A>
auto measure_time(F func, A... args){
	auto start = std::chrono::high_resolution_clock::now();
	func(args...);
	auto end = std::chrono::high_resolution_clock::now();
	return std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
}
```

## Syntax
Be aware that the dots (`...`) placement is different for:

- declaration of the template parameter pack: dots after the parameter restriction
- use of the template parameter pack as a type specifier: dots after the type name
- using the parameter pack in an expression: dots after the parameter pack name

Example:
```cpp
template<typename... T> // dots after the parameter restriction
void func(T... args) { // dots after the parameter type
	auto result = other_func(args...); // dots after the parameter pack name
} 
```

## Parameter Pack Expansion
When using the dots (`...`), the parameter pack is expanded. There are many allowed contexts for the expansion, with different rules for the expansion.

When having a parameter pack `A...`, available as `A... args`, it can be used:

- in a function call: `func(args...)` expands to `func(arg1, arg2, ..., argN)`
- class initialization: `My_class(args...)` expands to `My_class(arg1, arg2, ..., argN)`
- brace initialization: `{args...}` expands to `{arg1, arg2, ..., argN}`
- template argument list: `std::tuple<args...>` expands to `std::tuple<arg1, arg2, ..., argN>`
- function parameter list: `template<typename... A> void func(A... args)` expands to `void func(A1 arg1, A2 arg2, ..., AN argN)`
- class template parameter list: `template<typename... A> class My_class<A...>` expands to `My_class<A1, A2, ..., AN>`
- base class specifier: `class My_class: public Args...` expands to `class My_class: public A1, public A2, ..., public AN`
- lambda capture: `[args...]` expands to `[arg1, arg2, ..., argN]`

## Fold Expressions
[cppreference](https://en.cppreference.com/w/cpp/language/fold)

Fold expressions is a powerful feature that allows to cleanly implement operations on the whole parameter pack at once, which would otherwise be very difficult to implement.

There are four possible patterns for fold expressions:

- `(<pack> <operator> ...)`
- `(... <operator> <pack>)`
- `(<pack> <operator> ... <operator> <initial value>)`	
- `(<initial value> <operator> ... <operator> <pack>)`

Here, 

- the `<operator>` is any binary operator (arithmetic, logical, bitwise, assignment, `,`,...).
- the `<initial value>` is an expression without any operator with higher precedence than the `<operator>`.

The fold expression is evaluated as follows:

- `(T... <operator> ...)` evaluates to `(<T1> <operator> (<T2> <operator> ... <operator> <TN>))`
- `(... <operator> T...)` evaluates to `((<T1> <operator> <T2>) <operator> ... <operator> <TN>)`
- `(T... <operator> ... <operator> <initial value>)` evaluates to `(<T1> <operator> (<T2> <operator> ... <operator> (<TN> <operator> <initial value>)))`
- `(<initial value> <operator> ... <operator> <T...>)` evaluates to `((((<initial value> <operator> <T1>) <operator> <T2>) <operator> ... <operator> <TN>)`

Note that we can use fold expressions anywhere where we can use parameter pack expansion. Therefore, we can use them even in e.g. requires expression.

### Examples
An example of a fold expression used for a sum **function template**:
```cpp
template<typename... Args>
auto sum(Args... args){
	return (... + args);
}
```

Fold expression in the **requires expression**:
```cpp
template<typename... NO>
template<template <typename, class...> class S>
requires(DARP_benchmark_solver_constructor_interface<S,NO> && ...)
```

The above requires expression will be expanded to:
```cpp
(DARP_benchmark_solver_constructor_interface<S,NO1> && DARP_benchmark_solver_constructor_interface<S,NO2> && ... && DARP_benchmark_solver_constructor_interface<S,NON>)
```



# Using Complicated Types as Template Arguments
Sometimes, it can be very tricky to determine the template argument we need in order to use the template. The correct argument can be for example a return value of some function,  templete function, or even member function of a template instanciation which has other templates as argument...

To make it easier, we can, istead of suplying the correct arguments, evaluate an expression that returns the correct type and then use the [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) specifier.  For more info, see the *Determining Type from Expressions* section.


# Abbreviated function templates
[cppreference](https://en.cppreference.com/cpp/language/function_template#Abbreviated_function_template)

We can use `auto` instead of a function parameter type. This effectively creates a function template. Example:
```cpp
void func(auto a);
```
Is equivalent to:
```cpp
template<typename T>
void func(T a);
```

We can restrict the auto type by using a concept:

```cpp
void func(Integral auto a);
```
Is equivalent to:
```cpp
template<Integral T>
void func(T a);
```

This shorthand syntax has some limitations. We cannot use it if:

- we need support for C++17 or older,
- there is a dependency between the template parameters (e.g. `func(T a, T b)`,
- We need to acces the type of the parameter in the function body.


