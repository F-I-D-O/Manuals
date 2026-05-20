# Flowcharts
[Wiki](https://en.wikipedia.org/wiki/Flowchart)

Flowcharts are a type of diagram that is used to represent flow of control. The specific usages may be, for example, 

- algorithms
- processes
- data flow
- decision making

Flowchart diagram components are:

- **Flowline**, an arrow, connects the components of the flowchart in the direction of the flow of control.
- **Terminal**, rounded rectangle (stadium), used to represent the start or end of the flowchart
- **Process**, rectangle, used to represent a process
- **Decision**, diamond, used to represent a decision



# Diagrams with D2

- [Homepage](https://d2lang.com/)
- [GitHub](https://github.com/terrastruct/d2)
- [Tutorial](https://d2lang.com/tour/)

D2 is a system that can usea D2 declarative format as input and export it to a several formats, including `png`, `svg`, `pdf`, `html`, and `md`.

## Installation
[Official documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md)

### Windows
[Official documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md#windows)

The Windows `msi` installer can be downloaded from the [Releases page](https://github.com/terrastruct/d2/releases). Note that the installer has no configuration options, so it may appear as faulty, but it is working.


## CLI
The basic usage of d2 is to run it in command line: `d2 <input file>`. This command will compile the file to svg. Most useful options are:

- `--watch`, `-w`: This will automatically start a server where the generated `svg` file is displayed. It will also watch the file for changes and reload the web page with the new diagram.
- `--scale <float>`: Scale the output. Default is `-1`, which means fit the whole `svg` to the screen.
- `--layout <layout engine>`: Layout engine to use. Options are:
    - `dagre`: Directed Acyclic Graph Layout (default)
    - `elk`: ELK Layout
    
## Basic Syntax
Any new line not prefixed with an existing key is considered a new element, e.g.,

```d2
element 1
element 2
```

adds two elements with IDs `element 1` and `element 2`.

When we want to configure elements or add subelements, we can use two different syntaxes:

- prefix: `element.property = value`
- JSON-like syntax: `element{ "property": value }`

Note that this syntax is used for both properties (like styles, position, etc.) and subelements. The logic is:

1. it is a valid D2 key: apply the configuration, or
2. it is NOT a valid D2 key: add it as a subelement


### Connections
[Documentation](https://d2lang.com/docs/connections/)

Connections are special types of elements that are used to connect the components of the flowchart. Instead of using new ID for declaring the connection, we use the following syntax:
```d2
<element from id> <connection type> <element to id>
```

The connection type is one of the following:

- `->`: arrow to
- `<-`: arrow from
- `<->`: bidirectional arrow
- `--`: line

Same as for normal elements, collection may have properties and labels.


### Object Lables
Objects labels are the text printed in or below the object. **By default, the label is the ID of the object.** We can change the label:

- by setting the `label` property of the object (prefix or JSON-like syntax), or
- by adding the text behind semicolon: `<element id>: <label text>`

By default, the label is printed inside the object, which resizes  to fit the label. If the size of the object is set, the behavior defers between *Layout engines*:
- Dagre: the set size of the object is ignored,
- ELK: the label is printed below the object.


## Styling
[Documentation](https://d2lang.com/tour/style/)

### Shapes
[Documentation](https://d2lang.com/tour/shapes/)

Shapes are set using the `shape` property. The most common shapes are:

- `rectangle`
- `diamond`

Some shapes does not have a keyword, but can be created using styling:

- **stadium** (flowchart terminal): `
    ```d2
    shape = rectangle
    style.border-radius = 100
    ```

### Style keywords

- [border-radius](https://d2lang.com/tour/style/#border-radius)

### Text Wrapping
Automatic text wrapping is not supported. We have to wrap the text manually by using the `\n` character.


## Layout engine configuration
[Documentation](https://d2lang.com/tour/layouts/)

D2 supports three layout engines: Dagre, ELK, and TALA, these can be set by the `--layout` command line option. Moreover, we can configure each layout engine by its specific command line options, named as `<layout engine>-<option>`.


### ELK

- [D2 Documentation](https://d2lang.com/tour/elk/)
- [ELK Documentation](https://eclipse.dev/elk/reference.html)

Supported ELK layout options:

- [`--elk-nodeNodeBetweenLayers`](https://eclipse.dev/elk/reference/options/org-eclipse-elk-layered-spacing-nodeNodeBetweenLayers.html): Distance between nodes in different layers (see the Layered algorithm documentation to understand the meaning of layers)
    - lower number means more dense layout, but also greater chance of overlapping
    - D2 default is `70`, but ELK default is `20`, so there is definitely a room for decreasing the value
