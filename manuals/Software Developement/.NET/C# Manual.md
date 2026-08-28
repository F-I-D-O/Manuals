# Introduction
C# is the main langiage for .NET development. Principially, it is most similar to Java:

- it is managed, i.e., the runtime is provided by the .NET framework
- it is object-oriented
- memory management is done by the runtime

However, there are also differences:

- top level statements are allowed, similarly to Python, and can be used as the entry point of the program
- there are a lot of available language features, similarly to C++


# References
[Nullable Reference Types](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/nullable-reference-types)

Same as in Java, values are hold by reference by defualt. So in `string a = "hello";` is a reference to the string `"hello"`. 

However, in C#, the static analysis prevents some `NullPointerException` by emiting warnings if the reference is not initialized - the referenc is non-nullable by default, like in C++.The following statements have similar meaning:

- **C#**: `string a = "hello";`
- **C++**: `std::string& a = new std::string("hello");`
- **Java and Python**: not possible

To create a nullable reference, we can use the `?` operator. The following statements have similar meaning:

- **C#**: `string? a = null;`
- **C++**: `std::string* a = nullptr;`
- **Java**: `String a = null;`
- **Python**: `a = None`



# Operators

## Member access operators
[Official documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators)

There are the following operators for accessing members:

- `.`: member access
- `[]`: array or indexeraccess
- `.?`: nullable member access
- `?[]`: nullable array or indexer access: does not throw if the left operand is `null`, returns `null` instead
- `()`: method or delegate invocation
- `[^]`: array or indexer access, but from the end of the array/indexer
- `[..]`: range access - returns a range of elements from the array/indexer


## Nullable access operators
[Official documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/member-access-operators#null-conditional-operators--and-)

The nullable access operators (`?.`, `?[]`) are similar to the non-nullable operators (`.`, `[]`), but they return `null` instead of throwing an exception if the left operand is `null`.

Moreover, since C# 14, these operators can be used for assignments as well, in which case the meaning is:

```csharp
person?.FirstName = "John";

// is equivalent to
if (person != null)
{
    person.FirstName = "John";
}
```


## Null-coalescing operators
[Official documentation](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/null-coalescing-operator)

There are two operators that can reduce the `if (x is null)` pattern in the code:

- `??`: returns the left operand if it is not null, otherwise the right operand
- `??=`: assigns the right operand to the left operand if the left operand is null



# Properties
[Official documentation](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties)

Properties are basically fields + getters and setters. The basic syntax with plain getter and setter is:

```csharp
public <type> <property name> { get; set; }
```

Same as fields, we can add the **iniitalizer**:

```csharp
public <type> <property name> { get; set; } = <initial value>;
```

We can set the **access modifier** both on the property and on the getter and setter:

- `public <type> <property name> { get; set; }`: both getter and setter are public
- `public <type> <property name> { get; private set; }`: getter is public, setter is private
- `private <type> <property name> { get; set; }`: both getter and setter are private


## Getter and Setter customization
if we want to customize the getter and setter, we use two things:

- `=>` operator after `get` or `set` to start the body of the getter or setter
- the `field` keyword, if we need to access the data member this property is associated with
- the `value` keyword, if we need to access the value passed to the setter
- `{` and `}` if we need more than one statement in the body

Full example:

```csharp
public string MyProperty { 
    get => field.ToUpper();
    set => {
        string newValue = value.ToLower();
        field = newValue.Trim();
    }
}
```


## Expression-bodied properties
[Official documentation](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties#expression-body-definitions)

If the property should have only a getter, we can use the `expression-bodied property` syntax:

```csharp
public <type> <property name> => <expression>;

// full body equivalent
public <type> <property name> { get => <expression>; }
```

Example:
```csharp
public string MyProperty => "Hello";
```

The expression may also refer to other properties:

```csharp
public string MyProperty => MyOtherProperty.ToUpper();
```


