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

- [`admin_level`](https://wiki.openstreetmap.org/wiki/Key:admin_level): administrative level of the element. See [Administrative levels](#administrative-levels) for more details.
- [`boundary`](https://wiki.openstreetmap.org/wiki/Key:boundary): area boundary. Most common value is [`administrative`](https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative) for official boundaries.
- [`name`](https://wiki.openstreetmap.org/wiki/Key:name): name of the element. This key holds the most obvious and most used name of the element, not always the official name.


## Administrative levels

- [Key: admin_level](https://wiki.openstreetmap.org/wiki/Key:admin_level)
- [Admin Level Hierarchy for individual countries](https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#Table_:_Admin_level_for_all_countries)
- [USA admin level hierarchy](https://wiki.openstreetmap.org/wiki/United_States_admin_level)


Numeric value determining the level of the element in the hierarchy. Here , we discuss only the administrative levels (i.e., elements with `boundary=administrative` tag), which is the most common use case.

Administrative levels ar numbered from 2 (independent country) to 10 (smallest administrative unit). An effort is taken to use the same numbering for the same type of administrative unit in different countries. In result, some numbers are not used for some countries (e.g., 3 in USA). 

Nevertheless, the numbering is only consistent within a country. For the numbering for each country, see [Admin Level Hierarchy for individual countries](https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#Table_:_Admin_level_for_all_countries). The typical meaning of individual levels is:

- 2: country
- 3: region. Unused in the majority of countries.
- 3: state, province, canton, 
- 5: district, prefecture, 
- 6: county, municipality, city
- 7: town, village, city district

The lower numbers differ too much between countries, so giving a general rule is not at all possible. 


# Search element by id
The searchbox does not work for ids. However, we can edit the URL to search for an element by id. Example:

- `https://www.openstreetmap.org/?way=<way id>`