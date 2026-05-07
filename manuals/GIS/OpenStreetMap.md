# OSM format
[specification](https://wiki.openstreetmap.org/wiki/Elements)

In `osm` format, the content is a set of *elements*, each of which can have *tags* - key-value pairs that describe the element. In the basic XML format, the elements are represented as XML elements, and the tags are represented as XML attributes.

There are three main types of **elements**:

- **Nodes**: points in the map
- **Ways**: linestrings that can represent roads, rivers, area boundaries, etc.
- **Relations**: defines relations between elements

Additionally, there are some **semantic elements** - elements that have no dedicated representation in the XML format, but instead, are represented by a combination of other elements. These elements are:

- **Areas**: two-dimensional objects, typically represented by closed ways that represent the boundary of the area.


# Tags
[wiki](https://wiki.openstreetmap.org/wiki/Tags)

There are over 100 000 tag keys and 190 million unique tag values on OpenStreetMap. The most common tag keys are:

- [`name`](https://wiki.openstreetmap.org/wiki/Key:name): name of the element. This key holds the most obvious and most used name of the element, not always the official name.
- [`boundary`](https://wiki.openstreetmap.org/wiki/Key:boundary): area boundary. Most common value is [`administrative`](https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative) for official boundaries.

# Search element by id
The searchbox does not work for ids. However, we can edit the URL to search for an element by id. Example:

- `https://www.openstreetmap.org/?way=<way id>`