# Data types
[official documentation](https://www.postgresql.org/docs/current/datatype.html)

## Date
[official documentation](https://www.postgresql.org/docs/current/datatype-datetime.html)

- `date`: for dates
- `time` for time
- `timestmp` for both date and time
- `interval`

### Select a part of date/time/timestamp
If we want just a part of a date, time, or timestamp, we can use the `extract` function. Example:
```sql
SELECT extract(hour FROM <date column name>) FROM...
```
Other parts can be extracted too. To extract **day of week**, we can use `isodow` (assigns 1 to Monday and 7 to Sunday).


## Auto incrementing columns
In PostgreSQL, sequences are used for auto-incrementing columns. When you are creating a new db table or adding a new column, the process of creating a new sequence can be automated by choosing an `identity` or a `serial` column type.

When updating an aexisting column, a manual intervention is required:
1. change the column to some numerical datatype
2. create the sequence:
```SQL
CREATE SEQUENCE <SEQUENCE NAME> OWNED BY <TABLE NAME>.<COLUMN NAME>;
```
3. adjust the value of the sequence:
```SQL
SELECT setval(pg_get_serial_sequence('<TABLE NAME>', '<COLUMN NAME>'), max(<COLUMN NAME>)) FROM <TABLE NAME>;
```
3. set the column to be incremented by the sequence:
```SQL
ALTER TABLE <TABLE NAME>
   ALTER COLUMN <COLUMN NAME> SET DEFAULT nextval('<SEQUENCE NAME>');
```


## Strings
There are many string function available, including the `format` function that works similarly to the C format function. For all functions, check the [documentation](https://www.postgresql.org/docs/9.1/functions-string.html).


## Arrays
[array functions and operators](https://www.postgresql.org/docs/8.4/functions-array.html)

To compute array **length**, use `array_length(contracted_vertices, 1)` where `1` stands for the first dimension.

To cretea an **array literal**, we use single quatation and curly brackets: `'{1, 2, 3}'`.

To check that some value match at least some member of the array, we use `ANY`:
```SQL
SELECT ...
FROM tab
WHERE tab.a = ANY(<array>)
```

### Working with the array members individualy
For using the members of an array in the `SELECT` or `JOIN`, we have to first split the array using the `unnest` function. This function transforms the result set to a form where there is a separate row for each member of the array (a kind of inverse operation to group by).

If we want to also keep the array index, we can use the `WITH ORDINALITY` expression, as shown in the [manual](https://www.postgresql.org/docs/current/functions-srf.html) or on [SO](https://stackoverflow.com/questions/8760419/postgresql-unnest-with-element-number).


## hstore
A specific feature of PostgreSQL is the [`hstore`](https://www.postgresql.org/docs/current/hstore.html) column type. It enables to store structured data in a single column. It can be used to dump variables that we do not plan to utilize in the database (i.e., in the SELECT, JOIN statements) frequently. 

When we, exceptionally, want to access a variable from a hstore column, we can use the following syntax:
```SQL
SELECT <COLUMN NAME>-><VARIABLE NAME> AS ...
```



# Selecting rows for deletion based on data from another table
If we want to delete rows from a table based on some condition on data from another table, we can use the `DELETE` statement with a `USING` clause. Example:
```SQL
DELETE FROM nodes_ways_speeds
USING nodes_ways
WHERE
    nodes_ways_speeds.to_node_ways_id = nodes_ways.id
	AND nodes_ways.area IN (5,6)
```



# Procedures and functions
## Calling a procedure
to exectue a stored procedure, use"
```SQL
CALL <procedure name>(<procedure arguments>)
```

Unlike in programing languages, there is no implicit type cast of the program arguments, including literals. Therefore, we need to cast all parameters explicitely, as in the following example:

```SQL
CREATE OR REPLACE PROCEDURE compute_speeds_for_segments(target_area_id smallint)
...

CALL compute_speeds_for_segments(1::smallint);
```


## Creating a procedure
[documentation](https://www.postgresql.org/docs/current/sql-createprocedure.html)

The syntax is as follows:
```SQL
CREATE PROCEDURE <name> (<params>)
LANGUAGE <language name>
<procedure body>
```
, while `<procedure body>` can be both a delimited string:

```SQL
AS $$
<sql statements>
$$
```

OR an active SQL body (since PostgreSQL 14):

```SQL
BEGIN ATOMIC
	<sql statements>
END
```

There are some differences between those syntaxes (e.g., the second one works only for SQL and is evaluated/checked for validity at the time of creation), bot in most cases, they are interchangable. 

For more details, check the [manual](https://www.postgresql.org/docs/current/sql-createprocedure.html).


## Variables
In PostgreSQL, all variables must be [*declared*](https://www.postgresql.org/docs/current/plpgsql-declarations.html) before assignmant in the `DECLARE` block which is before the sql body of the function/procedure/`DO`. The syntax is:
```SQL
<variable name> <variable type>[ = <varianle value>];
```

Example:
```PostgreSQL
CREATE OR REPLACE PROCEDURE compute_speeds_for_segments()
	LANGUAGE plpgsql
AS
$$
DECLARE
	dataset_quality smallint = 1;
BEGIN
	...
```

The, the value of a variable can be change using the classical assignment syntax:
```SQL
<variable name> = <varianle value>;
```

Be carful to **not use a variable name equal to the name of some of the columns** used in the same context, which results in a name clash. 


### Assigning a value to a variable using SQL
There are two options how to assign a value to a variable using SQL:
- using the `INTO` clause in the `SELECT` statement
- using a `SELECT` statement as rvlaue of the assignment

Example with `INTO`:
```PostgreSQL
SELECT name INTO customer_name FROM customers WHERE id = 1
```

EXAMPLE with `SELECT` as rvalue:
```PostgreSQL
customer_name = (SELECT name FROM customers WHERE id = 1)
```



## Functions
[Functions](https://www.postgresql.org/docs/12/sql-createfunction.html) in PostgreSQL have a similar syntax to procedures. 

Unlike for procedures, we need to specify a return type for function, either as an `OUT`/`INOUT` parameter, or using the `RETURNS` clause. To return tabular data, we use [`TABLE`](https://www.postgresql.org/docs/current/xfunc-sql.html#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE) return type:
```SQL
RETURNS TABLE(<param 1 name> <param 1 type>, ..., <param n name> <param n type>)
```
To select the result of a function with the return type above, call:
```SQL
SELECT * FROM <function signature>
```

### `RETURN NEXT` and `RETURN QUERY`
Sometimes, we need to do some cleanup after selecting the rows to be returned from function, or we need to build the result in a loop. In classical programming languages, we use variables for this purpose. In PG/plSQL, we can also use the [`RETURN NEXT` and `RETURN QUERY`](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING) constructs.
These constructs prepare the result, and **does not return from the function**. Instead, use an empty `RETURN` to return from the function. Example:

```SQL 
RETURN QUERY
SELECT ...;
DROP TABLE target_ways;
RETURN;
```

Note that for these constructs, the return type needs to be a `table` or `setof` type. The `RETURN QUERY` cannot be used for returning  a single value even if the query returns a single value. If we have a single value return type and need to do some postprocessing between selecting the value and returning from the function, we have to use a variable instead. 


## Deciding the language
For simple statements, we can use the SQL language. We need the PL/pgSQL if:
- we need to use variables or control statements specific to PL/pgSQL
- we need to use temporary tables, as the SQL language fails to recognize them if they are created inside the function/procedure


## Conditional filters based on the value of a variable or input parameter
To add some filter to the `WHERE` or `ON` clause of a query based on the value of a variable or input parameter, we can use the following technique:
1. set the variable or input parameter to `NULL` if we do not want to apply the filter
2. in the filter test for disjunction of NULL or the filter condition

Example:
```SQL
SELECT ... FROM ... 
WHERE param IS NULL OR some_column = param
```



# Temporary tables in PostgreSQL
To use a result set efficiently in a function or procedure, we often use temporary tables. Unlike in other relational database systems, in PostgreSQl, the lifetime of a temporary table is bound to a session. Therefoe, if we call a function that creates a tempoary table multiple times in a single session, we encounter an error, because the table already exists.

To tackle this problem, we need to delete all temporary tables manually. Luckily, there is a special [`DISCARD`](https://www.postgresql.org/docs/current/sql-discard.html) command that can be used to dtop all temporary tables at once:
```SQL
DISCARD TEMPORARY;
```



# `DO` command
The [`DO` command](https://www.postgresql.org/docs/12/sql-do.html) can be used to execude an anonymus code block in any of the languages suported by PostgreSQL.
It behaves like a function with no parameters and no return value. Syntax:
```SQL
DO [LANGUAGE <lang name>] <code>
```

The default language is `plpgsql`.

Example:
```SQL
DO $$
BEGIN
	RAISE NOTICE 'Hello world';
END
$$
```


# Window functions
PostgreSQL supports an extended syntax for [window functions](https://www.postgresql.org/docs/current/tutorial-window.html).

We can use it for example to retrieve the value of a column that has maximum value in another column, as demonstrated in an [SO answer](https://stackoverflow.com/questions/73773017/sql-group-by-get-value-on-one-column-based-on-order-of-another-column).


# PostGis

## Geometry columns
Postgis features can be utilized with geometry and geography column types. To add a new geometry column:
```SQL
ADD COLUMN <COLUUMN NAME> geometry(<GEOMETRY TYPE>, <SRID>)
```

## Spatial Indexing
[Documentation](http://postgis.net/workshops/postgis-intro/indexing.html)

Analogously to standard SQL column indicis, there are spatial indices in PostGIS. The only difference is that we need to add the `USING GIST` at the end of the `CREATE INDEX` statement:
```SQL
CREATE INDEX nodes_geom_idx
  ON nodes
  USING GIST (geom);
```


## Converting between geometry types
There are dedicated functions whcich we can use to convert between geometry types:
- `ST_Multi`: converts geometries to their multi-variant, e.g., `LineString` to `MultiLineString`.


## Compute area surrounding geometries
If we are ok with a convex envelope of the geometries, we can simply use the [`St_ConvexHull`](https://postgis.net/docs/ST_ConvexHull.html) functon. Howeever, if we need the exact shape, We have to use the [`St_ConcaveHull`](https://postgis.net/docs/ST_ConcaveHull.html) function which computes the concave hull of a geometry.

The `St_ConcaveHull` function takes an additional parameter ` param_pctconvex` which determines how *concave* is the result: 0 means strictly concave, while 1 means convex hull. Note that while lowere values leads to more acurate results, the computation is much slower. There is also another parameter `param_allow_holes` which determines whether holes in the object are permited (default false).



## Split area to polygons based on points
The split of spece into polygons based on a set of points is called *Voronoi diagram*. In PostGIS, we have a [`ST_Voronoi_Polygons](https://postgis.net/docs/ST_VoronoiPolygons.html) for that. To obtain a set of polygons from a set of points, it is necessary to
1. Aggregate the rows (`ST_Collect`)
2. Compute the polygon geometry (`ST_Voronoi_Polygons`)
3. Disaggregate the geometry into individual polygons (`ST_Dump`)

Also, there is an important aspect of how far the polygons will reach outside of the points. By default, it enlarge the area determined by the points by about 50%. If we need a larger area, we can use the `extend_to` parameter. If we need a smaller area, however, we need to compute the intersection with this smaller area afterwards manually.

Full example:
```SQL
SELECT st_intersection(
	(st_dump(
		st_voronoipolygons(st_collect(<GEOMETRY COLUMN>))
	)).geom, 
	(<select clause for area of desired voronoi polygons>)
) AS geom FROM ...
```

**If we need to join the polygons to the original points, we need to do it manually** (e.g. by `JOIN ... ON ST_Within(<POINT COLUMN>, <VORONOI POLYGONS GEO DUMP>)` ).


## Other Useful Functions
- [`ST_Within`] `ST_Within`(A, B) if A is completly inside B
- [`ST_Intersects`](https://postgis.net/docs/ST_Intersects.html) `ST_Intersects(g1, g2)` if `g1` and `g2` have at least one point in common.
- [`ST_Transform`](https://postgis.net/docs/ST_Transform.html): `ST_Transform(g, srid)` transforms geometry `g` to a projection defined by the `srid` and returns the result as a geometry.
- [`ST_Buffer`](https://postgis.net/docs/ST_Buffer.html): `ST_Buffer(g, radius)` computes a geometry that is an extension of `g` by `radius` to all directions
- [`St_Collect`](https://postgis.net/docs/ST_Collect.html) aggregates data into single geometry. It is usually apllied to a geometry column in an SQL selection.
- [`ST_Union`](https://postgis.net/docs/ST_Union.html)
- [`ST_Area`](https://postgis.net/docs/ST_Area.html)
- [`ST_Equals`](https://postgis.net/docs/ST_Equals.html)
- [`ST_MakeLine`](https://postgis.net/docs/ST_MakeLine.html): make line between two points
- [`ST_SetSRID`](https://postgis.net/docs/ST_SetSRID.html): sets the `SRID` of the geometry and returns the result as a new geometry.
- [`ST_MakePoint`](https://postgis.net/docs/ST_MakePoint.html): creates a point geometry from the given coordinates.


# PgRouting
[PgRouting](https://pgrouting.org/) is a PostgreSQL extension focused on graph/network manpulation. It contains functions for:
- finding the strongly connected components: [`pgr_strongComponents](https://docs.pgrouting.org/latest/en/pgr_strongComponents.html#index-0)
- graph contraction/simplification


## Finding strongly connected components
The function [`pgr_strongComponents`](https://docs.pgrouting.org/latest/en/pgr_strongComponents.html#index-0) finds the strongly connected components of a graph. The only parameter of the script is a query that should return edge data in the folowing format:
- `id`, 
- `source`,
- `target`, 
- `cost`,
- `reverse_cost`.

The first three parameters are obvious. The cost parameter does not have any effect. **You should provide a negative `reverse_cost`, othervise, the edge will be considered as bidirectional!**



# PL/pgSQL
[PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html) is a procedural language available in PostgreSQL databases. It can be used inside:
- functions
- procedures
- `DO` command


## Branching
PL/pgSQL has the following branching:
```SQL
IF <condition> THEN
	...
[ELSEIF
	...
]
[ELSE
	...
]
END IF
```

## Logging
Basic logging can be done using the `RAISE` command:
```SQL
RAISE NOTICE 'Some message';
```

We can add parameters by using the `%` placeholder:
```SQL
RAISE NOTICE 'Some message %', <variable or SQL command>;
```
For more, see the [documentation](https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html).



## Query diagnostics
Various information about the last query can be obtained using the `GET DIAGNOSTIC` command. For example, the number of rows affected by the last query can be obtained using the `ROW_COUNT` parameter:
```SQL
GET DIAGNOSTIC <variable> = ROW_COUNT;
```
The result is stored in the variable `<variable>`.

Note that this constract is not available in the SQL queries but only in a PL/pgSQL block.

For other diagnostic fields, see the [documentation](https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-DIAGNOSTICS).



# `psql`
`psql` is a basic command line utitiltyfor manipulating postgres database. 

To connect:
```bash
psql -d <db name> 
```
Then the psql commands can be executed. To execute command immediatelly, use the `-c ` parameter:
```bash 
psql -d <db name> -c "<command>"
```
Do not forget to quote the command.



# Importing data from csv
The prefered mathod depends on the characte of the data: 
- data exactly match the table  in the database: use `psql` `COPY` command
- data do not match the table, but they are small: 
	1. load the data with pandas
	2. process the data as needed
	3. use `pandas.to_sql` to upload the data
- data do not match the table and they are large:
	1. preprocess the data with bach commands
	2. use `psql` `COPY` to upload the data
- data do not match the table and they are large *and dirty*: use the [`file_fdw`](https://www.postgresql.org/docs/current/file-fdw.html) module: 		
	1. create a table for SQL mapping with tolerant column types (e.g., text for problematic columns)
	2. select from the mapping to the real table

## `psql COPY` command
The `COPY` command can be used to copy the input into a database table. A subset of database column can be selected, but that is not true for the input, i.e, all input columns have to be used. If a subset of input columns needs to be used, or some columns requires processing, you need to perform some preprocessing.

[`COPY` manual](https://www.postgresql.org/docs/current/sql-copy.html)

# Importing data from a shapefile
There are multiple options:
- `shp2psql`: simple tool that creates sql from a shapefile
	- easy start, almost no configuration
	- always imports all data from shapefile, cannot be configured to skip columns
	- included in the Postgres instalation
- `ogr2ogr`
	- needs to be installed, part of GDAL
- `QGIS`
	- The db manger can be used to export data from `QGIS`
	- data can be viewed before import
	- only suitable for creating new table, not for appending to an existing one

# Importing data from GeoJSON
For a single geometry stored in a GeoJSON file, the function [`ST_GeomFromGeoJSON`](http://postgis.net/docs/ST_GeomFromGeoJSON.html) can be used.
- just copy the geometry part of the file
- change the geometry type to match the type in db
- don't forget to surround the object with curly brackets

For the whole document, the `ogr2ogr` tool can be used.


# Lost Password to the Postgres Server
The password for the db superuser is stored in db `postgres`. In order to log there and change it, the whole authentification has to be turned off, and then we can proceed with changing the password. Steps:
1. find the `pg_hba.conf file` 
	- usually located in `C:\Program Files\PostgreSQL\13\data`
2. backup the file and replace all occurances of `scram-sha-256` in the file with `trust`
3. restart the posgreSQL service
	- in the Windows service management, there should be a service for postgresql running
4. change the password for the superuser
	1. `psql -U postgres`
	2.  `ALTER USER postgres WITH password 'yourpassword';` (do not forget the semicolon at the end!)
5. restore the `pg_hba.conf` file from backup
6. restart the postgreSQL service again
7. test if the new password works

# DataGrip
## Import Formats
DataGrip can handle imports only from separator baset files (csv, tsv).

## View Geometry
In the reuslt window/tab, click on the gear wheel -> `Show GeoView`. However, the **geoviewer has a fixed WGS84 projection, so you have to project the result to this projection first**.

##  Create a spatial Index
There is currently no GUI tool for that in DataGrip. Just add a normal index and modify the auto generated statement by changing `<column>` to `USING GIST(<column>)` at the end of the statement.


## Filter out store procedures
1. right-click on `routines`
1. click `open table`
1. sort by type


## Creating functions and procedures
There is no UI available currently, use Navicat or console


## Duplicate table
Drag the table in the database explorer and drop it to the location you want it to copy to.



# Navicat
## Cannot connect to db
Symptoms:
- cant connect to db server: `Could not connect`
- after editing the connection and trying to save it (ok button): `connection is being used`

Try:
1. close navicat
2. open navicat, edit connection
1. click test connection
1. click ok, and start the connection by double click



# PgAdmin
The best way to install the PgAdmin is to use the [EDB PostgreSQL installer](https://www.postgresql.org/download/windows/) and uncheck the database installation during the installation configuration. This way, we also install useful tools like `psql`

## Diagrams
To create diagram from an existing database: right click on the database -> `Generate ERD`



# Kill a hanging query
To kill a hanging query, we need to complete two steps:
1. identify the query PID
1. kill the query

To identify the PID of the problematic query, we can use tool such as [`pg_activity`](https://github.com/dalibo/pg_activity):
```bash
sudo -u postgres pg_activity -U postgres
```

To kill the query, run:
```sql
SELECT pg_cancel_backend(<PID>)
```

# Troubleshooting
If the db tools are unresponsive on certain tasks/queries, check if the table needed for those queries is not locke by some problematic query.

## Select PostgreSQL version
```SQL
SELECT version()
```

## `Tried to send an out-of-range integer as a 2-byte value`
This error is caused by a too large number of values in the insert statement. The maximum index is a 2-byte number (max value: 32767). The solution is to split the insert statement into smaller bulks.




