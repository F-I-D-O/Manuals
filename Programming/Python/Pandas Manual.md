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

> Written with [StackEdit](https://stackedit.io/).

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
- diltring using the string value: `<column selection>.str.<string function>`



# Working with columns
We can access columns using the array operator (`[]`) on the dataframe or on its [`loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html) property. 

The `[]` operator `loc` method has has many possible input parameters, the most common syntax is 
```Python
df.loc[<row selection>, <column selection>]
```
each selection has the form of `<start label>:<end label>`. For the whole column, we therefore use:
```Python
df.loc[:, <column name>]
```


Both methods can be used both for getting and setting the column:
```Python
a = df['col']
# or equivalently
a = df.loc[:, 'col']

df2['col'] = a
# or equivalently
df2.loc[:, 'col'] = a
```

## Difference between array operator on dataframe and on `loc`
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


## Selecting all columns but one
If we do not mind copying the dataframe, we can use the `drop` function. 

Otherwise, we can use the `loc` method and supply the filtered column lables obtained using the `columns` property:
```Python
df.loc[:, df.columns != '<column to skip>']
```

## Adding a column
The preferable way is to use the [`assign`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.assign.html) function:
```Python  
# adds a column named 'instance_length' with constant value
result_df_5_nyc_mv.assign(instance_length = 5) 
```

## Rename a column
To rename a column, we can use the pandas [`rename`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html) function:
```Python
df.rename(columns={'<old name 1>': '<new name 1>', '<old name 2>': '<new name 2>'})

# or equivalently
df.rename({'<old name 1>': '<new name 1>', '<old name 2>': '<new name 2>'}, axis='columns')
```


# Accessing rows
We can locate the rows of a dataframe in two ways:
- using the dataframe's index: `df.loc[<index>]`
- using the row number: `df.iloc[<row number>]`

If the dataframe is sorted by the index and the index starts from 0 (default), both `loc` and `iloc` deliver the same row. The dataframe index can be, however, arbitary sorted, it can be even non-numeric, so it is wise to distinguish between these two functions.



# Working with the index
Index of a dataframe `df` can be accessed by `df.index`. Standard range operation can be applied to index. 

## Changing the index
for that, we can use the [`set_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html) function.


# Aggregation
Analogously to SQL, pandas has a `groupby` function for aggreagting rows. Depending on the aggregate function we choose, we get a different statistic, for example:
```Python
df.groupby('col').sum()
```
Sums the results for each group (column by column)

To get a count, we need to call the `size` function:
```Python
df.groupby('col').size()
```




# Joins



# Insert dataframe into db
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


## Formatting the values
The values are formated by the [`format`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.format.html) function. Important parameters:
- `escape`: by default, the values are not escaped, to do so, we need to set `escape` to `'latex'`.


## Exporting to latex
For the export, we use the [`to_latex`](https://pandas.pydata.org/docs/dev/reference/api/pandas.io.formats.style.Styler.to_latex.html) function. Important parameters:



# Other useful functions
- [`drop_duplicates`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html) to quickly drop duplicate rows based on a subset of columns.
- [`factorize`](https://pandas.pydata.org/docs/reference/api/pandas.factorize.html) to encode a series values as a categorical variable, i.e., assigns a different number to each unique value in series.
- [`pivot_table`](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html): function that can aggragate and transform a dataframe in one step. with this function, one can create a pivot table, but also a lot more.



# Geopandas
Geopandas is a GIS addon to pandas, an equivalent to PostGIS. Unfortunately, **it currently supports only one geometry column per table.**

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
