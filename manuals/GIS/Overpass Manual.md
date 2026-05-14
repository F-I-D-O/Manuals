# Sources

- [wiki/Overpass QL](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL)

# Structure
Every statement ends with `;`. There are three types of statements:

- **Settings**: for configuring the whole query, enclosed in square brackets
- **Block statements**: for enabling branching, loops, etc.
- **Standalone queries**: for selecting data


# Settings
Each setting is a key-value pair enclosed in square brackets. All must be specified in the first statement. Example:
```Overpass QL
[out:json][timeout:25];
```



# Sets
Almost all statements works with sets of data. Unless specified, we work with a default set (`_`).

To write to a specific set, we can use `->.` operator: `<statement>->.<set>` writes the result of the `<statement>` to the `<set>`. The default set can be omitted: `<statement>` is equal to `<statement>->._`.



# Standalone statements

## `out` statement
All queries should contain an `out` statement that determines the output format.

- `out` is used for data only request
- `out geom` returns data with all elements associated with their geometry.

Note that while the output format can be specified, we cannot filter the output (e.g., [we cannot filter the relation members](https://gis.stackexchange.com/questions/433800/exclude-filter-relation-members-by-type-or-role)).

## Query Statements
[Overpass Wiki](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#The_Query_Statement)

These statements query for `osm` data. The syntax is: `<data type><tag filters><query filter>`.

The `<data type>` is one of the following:

- `node`: for nodes
- `way`: for ways
- `relation` or `rel`: for relations
- `area`: for areas
- `derived`: ?

Additionally, there are shortcuts for querying multiple data types at once: `nr`, `nw`, `wr`, and `nwr`.

The query statement can be filtered by:

- tag filters in square brackets
- query filters in parentheses

### Tag Filters
The [`<tag filters>`](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#By_tag_(has-kv)) is a (possibly empty) set of filters applied to the data type, effectively filtering the elements by their tags. Each filter is enclosed in square brackets. There are several types of filters:

- **key-value**: `key=value`, or `key!=value`
- **existence**: `key`, or `!key`
- **regex**: `key~regex`


### Query Filters
The `<query filter>` is a special filter that uses different logic than the tag filters. It is enclosed in parentheses. There are several types of query filters:

- **bounding box**: `<south>, <west>, <north>, <east>`
- [**child/parent**](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_(n,_w,_r,_bn,_bw,_br)): `[b]<element type><set name>` only select child/parent elements from the specified set.
    - The filter can be:
        - forward (default): select the child elements of the specified set
        - backward (prefixed with `b`): select the parent elements of the specified set
    - Each set is prefixed by an element type (`n`, `w`, `r`), so we can only select one type of elements from a set
    - Examples:
        - `node(w)` selects all nodes that are children of a way.
        - `node(w.let)` selects all nodes that are children of a way in the set `let`.
        - `way(bn.let)` selects all ways that are parent of a node in the set `let`.
- [**set membership**](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#By_input_set_(.setname)): `.<setname>`
- [**area**](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#By_area_(area)): `[<set name>.]area`. If the `<set name>` is omitted, the default set (`_`) is used. lter by the previously stored result of an area query statement.
- [**general conditions**](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Conditional_query_filter_(if:)): `if: <evaluator>`. The `<evaluator>` is an expression, posibly using tagg, literlas, operators, and more. Evaluators are described in a dedicated [Evaluator section](#evaluators).



# Evaluators
In general, we can use:

- literals: `1`, `"string"`, `true`, `false`, `null`
- tag valyes: `t["<tag key>"]`
- operators: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, `!`


# Selecting Multiple Data Sets
Implicitely, all filters are aplied to a default dataset called `_`  and also written to it. Therefore, we cannot do:
```
rel["admin_level"~".*"];
node;
```
because we are basically selecting nodes from a set of relations. Solutions:

1) Union statement
2) Named sets

## Union Utatement 
Union statement is surounded by parantheses. We can achieve the intended behaviour by:
```
(
rel["admin_level"~".*"];
node;
);
```

# Select Area Boundary
Sometimes, it is usefull to check the boundary of the named area. However, the administrative level differ for various areas cities, countries, so the `admin_level` relation cannot be used for that. Luckilly, there is an option to use the `pivot` filter. Example:
```
area["name"="Praha"];
node(pivot);
out geom;
```

## Discover the full name of an area
If we want to know the full name of the area while the above query return multiple results, we can do that in openstreet map:

1. Move the map to see the area
2. Click the button with cusor and question mark to select the exploration tool
3. Click inside the area
4. Scroll down to area relations
5. Click on the proper region
6. The `name` property is what we are looking for

## Filter areas with duplicite names
Sometimes, even the full name of the area is not specific enough. In that case, we can use two approaches:

- select the area by the area relation id
- specify the area by the higher level area (state, country)

### Select area by ID

1. select the requested area
2. copy the id and add 3 600 000 000 to it (start with 36 and fill zerose till there are 10 digits in total)
3. replace `area["name"="<NAME>]` with `area(<ID>)`. **Note that round brackets are used instead of square brackets!**

### Specify area with higher level area
In this exaple, we select the Coo County, Illinois.
```
area[name="Illinois"];
rel[name="Cook County"](area);
map_to_area;
node(pivot);
out geom;
```

[more info](https://dev.overpass-api.de/overpass-doc/en/full_data/area.html)



# Get historical data
To get historical data, prepend the query with a date statement. Example:
```
[date:"2016-01-01T00:00:00Z"];
area[name="City of New York"];
node(pivot);
out geom;
```

# Overpass in Python
In Python, we can use the [`overpy`](https://github.com/dellsystem/overpy) to access the Overpass API. The basic usage is:
```Python
import overpy

api = overpy.Overpass()

query = "node(50.0878, 14.4207, 50.0888, 14.4217); out;"
result = api.query(query)
```