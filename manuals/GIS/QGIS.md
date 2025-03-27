# Adding points from coordinates
The easiest way is to use *QuickWKT*

# Count the number of features in area

1. select the right layer
1. on the top panel, third row, select the tool `Select Features by area or single click`
1. select features
1. Open the attribute table for layer. In the heder, there should be the number of selected features

# Layers

## Adding layers
To add a layer, use `Layer` -> `Add Layer`. Each layer type has its own option in this menu.


## Temporary layer
Temporary layers are useful for experimenting. Whether we want to add a point, line, or area, we need a layer for that even if we do not intend to save the result. The right layer for this is the *temporary scratch layer* we can add it by:

`Layer` -> `Create layer` -> `New Temporary Scratch Layer...`

## Invalid layer
The layer can be marked as invalid because of a missing or invalid index column. **Each Postgis layer needs an id column consisting of unique integer values**.

## Postgis layer
Postgis layers are layers that are loaded from a Postgis database. A postgis layer can be created from:

- a table,
- a view,
- or a query.

In all cases, the layer data has to fulfill the following requirements:

- the layer has to have a column with unique integer values (id) that is used as a primary key,
- the layer has to have a column with geometry data, and
- the layer definition must not modify the data in the database (due to read-only transaction mode).
    - `nextval()` is therefore not allowed
    - creating temporary tables is not allowed



# Debugging
As an open-source project, QGIS has many bugs.

Frequently, the program does not behave as expected, but no problem is reported. In such cases, the best way to find out what is going on is to open the log window: `View` -> `Panels` -> `Log Messages`.
