When we do not want to store the GIS data in a database for some reason, we need to choose from one of the GIS formats. The most common GIS formats are:

- [Shapefile](https://en.wikipedia.org/wiki/Shapefile),
- [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON), and
- [GPS Exchange Format (GPX)](https://en.wikipedia.org/wiki/GPS_Exchange_Format).

There are also less common formats:

- [Geography Markup Language (GML)](https://en.wikipedia.org/wiki/Geography_Markup_Language)

Each of the formats has its adventages and disadventages, summarized in the table below:

| Format | File type | Supported geometry types | Multiple geometry types in a file | CRS | QGIS support | extension |
|--------|-----------|--------------------------|--------------------------------------|-----|-----------|-|
| Shapefile | Binary | Point, Line, Polygon | No | Variable | yes | .shp, .shx, .dbf | 
| GeoJSON | Text (JSON)| Point, Line, Polygon | Yes | WGS84[[source]](https://www.rfc-editor.org/rfc/rfc7946#section-4) | yes | .geojson |
| GPS Exchange Format | Text (XML)| Point, Line | Yes | WGS84 | yes | .gpx |
| GML | Text (XML)| Point, Line, Polygon | Yes | Variable | limited | .gml |



## Shapefile


## GeoJSON
[specification](https://datatracker.ietf.org/doc/html/rfc7946)

Geojson is a JSON format for encoding a variety of geographic data structures.

Note that **GeoJSON applications expect coordinates to be in the WGS84 coordinate reference system** (CRS). If the coordinates are in a different CRS, applications may not be able to interpret the data correctly.

## Geography Markup Language (GML)
[specification](https://www.ogc.org/publications/standard/gml/)

The GML is similar to GeoJSON, but it is based on XML. The problem with GML is that it is not widely used nowadays, and it is not supported by many GIS applications.
