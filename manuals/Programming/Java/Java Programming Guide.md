# Primitive types
Java has the following primitive types:
- **Integer types**: `byte`, `short`, `int`, `long`
- **Floating point types**: `float`, `double`
- **Character type**: `char`
- **Boolean type**: `boolean`

# Arrays
Arrays in Java are objects, and they are created using the `new` keyword. The syntax is:
```Java
int[] myArray = new int[10];
```
The array is then filled with zeros. The length of the array is fixed and cannot be changed. The array can be initialized using the following syntax:
```Java
int[] myArray = {1, 2, 3, 4, 5};
```

For working with arrays, the static methods from []`java.util.Arrays`](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html) class can be used. Some of the most important methods are:
- `copyOf` and `copyOfRange` for copying arrays
- `fill` for filling arrays with a specific value


# Classes
In java, there are the following types of classes:
- **Standard class**: similar to classes in other languages.
- **Record class**: a simple aggregate of values. 

## Record class
[official specification](https://docs.oracle.com/javase/specs/jls/se16/html/jls-8.html#jls-8.10)

Record class is a simple aggregate class. It is designed to replace the standard class in cases where the class is used only to hold the data (POJO). It is defined using the `record` keyword like this:
```Java
record MyRecord(int par1, String par2){
   ...
}
```
The advantage over the standard class is that the record class automatically declare data members for all parameters of the record header, and it generates the following methods:
- `equals`
- `hashCode`
- `toString`
- `getters` for all parameters
- `constructor` that accepts all parameters


# Standard Types


## Strings
Classical string literals has to be enclosed in quotes (`"my string"`). They cannot contain some characters (newline, `"`). The backslash (`\`) character is reserved for Java escape sequences  and need to be ecaped as `\\`.

In addition, since Java 15, there are text blocks, enclosed in three quotes:
```Java
"""
My long
"text block"
"""
```
The properties of text blocks:
- can be used as standard string literals
- can contain newlines, quotes, and some other symbols that have to be escaped in standard string literals.

The new line after opening triple quoute is obligatory. **Note that backslash (`\`) is still interpreted as Java escape character, so we need to escape it using `\\`**. 

There are no fstrings in Java, the best way for using variables in strings is to use the `String.format` method:
```Java
String s = String.format("My string with %s and %d", "text", 5);
```

## Collections
Java has a rich set of collections. Still, many are missing, notably some tuple class. Also, the typical tuple unpacking known from Python or C++ is not possible in Java and we have to use a verbose way of 1) creating a temporary object for all values, 2) accessing the values using the getters.

### List
List initialization in Java is complicated compared to other languages. we can initialize the list as:
```Java
List a = List.of(1, 2, 3);
```
However, this method returns an **immutable** list. If we need a mutable list, we have to pass the list to the `ArrayList` constructor:
```Java
List a = new ArrayList<>(List.of(1, 2, 3));
```
but with such a complicated syntax, we can use an input array directly:
```Java
List a = new ArrayList<>(Arrays.asList(1, 2, 3));
```

### Set
From java 9, sets can be simply initialized as:
```Java
Set<int> nums = Set.of(1,2,3);
```
Note that this method returns an immutable set. In the earlier versions of Java, the `Collections.singleton` method can be used. 


### Sorting
Some collections can be sorted using the `sort` member method. It is a **stable** sort, which use the natural order of the elements by default, but it can be customized using a comparator. The comparator interface expects two elements and should return a negative number if the first element is smaller, a positive number if the first element is greater, and zero if the elements are equal. 


# Overloading 
When calling an oveladed method with a null argument, we receive a compilation error: `reference to <METHOD> is ambiguous`. A solution to this problem is to cast the null pointer to the desired type:
```Java
public set(string s){
    ...
}

public set(MyClass c){
    ....
}

set(null) // doesn't work
set((MyClass) null) // works
set((String) null) // works
```



# Regular expressions
First thing we need to know about regexes in java is that we need to escape all backslashes (refer to the Strings chapter), there are no raw strings in Java.

We can work with regexes either by using specialized high level methods that accepts regex as string, or by using the tools from the `java.util.regex` package.

## Testing if string matches a regex
We can do it simply by: 
```Java
String MyString = "tests";
String MyRegex = "t\\p+"
boolean matches = myString.matches(myRegex);
```



# Exceptions
The exception mechanism in Java is similar to other languages. The big difference is, however, that in Java, all exception not derived from the `RuntimeException` class are [*checked*](https://en.wikipedia.org/wiki/Exception_handling#Checked_exceptions), which means that their handeling is enforced by the compiler. The following code does not compile, because the `java.langException` class is a checked exception class.
```Java
private testMethod{
    ...
    throw new Exception();
}
```  

Therefore, we need to handle the exception using the try cache block or add `throws <EXCEPTION TYPE>` to the method declaration.

When deciding between `try/catch` and `throws`, the rule of thumb is to use the `try/cache` if we can handle the exception and `throws` if we want to leave it for the caller. The problem arises when the method we are in implements an interface that does not have the `throws` declaration we need. Then the only solution is to use `try/cache` with a cache that does not handle the exception, and indicate the problem to the caller differently, e.g, by returning a `null` pointer.



# Logging
Java has a built-in logging mechanism in the `java.util.logging` package. Apart from that, there are many other logging libraries. In this section, we focus on the [SLF4J library](https://www.slf4j.org/) which is an abstraction. With SLF4J, we can switch between different logging libraries without changing the code.

To use SLF4J, we need to add the following dependency to the `pom.xml` file:
```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version><version></version>
</dependency>
```

Additionally, we need to add a backend of our choice. For example, we can use the `logback` library:
```xml
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version><version></version>
</dependency>
```

The SLF4J library detects the available backend automatically. 



# Genericity
[Oracle official tutorial for Java 8](https://docs.oracle.com/javase/tutorial/java/generics/index.html)

Like many other languages, Java offers generic types with the classical syntax:
```Java
class GenericClass<T>{
    ...
};
```

An object is then created as:
```Java
GenericClass<OtherClass> gc = new GenericClass<OtherClass>();
```


## Diamond operator
At all places where the type can be inferred, we can use the dianmond operator (`<>`) without specifiyng a type:
```Java
GenericClass<OtherClass> gc = new GenericClass<>();
```


## Raw types
[specification](https://docs.oracle.com/javase/specs/jls/se8/html/jls-4.html#jls-4.8)

For the backward compatibility of Java library classes that were converted to generic classes a concept of *raw types* was introduces. However, in addition, this concept brings a lot of very subtle compile errors, which are caused by a nonintentional creation of raw type instead of a specific type.
```Java
GenericClass gc = new GenericClass(); // raw type
```

The parameterized type can be assigned to the raw type, but when we do it the other way arround, the code emmits warning and is not runtime safe:
```Java
GenericClass<OtherClass> generic = new GenericClass<>();
GenericClass raw = generic // OK

GenericClass raw = new GenericClass();
GenericClass<OtherClass> generic = raw // unsafe
```
Calling the generic methods on raw types has a simmilar consequences.

But the worst property of raw types is that **all generic non-static members of raw types that are not inherited and are also eraw types. Therefore, the genericity is lost even for the completely unrelated type parameters, even specific types are erased to `Object`**. The consequence can be seen on the following example:
```Java
class GenericClass<T>{
    public List<String> getListofStrings()
};

GenericClass raw = new GenericClass();
raw.getListofStrings(); // returns List<Object> !!!
```


## Generic method
A generic method in Java is written as:
```Java
public <<GENERIC PARAM NAME>> <RESULT TYPE> <METHOD NAME>(<PARAMS>){
    ...
}
```
example:
```Java
public static <T> ProcedureParameterValidationResult<T> error(String msg){
    return new ProcedureParameterValidationResult<>(false, msg, null);
}
```

if the generic parameter cannot be infered from the method arguments, we can call the method with explicit generic argument like this:

```Java
<<GENERIC PARAM VALUE>><METHOD NAME>(<ARGUMENTS>);
```
example:
```Java
ProcedureParameterValidationResult.<String>error("Value cannot be empty.");
```

## Retrieving the type of a generic argument
Because the genericity in Java is resolved at runtime, it is not possible to use the generic parameter as a type. What does it mean? Whille it is possible to use `Myclass.class` it is not possible to use `T.class`. The same applies for the class methods.

The usual solution is to pass the class to the generic method as a method parameter:
```Java
void processGeneric(Class<T> classType){
    ...
}
```

## Default generic argument
It is not possible to set the default value of a generic parameter. If we want to achive such behavior, we need to create a new class:
```Java
class GeneriClass<T>{
    ...
}

class StringClass extends GenericClass<String>{};

```

## Wildcards
The wildcard symbol (`?` ) represents a concrete but unspecified type. It can be bounded by superclass/interface (`? exctends MyInterface`), or by sublcass (`? super MyClass`). The typical use cases:
- single non-generic method accepting generic types of multiple generic parameter values: 
```Java
myMethod(Wrapper<? extends MyInterface> wrapper){
    MyInterface mi = wrapper.get();
    ...
}
```
- method that can process generic class but does not need to work with the generic parameters at all:
```Java
getLength(List<?> list){
    return list.size();
}
```

## Difference between `MyClass`, `MyClass<Object>`, and `MyClass<?>`
```Java
class MyClass<T>{
    private T content;
    private set(T content){
        this.content = content;
    }
    private List<String> getList;
}

// raw type
processMyClass(MyClass myClass){...};

// My class of object types
processMyClass(MyClass<Object> myClass){...};

// My class of any specific type
processMyClass(MyClass<?> myClass){...};
```


|| `MyClass` (raw type)|`MyClass<Object>`|`MyClass<?>`|
|--|--|--|--|
| type safe (Check types at compile time) | no | yes | yes
|`set` can be called with| any `Object` | any `Object` | `null` only |
| `getList()` returns | `List<Object>` | `List<String>` | `List<String>` |
| `processMyClass` can be called with | any `List` | `List<Object>` only | any `List` |







# Enums
Java enumerations are declared using the `enum` keyword:
```Java
public enum Semaphore{
    RED,
    ORAGNGE,
    GREEN
}
```

If we need to add some additional members to the enum, we need to end the list of enum items with a semicolon first:
```Java
public enum Semaphore{
    RED,
    ORAGNGE,
    GREEN;
    
    public void doSomething(){
        ...
    }
}
```


## Iterating over enum items
we can iterate over enum items using the `values` method:
```Java
for(Semaphore s: Semaphore.values()){
    ...
}
```
The above code iterates over values of a specific enum. If we need an iteration over any enum (generic), we need to use a class method:
```java
Class<E> enumClass;
for(E item: enumClass.getEnumConstants()){
			
}
```

## Converting a string to enum
We can convert a String to enum using the `valueOf` method that is generated for each enum class>
```Java
Semaphore sem = Semaphore.valueOf("RED");
```
Note that the string has to match the enum value exactly, including the case. Extra whitespaces are not permited.

There is also a generic static `valueOf` method in the `Enum` class, which we can use for generic enums:
```Java
Class<E> enumClass;
E genEnumInst = Enum.valueOf(enumClass, "RED");
```
Note that here `E` has to be a properly typed enum (`Enum<E>`), not the raw enum (`Enum`).



# File System
The modern class for working with paths is the [`Path`](https://docs.oracle.com/javase/8/docs/api/java/nio/file/Path.html) class from the `java.nio.file` package. 

Other important class is the [`Files`](https://docs.oracle.com/javase/8/docs/api/java/nio/file/Files.html) class, which contains static methods for working with files and directories. Important methods:
- `exists`
- `isDirectory`
- `isRegularFile`
-  methods for iterating over files (see next section)


## Iterating over files in a directory
We can iterate the files in a directory using the [`Files`](https://docs.oracle.com/javase/8/docs/api/java/nio/file/Files.html) class:
- `Files.list`: flat list of files
- `Files.walk`: recursive list of files

Both methods return a `Stream<Path>` object.


## Creating a directory
The directory can be created from any `Path` object using the `Files.createDirectory` method. 

We can also create a directory from a `File` object using the `mkdir` and `mkdirs` methods. 


# Date and Time
[Baeldung tutorial](https://www.baeldung.com/java-8-date-time-intro)

The following classes are intended for working with date and time in Java:
- [`LocalDate`](https://docs.oracle.com/javase/8/docs/api/java/time/LocalDate.html): date without time
- [`LocalTime`](https://docs.oracle.com/javase/8/docs/api/java/time/LocalTime.html): time without date
- [`LocalDateTime`](https://docs.oracle.com/javase/8/docs/api/java/time/LocalDateTime.html): date and time

The `LocalDateTime` als has its timezone/localization aware counterpart:
- [`ZonedDateTime`](https://docs.oracle.com/javase/8/docs/api/java/time/ZonedDateTime.html): date and time with timezone


# Lambda expressions
[wiki](https://en.wikipedia.org/wiki/Anonymous_function#Java)

An important thing about lambda expressions in Java is that we can only use them to create types satisfying some functional interface. This means that:
- They can be used only in a context where a functional interface is expected
- They need to be convertible to that interface. 

The example that demonstrate this behavior is bellow. Usually, we use some standard interface, but here we create a new one for clarity:

```Java
interface OurFunctionalInterface(){
    int operation(int a)
}

...

public void process(int num, OurFunctionalInterface op){
    ...
}
```

With the above interface and method that uses it, we can call
```Java
process(0, a -> a + 5)
```
Which is an equivalent of writing

```Java
OurFunctionalInterface addFive = a -> a + 5;
process(0, addFive);
```

## Syntax
A full syntax for lambda expressions in Java is:
```Java
(<PARAMS>) -> {
    <EXPRESSIONS>
}
```

If there is only one expression, we can ommit the code block:
```Java
(<PARAMS>) -> <EXPRESSION>
```
And also, we can ommit the `return` statement from that expression. The two lambda epressions below are equivalent:
```Java
(a, b) -> {return a + b;}
(a, b) -> a + b
```

If there is only one parameter, we can ommit the parantheses:
```Java
<PARAM> -> <EXPRESSION>
```

By default, the parameter types are infered from the functional interface. If we need more specific parameters for our function, we can specify the parameter type, we have to specify all of them however:
```Java
(a, b) -> a + b // valid
(int a, int b) -> a + b // valid
(int a, b) -> a + b // invalid
```
Also, it is necesary to use the parantheses, if we use the param type.


## Method references
We can also create lambda functions from existing mehods (if they satisfy the desired interface) using a mechanism called *method reference*. For example, we can use the `Integer.sum(int a, int b)` method in conext where the `IntBinaryOperator` interface is required. Instead of 
```Java
IntBinaryOperator op = (a, b) -> a + b; // new lambda body
``` 
we can write:
```Java
IntBinaryOperator op = Integer::sum; // lambda from existing function
```


## Exceptions in lambda expressions
Beware that the checked exceptions thrown inside lambda expressions has to be caught inside the lambda expression. The following code does not compile:
```Java
try{
    process(0, a -> a.methodThatThrows())
catch(exception e){
    ...
}
```
Instead, we have to write:
```Java
process(0, a -> {
    try{
        return a.methodThatThrows());
    catch(exception e){
        ...
    }
}
```


# Iteration
Java for each loop has the following syntax:
```Java
for(<TYPE> <VARNAME>: <ITERABLE>){
    ...
}
```
Here, the `<ITERABLE>` can be either a Java `Iterable`, or an array. 


## Enumerated iteration
There is no `enumerate` equivalent in Java. [One can use a stream API range method](https://stackoverflow.com/questions/66662506/how-to-enumerate-add-indices-to-a-list-like-collection-in-java), however, it is less readable than standard for loop because the code execuded in loop has to be in a separate function.


## Iterating using an iterator
The easiest way how to iterate if we have a given iterator is to use its `forEachRemaining` method. It takes a `Consumer` object as an argument, iterates using the iterator, and calls `Consumer.accept` method on each iteration. The example below uses a lambda function that satisfies the consumer interface:

```Java
class Our{
    void process(){
        ...
    }
    ...
}

Iterator<Our> objectsIterator = ...;

objectsIterator.forEachRemaining(o -> o.process());
```



# Functional Programming
## Turning array to stream
```Java
Arrays.stream(<ARRAY>);
```

## Creating stream from iterator
The easiest way is to first create an `Iterable` from the iterator and then use the `StreamSupport.stream` method:
```Java
Iterable<JsonNode> iterable = () -> iterator;
var stream = StreamSupport.stream(iterable.spliterator(), false);
```

## Filtering
A lambda function can be supplied as a filter:
```Java
stream.filter(number -> number > 5)
```
returns a stream with numbers greater then five.


## Transformation
We can transform the stream with the `map` function:
```Java
transformed = stream.map(object -> doSomething(object))
```


## Materialize stream
We can materrialize stream with the collect metod:
```Java
List<String> result = stringStream.collect(Collectors.toList());
```
Which can be, in case of `List` shorten to:
```Java
List<String> result = stringStream.toList();
```




# `var`
[openjdk document](https://openjdk.org/projects/amber/guides/lvti-style-guide)

Using var is similar to `auto` in C++. Unlike in C++, it can be used only for local variables.

The `var` can be tricky when using together with diamond operator or generic methods. The compilation works fine, however, the raw type will be created.


# Type cast
Java use a tradidional casting syntax:
```
 (<TARGET TYPE>) <VAR>
```

There are two different types of cast:
- *value cast*, which is used for value types (only primitive types in Java) and change the data
- *reference cast*, which is used for Java objects and does not change it, it just change the objects interface

## Reference cast
The *upcasting* (casting to a supertype) is done implicitely by the compiler, so instead of
```Java
Object o = (Object) new MyClass();
```

we can do
```Java
Object o = new MyClass();
```

Typically, we need to use the explicit cast for *downcasting*:
```Java
Object o = ...;
MyClass c = (MyClass) o; // when we are sure that o is an instance of MyClass...
```

Downcasting to an incorrect type leads to a runtime `ClassCastException`.

Casting to an unrelated type is not allowed by the compiler.

## Casting generic types
Casting with generic types is notoriously dangerous due to type erasure. The real types of generic arguments are not known at runtime, therefore, an incorrect cast does not raise an error:
```Java
Object o = new Object();
String s = (String) o; // ClassCatsException

List<Object> lo = new ArrayList<>();
List<String> ls = (List<String>) lo; // OK at runtime, therefore, it emmits warning at compile time.

```


## Casting case expression
Often, when we work with an interface, we have to treat each implementation differently. The best way to handle that is to use the polymorphism, i.e., add a dedicated method for treating the object to the interface and handle the differences in each implementation. However, sometimes, we cannot modify the interface as it comes from the outside of our codebase, or we do not want to put the code to the interface because it belongs to a completely different part of the application (e.g., GUI vs database connection). A typicall solution for this is to use branching on instanceof and a consecutive cast:

```Java
if(obj instance of Apple){
    Apple apple = (Apple) obj;
    ...
}
else if(obj instance of Peach){
    Peach peach = (Peach) obj;
    ...
}
...
```

### Casting `switch`
This approach works, it is safe, but it is also error prone. A new preview `swich` statement is ready to replace this technique:
```Java
switch(obj)
    case Apple apple:
        ...
        break;
    case Peach peach:
        ...
        break;
    ...
}
```

Note that unsafe type opperations are not allowed in these new `switch` statements, and an error is emitted instead of warning:

```Java
List list = ...

List<String> ls = (List<String>) list; // warning: unchecked

switch(list){
    case List<String> ls: // error: cannot be safely cast
        ...
}
```



# Random numbers

## Generate random integer
To get an infinite iterator of random integers, we can use the [`Random.ints`](https://docs.oracle.com/javase/8/docs/api/java/util/Random.html#ints-int-int-) method:
```Java
var it = new Random().ints(0, map.nodesFromAllGraphs.size()).iterator();\
int a = it.nextInt();
```


# Reflection
Reflection is a toolset for working with Java types dynamically. 

## Get class object
To obtain the class object, we can use:
- the `forName` method of the `Class` class:
    ```Java
    Class<?> c = Class.forName("java.lang.String");
    ```
    - This way, we can load classes dynamically at runtime.
- `myString.getClass()` if we have an instance or
- `String.class` if we know the class at compile time.
 from an object of the class (e.g.,. The method can be then iterated using the `getDeclaredMethods` method of the `Class` class.


## Test if a class is a superclass or interface of another class
It can be tested simply as:
```Java
ClassA.isAssignableFrom(ClassB)
```

## Get field or method by name
```Java
Field field = myClass.getDeclaredField("fieldName");
Method method = myClass.getMethod("methodName", <PARAM TYPES>);
```
Here, the `<PARAM TYPES>` is a list of classes that represent the types of the method parameters, e.g., `String.class, MyClass.class` for a method that accepts a string and an instance of `MyClass`.

## Call method using Method object
```Java
method.invoke(myObject, <PARAMS>);
```





# SQL
Java has a build in support for SQL in package `java.sql`. The typical operation:
1. 
1. 
1. create a `PreparedStatement` from the cursor using the SQL string as an input
1. Fill the parameters of the `PreparedStatement`
1. Execute the query

## Filling the query parameters
This process consist of safe replacement of `?` marks in the SQL string with real values. The `PreparedStatement` class has dedicated methods for that:
- `setString` for strings
- `setObject` for complex objects

Each method has the index of the `?` to be replaced as the first parameter. **The index start from 1**.

Note that these methods can be used to supply arguments for data part of the SQL statement. **If the `?` is used for table names or SQL keywords, the query execution will fail.** Therefore, if you need to dynamically set the non-data part of an SQL query (e.g., table name), you need to sanitize the argument manually and add it to the SQl querry. 


## Processing the result
The java sql framework returns the result of the SQL query in form of a [`ResultSet`](https://docs.oracle.com/javase/7/docs/api/java/sql/ResultSet.html). To process the result set, we need to iterate the rows using the `next` method and for each row, we can access the column values using one of the methods (depending on the dtat type in the column), each of which accepts either column index or label as a parameter. Example:
```Java
var result = statement.executeQuery();
while(result.next()){
   var str = result.getString("column_name"));
   ...
}
```



# Jackson
Described in the Jackson manual.



# Dependency injection with Guice
Dependency injection is a design pattern that allows interaction between objects without wiring them manually. It works best in large applications with many independent components. When we want to use Singletons in our application, it is time to consider using a dependency injection.

Guice is very convenient as it has many features that make using DI even easier. For example, any component can be used in DI by simply annotating the constructor with `@Inject`. Note that there can be only one constructor annotated with `@Inject` in a class.

To mark a component that should be used as a singleton, we annotate the class with `@Singleton` annotation.




## Assisted injection
If the class has a constructor with some parameters that are not provided by the Guice, we can use the *assisted injection*
Assisted Injection is a mechanism to automatically generate factories for classes that have a constructor with mixed Guice and non-Guice parameters. 
Instead of a factory class, we provide only a factory interface:
```Java
public interface MyFactory {
    MyClass create(String param1, int param2);
}
```
This factory can than be used to create the object:
```Java
class MyClass{
    @Inject
    MyClass(
        <parameters provided by Guice>,
        @Assisted String param1,
        @Assisted int param2
    ){
        ...
    }
}
```

The non-Guice parameters are assigned using the parameters of the factory's `create` method. The matching is determined by the parameter type. If the parameter type is not unique, among all @Assisted parameters, we have to provide the `@Assisted` annotation with the `value` parameter:
```Java
public interface MyFactory {
    MyClass create(@Assisted("param1") String param1, @Assisted("param2") String param2);
}

class MyClass{
    @Inject
    MyClass(
        <parameters provided by Guice>,
        @Assisted("param1") String param1,
        @Assisted("param2") String param2
    ){
        ...
    }
}
```


# Progress bar
For the progress bar, there is a good library called [`progressbar`](https://github.com/ctongfei/progressbar)

The usage is simple, just wrap any iterable, iterator, stream or similar object with the `ProgressBar.wrap` method:
```Java
ArrayList<Integer> list =  ...
for(int i: ProgressBar.wrap(list, "Processing")){
    ...
}

// or with a stream
Stream<Integer> stream = ...
progressStream = ProgressBar.wrap(stream, "Processing");
progressStream.forEach(i -> ...);

// or with an iterator
Iterator<Integer> iterator = ...
progressIterator = ProgressBar.wrap(iterator, "Processing");
while(iterator.hasNext()){
    ...
}
```

