# Adding points from coordinates
The easiest way is to use *QuickWKT*

# Count the number of features in area
1. select the right layer
1. on the top panel, third row, select the tool `Select Features by area or single click`
1. select features
1. Open the attribute table for layer. In the heder, there should be the number of selected features

# Postgis Layers

## Adding layers
`Layer` -> `Add Layer`

## Temporary layer
Temporary layers are useful for experimenting. Whether we want to add a point, line, or area, we need a layer for that even if we do not intend to save the result. The right layer for this is the *temporary scratch layer* we can add it by:

`Layer` -> `Create layer` -> `New Temporary Scratch Layer...`

## Invalid layer
The layer can be marked as invalid because of a missing or invalid index column. **Each Postgis layer needs an id column consisting of unique integer values**.
