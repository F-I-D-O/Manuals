In plotly, we have two options:

- plot quickly with plotly express
- full control using graph objects

Note that these options can hardly be mixed. For example, we cannot use plotly express to create a figure and then add a subplot to it. Similarly, we cannot use the `make_subplots` function to create a figure and then add a plotly express plot to it.


In general, it is easier to use plotly express, so we should use it if we are not affected by its limitations. **The plotly express cannot**

- create **custom subplots**. However, automatic "facet" subplots (same plot divided between multiple plots using some data attribute) are possible.
- **z-order** of the traces. For example, we need to first plot a trace using graph objects. Then it is much easier to plot the rest of the traces using graph objects as well.


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
- `hover_data`: the list of columns to show in the hover tooltip. Axes columns are shown automatically.
- `text`: text labels for the data points. 


### Automatic color assignment
If we use the color parameter of a graph, plotly express plots a trace for each color value and assigns a color to the trace. To customize this color, we can use two parameters:

- `color_discrete_sequence`: list of the colors to be used
- `color_discrete_map`: dictionary mapping the color values to the colors. 

With the `color_discrete_sequence` parameter, plotly express iterates through the list of colors and assigns the colors to the color values in the order they appear in the data. If the number of colors is less than the number of color values, the colors are reused. If the number of colors is greater, the colors are truncated. Therefore, this parameter is useful only if:

- the number of colors is equal to the number of color values
- the number of colors is greater than the number of color values and we use categorical colors, so the truncation does not matter.

The `color_discrete_map` parameter is more flexible. We can manually assign the colors to the color values, to use the color scale optimally. 

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


## Line Chart
[documentation](https://plotly.com/python/line-charts/)

[reference](https://plotly.github.io/plotly.py-docs/generated/plotly.express.line.html)

For line charts in plotly express, we use the `px.line` function. The basic syntax is:
```python
px.line(<dataframe>, <xcol name>, <y col name>)
```



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

### Sharing the axes titles between rows and columns
Unfortunately, the axes titles cannot be easily shared between rows and columns. The only way is configure the axis text manually. Example:
```python
# remove y axis titles except for the first subplot
for i in range(1, 4):
    fig.update_yaxes(title_text='', row=1, col=i)
# set the text of the first y axis
fig.update_yaxes(title_text="Comp. time relative to IH", row=1, col=1)

```


## 3D Scatter Plot
[documentation](https://plotly.com/python/3d-scatter-plots/)

For 3D scatter plots, we use the [`scatter_3d`](https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_3d.html) function. The basic syntax is:
```python
fig = px.scatter_3d(<dataframe>, <xcol name>, <y col name>, <z col name>)
```



# Plotly Graph Objects
[documentation](https://plotly.com/python/graph-objects/)

If the plotly express is not enough, we can use the graph objects. We need to use the second option only for complex figures, for example:

- facet plots with more than one metric
- plots with custom traces *behind* the plotly express traces

We can either add the graph objects to a plotly express figure or create a graph objects figure from scratch. Most of the time, we will use the first option, as using plotly express is easier.

For **adding traces** to the figure, we can use the [`add_trace`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.add_trace) function. Important parameters:

- `row`, `col`: the row and column of the subplot where to add the trace. 
    - Both parameters have to be set.
    - The numbering starts from 1.

To **make the figure from scratch**, we can use the [`make_subplots`](https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html) function from the `plotly.subplots` module. Example:
```python
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=2)
```
Important parameters:

- `rows`, `cols`: the number of rows and columns in the figure
- `shared_xaxes`, `shared_yaxes`: configures the axes sharing. Possible values:
    - `False (default)`: each subplot has its own axes
    - `True`: only one axis per row (for `shared_xaxes`) or column (for `shared_yaxes`). 
    - `row` or `col`: equivalent to `True`, applicable only to `shared_xaxes` or `shared_yaxes`, respectively.
    - `all`: all subplots share the same axes
- `horizontal_spacing`, `vertical_spacing`: the spacing between the subplots in relative units, values are in the range `[0, 1]`. 
    - The default is `0.2` for both, which means that the space between each subplot is 20% of the figure width/height.
- `subplot_titles`: the titles of the subplots.




## Common Parameters For All Types of Plots
The main difference between the plotly express and the graph objects is the data parameters. For plotly express, we pass the dataframe and the column names for the x and y axes. In contrast, **we pass the data to the graph functions as iterables, one for each axis**. Therefore, we have to use a single column from the dataframe, not the whole dataframe, even if it contains just one column.

### Legend
The name in the legend is determined by the `name` parameter of the trace. To share the legend between multiple traces, the following steps are needed:

1. set the `name` parameter of all traces to the same value
2. set the `showlegend` parameter of one trace to `True` and to `False` for all other traces


## Bar Chart
The basic syntax is:
```python
go.Bar(x, y, ...)
```

Some more complicated examples are in the [documentation](https://plotly.com/python/bar-charts/#basic-bar-charts-with-plotlygraphobjects).


### Stacked or grouped bars
Unlike plotly express, the graph objects do not have the `color` parameter to set the column to use for determining the group to which the bar belongs. There are two options how to create stacked or grouped bars:

- create a trace for each group manually and add them all to the figure
- crete the figure with plotly express and then extract the traces from the figure
    ```python
    for trace in occ_fig.data:
        fig.add_trace(trace, row=1, col=i + 1)
    ```

Also, to set the bar mode, we need to use the `update_layout` as the `go.Bar` function does not have the `barmode` parameter. Example:
```python
fig.update_layout(barmode="stack")
```


## Line and Scatter Plots
[line plot documentation](https://plotly.com/python/line-charts/#line-plot-with-goscatter)

Line plots, scatter plots and shapes, all of that can be created by the [`go.Scatter`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html) function. Example:
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


## Shapes
[documentation](https://plotly.com/python/shapes/)

There are various ways how to create shapes in plotly:

- for simple higlight of regions on x or y axis, we can use the [`add_vrect`](https://plotly.github.io/plotly.py-docs/generated/plotly.html#plotly.basedatatypes.BaseFigure.add_vrect) and [`add_hrect`](https://plotly.github.io/plotly.py-docs/generated/plotly.html#plotly.basedatatypes.BaseFigure.add_hrect) functions ([introductory example](https://plotly.com/python/shapes/#highlighting-time-series-regions-with-rectangle-shapes), [documentation](https://plotly.com/python/horizontal-vertical-shapes/)).
    - only for recangles spaning the whole height or width of the plot
- The shapes can be created by supplying the coordinates of the shape to the `go.Scatter` function and setting the `fill` parameter to `"toself"`. ([documentation](https://plotly.com/python/shapes/#shapedrawing-with-scatter-traces))
    - this method has a serious limitation: **the filled scatter plots are always above the other traces**
- finally, we can use the [`add_shape`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.add_shape) function to add a shape to the figure.

**There is no way how to fill shapes with a patern fill.**

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


## 3D plots

### Common Parameters


#### Setting color of the plots with continuous color scale
If the plot type is continuous (e.g., surface plot, cone plot), we cannot set a color for the whole trace as a continuous color scale is used. However, we can set the colorscale using the `colorscale` parameter. Example:
```python
fig.add_trace(go.Surface(z=z, colorscale="Viridis"))
```
The color scale can be also set manually as a list of colors. This way, we can overcome the limitation of the continuous color scale and set the color of the whole trace. Example:
```python
fig.add_trace(go.Surface(z=z, colorscale=[[0, "red"], [1, "red"]]))
```


### 3D Scatter Plot
[documentation](https://plotly.com/python/3d-scatter-plots/)

The 3D scatter plot is created using the [`go.Scatter3d`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter3d.html) function. Example:
```python
go.Scatter3d(x, y, z, ...)
```


### Surface Plots
There are multiple types of plots that may be considered as surface plots in plotly:

- [**3D surface**](https://plotly.com/python/3d-surface-plots/) (`go.Surface`): a surface plot defined by a grid of x, y, and a 2D array of z values of the shape (|x|, |y|). The surface is plotted for all combinations of x and y, which makes this function suitable only for cases where the surface is defined for all combinations of x and y.
- [**3D mesh**](https://plotly.com/python/3d-mesh/) (`go.Mesh3d`): a surface plot defined by vertices (points) and faces (connections between the points). The connections are defined by triangles, which can be either defined manually or computed automatically using a triangulation algorithm. 
- [**Tri-surface**](https://plotly.com/python/trisurf/) (`figure_factory.create_trisurf`): a surface plot created by a triangulation of the data points. It accepts triangles in a single argument. I have to further investigate, how it differs from the 3D mesh plot.

#### 3D Surface Plot
[documentation](https://plotly.com/python/3d-surface-plots/)

The 3D surface plot is created using the [`go.Surface`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Surface.html) function. 


#### 3D Mesh Plot
[documentation](https://plotly.com/python/3d-mesh/)

The 3D mesh plot is created using the [`go.Mesh3d`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Mesh3d.html) function. Example:
```python
x = [1, 1, 1]
y = [1, 2, 1]
z = [0, 0, 1]

fig.add_trace(go.Mesh3d(x=x, y=y, z=z))
```

This way, the triangulation is used to compute the connections between the points. If we want to use a different triangulation, we can use the `i`, `j` and `k` parameters. These parameters define the indices (in the source data used for `x`, `y`, and `z`) of the vertices that form the triangles. For example, `i[0]`, `j[0]` and `k[0]` define the vertices of the first triangle. Example code:
```python
x = [1, 1, 1]
y = [1, 2, 1]
z = [0, 0, 1]
i = [0]
j = [1]
k = [2]

fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k))
```

Note that here, the `i`, `j` and `k` parameters are redundant, as there is only one possible triangulation of the three points. However, for more complex surfaces, there can be multiple valid triangulations, and the `i`, `j` and `k` parameters can be used to select the triangulation manually.



### Cone Plots
[documentation](https://plotly.com/python/cone-plot/)

[reference](https://plotly.com/python/reference/cone/)

The main parameters of the cone plot are:

- `x`, `y`, `z`: the coordinates of the cone base
- `u`, `v`, `w`: the vector defining the direction and length of the cone




# Customizing the Figure
The figure object can be custommized in many ways.


## Size and margins
The size and margins can be set using the `figure.update_layout` function. The specific parameters are:

- `width`: the width of the figure in pixels
- `height`: the height of the figure in pixels
- `autosize`: needs to be `False` if we want to set the width and height manually
- `margin`: dictionary containing the margins (`l`, `r`, `t`, `b`) and one another property: `pad`. All properties are in pixels. 
    - `l`, `r`, `t`, `b`: distance between the plot and the figure border. Note that titles are not included in the plot, so we have make space for the titles if we set margins manually.
    - `pad`: distance between the plotting area (i.e., the plotting coordinates for data points) and the axis lines. Most of the time, this should be set to `0` (default)

Unfortunately, **there is no way how to set the margins automatically** to fit all content like titles, annotations, etc.  

[documentation](https://plotly.com/python/setting-graph-size/#adjusting-height-width--margins-with-graph-objects)

[reference](https://plotly.com/python/reference/layout/#layout-margin)


## Customize axes
For customizing the axes, we can use the `figure.update_xaxes` and `figure.update_yaxes` functions. By default, the functions will update all axes. To update only a specific axis, we can use the `row` and `col` parameters. 

[axis reference](https://plotly.com/python/reference/layout/xaxis/)

The **range** of the axis is determined automatically as the range of the data plus some margin. If we want any other range, we need to set it manually using the `range` parameter, e.g.: `range=[0, 1]`. Unfortunately, **there is no way how to automatically set the range to match the data range exactly**

Another thing we usually want to customize are the ticks. Important tick parameters are:

- `dtick`: the distance between the ticks
- `tickvals`: the exact values of the ticks. This overrides the `dtick` parameter.
- `ticks`: the position of the ticks. Can be `outside`, `inside` or `""` (no ticks, default).
- `ticklen`: the length of the ticks in pixels
- `tickformat`: the format of the tick labels. Depending on the axis datatype, we can use number formats (e.g., `".2f"` for two decimal places), datetime formats (e.g., `"%Y-%m-%d"` for dates) or scientific notation (e.g., `"e"` for scientific notation).
    - for percentage, we can use `".0%"` for integer percentage and `".1%"` for one decimal place. Note that this way, the `%` sign is added automatically to each tick label. If we do not want this, we can either set the text manually using the `ticktext` parameter, or multiply the data by 100.
- `tickangle`: the angle of the tick labels in degrees

Other important parameters are:

- `title_text`: the title of the axis. 
- `linecolor`: the color of the axis line
- `gridcolor`: the color of the grid lines
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


### Customizing shared axes
By default, only tick labels are shared between subplots with shared axes. To share other properties (tick markers, axis title) we need to hide them manually and add them to the first subplot. Example:
```python
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(showticklabels=True, row=1, col=1)
```


### 3d axes
[documentation](https://plotly.com/python/3d-axes/)

Unfortunately, the customization of the 3d axes works differently than for the 2d axes. The `update_xaxes` and `update_yaxes` functions do not work for the 3d axes. Instead, we need to use the `update_layout` function with the `scene` parameter. Example:
```python
fig.update_layout(scene=dict(
    xaxis=dict(
        title="x",
        titlefont_size=16,
        tickfont_size=14,
    ),
    yaxis=dict(
        title="y",
        titlefont_size=16,
        tickfont_size=14,
    ),
    zaxis=dict(
        title="z",
        titlefont_size=16,
        tickfont_size=14,
    ),
))
```

**One thing that is not possible to customize idn 3D is the position of the axis**. The x and y axes are always in the bottom, while the z axis is always on the left.


### Change position of the axis title
Unfortunately, there is no way how to change the position of the axis title. The solution is to hide the title and add a new annotation with the title text. Example:
```python
fig.update_xaxes(title_text="")
fig.add_annotation(
    text="Comp. time relative to IH",
    xref="paper",
    yref="paper",
    x=-0.09,
    y=0.5,
    showarrow=False,
    font=dict(
        size=14,
    ),
    textangle=270,
)
```



## Legend
[documentation](https://plotly.com/python/legend/)

[reference](https://plotly.com/python/reference/layout/#layout-legend)

The legend can be styled using the `figure.update_layout` function. 
The most important parameters are:

- `legend_title`: the title of the legend
- `legend`: dictionary containing many parameters
    - `orientation`: `h` or `v` for horizontal or vertical legend
    - `x`, `y`: the position of the in normalized coordinates of the whole plot.
    - 'xref', `yref`: the coordinate system of the x and y coordinates. Can be   
        - `"container"`: the whole plot
        - `"paper"` (default): the plotting area
    - `xanchor`, `yanchor`: the position of the legend box relative to the x and y coordinates
    - `title`: if string, the title of the legend (equivalent to the `legend_title` parameter). If dictionary, multiple legend title parameters can be set.
    - `bordercolor`: the color of the legend border
    - `borderwidth`: the width of the legend border

Unfortunately, **there is no way how to customize the padding between the legend items and the legend box**. Also, **it is not possible to set the legend border to have rounded corners**. 

### Hide legend
To hide the legend, we can use the `showlegend` parameter. Example:
```python
fig.update_layout(showlegend=False)
``` 

### Legend items order
The order of the legend items is determined by the order of the traces in the figure. However, we can change the order using the `legend_traceorder` parameter. Example:
```python
fig.update_layout(legend_traceorder="reversed")
```

### Legend position
The coordinates of the legend are normalized with respect to each axis.
By default, the legend `x` and `y` coordinates are set so that the legend is outside the plot, in the top right corner. 
If the legend is positioned inside the plot, the plot expands to the whole width, but if the legend is positioned outside the plot, the plot width is smaller to leave space for the legend.


### Legend items text
The legend item text is determined by the `name` parameter of the trace. Therefore, to customize the legend item text, we need to set the `name` parameter of the trace. For normal single trace functions, this is simple:
```python
fig.add_trace(go.Scatter(x=x, y=y, name="Custom name"))
```

However, it can be complicated for plotly express functions that plot multiple traces at once, as these determine the `name` parameter automatically from data. For example, when we use the `color` parameter, the `name` parameter is set to the color value. To overcome this, we have two options:

- set the `name` parameter manually for each trace after the figure is created
- change the data so that the `name` parameter is set automatically to the desired value. 

The first approach is usually preferable as we do not mix the data and appearance. To change the `name` parameter, we can use the `update_traces` function:
```python
for trace in fig.data:
    trace.name = process_name(trace.name)
```




## Figure Annotations
[documentation](https://plotly.com/python/text-and-annotations/)

For adding annotations to the whole Figure, we can use the [`add_annotation`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.add_annotation) function. The most compliated and also most limited aspect is the positioning of the annotation. There are two things we can position:

- the head of the annotation, which is the position the annotation arrow points to, or the position of the text in case of no arrow
- the tail of the annotation, which is the position of the annotation arrow, if present

### Setting the head of the annotation
There are two settings for head of the annotation for each axis:

- [`xref`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.xref) and [`yref`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.yref): the mode of the positioning, and
- [`x`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.x) and [`y`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.y): the coordinates

The `xref` and `yref` parameters can be set to:

- `"paper"`: The whole figure mode, where 0 means the left/bottom and 1 means the right/top of the figure.
- `<axis reference>`: The axis mode, where the axis coordinates are used for positioning.
    - for `<axis reference>`, we can use `"x"` or `"y"` for simple plots and `"x1"-"x<n>"` or `"y1"-"y<n>"` for subplots.

By default, the `<axis reference>` is used for simple plots and `"paper"` for subplots.


### Setting the tail of the annotation
There are two settings for the tail of the annotation for each axis:

- [`axref`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.axref) and [`ayref`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.ayref): the mode of the positioning, and
- [`ax`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.ax) and [`ay`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.layout.Annotation.ay): the coordinates

The `axref` and `ayref` parameters can be set to:

- `"pixel"`: The pixel mode, where the coordinates are in pixels relative to the whole figure, where the origin is the bottom left corner of the figure.
- `<axis reference>`: Same as for the head of the annotation, but must be equal to the `xref`/`yref`, ottherwise, the arrow will not be visible.
    - e.g., setting `xref` to `"x1"` and `axref` to `"x2"` is not allowed


### Positinoing the text relative to the arrow
**There is no way how to position the text of the annotation with respect to the arrow**. The text position is:

- the head of the annotation, if the arrow is not present, or
- the tail of the annotation, if the arrow is present

If we want to, for example, need to position the text of the annotation above the arrow, so that the text is parallel to the arrow, we need to use two annotations.

### Other important parameters

- `text`: the text of the annotation
- `showarrow`: if `True`, an arrow will be added to the annotation, if False, only the text will be added. Default is `True`.
- `textangle`: the angle of the text in degrees,
- `bgcolor`: the background color of the annotation



## Markers
[documentation](https://plotly.com/python/marker-style/)

To style the markers, we can use the `update_traces` function. Example:
```python
fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
```

Marker parameters:

- `size`: the size of the marker in pixels
- `line`: dictionary containing border parameters
    - `width`: the width of the border in pixels. The default is 0. This setting is ignored for 3d scatter plots, where the border width is always 1 (see [github issue](https://github.com/plotly/plotly.js/issues/3796))
    - `color`: the color of the border
- `color`: the color of the marker. To make the marker transparent, it is best to use the `rgba` format. Example: `rgba(255, 0, 0, 0.5)` for a red marker with 50% transparency.

### Adding a marker to a hard-coded location
To add a marker to a hard-coded location, we can add it as a new trace. Note that we can add new traces even to a figure created using plotly express. 


## Lines
Lines can be styled using the line parameter of the plotting functions or using the `update_traces` function. Important parameters:

- `color`: the color of the line
- `width`: the width of the line in pixels
- `dash`: the dash pattern. Can be
    - `"solid"` (default)
    - `"dot"`: dense dashed line
    - `"dash"`: sparse dashed line
    - ... 
    


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

### Subplot titles

#### Automatic subplot titles (facet plots)
When using facet plots, the subplot titles are generated automatically as `<facet column name>=<facet column value>`. Usually, we want to remove the column name and keep only the value. To do this, we can use the `for_each_annotation` function. Example:
```python
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
``` 

#### Individual subplot titles
To set the title of an individual subplot, we can use the `subplot_titles` parameter of the `make_subplots` function. 


To **position the subplot titles**, we have to update all annotations. To prevent the need to filter the titles, it is best to update all annotations right after the `make_subplots` call. Example:
```python
fig = make_subplots(...)
fig.update_annotations(yshift=10) # move the subplot titles 10 pixels up
```

## Z-Order of the Traces
The z-order of the traces cannot be configured. Instead, the traces are drawn in the order they are added to the figure. 

This simple rule has an exception: the webGL traces are always drawn on top of the standard traces. Because all plotly express traces are WebGL traces, they are drawn on top of the graph objects traces added later if those are not WebGL. To overcome this limitation, we have two options:

- not combine plotly express and graph objects traces and convert everything to graph objects for figures with custom traces
- use the webGL versions of the graph objects traces. Example:
    ```python
    fig.add_trace(go.Scattergl(...))
    ```


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
To add math symbols, we can use the LaTeX syntax. However, when using it, all text must be wrapped in math mode, not just the symbols. Example:
```python
fig.add_annotation(x=0.5, y=0.5, text=r"$\\text{{Title: }} \alpha  \\text{{ and }}  \beta $", xref="x5", yref="y5", showarrow=False)
```

**Note that the LaTeX syntax does not work in vscode out of the box** [[issue]](https://github.com/microsoft/vscode-jupyter/issues/8131). We need to add the following code:
```python
import plotly
from IPython.display import display, HTML

plotly.offline.init_notebook_mode()
display(HTML(
    '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
))
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


# Colors
[documentation](https://plotly.com/python/discrete-color/)

For colors in plotly, we can use the color scales supplied by plotly express. These are:

- `px.colors.sequential`: sequential color scales
- `px.colors.diverging`: diverging color scales
- `px.colors.qualitative`: qualitative color scales
