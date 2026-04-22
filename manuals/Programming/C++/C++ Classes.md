# Classes and structs
The only difference between a `class` and a `struct` is that in class, all 
members are private by default.


# Static Members
[cppreference](https://en.cppreference.com/w/cpp/language/static.html)

Inside a class, the keyword `static` marks members that are not bound to any specific instance of the class, but to the class itself.

They are declared as with the keyword `static`, but defined without it. 

To use a static member, we use the syntax `<class_name>::<member_name>`.

## Class Constants
Class constants are static members that are defined as constants. They can be defined in two ways:

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

# Friend declaration
[cppreference](https://en.cppreferececom/friend)

Sometimes, we need to provide an access to private members of a class to some other classes. In java, for example, we can put both classes to the same package and set the members as package private (no specifier). In C++, there is an even stronger concept of friend classes.

We put a `friend` declaration to the body of a class whose *private* members should be accessible from some other class. The declaratiton can look as follows:
```cpp
Class To_be_accesssed {
	friend Has_access;
}
```
Now the `Has_access` class has access to the `To_be_accesssed`'s private members.

Note that the **friend relation is not transitive, nor symetric, and it is not inherited.**


## Template friends
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
We can check if a class is copy constructible using the [`std::is_copy_constructible`](https://en.cppreference.com/w/cpp/types/is_copy_constructible) type trait:
```cpp
static_assert(std::is_copy_constructible<My_class>::value); // or equivalent using
static_assert(std::is_copy_constructible_v<My_class>); 
```

However, **the `std::is_copy_constructible` is not a reliable way to check if a class is copy constructible!**. When it evaluates to false:

- the class have an explicitly deleted copy constructor
- the copy constructor is inaccessible (protected, private)
- the copy constructor is not declared because of the rule of five/five, i.e., one of the other constructors/assignments/destructors is defined
- only non-const copy constructor is available

When it evaluates to true, while the class is not copy constructible:

- the copy constructor is implicitly deleted due to members that are not copy constructible
- the copy constructor is declared, but not defined (results in linker error)

The only robust solution is to create a test where an actual copy constructor is called. An example:

```cpp
// message to be displayed in the compiler output. Without this, developers can be confused, as the test file or function is typically not in the error stack trace.
#pragma message("NOTICE: Compiling copy contract test: Test_class. If the compilation of this unit fails, it almost certainly means that the contract was broken and Test_class class is not copy constructible.")

#include <type_traits>
#include "gtest/gtest.h"

#include "test_class.h"

namespace {
static_assert(std::is_copy_constructible_v<Test_class>);

TEST(compile_time, test) {
	Test_class t1;
	Test_class t2 = t1;
}
}
```

    
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



# Const correctness for classes

A variable is non-mutable (const) if it is:

- `const`-qualified
- it is a member of a const object and it is not declared as [mutable](https://en.cppreference.com/w/cpp/language/cv.html#mutable)

Non mutable variables:

- cannot be reassigned
- non-const member functions of them cannot be called


A member function can be declared with const qualifier at the end of the declaration. A function declared with const:

- accesses its instance as `const *<class_name>` instead of `<class_name>*`
- by conclusion, see all members as const which means:
    - non-const member functions of the object cannot be called
    - non-const member variables of the object are accessed as const references


**For members, the const keyword can break the move operations on the object**. For example we cannot move from a const `std::unique_ptr<T>` object. While this is also true for local variable, in members, it can lead to hard to find compilation errors, as a single const `std::unique_ptr<T>`  member deep in the object hierarchy breaks the move semantic for the whole class and all subclasses.

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