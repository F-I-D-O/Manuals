# JSON

- [Wikipedia](https://en.wikipedia.org/wiki/JSON)
- [Official website](https://www.json.org/json-en.html)



# JSON Schema

- [Wikipedia](https://en.wikipedia.org/wiki/JSON_Schema)
- [Official website](https://json-schema.org/)

JSON Schema is a JSON-based format for defining the structure of JSON data, similar to XML Schema. It can be used to validate JSON data.

Typically, each property in the JSON file has a corresponding object in the JSON Schema. That object has the following properties:

- [`type`](https://json-schema.org/understanding-json-schema/reference/type): the type of the property
- `title`: the short description of the property
- `description`: the long description of the property
- `properties`: an object defining the child properties of the property, if the property is an object
- `items`: an object defining the items of the property, if the property is an array


## Root object of the JSON Schema

The root object of the JSON Schema describes the root object of the JSON file. Additionally, it usually has the following properties:

- [`$schema`](https://json-schema.org/understanding-json-schema/reference/schema): the URI of the JSON Schema draft that is used. Not required, but recommended.
- [`$id`](https://json-schema.org/understanding-json-schema/reference/id): the unique identifier of the JSON Schema. Again, not required, but recommended.


## Referencing other JSON Schemas
When the complexity of the JSON Schema grows, and we may need to use the same child objects in multiple places, it may be helpful to split the JSON Schema into multiple files, and reference them from the root object. To do that, we can use the [`$ref`](https://json-schema.org/understanding-json-schema/reference/json_schema.html#id) property. Example:

- `child_schema.json`:
    ```json
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/child_schema.json",
        "title": "Child Schema",
        "description": "A schema for a child object",
        "properties": {
            "name": {
                "type": "string"
            }
        }
    }
    ```
- `root_schema.json`:
    ```json
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/root_schema.json",
        "title": "Root Schema",
        "description": "A schema for a root object",
        "properties": {
            "child": {
                "description": "A child object",
                "$ref": "https://example.com/child_schema.json"
            }
        }
    }
    ```

## Conditions
[official documentation](https://json-schema.org/understanding-json-schema/reference/conditionals#ifthenelse)

We can use programming-like branching objects to define conditional properties. The syntax is:

```json
{
    "if": {
        <object defining the condition>
    },
    "then": {
        <schema if the condition is true>
    },
    "else": {
        <schema if the condition is false>
    }
}
```

Example:
```json
{
    "if": {
        "properties": {
        "country": { "const": "United States of America" }
        }
    },
    "then": {
        "properties": {
        "postal_code": { "pattern": "[0-9]{5}(-[0-9]{4})?" }
        }
    },
    "else": {
        "properties": {
        "postal_code": { "pattern": "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]" }
        }
    }
}
```
