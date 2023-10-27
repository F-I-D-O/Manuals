# Creating a DataFrame
The `DataFrame` class has a constructor that supports multiple formats of input data as well as many configuration parameters. Therefore , for most formats of input data, we can create a dataframe using the constructor. However, we can also crete a dataframe using the `from_*` functions, and for some formats, these functions are the only way to create a dataframe.

## From a dictionary
When having a dictionary, we can choose between two options the constructor and the [`from_dict`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html) function.

The required syntax depend on the shape of the dictionary with respect to the required dataframe.

### Keys are column names, values are list of column values
```python
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
# or equivalently
df.DataFrame.from_dict({'col1': [1, 2], 'col2': [3, 4]})
```
Note that the values of the dictionary have to be lists. If we have a dictionary with values that are not lists (i.e., only one row), we have to use the `orient` parameter to specify the orientation of the data and then transpose the dataframe:
```python
d = {'col1': 1, 'col2': 2}

df = pd.DataFrame.from_dict(d, orient='index').T
# or equivalently
df = pd.DataFrame([d], columns=d.keys())
```


### Keys are indices, values are values of a single column
```python
df = pd.DataFrame.from_dict({'row1': 1, 'row2': 2}, orient='index', columns=['Values'])
```


### Keys are indices, values are values of single row
```python
df = pd.DataFrame.from_dict({'row1': [1, 2], 'row2': [3, 4]}, orient='index')
```


### Keys are one column, values are another column
```python
d = {'row1 col1': 'row1 col2', 'row2 col1': 'row2 col2'

df = pd.DataFrame.from_dict(d.items())

# or equivalently
df = pd.DataFrame({'col1': d.keys(), 'col2': d.values()})
``` 



## From a list of dictionaries
```python
df = pd.DataFrame([{'col1': 1, 'col2': 3}, {'col1': 2, 'col2': 4}])
```

## From a list of lists
```python
df = pd.DataFrame([[1, 3], [2, 4]], columns=['col1', 'col2'])
```

## From 


# Obtaining info about dataset
For a DataFrame `df`:
- column names: `df.columns`
- column types: `df.dtypes`
- number of rows: `len(df)`

# Iteration

## Standard Iteration
https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas

Iteration without modifying the dataframe. From the fastest to the slowest.

### Vector operations

### List Comprehensions

### Apply

### itertuples()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.htm

Returns dataframe rows as pandas named tuples with index as the first member of the tuple.


### iterrows()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html

returns a tuple (index, data)

 - it does not preserve the dtype 


### items()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.items.html
Iterates over columns

## Iteration with modification
When doing some modifications, we need to copy the dataframe and do the modifications on the copy.



# Filtration
```python
filtered = df[df['max_delay'] == x]
```
or equivalently:
```python
filtered = df[df.max_delay == x]
```


## Filtration by Multiple Columns
Example:
```python
filtered = df[(df['max_delay'] == x) & (df['exp_length'] == y)]
```

## Accept multiple values
For that, we can use the [`isin`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html) function:
```python
filtered = df[df['max_delay'].isin([x, y])]
```


## Using the query function
The query function can be used for more complicated filters. It is more flexible and the syntax is less verbose. The above filter can be rewriten as:
```python
filtered = df.query('max_delay == x and exp_length == y']
```


## Filtering Series
A seris can be filtered even simpler then the dataframe:
```python
s = df['col']
sf = s[s <= 10] # now we have a Series with values from df['col'] less than 10
```


## Useful filter functions
- non null/nan values: `<column selection>.notnull()`
- filtring using the string value: `<column selection>.str.<string function>`



# Selection
If we want to select a part of the dataframe (a set of rows and columns) independently of the values of the dataframe (for that, see [filtration](#filtration)), we can use these methods:
- [`loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html): select by label, works for both rows and columns
- [`iloc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html): select by position, works for both rows and columns
- `[]`: select by label, works only for columns

There are also other methods that works for selection but does not work for setting values, such as:
- [`xs`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.xs.html): select by label, works for both rows and columns


## `loc`
The operator `loc` has has many possible input parameters, the most common syntax is 
```Python
df.loc[<row selection>, <column selection>]
```
each selection has the form of `<start label>:<end label>`. For the whole column, we therefore use:
```Python
df.loc[:, <column name>]
```


## Difference between array operator on dataframe and on `loc`
Both methods can be used both for getting and setting the column:
```Python
a = df['col']
# or equivalently
a = df.loc[:, 'col']

df2['col'] = a
# or equivalently
df2.loc[:, 'col'] = a
```

The difference between these two methods is apparent when we want to use a chained selection, i.e., selecting from a selection. While the `loc` selects the appropriate columns in one step, so we know that we still refer to the original dataframe, the array operator operations are separate, and therefore, the result value can refer to a temporary:
```Python
dfmi.loc[:, ('one', 'second')] = value # we set a value of a part of dfmi
dfmi['one']['second'] = value # can be dangerous, we can set value to a temporary
```

This problem is indicated by a `SettingWithCopy` warning. Sometimes it is not obvious that we use a chain of array operator selections, e.g.:
```Python
sel = df[['a', 'b']]
.....
sel['a'] =  ... # we possibly edit a temporary!
```
For more, see the [dovumentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy).


## `iloc`
The `iloc` method works similarly to the `loc` method, but it uses the position instead of the label.

Be aware that **if the `iloc` operator selects by single value (e.g.: `df.iloc[3]`), it returns the single row as series**. To get a dataframe slice, we need to use a list of values (e.g.: `df.iloc[[3]]`).


## Selecting all columns but one
If we do not mind copying the dataframe, we can use the `drop` function. 

Otherwise, we can use the `loc` method and supply the filtered column lables obtained using the `columns` property:
```Python
df.loc[:, df.columns != '<column to skip>']
```


## Multi-index selection
[documentation](https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-advanced-hierarchical)

When selecting from a dataframe with a multi-index, things get a bit more complicated. We can specify index levels using the `level` argument. Example:
```Python
df.loc[<row selection>, <column selection>, level=<level number>]
```

If we want to specify more than one level, we can use a tuple:
```python
df.loc[(<row index level 1>, <row index level 2>, ...), (<col index level 1>, <col index level 2>, ...)]
```

If we select an upper level only, all lover level values are selected.

For more complex cases where we wanto to select all from upper level but limit the lower level, we can use the [`slice`](https://pandas.pydata.org/docs/user_guide/advanced.html#using-slicers) function:
```python
df.loc[(slice(None), slice('15', '30')), ...]
```
We can obtain the same result with a more readable syntax using the [`IndexSlice`](https://pandas.pydata.org/docs/reference/api/pandas.IndexSlice.html) object:
```python
idx = pd.IndexSlice
dft.loc[idx[:, '15':'30'], ...]
```

Also, note that for multi-index slicing, the index needs to be sorted. If it is not, we can use the [`sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html) function.



# Sorting
for sorting the dataframe, we can use the [`sort_values`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html) function. The first argument is the list of columns to sort by, starting with the most important column. Example:
```python
df.sort_values(['col1', 'col2'])
```

If we want to use a custom sorting function, we can use the `key` argument. The key function should satisfy the classical python sorting interface (see Python manual) and additionaly, it should be a vector function, i.e., instead of returning a single position for a given value, it should return a vector of positions for a given vector of values. Example key function:
```python
def key_fn(l: list):
    return [len(x) for x in l]
```


# Working with columns


## Adding a column
The preferable way is to use the [`assign`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.assign.html) function:
```Python  
# adds a column named 'instance_length' with constant value
result_df_5_nyc_mv.assign(instance_length = 5) 
```

Multiple columns can be added at once:
```Python
trips = trips.assign(dropoff_datetime = 0, dropoff_GPS_lon = 0, dropoff_GPS_lat = 0, pickup_GPS_lon = 0, pickup_GPS_lat = 0)
```


## Rename a column
To rename a column, we can use the pandas [`rename`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html) function:
```Python
df.rename(columns={'<old name 1>': '<new name 1>', '<old name 2>': '<new name 2>'})

# or equivalently
df.rename({'<old name 1>': '<new name 1>', '<old name 2>': '<new name 2>'}, axis='columns')
```






# Working with the index
Index of a dataframe `df` can be accessed by `df.index`. Standard range operation can be applied to index. 

## Changing the index
For that, we can use the [`set_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html) function.


## Renaming the index
The [`Index.rename`](https://pandas.pydata.org/docs/reference/api/pandas.Index.rename.html) function can be used for that.


# Aggregation
Analogously to SQL, pandas has a [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function for aggreagting rows. The usage is as follows:
```Python
group = df.groupby(<columns>) # returns a groupby object grouped by the columns
sel = group[<columns>] # we can select only some columns from the groupby object
agg = sel.<aggregation function> # we apply an aggregation function to the selected columns
```
we can skip the `sel` step and apply the aggregation function directly to the groupby object. This way, the aggregation function is applied to all columns.

For the aggregate function, we can use one of the prepared aggregation functions, for example:
- `sum`
- `mean`
- `median`
- `min`
- `max`
- `count`

Full example (sum):
```Python
df.groupby('col').sum()
```
Sums the results for each group (column by column)

To get a count, we can call the `size` function:
```Python
df.groupby('col').size()
```

## Custom aggegate function
Also, there is a general [`agg`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html) function that can be used to apply a custom aggregation function. Example:
```Python
df.groupby('col').agg({'col1': 'sum', 'col2': 'mean'})
```

We can also use the `apply` method. This function takes a dataframe as an argument and returns a series. Example:
```Python
def agg_fn(df):
    return pd.Series([df['col1'].sum(), df['col2'].mean()], index=['sum', 'mean'])
```

The difference between `agg` and `apply` is summarized in the following table:

property | agg | apply |
| --- | --- | --- |
| applied to | each specified column | whole dataframe |
| output | dataframe | series |
| can use multiple aggregate functions | yes | no |
| can be applied to dataframe | no | yes |



# Joins


# Appending one dataframe to another
We can use the [`concat`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) function for that:
```python
pd.concat([df1, df2])
```

# I/O

## csv
For reading csv files, we can use the [`read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) function. Important params:
- `sep`: separator
- `header`: row number to use as column names. If `None`, no header is used
- `skiprows`: number of rows to skip from the beginning
- `delim_whitespace`: if `True`, the whitespace is used as a separator. The `sep` parameter is ignored in that case. This is a way how to read a file with variable number of whitespaces between columns.


For export, we can use the `to_csv` method for that:
```python
df.to_csv(<file name> [, <other params>])
```



## Insert dataframe into db
We can use the `to_sql` method for that:
```python
df.to_sql(<table name>, <sql alchemy engine> [, <other params>])
```

Important params:
- to append, not replace existing records: `if_exists='append'`
- do not import dataframe index: `index=False`

For larger datasets, it is important to not insert everything at once, while also tracking the progress. The following code does exactly that

```python
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

chunksize = int(len(data) / 1000) # 0.1%
with tqdm(total=len(data)) as pbar:
    for i, cdf in enumerate(chunker(data, chunksize)):
        cdf.to_sql(<table name>, <sqlalchemy_engine>)
        pbar.update(chunksize)
```
**If the speed is slow, it can be caused by a low upload speed of your internet connection.** Note that due to the SQL syntax, the size of the SQL strings may be much larger than the size of the dataframe.



# Latex export
Currently, the [`to_latex`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_latex.html) function is deprecated. The `Styler` class should be used for latex exports instead. You can get the `Styler` from the DataFrame using the `style` property. The usual workfolow is:
1. Create a `Styler` object from the dataframe using the `style` property.
1. Apply the desired formatting to the styler object.
1. Export DataFrame to latex using the `to_latex` method.

Keep in mind that **the `Styler` object is immutable, so you need to assign the result of each formatting operation to a new variable or chain the calls**. Example:
```Python
# wrong, the format is not apllied
df.style.format(...)
df.style.to_latex(...)

# correct: temp var
s = df.style.format(...)
s.to_latex(...)

# correct: chain calls
df.style.format(...).to_latex(...)
```

## Formatting the index: columns and row labels
The columns' and row labels' format is configures by the [`format_index`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.format_index.html) function.
Important parameters:
- `axis`: 0 for rows, 1 for columns (cannot be both)
- `escape`: by default, the index is not escaped, to do so, we need to set `escape` to `'latex'`.


## Formatting or changing the values
The values are formated by the [`format`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.format.html) function. Important parameters:
- `escape`: by default, the values are not escaped, to do so, we need to set `escape` to `'latex'`.
- `na_rep`: the string to use for missing values
- `precision`: the number of decimal places to use for floats

## Replacing values
For replace some values for the presentation with something else, we can  also use the `format` function.For example, to change the boolean presentation in column `col` we call:
```python
df.style.format({'col': lambda x: 'yes' if x else 'no'})
```

## Hihglighting min/max values
For highlighting the min/max values, we can use the [`highlight_min`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.highlight_min.html) and [`highlight_max`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.highlight_max.html) functions. Important parameters:
- `subset`: the columns in which the highlighting should be applied
- `props`: the css properties to apply to the highlighted cells


## Hiding some columns, rows, or indices
For hiding some columns, rows, or indices, we can use the [`hide`](https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.hide.html) function. Format:
```python
df.style.hide(<index name>) # hide the index with the given name
```
By default, the `<index_name>` refers to the row index. **To hide a column**:
```python
df.style.hide_columns(<column name>, axis=1)
```

To hide row index:
```python
df.style.hide(axis='index')
```


## Changing the header (column labels)
There is no equivalent to the header parameter of the old `to_latex` function in the new style system. Instead, it is necessary to change the column names of the dataframe. 



## Exporting to latex
For the export, we use the [`to_latex`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.to_latex.html) function. Important parameters:
- `convert_css`: if `True`, the css properties are converted to latex commands
- `multirow_align`: the alignment of the multirow cells. Options are `t`, `c`, `b`
- `hrules`: if set to `True`, the horizontal lines are added to the table, specifically to the top, bottom, and between the header and the body. Note that these hrules are realized as the `\toprule`, `\midrule`, and `\bottomrule` commands from the `booktabs` package, so the package has to be imported  .
- `clines`: configuration for hlines between rows. It is a string composed of two parts divided by `;` (e.g.: `skip-last;data`). The parts are:
    - whether to skip last row or not (`skip-last` or `all`)
    - whether to draw the lines between indices or the whole rows (`index` or `data`)


# Displaying the dataframe in console
We can display the dataframe in the conslo print or int the log just by supplying the dataframe as an argument because it implements the `__repr__` method. Sometimes, however, the default display parameters are not sufficient. In that case, we can use the [`set_option`](https://pandas.pydata.org/docs/reference/api/pandas.set_option.html) function to change the display parameters:
```python
pd.set_option('display.max_rows', 1000)
```

Important parameters:
- `display.max_rows`: the maximum number of rows to display
- `display.max_columns`: the maximum number of columns to display
- `display.max_colwidth`: the maximum width of a column



# Other useful functions
- [`drop_duplicates`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html) to quickly drop duplicate rows based on a subset of columns.
- [`factorize`](https://pandas.pydata.org/docs/reference/api/pandas.factorize.html) to encode a series values as a categorical variable, i.e., assigns a different number to each unique value in series.
- [`pivot_table`](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html): function that can aggragate and transform a dataframe in one step. with this function, one can create a pivot table, but also a lot more.
- [`cut`](https://pandas.pydata.org/docs/reference/api/pandas.cut.html): function that can be used to discretize a continuous variable into bins.


## `pivot_table`
The pivot table (mega)function do a lot of things at once:
- it aggregates the data
- it transforms the data
- it sorts the data due to reindexing

Although this function is very powerfall there are also many pitfalls. The most important ones are:
- column data type change for columns with missing values

### Column data type change for columns with missing values
The tranformation often creates row-column combinations that do not exist in the original data. These are filled with `NaN` values. But some data types does not support `NaN` values, and in conclusion, the data type of the columns with missing values is changed to `float`. Possible solutions:
- we can use the `fill_value` parameter to fill the missing values with some value that is supported by the data type (e.g. -1 for integers)
- we can use the `dropna` parameter to drop the rows with missing values
- we can change the data type of the columns with missing values prior to calling the `pivot_table` function. For example, the [pandas integer data types](https://pandas.pydata.org/docs/reference/arrays.html#nullable-integer) support `NaN` values.



# Geopandas
Geopandas is a GIS addon to pandas, an equivalent to PostGIS. Unfortunately, **it currently supports only one geometry column per table.**

**Do not ever copy paste the geometries from jupyter notebook as the coordinates are rounded!** Use the `to_wkt` function instead.

## Create a geodataframe from CSV
Geopandas has it's own `read_csv` function, however, it requires a very specific csv format, so it is usually easier to first import csv to pandas and then create geopandas dataframe from pandas dataframe.

## Converting pandas Dataframe to geopandas Dataframe
The geopandas dataframe constructor accepts pandas dataframes, we just need to specify the geometry column and the coordinate system:
```Python
gdf = gpd.GeoDataFrame(
    <PANDAS DATAFRAME>
    geometry=gpd.points_from_xy(<X COLUMN>, <Y COLUMN>),
    crs=<SRID>
)
```

## Create geodataframe from `shapely`
To load data from shapely, execute
```Python
gdf = gpd.read_file(<PATH TO FOLDER WITH SHAPEFILES>)
```

## Working with the geometry
The geometry can be accessed using the `geometry` property of the geodataframe.


## Spliting multi-geometry columns
If the geometry column contains multi-geometries, we can split them into separate rows using the [`explode`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.explode.html) function:
```Python
gdf = gdf.explode()
```



## Insert geodataframe into db

### preprocesssing
Before inserting a geodataframe into the database, we need to process it a little bit:
1. set the SRID: `gdf.set_crs(epsg=<SRID>, allow_override=True, inplace=True)`
2. set the geometry: `gdf.set_geometry('geom', inplace=True)`
3. select, rename, or add columns so that the resulting geodataframe match the corresponding database table. This process is same as when working with `pandas`

### Simple insertion
When the data are in the correct format and we don|t need any customization for the db query, we can use the `to_postgis` method:
```Python
gdf.to_postgis(<TABLE NAME>, <SQL ALCHEMY CONNECTION>, if_exists='append')
```

### Customized Insertion: `geoalchemy`
If we need some special insert statement, we cannot rely on the `geodataframe.to_postgis` function, as it is not flexible enough. The `pandas` `dataframe.to_sql` function is more flexible, however, it has trouble when working with geodata. The easiest options is therefore to use [`geoalchemy`](https://geoalchemy-2.readthedocs.io/en/latest/), the database wraper used in `geopandas` (extension of `sqlalchemy`, which is a database wrapper for `pandas`). 

First, we need to create the insert statement. The example here uses a modification for handeling duplicite elements.
```Python
meta = sqlalchemy.MetaData()    # create a collection for geoalchemy database  
                                # objects

table = geoalchemy2.Table(
    '<TABLE NAME>', meta, autoload_with=<SQL ALCHEMY CONNECTION>)
insert_statement 
    = sqlalchemy.dialects.postgresql.insert(table).on_conflict_do_nothing()
```

In the above example, we create a `geoalchemy` representation of a table and then we use this representation to create a customized insert statement (the [`on_conflict_do_nothing`](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert.on_conflict_do_nothing) is the speciality here.). Note that we use a [`speciatl PostgreSQL insert statement`](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.insert) instead of the standard SQLAlchemy insert statement.

Second, we need to prepare the data as a list of dictionary entries:
```Python
list_to_insert = [
    {'id': 0, 'geom': <GEOM>, ...},
    {'id': 0, 'geom': <GEOM>, ...},
    ....
]
```
Note that the geometry in the geodataframe is in the shapely format. Therefore, we need to convert it to string using the `geoalchemy` [`from_shape`](https://geoalchemy-2.readthedocs.io/en/latest/shape.html) function:
```Python
geoalchemy2.shape.from_shape(<GEOMETRY>, srid=<SRID>)
```


Finally, we can execute the query using an `sqlalchemy` connection:
```Python
sqlalchemy_connection.execute(insert_statement, list_to_insert)
```
