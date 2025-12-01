# Sources

- [wiki/Overpass QL](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL)

# Strucutre
Every statement ents with `;`.

## Sets
Almost all statements works with sets of data. Unless specified, we work with a default set (`_`).

To wrrito to a specific set, we can use `->.` operator: `<statement>->.<set>` writes the result of the `<statement>` to the <set>. The default set can be ommited: `<statement>` is equal to `<statement>->._`.



# `out` statement
All queries should contain an `out` statement that determines the output format.

- `out` is used for data only request
- `out geom` returns data with all elements associated with their geometry.

Note that while the output format can be specified, we cannot filter the output (e.g., [we cannot filter the ralation members](https://gis.stackexchange.com/questions/433800/exclude-filter-relation-members-by-type-or-role)).

# Area specification
We select an area by name as:
```
area["name"="Letkov"];
```
And then we used it as: 
```
node(area);
```

If we need more areas in a query, we can store them in variable:
```
area["name"="Letkov"]->.let;
```
And:
```
node(area.let);
```

**Important note:** If an area needs to be used repetadly, it has to be named, as the value of `area` (`area._`) is replaced by the output of any statement.

# Filtering
filters are specified in brackets:
```
rel["admin_level"=8];
```

It is also possible to use a regex filtering, we just neeed to replace `=` with `~`:
```
rel["admin_level"~".*"];
```

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