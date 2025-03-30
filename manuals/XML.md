XML is a text format for storing hierarchical data. It was the most popular format for hierarchical data before JSON became popular. 

# Namespaces
[wiki](https://en.wikipedia.org/wiki/XML_namespace)

Namespaces are used to avoid element name conflicts in XML documents. They allow you to use the same element name in the same document without causing ambiguity.

Namespaces are declared using the `xmlns:<prefix>` attribute in the root element of the XML document:
```xml
<root xmlns:ns="http://example.com/ns">
    <ns:element>Value</ns:element>
</root>
```

There can be multiple namespaces in a document, each namespace have a different prefix.

Typically, the document also has a *default namespace* (without a prefix) that applies to all elements in the document that do not have a prefix.

```xml
<root xmlns="http://example.com/ns">
    <element>Value</element>
</root>
```

Note that handling of namespace prefixes differ between the types of XML processors:

- **DOM**: use the namespace prefixes as declared in the `xmlns` attributes.
- **XPath**: ignores the prefixes declared in `xmlns`. Instead, we have to provide the binding of prefixes to namespase URIs, typically as a dictionary or a map. Check the [XPath section](#namespaces-in-xpath) for more details.

Note that **usage of namespaces is optional**, you can use XML without namespaces. Also note, that to determine the namespace of an element, it is not enough to look at the element name, because the default namespace can be used. In other words, an element without a prefix can be either in the default namespace or in no namespace at all.



# XPath
[wiki](https://en.wikipedia.org/wiki/XPath)

XPath (XML Path Language) is a language for navigating XML documents. It allows you to select nodes in an XML document using a path expression.

Each path consists of a series of steps separated by slashes (`/`). Each step has three parts:

- **axis**: specifies the direction to navigate in the XML document, e.g. child, parent,...
- **node test**: specifies the name of the node to select, e.g. `book`, `author`, `title`.
- **predicate**: specifies a condition to filter the nodes, e.g.: selecting only nodes with a specific attribute or value.

## Axis specifiers
Only the most common axis specifiers are listed here.

- `<name>`, `child::<name>`: selects child nodes with the specified name.
- `/<name>`, `descendant::<name>`: selects descendant nodes with the specified name.
- `..`, `parent`: selects the parent node of the current node.


## Node tests

- `*`: all nodes
- `<name>`: selects nodes with the specified name.
- `@<name>`: selects attributes with the specified name.
- `*[<number>]`: selects the node at the specified index (1-based).
- `*[last()]`: selects the last node in the current context.


## Namespaces in XPath
An unintuitive aspect of XPath is that it **does not read the namespaces prefixes from the XML document**. When using XPath in documents with namespaces we have to use the facilities of the XPath processor implementation to bind the prefixes to the namespaces. This includes the default namespace, which does not have a prefix in the XML document, but must be bound to a prefix when using XPath.

The binding method depends on the implementation, it is usually done by using a dictionary or a map. Examples of for the most common Programming languages can be found in a [SO post](https://stackoverflow.com/questions/40796231/how-does-xpath-deal-with-xml-namespaces).

It may seem strange that XPath ignores the prefixes declared in `xmlns`, yet the matching of namespace URIs to elements is done correctly. This has the following reason:

- Typically, the XML document is parsed by a DOM parser, which creates a tree of elements. As stated above, the DOM parser uses the prefixes declared in `xmlns`.
- Xpath then queries the already parsed document. In this parsed document, each element has the namespace URI already assigned by the DOM parser. Therefore, with the XPath, we can use a completely different prefix than the one declared in the XML document.


