[Documentation](https://github.com/FasterXML/jackson-docs)

Jackson is a (de)serialization library primarily focused to the JSON format. It supports annotations for automatic serialization and deserialization of Java objects.

Jackson have two basic modes:
- **Object mapper mode**, JSON is (de)serialized from/to Java objects
- **Parser/Generator mode**, JSON is parsed/generated one token at a time

To make it even more complicated, the Object mapper mode can be used in two ways:
- **Data binding**, where the JSON is (de)serialized from/to Java objects that we provide for this purpose
- **Tree model**, where the JSON is (de)serialized from/to a tree structure of Jackson objects


Tutorials:
- [Official databind tutorial](https://github.com/FasterXML/jackson-databind/)
- [Jenkov tutorial](https://jenkov.com/tutorials/java-json/index.html) (old but gold)



# Object mapper with data binding

The basic usage is:
```Java
public class MyClass{
    public String par1;
    public int par2;
    ...
}

ObjectMapper mapper = new ObjectMapper();

// Deserialization
MyClass myClass = mapper.readValue(new File("path/to/file.json"), MyClass.class);

// Serialization
MyClass myObject = new MyClass();
...
mapper.writeValue(new File("path/to/file.json"), myObject);
```

By defualt, Jackson:
- (de)serialize from/to public fields or public setters/getters with the same name as the JSON property
- all JSON properties are deserialized and all public fields or public getters are serialized
- if there is no matching field or setter to a JSON property, the deserialization fails

However, we can customize the (de)serialization process using many annotations. This way, we can ignore some fields or JSON properties, use constructors or factory methods for deserialization, (de)serialize from/to arrays and objects, and many other things.



## Ignore specific fields
If you want to ignore specific fields during serialization or deserialization, you can use the [`@JsonIgnoreProperties` annotation](https://fasterxml.github.io/jackson-annotations/javadoc/2.6/com/fasterxml/jackson/annotation/JsonIgnoreProperties.html). Use it as a class or type annotation. Example:

```Java
@JsonIgnoreProperties({ "par1", "par2" })
public class ConfigModel {
    // "par1" and "par2" will be ignored 
}
```

This annotation can also prevent the "Unrecognized field" error during deserialization, as the ignored fields does not have to be present as Java class members.

we can achieve the same by field annotations, specifically the [`@JsonIgnore`](https://fasterxml.github.io/jackson-annotations/javadoc/2.6/com/fasterxml/jackson/annotation/JsonIgnore.html) annotation. Example:
```Java
public class ConfigModel {
    @JsonIgnore
    public String par1;
    @JsonIgnore
    public int par2;
}
```


## Include only specific fields
If the fields to be (de)serialized are only a minority of all fields, we can use a reverse approach: the `@JsonIncludeProperties` annotation. For example:
```Java
@JsonIncludeProperties({ "par1", "par2" })
public class ConfigModel {
    // only "par1" and "par2" will be (de)serialized
}
```

Note that unlike for ignoring, there is no field annotation for including only specific fields. The `@JsonInclude` annotation serves a different purpose.


## Represent a class by a single member
If we want the java class to be represented by a single value in the **serialized** file, we can achieve that by adding the [`@JsonValue`](https://fasterxml.github.io/jackson-annotations/javadoc/2.8/com/fasterxml/jackson/annotation/JsonValue.html) annotation above the member or method that should represent the class. Note, however, that this only works for simple values, because the member serializers are not called, the members is serialized as a simple value instead. **If you want to represent a class by a single but complex member, use a custom serializer instead**. 

An equivalent annotation for **deserialization** is the `@JsonCreator` annotation which should be placed above a constructor or factory method.


## Deserialization
The standard usage is:
```Java
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
```Java
ObjectReader or = mapper.readerForUpdating(instance); // special reader
or.readValue(file) // we can use the method we already know on the object reader
```

Note that **by default, the update is shalow**. Only the `instance` object itself is updated, but its members are brand new objects. If you want to keep all objects from an existing object hierarchy, you need to use the `@JsonMerge` annotation.
You should put this annotation above any member of the root object you want to update instead of replacing it. **The `@JsonUpgrade` annotation is recursive**: the members of the member annotated with `@JsonUpgrade` are updated as well and so on.


#### Updating polymorphic types
For updating polymorpic type, the rule is that the exact type has to match. Also, you need jackson-databind version 2.14.0 or greater.


### Read just part of the file
For reading just part of the file, use the `at` selector taht is available in the `ObjectReader` class. We need to first obtain the reader from a mapper, and then use the selector:
```Java
ObjectReader reader = mapper.readerFor(Instance.class);
Instance instance = reader.at("data").readValue(file)
```
Note that if the path parameter of the `at` method is incorrect, the method throws an exception with the message: "no content to map due to end-of-input".

### Check that some node is present
To check for presence of a node, we should use the `JsonPointer` class:
```Java
JsonPointer jsonPointer = Json.createPointer("<JSON PATH>");
boolean found = jsonPointer.containsValue(jsonStructure);
```

We can also use the `JsonPointer` in the `at` method:
```Java
JsonPointer jsonPointer = Json.createPointer("<JSON PATH>");
boolean found = jsonPointer.containsValue(jsonStructure);

if(found){
    Instance instance = reader.at(jsonPointer).readValue(file, Instance.class)
}
```

### Interface or abstract class
When serializing interface or abstract class, it is important to include the implementation type into serialization. Otherwise, the deserialization fails, because it cannot determine the concreate type. To serialize the concrete type, we can use the [`@JsonRypeInfo`](https://fasterxml.github.io/jackson-annotations/javadoc/2.4/com/fasterxml/jackson/annotation/JsonTypeInfo.html) and `JsonSubTypes` annotations:

```Java
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

```Java
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
```Java
T deserialize(JsonParser jsonParser, DeserializationContext deserializationContext)
```
where T is the type of the object we are deserializing. 

To get the Jaksons representation of the JSON tree, we can call:
```Java
JsonNode node = jsonParser.getCodec().readTree(jsonParser);
```

We can get all the fields by calling using the `node.fields()` method. For arrays, there is a method `node.elements()`;

#### Registering the deserializer
```Java
ObjectMapper mapper = new ObjectMapper();
SimpleModule module = new SimpleModule();
module.addDeserializer(OurClass.class, new OurClassDeserializer());
mapper.registerModule(module);
```

#### Custom deserializer with generic types
When we need a custom deserializer for a generic class, we need to use a wildcard to cover multiple values of generic argument:
```Java
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
```Java
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
```Java
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
```Java
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
```Java
public class MyCustomSerializer extends JsonSerializer<MyClass> {
	@Override
	public void serialize(MyClass myClass, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
		...
	}
}
```
Analogously to custom deserializer, we can register custom serializer either in the object mapper:
```Java
SimpleModule module = new SimpleModule();
module.addSerializer(MyClass.class, new MyCustomSerializer());
mapper.registerModule(module);
```
or by annotating the class:
```Java
@JsonSerialize(using = MyCustomSerializer.class)
public class MyClass{
    ...
}
```

You can call standard serializers from custom serializers using the `SerializerProvider` and `JsonGenerator` instances supplied as a parameters of the `serialize` method. For example the standard serialized value of som inner/member object class can be obtained using:
```Java
serializerProvider.defaultSerializeValue(myInnerInstance, jsonGenerator);
``` 

## Annotations

### Multiple objects 
If there are multiple objects involved in the (de)serializetion, we can use the `@JsonCreator` and `@JsonProperty` annotations to split the work:
```Java
@JsonCreator
public ConfigModel(
    @JsonProperty("first") ClassA instanceA,
    @JsonProperty("second") ClassB instanceB
) {
    ...
}
```
in the above examples, the `first` and `second` are keys mapping the objects in the serialized file from which `instanceA` and `instanceB` should be created.



# Object mapper with tree model
[Jenkov tutorial on JsonNode](https://jenkov.com/tutorials/java-json/jackson-jsonnode.html)

To get the tree model, we can use the `readTree` method of the `ObjectMapper` class:
```Java
ObjectMapper mapper = new ObjectMapper();
JsonNode node = mapper.readTree(new File("path/to/file.json"));
```

## Iterating over JSON array
First we need to convert the node representing the array to the `ArrayNode` class. Then we can iterate over the array using for each or the `get` method:
```Java
ArrayNode array = (ArrayNode) node.get("array");
for(JsonNode element: array){
    ...
}

// or
for(int i = 0; i < array.size(); i++){
    JsonNode element = array.get(i);
    ...
}
```

## Iterating over JSON object
First we need to convert the node representing the object to the `ObjectNode` class. Then we can iterate over the object using the `fieldNames` method:
```Java
ObjectNode object = (ObjectNode) node.get("object");
for(String fieldName: object.fieldNames()){
    JsonNode value = object.get(fieldName);
    ...
}
```



# CSV with Jackson
[documentation](https://github.com/FasterXML/jackson-dataformats-text/tree/2.17/csv)

To read a CSV file with Jackson, we need to use the `CsvMapper` class. The basic usage is:
```Java
CsvMapper mapper = new CsvMapper(); 

// iterator construction
MappingIterator<<row type>> it = mapper....readValues(new File("path/to/file.csv");

// iterator usage
while(it.hasNext()){
    <row type> row = it.next();
    ...
}
```
Here the `<row type` is the target type that should represent a single row. Depending on it, there will be different code in place of `mapper...`. For example, to get a list of strings for each row, we can use:
```Java
MappingIterator<List<String>> it = mapper.readerForListOf(String.class)...
```

## Use the header
If the CSV file has a header, we can use it to load each row into a map of key-value pairs:
```Java
CsvSchema schema = CsvSchema.emptySchema().withHeader();
MappingIterator<Map<String, String>> it = mapper.readerForMapOf(String.class).with(schema).readValues(new File("path/to/file.csv"));
```