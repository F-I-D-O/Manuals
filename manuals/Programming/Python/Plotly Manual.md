In plotly, we have two options:
- plot quickly with plotly express
- full control using graph objects

Note that thes options can hardly be mixed. For example, we cannot use plotly express to create a figure and then add a subplot to it. Similarly, we cannot use the `make_subplots` function to create a figure and then add a plotly express plot to it.


In general, it is easier to use plotly express, so we should use it if we are not affected by its limitations. **The plotly express cannot**
- create **custom subplots**. Howwever, automatic "facet" subplots (same plot divided between multiple plots using some data attribute) are possible.


# Plotly Express
[documentation](https://plotly.com/python/plotly-express/)
Plotly express modul is loaded as:
```python
import plotly.express as px
```

## Common Parameters For All Types of Plots
- `data_frame`: the dataframe to use. Mandatory, first positional parameter.
- `x`: the name of the column to use as x axis. Mandatory, second positional parameter.
- `color`: the name of the column to use as color.
- `facet_col`: the name of the column to use as facet column.
- `facet_row`: the name of the column to use as facet row.
- `color_discrete_sequence`: the list of colors in hexadecimal format to use for the color column. If the number of colors is less than the number of categories, the colors are reused. If the number of colors is greater, the colors are truncated.
- `title`: the title of the plot. 


## Histogram
[documentation](https://plotly.com/python/histograms/)

Note that the **Plotly histogram is only good for simple cases of small size**. See below for more details.

Plotly express has [`histogram`](https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html) function for creating histograms. The basic syntax is:
```python
px.histogram(<dataframe>, <xcol name>)
```

The y is then the number of occurences of each value in the x column. 

Important parameters:
- `nbins`: number of bins. 

### Plotly Histogram Limitations
Plotly histogram is only good for simple cases of small size. This is because it first stores all data points in JSON and only computes the bins on the javascript size. As a result, the function is slow and the size of the Jupyter notebook cell can be enormous (hundreds of MBs).

For more complex figures, it is better to generate the histogram manually (using numpy or pandas) and then plot it using the `px.bar` function.



## Bar Chart
[documentation](https://plotly.com/python/bar-charts/)

[reference](https://plotly.github.io/plotly.py-docs/generated/plotly.express.bar.html)

For bar charts, we use the `px.bar` function. The basic syntax is:
```python
px.bar(<dataframe>, <xcol name>, <y col name>)
```

Important parameters:
- `barmode`: how to combine the bars in case of multiple traces. Can be `group` (default), `stack` (default in *facet plots*), `relative` or `overlay`.
- `bargap`: the gap between bars.
- `bar_groupgap`: the gap between the bars from the same group (only for `barmode = group`).

Unfortunately, **there is no way how to represent missing values** in the bar chart (they appear as `y = 0`).
To mark the missing values, we can use annotations. 

### Why bar charts with a lot of records appear transparent?
If the number of records is large, the bar chart may appear transparent. This is because each bar has a border, which has a brighter color. To prevent this effect, we have to remove the border:
```python
fig.update_traces(marker_line_width=0)
```

### Numerical vs categorical color
The values in the color column are interpreted as numerical (continuous) if the column is numeric and as categorical if the column is of any other type. Even if the color column contains only integers, it is still interpreted as numerical with all consequences (color bar instead of categorical colors, `color_discrete_sequence` parameter is ignored, etc.). To force the categorical interpretation, we can convert the column to a string. Example:
```python
px.bar(df, x="x", y="y", color=df["color"].astype(str))
```

## Scatter Plot
[documentation](https://plotly.com/python/line-and-scatter/)

For scatter plots, we use the [`scatter`](https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter.html) function. The basic syntax is:
```python
px.scatter(<dataframe>, <xcol name>, <y col name>)
```

Important parameters:



## Automatic Subplots: Facet plots
[Facet plots](https://plotly.com/python/facet-plots/) can be created using the same plot function as for normal plotly express plots and supplying the `facet_col` and/or `facet_row` parameters. Example:
```python
fig = px.histogram(df, x="column", facet_row="<col 1>", facet_col="<col 2>")
```
Here, the figure will be devided into subplotts. Each row will share the `<column 1>` values, and each column will share the `<column 2>` values. The number of rows and columns will be determined automatically as the number of unique values in `<column 1>` and `<column 2>`, respectively.

### Independent axes between rows and columns
It can happen that each row or column should have its own x or y axis due to a different scale. We can accomplish this by calling the `update_xaxes` and `update_yaxes` functions on the figure. Example:
```python
fig.update_xaxes(matches=None)
fig.update_yaxes(matches=None)
```

### Removing the column name from the row/column annotations
For each row and column, a label is added to the subplot. This label has a format of `<column name> = <value>`. To remove the column name, we can use the `for_each_annotation` function. Example:
```python
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
```


### Sharing the axes titles between rows and columns
Unfortunately, the axes titles cannot be easily shared between rows and columns. The only way is to delete the titles and add shared titles manually using the `add_annotation` function. Example:
```python
# shared y axis title
fig.for_each_yaxis(lambda y: y.update(title = ''))
fig.add_annotation(x=-0.05, y=0.5, text="Vehicle hours", textangle=-90, xref="paper", yref="paper", showarrow=False)

# shared x axis title
fig.for_each_xaxis(lambda y: y.update(title = ''))
fig.add_annotation(x=0.5, y=-0.12, text="Occupancy",  xref="paper", yref="paper", showarrow=False)
```



# Plotly Graph Objects


## Bar Chart
The basic syntax is:
```python
go.Bar(x, y, ...)
```

Some more complicated examples are in the [documentation](https://plotly.com/python/bar-charts/#basic-bar-charts-with-plotlygraphobjects).


## Line Chart
[documentation](https://plotly.com/python/line-charts/#line-plot-with-goscatter)

The line chart is created using the [`go.Scatter`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html) function. Example:
```python
go.Scatter(x, y, ...)
```

Important parameters:
- `mode`: the mode of the line. 
    - Can be:
        - `lines`,
        - `markers`,
        - `lines+markers`,
        - `text`,
        - `lines+text`,
        - `markers+text`,
        - `lines+markers+text`. 
    - The default is `lines+markers` if  there are less than 20 data points and `lines` otherwise.
- `line`: dictionary containing the line parameters. The most important parameters are:
    - `color`: the color of the line
    - `width`: the width of the line


## Create subplots
[documentation and examples](https://plotly.com/python/subplots/)

To create a figure with multiple subplots, we use the `make_subplots` function. Example:

```python
fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
              row=1, col=1)
...
fig.show()
```

Importanta parameters:
- `shared_xaxes` and `shared_yaxes`: if `True`, the subplots will share the same x and y axes. 
- `x_title` and `y_title`: the titles of the x and y axes. 
- `horizontal_spacing` and `vertical_spacing`: the spacing between the subplots.




# Customizing the Figure
The figure object can be custommized in many ways.


## Size and margins
The size and margins can be set using the `figure.update_layout` function. The specific parameters are:
- `width`: the width of the figure in pixels
- `height`: the height of the figure in pixels
- `autosize`: needs to be `False` if we want to set the width and height manually
- `margin`: dictionary containing the margins. The format is: `l`, `r`, `t`, `b`: the left, right, top and bottom margins in pixels
- `pad`: the padding between the plot and the margins in pixels

[documentation](https://plotly.com/python/setting-graph-size/#adjusting-height-width--margins-with-graph-objects)


## Customize axes
For customizing the axes, we can use the `figure.update_xaxes` and `figure.update_yaxes` functions. By default, the functions will update all axes. To update only a specific axis, we can use the `row` and `col` parameters. 

[axis reference](https://plotly.com/python/reference/layout/xaxis/)

The most important parameters are:
- `dtick`: the distance between the ticks
- `tickvals`: the exact values of the ticks. This overrides the `dtick` parameter.
- `title_text`: the title of the axis. Note that **this text is only used if the tickavls are set manually**.
- `range`: range of the axis, e.g.: `range=[0, 1]`. By default, the range is determined automatically as the range of the data plus some margin. Unfortunately, **there is no way how to automatically set the range to match the data range exactly**.
- `linecolor`: the color of the axis line
- `mirror`: if `True`, the axis line will be mirrored to the other side of the plot

### Drawing borders using axes
The borders can be drawn using the axes. To draw a  black border around the plot, we can use the following code:
```python
fig.update_xaxes(linecolor="black", mirror=True)
fig.update_yaxes(linecolor="black", mirror=True)
```

### Customizing datetime axes
Unfortunately, we cannot treat the datetime axes as expected, i.e., using the datetime objects. For example, to set the tick interval, we cannot use the `datetime.timedelta` object. Instead, we need to use the number of milliseconds. Example:
```python
fig.update_xaxes(dtick=1000 * 60 * 60 * 24 * 7) # one week interval
```



## Legend
[documentation](https://plotly.com/python/legend/)
[reference](https://plotly.com/python/reference/layout/#layout-legend)

The legend can be styled using the `figure.update_layout` function. 
The most important parameters are:
- `legend_title_text`: the title of the legend
- `legend`: dictionary containing many parameters
    - `orientation`: `h` or `v` for horizontal or vertical legend
    - `x`, `y`: the position of the legend from the bottom left corner of the figure
    - `xanchor`, `yanchor`: the position of the legend box relative to the x and y coordinates
    - `title`: if string, the title of the legend (equivalent to the `legend_title_text` parameter). If dictionary, multiple legent title parameters can be set.

Unfortunately, **there is no way how to customize the padding between the legend items and the legend box**. 

### Hide legend
To hide the legend, we can use the `showlegend` parameter. Example:
```python
fig.update_layout(showlegend=False)
``` 



## Adding Figure Annotations
For adding annotations to the whole Figure, we can use the [`add_annotation`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.add_annotation) function. 

Important parameters:
- `x`, `y`: the x and y coordinates of the annotation
- `text`: the text of the annotation
- `xref`, `yref`: the coordinate system of the x and y coordinates. Can be `"paper"` or `"data"`.
- `showarrow`: if `True`, an arrow will be added to the annotation
- `textangle`: the angle of the text in degrees


**By default** the annotation is meant to annotate the data. Therefore, **the `x` and `y` coordinates use the coordinate system of the data** (x and y axes). To align the annotation with respect to the whole figure, we need to set the `xref` and `yref` parameters to `"paper"`. In this case, the `x` and `y` coordinates are in the range `[0, 1]` and the origin is the bottom left corner of the figure.

### Annotations in facet plots
When using facet plots, the annotations are added to the whole figure. Therefore, the `x` and `y` coordinates are in the range `[0, 1]` and the origin is the bottom left corner of the figure. To align the annotation with respect to the subplot, we need to set the `xref` and `yref` parameters to the x and y axes of the subplot. Example:
```python
fig.add_annotation(x=0.5, y=0.5, text="Title", xref="x5", yref="y5", showarrow=False)
```

Unfortunately, **there is no way how to set the `xref` and `yref` parameters automatically**. Therefore, we need to compute them manually for each annotation.



## Markers
[documentation](https://plotly.com/python/marker-style/)

To style the markers, we can use the `update_traces` function. Example:
```python
fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
```


### Adding a marker to a hard-coded location
To add a marker to a hard-coded location, we can add it as a new trace. Note that we can add new traces even to a figure created using plotly express. 


## Title
[documentation](https://plotly.com/python/figure-labels/#align-plot-title)

The title can be set using the plotly express functions or when creating the graph objects figure. To update the text or to customize the title layout, we can use the `update_layout` function with the `title` object parameter. Example:
```python
fig.update_layout(
    title={
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.85,
        'yanchor': 'top'
    }
)
```
Important parameters:
- `x`, `y`: the x and y coordinates of the title. The origin is the bottom left corner of the figure.
- `xanchor`, `yanchor`: the position of the title relative to the x and y coordinates. Can be `left`, `center` or `right` for `xanchor` and `top`, `middle` or `bottom` for `yanchor`.


## Other Layout Parameters (background, borders, etc.)
- background color: `plot_bgcolor`
- border: borders are best drawn by showing and mirroring the axes (see the axis section above).



# Text
[documentation](https://plotly.com/python/text-and-annotations)

## Subscript and superscript
To add a subscript or superscript to a text, we can use HTML tags. Example:
```python
fig.add_annotation(x=0.5, y=0.5, text="Title<sub>subscript</sub>", xref="x5", yref="y5", showarrow=False)
```

## Bold and italic
To add bold or italic text, we can use the HTML tags `<b>` and `<i>`. Example:
```python
fig.add_annotation(x=0.5, y=0.5, text="Title<b>bold</b><i>italic</i>", xref="x5", yref="y5", showarrow=False)
```

## Math symbols
To add math symbols, we can use the LaTeX syntax. Example:
```python
fig.add_annotation(x=0.5, y=0.5, text=r"Title$ \alpha $ and $ \beta $", xref="x5", yref="y5", showarrow=False)
```



# Exporting the Figure
[documentation](https://plotly.com/python/static-image-export/)

The static export is handeled using the figure's `write_image` function. Example:
```python
fig.write_image("figure.png")
```

The output format is determined by the extension.

The margins of the figure should be set for the figure itself, not for the export.

## Export hangs out 
It can be cause by kaleido. The solution si to install an older version, specifically `0.1.0.post1`.

https://community.plotly.com/t/static-image-export-hangs-using-kaleido/61519/4

