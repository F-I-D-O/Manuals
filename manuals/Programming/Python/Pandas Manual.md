# Main principles
Pandas extensively uses the term axis. In Pandas, axis 0 is vertical (rows) and axis 1 is horizontal (columns). 


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

## Creating a zero or constant-filled dataframe
To create a dataframe filled with a constant, we can use the dataframe constructor and pass the constant as the first (data) argument:
```python
df = pd.DataFrame(0, index=range(10), columns=['col1', 'col2'])
```

### Generating the index
As displayed in the above example, we can generate a numerical index using the `range` function. However, there are more options:
- date index with [`date_range`](https://pandas.pydata.org/docs/reference/api/pandas.date_range.html)
    - `pd.date_range(<start date>, <end date>, freq=<frequency>)`



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
The [`apply`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html) function can be used to apply a function to each row or column of the dataframe. For iterating over rows, we need to set the `axis` parameter to 1. Example:
```python
df['new_col'] = df.apply(lambda row: row['col1'] + row['col2'], axis=1)
```


### itertuples()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html

Returns dataframe rows as pandas named tuples with index as the first member of the tuple.


### iterrows()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html

returns a tuple (index, data)

 - it does not preserve the dtype 


### items()
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.items.html
Iterates over columns

## Iteration with modification
For modification, the best strategy is to:
1. select what we want to modify (see [selection](#selection))
1. modify the selection with the assignment operator. The right side of the assignment operator can be the result of an iteration.



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
- null values: `<column selection>.isnull()`
- non null/nan values: `<column selection>.notnull()`
- filtring using the string value: `<column selection>.str.<string function>`
- filtering dates: `<column selection>.dt.<date function>`



# Selection
If we want to select a part of the dataframe (a set of rows and columns) independently of the values of the dataframe (for that, see [filtration](#filtration)), we can use these methods:
- [`loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html): select by index, works for both rows and columns
- [`iloc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html): select by position, works for both rows and columns
- `[]`: select by index, works only for columns

There are also other methods that works for selection but does not work for setting values, such as:
- [`xs`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.xs.html): select by label, works for both rows and columns

The return type of the selection is determined by the number of selected rows and columns. For a single row or column, the result is a series, for multiple rows and columns, the result is a dataframe. If we want to get a dataframe for a single row or column, we can use the `[]` operator with a list of values:
```python
df[['col1']]
# or 
df.loc[['row1']]
# or
df.iloc[[0]]
```


## `loc`
The operator [`loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html) has many possible input parameters, the most common syntax is 
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
The `iloc` method works similarly to the `loc` method, but it uses the position instead of the label. To select more values, we can use the slice syntax
```Python
df.iloc[<start position>:<end position>:<step>,<collumn slicing...>]
```

Be aware that **if the `iloc` operator selects by single value (e.g.: `df.iloc[3]`), it returns the single row as series**. To get a dataframe slice, we need to use a list of values (e.g.: `df.iloc[[3]]`).


## Selecting all columns but one
If we do not mind copying the dataframe, we can use the `drop` function. 

Otherwise, we can use the `loc` method and supply the filtered column lables obtained using the `columns` property:
```Python
df.loc[:, df.columns != '<column to skip>']
```


## Multi-index selection
[documentation](https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-advanced-hierarchical)

When selecting from a dataframe with a multi-index, things get a bit more complicated. There are three ways how to select from a multi-index dataframe:
- using `loc` with slices: simple, but verbose
- using `loc` with `IndexSlice` object: more readable, but requires the `IndexSlice` object to be created first
- using `xs` function, neat, but does not support all the features, e.g., it does not support ranges

### Using `loc` 
The general `loc` usage is the same as for a single index dataframe:
```Python
df.loc[<row selection>, <column selection>]
```
However, each selection is now a tuple, where each element of the tuple corresponds to one level of the multi-index:
```Python
df.loc[(<row selection level 1>, <row selection level 2>, ...), (<column selection level 1>, <column selection level 2>, ...)]
```
The `<row selection>` can be a specifica value, a list of values, or a slice. Note that we have to use the `slice` function, as pandas uses the standard slice syntax for something else. 

We can skip lower levels to select all values from those levels. However, we cannot skip upper levels. If we want to select all values from the upper level, we need to use the `slice(None)` for that level:
```python
df.loc[(slice(None), slice(15, 30)), ...]
```

Note that for multi-index slicing, the index needs to be sorted. If it is not, we can use the [`sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html) function.

[`pandas slicing documentation`](https://pandas.pydata.org/docs/user_guide/advanced.html#using-slicers) 


#### Using `IndexSlice` for more readable syntax 
We can obtain the same result with a more readable syntax using the [`IndexSlice`](https://pandas.pydata.org/docs/reference/api/pandas.IndexSlice.html) object:
```python
idx = pd.IndexSlice
dft.loc[idx[:, 15:30], ...]
```


#### Handeling the `too many indexers` error
Sometimes, when using the `loc` method, the selection can fail with the `too many indexers` error, because it is ambiguous whether we select by rows or by columns. In that case, we can either  
- use the `axis` parameter to specify the axis to select from:
    ```python
    df.loc(axis=0)[<row selection>]
    ```
- or use the IndexSlice instead.


### Using `xs`
The [`xs`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.xs.html) function can be used to select from a multi-index dataframe. However, slices (ranges) are not supported. Example:
```python
df.xs(15, level=1) # selects all rows with level 1 equal to 15
```


## Select row with a maximum value in a column
To get the index of the row with the maximum value in a column, we can use the `idxmax` function:
```python
df['col'].idxmax()
```
Then we can use the `loc` method to get the row.


## Selecting a single value (cell, scalar)
When we select a single value from a dataframe, the result is sometimes a series, especially when we use a filtration. To get a scalar, we can use the `item()` method:
```python
df.loc[<row>, <column>].item()
```



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

### Rename a Series (column)
The column name in the series object is actually the name of the series. To rename the series, we can use the [`rename`](https://pandas.pydata.org/docs/reference/api/pandas.Series.rename.html) function, or we can set the `name` property of the series:
```Python
s.rename('<new name>')
# or equivalently
s.name = '<new name>'
```



# Working with the index
Index of a dataframe `df` can be accessed by `df.index`. Standard range operation can be applied to index. 

## Selecting just a single index level from a multi-index
If we want to select just a single index level, we can use the [`get_level_values`](https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.get_level_values.html) function:
```python
df.index.get_level_values(<level>)
```
Note however, that this function returns duplicated values when there are multiple values in other levels. To get unique values, we can use the [`unique`](https://pandas.pydata.org/docs/reference/api/pandas.Series.unique.html) function.

There is also another method, that returns unique values: the level property:
```python
df.index.levels[<level>]
```
However, **this way, we can get outdated values**, as the values are not always updated when the index is changed. To get the updated values, we need to call the method [`remove_unused_levels`](https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.remove_unused_levels.html) after each change of the index.


## Changing the index

### Using columns as a new index
For that, we can use the [`set_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html) function.


### Using an existing index to create a new index
For that, we can use the [`reindex`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reindex.html) function. The first parameter is the new index. Example:
```python
df.reindex(df.index + 1) # creates a new index by adding 1 to the old index
```
Important parameters:
- `fill_value`: the value to use for missing values. By default, the missing values are filled with `NaN`.


### Creating index from scratch
To create an index from scratch, we just assign the index to the dataframe `index` property:
```python
df.index = pd.Index([1, 2, 3, 4, 5])
```
We can also assign a range directly to the index:
```python
df.index = range(5)
```

To create more complicated indices, dedicated functions can be used:
- [`MultiIndex.from_product`](https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.from_product.html): creates a multi-index from the cartesian product of the given iterables


## Renaming the index
The [`Index.rename`](https://pandas.pydata.org/docs/reference/api/pandas.Index.rename.html) function can be used for that.


# Aggregation
Analogously to SQL, pandas has a [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function for aggreagting rows. The usage is as follows:
```Python
group = df.groupby(<columns>) # returns a groupby object grouped by the columns
sel = group[<columns>] # we can select only some columns from the groupby object
agg = sel.<aggregation function> # we apply an aggregation function to the selected columns
```

We can skip the `sel` step and apply the aggregation function directly to the groupby object. This way, the aggregation function is applied to all columns.

Example (sum):
```Python
df.groupby('col').sum()
```
Sums the results for each group (column by column)

To get a count, we can call the `size` function:
```Python
df.groupby('col').size()
```

Note that unlike in SQL, the aggregation function does not have to return a single value. It can return a series or a dataframe. In that case, the result is a dataframe with the columns corresponding to the returned series/dataframe. In other words, the **aggregation does not have to actually aggregate the data, it can also transform it**.

In the groupby object, the columns used for grouping are omitted if each group is aggregated to exactly one row. To keep them, we can use the `group_keys` parameter of the `groupby` function.



## Aggregate functions
For the aggregate function, we can use one of the prepared aggregation functions. Classical functions(single value per group):
- `sum`
- `mean`
- `median`
- `min`
- `max`
- `count`

Transformation functions (value for each row):
- [`cumsum`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.cumsum.html): cumulative sum
- [`diff`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.diff.html): difference between the current and the previous row.
    - the `periods` parameter specifies which row to use for the difference. By default, it is the previous row (periods=1). For next row, use periods=-1, but note that the result is then negative. We can use the `abs` function to get the absolute value.


## Custom aggegate function
Also, there are more general aggregate functions:
-  [`agg`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html) function that is usefull for applying different functions for different columns and
- [`apply`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.apply.html): the most flexible function that can be used for custom aggregation and transformation operations.

These two functions have different interfaces for the custom aggregation functions they call. These are summarized in the following table:

property | agg | apply |
| --- | --- | --- |
| can just transform the data | no | yes |
| can use data from one column in another column | no | yes |
| applied to | each specified column | the whole dataframe representing single group |
| output | dataframe | scalar, series, or dataframe |
| can use multiple aggregate functions | yes | no |


### `agg`
 Example:
```Python
df.groupby('col').agg({'col1': 'sum', 'col2': 'mean'})
```

### `apply`
The [`apply`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.apply.html) function takes a custom function as an argument. That custom aggregation function:
- takes a DataFrame/Series (depending on the source object) as the first argument
    - this dataframe/series contains the data for the group (all columns)
- returns a Series, DataFrame, or a scalar
    - when a scalar is returned, the result is a series with the scalar value for each group
    - we do not have to reduce the data to a single value or a single row, we can just transform the data arbitrarily.

The process works as follows:
1. The dataframe is split into groups according to the `groupby` function.
1. The custom function is applied to each group.
1. The results are combined into a single dataframe.

In other words, the custom function only sees the dataframe/series representing the group, not the whole dataframe/series. The grouping and compining aggreate results is done by the `apply` function.



## Time aggregation
We can also aggregate by time. For that, we need an index or column with datetime values. Then, we can use the [`resample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html) function. Example:
```Python
df = pd.DataFrame({'col1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, index=pd.date_range('2021-01-01', periods=10, freq='1D'))

df.resample('1H').sum()
```
The aggregate function is applied to each group in case of multiple values in the same time slot (*downsampling*). In case of no values in the time slot (*upsampling*), the value is filled with `NaN`. We can use the [`ffill`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ffill.html) function to fill in the missing values. Example:
```Python
df.resample('1H').sum().ffill()
```



# Joins
Similarly to SQL, Pandas has a way to join two dataframes. There are two functions for that:
- [`merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html): the most general function that has the behavior known from SQL
- [`join`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.join.html): a more specialized function, 

The following table lists the most important differences between the two functions:

property | merge | join |
| --- | --- | --- |
| default join type | inner | left |
| join right table via | column (default) or index (`right_index=True`) | index |
| join left table via | column (default) or index (`left_index=True`) | index, or column (`on=key_or_keys`) |

There is also a static [`pd.merge`](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) function. All `merge` and `join` methods are just wrappers around this function.

The indexes are lost after the join (if not used for the join). To keep an index, we can store it as a column before the join.




# Appending and Concatenating data
In pandas, there is a [`concat`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) function that can be used to concatenate data:
```python
pd.concat([df1, df2])
```
It can concatenate dataframes or series and it can concatenate vertically (by rows, default) or horizontally (by columns)

By default, the indices from both input parameters are preserved. To reset the index, we can use the `ignore_index` parameter. Alternatively, to preserve one of the indices, we can set the index of the other dataframe to the index of the first dataframe before the concatenation using the `set_index` function.


# Pandas Data Types


## Object
If pandas does not recognize the type of the column, or there are multiple types in the column, it uses the `object` type. However this may sound like a wonderful solution, it causes many problems, so be sure to avoid object type columns at all costs. Typically, the problem arises when we try to apply a vector operation to the column:
- we round a column with mix of floats and ints: fail (`loop of ufunc does not support argument 0 of type float which has no callable rint method`)
- we need to apply string functions, but the column contains numbers as well

The solution is usually:
1. fill the missing values with the `fillna` function
2. convert the column to `str` type using the `astype` function
3. apply string functions to clear the data
4. convert the column to the desired type



## Categorical data
Sometimes, it can be usefull to treat a column as a categorical variable instead of a string or a number. For that, we can use the [`Categorical`](https://pandas.pydata.org/docs/reference/api/pandas.Categorical.html) class. The constructor accepts the values of to be converted to categorical variable (list, column,...) and optional parameters. The most important parameters are:
- `categories`: the list of categories. If not specified, the categories are inferred from the data. If specified, the categories are used as the categories of the categorical variable. If the data contains values that are not in the categories, the `Categorical` constructor raises an error. If the categories contain values that are not in the data, the values are converted to `NaN`.
- `ordered`: if `True`, the categories are ordered in the order of the `categories` parameter.  


## Datetime
Pandas has a special type for datetime values. One of its dangerous properties is that zero parts of the datetime are truncated both when displaying and on export:
```python
df = pd.DataFrame({'date': pd.to_datetime(['2021-01-01 00:00:00', '2021-01-01 00:00:00'])})
print(df)
# output:
# '2021-01-01'
# '2021-01-01'
```



# I/O

## csv
For reading csv files, we can use the [`read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) function. Important params:
- `sep`: separator
- `header`: row number to use as column names. If `None`, no header is used
- `skiprows`: number of rows to skip from the beginning
- `delim_whitespace`: if `True`, the whitespace is used as a separator. The `sep` parameter is ignored in that case. This is a way how to read a file with variable number of whitespaces between columns.


For export, we can use the [`to_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html) method:
```python
df.to_csv(<file name> [, <other params>])
```

Useful parameters:
- `index`: if `False`, the index is not exported
- `index_label`: the name of the index column


## Json
For exporting to json, we can use the [`to_json`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html) function. 

By default, the data are exported as a list of columns. To export the data as a list of rows, we can use the `orient` parameter:
```python
df.to_json(<file name>, orient='records')
```

Other important parameters:
- `indent`: the number of spaces to use for indentation


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
For hiding some columns, rows, or indices, we can use the [`hide`](https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.hide.html) function. Important Parameters:
- `axis`: 0 for hiding row indices (default), 1 for hiding column names
- `level`: the level of the multi-index to hide (default is all levels)
- `subset`: the columns or rows to hide (default is all columns or rows)

When used without the `subset` parameter, the `hide` function hides the whole index. To hide just a selected row or column from the data, the subset parameter has to be used.

By default, the `<index_name>` refers to the row index. **To hide a column**:
```python
df.style.hide_columns(<column name>, axis=1)
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


## `to_datetime`
The [`to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) function can convert various inputs to datetime. It can be used to both scalars and vectors. Important parameters:
- `unit`: the unit of the input, e.g., `s` for seconds.
- `origin`: the origin of the input, e.g., `unix` for unix timestamps. It can be also any specific `datetime` object.


## `squeeze`
The [`squeeze`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.squeeze.html) function removes the unnecessary dimension from a dataframe or series. It is usefull when we want to convert a dataframe with a single column to a series, or a series with a single value to a scalar.


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
