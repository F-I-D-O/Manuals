# Adding layers
`Layer` -> `Add Layer`

# Count the number of features in area
1. select the right layer
1. on the top panel, third row, select the tool `Select Features by area or single click`
1. select features
1. Open the attribute table for layer. In the heder, there should be the number of selected features

# Postgis Layers

## Invalid layer
The layer can be marked as invalid because of a missing or invalid index column. **Each Postgis layer needs an id column consisting of unique integer values**.