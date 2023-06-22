---
title: "Installation"
permalink: /docs/installation/
excerpt: "Instructions for installing the theme for new and existing Jekyll based sites."
last_modified_at: 2019-08-20T21:36:18-04:00
toc: true
---

# Strings
Classical string literals has to be enclosed in quotes (`"my string"`). They cannot contain some characters (newline, `"`). The backslash (`\`) character is reserved for Java escape sequences  and need to be ecaped as `\\`.

In addition, since Java 15, there are text blocks, enclosed in three quotes:
```java
"""
My long
"text block"
"""
```
The properties of textt blocks:
- can be used as standard string literals
- can contain newlines, quotes, and some other symbols that have to be escaped in standard string literals.

The new line after opening triple quoute is obligatory. **Note that backslash (`\`) is still interpreted as Java escape character, so we need to escape it using `\\`**. 



# Overloading 
When calling an oveladed method with a null argument, we receive a compilation error: `reference to <METHOD> is ambiguous`. A solution to this problem is to cast the null pointer to the desired type:
```java
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
```java
String MyString = "tests";
String MyRegex = "t\\p+"
boolean matches = myString.matches(myRegex);
```



# Exceptions
The exception mechanism in Java is similar to other languages. The big difference is, however, that in Java, all exception not derived from the `RuntimeException` class are [*checked*](https://en.wikipedia.org/wiki/Exception_handling#Checked_exceptions), which means that their handeling is enforced by the compiler. The following code does not compile, because the `java.langException` class is a checked exception class.
```java
private testMethod{
    ...
    throw new Exception();
}
```  

Therefore, we need to handle the exception using the try cache block or add `throws <EXCEPTION TYPE>` to the method declaration.

When deciding between `try/catch` and `throws`, the rule of thumb is to use the `try/cache` if we can handle the exception and `throws` if we want to leave it for the caller. The problem arises when the method we are in implements an interface that does not have the `throws` declaration we need. Then the only solution is to use `try/cache` with a cache that does not handle the exception, and indicate the problem to the caller differently, e.g, by returning a `null` pointer.


# Genericity
[Oracle official tutorial for Java 8](https://docs.oracle.com/javase/tutorial/java/generics/index.html)

Like many other languages, Java offers generic types with the classical syntax:
```java
class GenericClass<T>{
    ...
};
```

An object is then created as:
```java
GenericClass<OtherClass> gc = new GenericClass<OtherClass>();
```


## Diamond operator
At all places where the type can be inferred, we can use the dianmond operator (`<>`) without specifiyng a type:
```java
GenericClass<OtherClass> gc = new GenericClass<>();
```


## Raw types
[specification](https://docs.oracle.com/javase/specs/jls/se8/html/jls-4.html#jls-4.8)

For the backward compatibility of Java library classes that were converted to generic classes a concept of *raw types* was introduces. However, in addition, this concept brings a lot of very subtle compile errors, which are caused by a nonintentional creation of raw type instead of a specific type.
```java
GenericClass gc = new GenericClass(); // raw type
```

The parameterized type can be assigned to the raw type, but when we do it the other way arround, the code emmits warning and is not runtime safe:
```java
GenericClass<OtherClass> generic = new GenericClass<>();
GenericClass raw = generic // OK

GenericClass raw = new GenericClass();
GenericClass<OtherClass> generic = raw // unsafe
```
Calling the generic methods on raw types has a simmilar consequences.

But the worst property of raw types is that **all generic non-static members of raw types that are not inherited and are also eraw types. Therefore, the genericity is lost even for the completely unrelated type parameters, even specific types are erased to `Object`**. The consequence can be seen on the following example:
```java
class GenericClass<T>{
    public List<String> getListofStrings()
};

GenericClass raw = new GenericClass();
raw.getListofStrings(); // returns List<Object> !!!
```


## Generic method
A generic method in Java is written as:
```java
public <<GENERIC PARAM NAME>> <RESULT TYPE> <METHOD NAME>(<PARAMS>){
    ...
}
```
example:
```java
public static <T> ProcedureParameterValidationResult<T> error(String msg){
    return new ProcedureParameterValidationResult<>(false, msg, null);
}
```

if the generic parameter cannot be infered from the method arguments, we can call the method with explicit generic argument like this:

```java
<<GENERIC PARAM VALUE>><METHOD NAME>(<ARGUMENTS>);
```
example:
```java
ProcedureParameterValidationResult.<String>error("Value cannot be empty.");
```

## Retrieving the type of a generic argument
Because the genericity in Java is resolved at runtime, it is not possible to use the generic parameter as a type. What does it mean? Whille it is possible to use `Myclass.class` it is not possible to use `T.class`. The same applies for the class methods.

The usual solution is to pass the class to the generic method as a method parameter:
```java
void processGeneric(Class<T> classType){
    ...
}
```

## Default generic argument
It is not possible to set the default value of a generic parameter. If we want to achive such behavior, we need to create a new class:
```java
class GeneriClass<T>{
    ...
}

class StringClass extends GenericClass<String>{};

```

## Wildcards
The wildcard symbol (`?` ) represents a concrete but unspecified type. It can be bounded by superclass/interface (`? exctends MyInterface`), or by sublcass (`? super MyClass`). The typical use cases:
- single non-generic method accepting generic types of multiple generic parameter values: 
```java
myMethod(Wrapper<? extends MyInterface> wrapper){
    MyInterface mi = wrapper.get();
    ...
}
```
- method that can process generic class but does not need to work with the generic parameters at all:
```java
getLength(List<?> list){
    return list.size();
}
```

## Difference between `MyClass`, `MyClass<Object>`, and `MyClass<?>`
```java
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




# Collections
## Set
From java 9, sets can be simply initialized as:
```java
Set<int> nums = Set.of(1,2,3);
```
Note that this method returns an immutable set. In the earlier versions of Java, the `Collections.singleton` method can be used. 



# Enums
Java enumerations are declared using the `enum` keyword:
```java
public enum Semaphore{
    RED,
    ORAGNGE,
    GREEN
}
```

## Iterating over enum items
we can iterate over enum items using the `values` method:
```java
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
```java
Semaphore sem = Semaphore.valueOf("RED");
```
Note that the string has to match the enum value exactly, including the case. Extra whitespaces are not permited.

There is also a generic static `valueOf` method in the `Enum` class, which we can use for generic enums:
```java
Class<E> enumClass;
E genEnumInst = Enum.valueOf(enumClass, "RED");
```
Note that here `E` has to be a properly typed enum (`Enum<E>`), not the raw enum (`Enum`).



# Lambda expressions
[wiki](https://en.wikipedia.org/wiki/Anonymous_function#Java)

An important thing about lambda expressions in Java is that we can only use them to create types satisfying some functional interface. This means that:
- They can be used only in a context where a functional interface is expected
- They need to be convertible to that interface. 

The example that demonstrate this behavior is bellow. Usually, we use some standard interface, but here we create a new one for clarity:

```java
interface OurFunctionalInterface(){
    int operation(int a)
}

...

public void process(int num, OurFunctionalInterface op){
    ...
}
```

With the above interface and method that uses it, we can call
```java
process(0, a -> a + 5)
```
Which is an equivalent of writing

```java
OurFunctionalInterface addFive = a -> a + 5;
process(0, addFive);
```

## Syntax
A full syntax for lambda expressions in Java is:
```java
(<PARAMS>) -> {
    <EXPRESSIONS>
}
```

If there is only one expression, we can ommit the code block:
```java
(<PARAMS>) -> <EXPRESSION>
```
And also, we can ommit the `return` statement from that expression. The two lambda epressions below are equivalent:
```java
(a, b) -> {return a + b;}
(a, b) -> a + b
```

If there is only one parameter, we can ommit the parantheses:
```java
<PARAM> -> <EXPRESSION>
```

By default, the parameter types are infered from the functional interface. If we need more specific parameters for our function, we can specify the parameter type, we have to specify all of them however:
```java
(a, b) -> a + b // valid
(int a, int b) -> a + b // valid
(int a, b) -> a + b // invalid
```
Also, it is necesary to use the parantheses, if we use the param type.


## Method references
We can also create lambda functions from existing mehods (if they satisfy the desired interface) using a mechanism called *method reference*. For example, we can use the `Integer.sum(int a, int b)` method in conext where the `IntBinaryOperator` interface is required. Instead of 
```java
IntBinaryOperator op = (a, b) -> a + b; // new lambda body
``` 
we can write:
```java
IntBinaryOperator op = Integer::sum; // lambda from existing function
```


## Exceptions in lambda expressions
Beware that the checked exceptions thrown inside lambda expressions has to be caught inside the lambda expression. The following code does not compile:
```java
try{
    process(0, a -> a.methodThatThrows())
catch(exception e){
    ...
}
```
Instead, we have to write:
```java
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
```java
for(<TYPE> <VARNAME>: <ITERABLE>){
    ...
}
```
Here, the `<ITERABLE>` can be either a Java `Iterable`, or an array. 


## Enumerated iteration
There is no `enumerate` equivalent in Java. [One can use a stream API range method](https://stackoverflow.com/questions/66662506/how-to-enumerate-add-indices-to-a-list-like-collection-in-java), however, it is less readable than standard for loop because the code execuded in loop has to be in a separate function.


## Iterating using an iterator
The easiest way how to iterate if we have a given iterator is to use its `forEachRemaining` method. It takes a `Consumer` object as an argument, iterates using the iterator, and calls `Consumer.accept` method on each iteration. The example below uses a lambda function that satisfies the consumer interface:

```java
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
```java
Arrays.stream(<ARRAY>);
```

## Creating stream from iterator
The easiest way is to first create an `Iterable` from the iterator and then use the `StreamSupport.stream` method:
```java
Iterable<JsonNode> iterable = () -> iterator;
var stream = StreamSupport.stream(iterable.spliterator(), false);
```

## Filtering
A lambda function can be supplied as a filter:
```java
stream.filter(number -> number > 5)
```
returns a stream with numbers greater then five.


## Transformation
We can transform the stream with the `map` function:
```java
transformed = stream.map(object -> doSomething(object))
```


## Materialize stream
We can materrialize stream with the collect metod:
```java
List<String> result = stringStream.collect(Collectors.toList());
```
Which can be, in case of `List` shorten to:
```java
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
```java
Object o = (Object) new MyClass();
```

we can do
```java
Object o = new MyClass();
```

Typically, we need to use the explicit cast for *downcasting*:
```java
Object o = ...;
MyClass c = (MyClass) o; // when we are sure that o is an instance of MyClass...
```

Downcasting to an incorrect type leads to a runtime `ClassCastException`.

Casting to an unrelated type is not allowed by the compiler.

## Casting generic types
Casting with generic types is notoriously dangerous due to type erasure. The real types of generic arguments are not known at runtime, therefore, an incorrect cast does not raise an error:
```java
Object o = new Object();
String s = (String) o; // ClassCatsException

List<Object> lo = new ArrayList<>();
List<String> ls = (List<String>) lo; // OK at runtime, therefore, it emmits warning at compile time.

```


## Casting case expression
Often, when we work with an interface, we have to treat each implementation differently. The best way to handle that is to use the polymorphism, i.e., add a dedicated method for treating the object to the interface and handle the differences in each implementation. However, sometimes, we cannot modify the interface as it comes from the outside of our codebase, or we do not want to put the code to the interface because it belongs to a completely different part of the application (e.g., GUI vs database connection). A typicall solution for this is to use branching on instanceof and a consecutive cast:

```java
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
```java
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

```java
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
```java
var it = new Random().ints(0, map.nodesFromAllGraphs.size()).iterator();\
int a = it.nextInt();
```


# Reflection
Reflection is a toolset for working with Java types. Its methods can be accessed from a class object associated with all classes. 

The class object represents the type and it can be accessed either by `MyClass.class` or by calling the `MyClass.getClass` method. The type of the class object is Class<>


## Test if a class is a superclass or interface of another class
It can be tested simply as:
```java
ClassA.isAssignableFrom(ClassB)
```

## Get field by name
```java
Field field = MyClass().getDeclaredField("fieldName");
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
```java
var result = statement.executeQuery();
while(result.next()){
   var str = result.getString("column_name"));
   ...
}
```



# Jackson
[Documentation](https://github.com/FasterXML/jackson-docs)

Jackson is a (de)serialization library primarily focused to the JSON format. It supports annotations for automatic serialization and deserialization of Java objects.

## Ignore specific fields
If you want to ignore specific fields during serialization or deserialization, you can use the [`@JsonIgnoreProperties` annotation](https://fasterxml.github.io/jackson-annotations/javadoc/2.6/com/fasterxml/jackson/annotation/JsonIgnoreProperties.html). Use it as a class or type annotation. Example:

```java
@JsonIgnoreProperties({ "par1", "par2" })
public class ConfigModel {
    // "par1" and "par2" will be ignored 
}
```

This annotation can also prevent the "Unrecognized field" error during deserialization, as the ignored fields does not have to be present as Java class members.


## Represent a class by a single member
If we want the java class to be represented by a single value in the **serialized** file, we can achieve that by adding the [`@JsonValue`](https://fasterxml.github.io/jackson-annotations/javadoc/2.8/com/fasterxml/jackson/annotation/JsonValue.html) annotation above the member or method that should represent the class. Note, however, that this only works for simple values, because the member serializers are not called, the members is serialized as a simple value instead. **If you want to represent a class by a single but complex member, use a custom serializer instead**. 

An equivalent annotation for **deserialization** is the `@JsonCreator` annotation which should be placed above a constructor or factory method.


## Deserialization
The standard usage is:
```java
ObjectMapper mapper = new ObjectMapper();
// ... configure mapper

File file = new File(<PATH TO FILE>);

Instance instance = mapper.readValue(file, Instance.class);
```

By default, new objects are created for all members in the object hierarchy that are either present in the serialized file.

New objects are created using the setter, if exists, otherwise, the costructor is called.


### Multiple Setters
If there are multiple setters, we need to specify the one that should be used for deserialization by marking it with the `@JsonSetter` annotation.


### Update existing instance
You can update an existing instance using the [`readerForUpdating`](https://fasterxml.github.io/jackson-databind/javadoc/2.9/com/fasterxml/jackson/databind/ObjectMapper.html#readerForUpdating-java.lang.Object-) method:
```java
ObjectReader or = mapper.readerForUpdating(instance); // special reader
or.readValue(file) // we can use the method we already know on the object reader
```

Note that **by default, the update is shalow**. Only the `instance` object itself is updated, but its members are brand new objects. If you want to keep all objects from an existing object hierarchy, you need to use the `@JsonMerge` annotation.
You should put this annotation above any member of the root object you want to update instead of replacing it. **The `@JsonUpgrade` annotation is recursive**: the members of the member annotated with `@JsonUpgrade` are updated as well and so on.


#### Updating polymorphic types
For updating polymorpic type, the rule is that the exact type has to match. Also, you need jackson-databind version 2.14.0 or greater.


### Read just part of the file
For reading just part of the file, use the `at` selector taht is available in the `ObjectReader` class. We need to first obtain the reader from a mapper, and then use the selector:
```java
ObjectReader reader = mapper.readerFor(Instance.class);
Instance instance = reader.at("data").readValue(file)
```
Note that if the path parameter of the `at` method is incorrect, the method throws an exception with the message: "no content to map due to end-of-input".

### Check that some node is present
To check for presence of a node, we should use the `JsonPointer` class:
```java
JsonPointer jsonPointer = Json.createPointer("<JSON PATH>");
boolean found = jsonPointer.containsValue(jsonStructure);
```

We can also use the `JsonPointer` in the `at` method:
```java
JsonPointer jsonPointer = Json.createPointer("<JSON PATH>");
boolean found = jsonPointer.containsValue(jsonStructure);

if(found){
    Instance instance = reader.at(jsonPointer).readValue(file, Instance.class)
}
```

### Interface or abstract class
When serializing interface or abstract class, it is important to include the implementation type into serialization. Otherwise, the deserialization fails, because it cannot determine the concreate type. To serialize the concrete type, we can use the [`@JsonRypeInfo`](https://fasterxml.github.io/jackson-annotations/javadoc/2.4/com/fasterxml/jackson/annotation/JsonTypeInfo.html) and `JsonSubTypes` annotations:

```java
@JsonTypeInfo(
	use = JsonTypeInfo.Id.CLASS, // what value should we store, here the class name
	include = JsonTypeInfo.As.PROPERTY, // serialize as a property of the JSON object
	property = "type" // property name
)
public interface Interface  {
    ...
}

```

Te above code will work, the full class name will be serialized in the file, however. If we want to use a shorter syntax, i.e., some codename for the class, we need to specify a mapping between this codename and the conreate class:

```java
@JsonTypeInfo(
	use = JsonTypeInfo.Id.NAME, // what value should we store, here a custom name
	include = JsonTypeInfo.As.PROPERTY, // serialize as a property of the JSON object
	property = "type" // property name
)
@JsonSubTypes({
    @JsonSubTypes.Type(value = Implementation.class, name = "Implementation name")
})
public interface Interface  {
    ...
}
```

#### Custom deserializer
An alternative to `@JsonTypeInfo` is to use a custom deserializer: 
https://stackoverflow.com/questions/44122782/jackson-deserialize-based-on-type

### Custom deserializer
If our architecture is so complex or specific that none of the Jackson annotations can help us to achieve the desired behavior, we can use a custom deserializer. For that we need to:
1. Implement a custom deserializer by extending the `JsonDeserializer` class
1. Registering the deserializer in the `ObjectMapper`

#### Creating a custom deserializer for class
The only method we need to implement is the:
```java
T deserialize(JsonParser jsonParser, DeserializationContext deserializationContext)
```
where T is the type of the object we are deserializing. 

To get the Jaksons representation of the JSON tree, we can call:
```java
JsonNode node = jsonParser.getCodec().readTree(jsonParser);
```

We can get all the fields by calling using the `node.fields()` method. For arrays, there is a method `node.elements()`;

#### Registering the deserializer
```java
ObjectMapper mapper = new ObjectMapper();
SimpleModule module = new SimpleModule();
module.addDeserializer(OurClass.class, new OurClassDeserializer());
mapper.registerModule(module);
```

#### Custom deserializer with generic types
When we need a custom deserializer for a generic class, we need to use a wildcard to cover multiple values of generic argument:
```java
public class OurDeserializer extends JsonDeserializer<OurGenericClass<?>>{
    ...
}
```

If we also need to get the generic argument type from JSON, we need to implement the `ContextualDeserializer` interface. This is discribed in a [SO answer](https://stackoverflow.com/questions/36159677/how-to-create-a-custom-deserializer-in-jackson-for-a-generic-type).


#### Custom deserializer with inheritance
We can have a common deserializer for both parent and child class, or multiple child classes. However, it is necessary to 
- make the deserializer generic and
- register the deserializer for all classes, not just for the parent.

Example:
```java
public class PolymorphicDeserializer<T extends Parent> extends JsonDeserializer<T>

    @Override
    public T deserialize(JsonParser p, DeserializationContext ctxt) throws IOException, JsonProcessingException {
        ...
    }
}

module.addDeserializer(ChildA.class, new PolymorphicDeserializer<>());
module.addDeserializer(ChildB.class, new ProcedureParameterDeserializer<>());

```



## Serialization
Standard serialization:
```java
// compressed
mapper.writer().writeValue(file, object);

//  or with indents, etc.
mapper.writerWithDefaultPrettyPrinter().writeValue(file, object); 
```

By default, new objects are created for all members in the object hierarchy that are either:
- public value mebers (fields)
- public getters: public methods with name `get<NAME>`, where `<NAME>` is a name of some value member

Other getters with different name are called only if there is an annotation above them. A special annotation dedicated for this is `@JsonProperty`.


### Appending to an existing file
To append to an existing file, we need to create an output stream in the append mode and then use it in jackson:
```java
ObjectMapper mapper = ...
JsonGenerator generator = mapper.getFactory().createGenerator(new FileOutputStream(new File(<FILENAME>), true));
mapper.writeValue(generator, output);
```

### Complex member filters
Insted of adding annotations to each member we want to ignore, we can also apply some more compex filters, to do that, we need to:
1. add a `@JsonFilter("<FILTER NAME>")` annotation to all classes for which we want to use the filter
2. create the filter
3. pass a set of all filters we want to use to the writer we are using for serialization

The example below keeps only members inherited from `MyClass`:
```java
// object on which we apply the filter
@JsonFilter("myFilter")
class targetClass{
    ...
}

// filter
PropertyFilter filter = new SimpleBeanPropertyFilter() {
    @Override
    public void serializeAsField(
        Object pojo, JsonGenerator jgen, SerializerProvider provider, PropertyWriter writer
    ) throws Exception {
        if(writer.getType().isTypeOrSubTypeOf(MyClass.class)){
            writer.serializeAsField(pojo, jgen, provider);
        }
    }

};

FilterProvider filters = new SimpleFilterProvider().addFilter("myFilter", filter);

// use a writer created with filters
mapper.writer(filters).writeValue(generator, output);
...
```

### Flatting the hierarchy
When we desire to simplify the object hierarchy, we can use the [`@JsonUnwrapped`](https://fasterxml.github.io/jackson-annotations/javadoc/2.4/com/fasterxml/jackson/annotation/JsonUnwrapped.html) annotation above a member of a class. With this annotation, the annotated member object will be skipped while all its members will be serialized into its parent.

### Custom serializer
If the serialization requirements are too complex to be expressed using Jackson annotations, we can use a custom serialzier:
```java
public class MyCustomSerializer extends JsonSerializer<MyClass> {
	@Override
	public void serialize(MyClass myClass, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
		...
	}
}
```
Analogously to custom deserializer, we can register custom serializer either in the object mapper:
```java
SimpleModule module = new SimpleModule();
module.addSerializer(MyClass.class, new MyCustomSerializer());
mapper.registerModule(module);
```
or by annotating the class:
```java
@JsonSerialize(using = MyCustomSerializer.class)
public class MyClass{
    ...
}
```

You can call standard serializers from custom serializers using the `SerializerProvider` and `JsonGenerator` instances supplied as a parameters of the `serialize` method. For example the standard serialized value of som inner/member object class can be obtained using:
```java
serializerProvider.defaultSerializeValue(myInnerInstance, jsonGenerator);
``` 

## Annotations

### Multiple objects 
If there are multiple objects involved in the (de)serializetion, we can use the `@JsonCreator` and `@JsonProperty` annotations to split the work:
```java
@JsonCreator
public ConfigModel(
    @JsonProperty("first") ClassA instanceA,
    @JsonProperty("second") ClassB instanceB
) {
    ...
}
```
in the above examples, the `first` and `second` are keys mapping the objects in the serialized file from which `instanceA` and `instanceB` should be created.





