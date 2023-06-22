# Jackson
## Usefull Annotations
- [`@JsonIncludeProperties`](http://fasterxml.github.io/jackson-annotations/javadoc/2.12/com/fasterxml/jackson/annotation/JsonIncludeProperties.html): Ignore all properties except listed
- `@JsonProperty("my_name")`: Custom name of the JSON key
- `@JsonIgnore`: Ignore the json property below

## Wrapping the Obejct in Another JSON Object
To do that, use these annotations above the class. 
```java
@JsonTypeName(value = "action")
@JsonTypeInfo(include=As.WRAPPER_OBJECT, use=Id.NAME)
```
If you do not care about the name, you can skip the `@JsonTypeName` annotation.

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTQ1MDY3MTE2MiwtMTM5NTAxOTY4MCwtMT
Q5Mzk5MzQ2LDczMDk5ODExNl19
-->