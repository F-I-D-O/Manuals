


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

- [arrays](https://www.postgresql.org/docs/current/arrays.html)
- [array functions and operators](https://www.postgresql.org/docs/8.4/functions-array.html)

arrays are declared as `<type>[]`, e.g., `integer[]`. The type can be any type, including composite types.

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

This data type requires the `hstore` extension to be enabled in the database. To enable it, use the following command:
```SQL
CREATE EXTENSION hstore;
```

When we, exceptionally, want to access a variable from a hstore column, we can use the following syntax:
```SQL
SELECT <COLUMN NAME>-><VARIABLE NAME> AS ...
```


# Schemas
[official documentation](https://www.postgresql.org/docs/current/ddl-schemas.html)

Schemas in PostgreSQL are implemented as namespaces according to the SQL standard. 


## Search path
[official documentation](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATH)

Usually, we does not have to qualify the table name with the schema name, as the schema name is in the *search path*.

By default the search path is set to `"$user", public`, which means that the tables are first searched in the schema with the same name as the user, and then in the `public` schema.

To show the current search path, run:
```SQL
SHOW search_path;
```

To change the search path, run:
```SQL
SET search_path TO <schema name list>;
```



# Editing the database
The commands for editing the database mostly follows the SQL standard. 

## Creating objects (tables, indexes, etc.)
The syntax for creating objects is mostly the same as in the SQL standard: 
```SQL
CREATE <object type> <object name> <object parameters>
```

## `IF NOT EXISTS` modifier
An important modifier is the `IF NOT EXISTS` clause that prevents errors when the object already exists. This is very useful if we want to update the database schema that is in the development phase with some automated script without the need to drop the database every time. However, this modifier is not available for all objects. It is available for:

- `TABLE`
- `INDEX`
- `SEQUENCE`
- `VIEW`
- `MATERIALIZED VIEW`
- `PROCEDURE`
- `FUNCTION`
- `TRIGGER`

However, it is not available for:

- `DATABASE`
- `SCHEMA`
- `USER`
- `CONSTRAINT`

For these objects, we have to use some workaround. There are three options in general:

1. check if the object exists before creating it ([SO example with Constraint](https://stackoverflow.com/a/6804058/1827955))
2. delete the object before creating it
3. catch the error and ignore it ([SO example with Constraint](https://stackoverflow.com/a/32526723/1827955))




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



# Temporary tables
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


# Return data from `INSERT`, `UPDATE`, and `DELETE` statements
In PostgreSQL, the `INSERT`, `UPDATE`, and `DELETE` statements can return data with the `RETURNING` clause. The syntax is as follows:
```SQL
INSERT INTO <table name> ... RETURNING <column name>
```

This is especially useful when inserting data into a table with an auto-incrementing column, as we can retrieve the value of the column after the insert.


# Various specific tasks

## Selecting rows for deletion based on data from another table
If we want to delete rows from a table based on some condition on data from another table, we can use the `DELETE` statement with a `USING` clause. Example:
```SQL
DELETE FROM nodes_ways_speeds
USING nodes_ways
WHERE
    nodes_ways_speeds.to_node_ways_id = nodes_ways.id
	AND nodes_ways.area IN (5,6)
```


## Handeling duplicates in the `INSERT` statement
To handle duplicates on `INSERT`, PostgreSQL provides the `ON CONFLICT` clause (see the [`INSERT`](https://www.postgresql.org/docs/current/sql-insert.html) documentation).

The options are:

- `DO NOTHING`: do nothing
- `DO UPDATE SET <column name> = <value>`: update the column to the given value


## Random oredering
To order the result set randomly, we can use the `RANDOM()` function in the `ORDER BY` clause:
```SQL 
SELECT ...
FROM ...
ORDER BY RANDOM()
```

### Random ordering with a seed (Pseudo-random ordering)
To receive a determinisic (repeatable) random ordering, we can use the `setseed` function:
```SQL
SELECT setseed(0.5);
SELECT ...
FROM ...
ORDER BY RANDOM();
```

Note that we need two queries, one for setting the seed and one for the actual query. If we does not have an option to call arbitrary queries, we have to use `UNION`:
```SQL
SELECT col_1, ..., col_n FROM (
	SELECT _, null AS col_1, ..., null AS col_n FROM setseed(0.5)
	UNION ALL
	SELECT null AS _, col_1, ..., col_n
	FROM ...
	OFFSET 1
)
ORDER BY RANDOM()
```

The `OFFSET 1` is used to skip the first row, which is the result of the `setseed` function.

The union is the only way to guarantee that the seed will be set before the actual query. Other options, such as `WITH` or `SELECT ... FROM (SELECT setseed(0.5))` do not guarantee the order of execution, and produce a different result for each call.


# PostGis
PolsGIS is an extension for PostgreSQL that adds support for spatial data. 

To enable the extension, we need to:

1. install the extension
	- e.g., using the bundeled stack builder application
1. enable the extension in the database
	```SQL
	CREATE EXTENSION postgis;
	```

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
- [`ST_Equals`](https://postgis.net/docs/ST_Equals.html)
- [`ST_MakeLine`](https://postgis.net/docs/ST_MakeLine.html): make line between two points
- [`ST_SetSRID`](https://postgis.net/docs/ST_SetSRID.html): sets the `SRID` of the geometry and returns the result as a new geometry.
- [`ST_MakePoint`](https://postgis.net/docs/ST_MakePoint.html): creates a point geometry from the given coordinates.
- [`ST_Area`](https://postgis.net/docs/ST_Area.html): computes the area of a geometry. The units of the result are the same as the units of the `SRID` of the geometry (use UTM coordinate system for getting the area in square meters).


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
[Documentation](https://www.postgresql.org/docs/current/app-psql.html)

`psql` is a basic command line utitilty for manipulating postgres database. 

To connect, type:
```bash
psql -d <db name> 
```
Then the SQL commands can be executed. 

Note that no matter what SQL commands you plan to execute, **you have to connect to a specific database**. Ommitting the `-d` parameter will not connect you to the server in some admin mode, but instead, it will connect you to the default database, which is usually the database with the same name as the user name. If there is no such database, the connection will fail.

To execute command immediatelly without starting interactive session, use the `-c ` parameter:
```bash 
psql -d <db name> -c "<command>"
```
Do not forget to quote the command. Also, note that certain SQL commands, such as `CREATE DATABASE` requires its own session. To combine them with other SQL commands, you can use multiple `-c` parameters:
```bash
psql -d <db name> -c "CREATE DATABASE <db name>" -c "<other command>"
```

Other useful parameters:

- `-X`: do not read the `~/.psqlrc` file. This is useful when debuging the `psql` commands or running scripts, as it disables any customizations.
- `-U <user name>`: connect as a different user. If not specified, the current user is used.
- `-p`<port number>: specify the port number.  (default is 5432)


## meta-commands
The `psql` has its own set of commands, called *meta-commands*. These commands start with a backslash (`\`) and can be used inside SQL queries (either interactively, or in the -c argument). Example:
```bash
psql -d <db name> -c "\l+"
``` 
The above command lists all databases, including additional information.

Note that the **meta-commands cannot be combined with SQL queries passed to the `-c` parameter**. As `-c` argument, we can use either:

- a plain SQL query without any meta-commands
- a single meta-command without any SQL query (like the example above)

*(In* `\copy public.nodes FROM nodes.csv CSV HEADER`*, the string after `\copy` is a list of arguments, not an SQL query)*

When we want to combine a meta-command with an SQL query, we need to use some of the workarounds:

- use the `psql` interactive mode
- use the `psql` `--file` parameter to execute a script from a file
- pipe the commands to `psql` using `echo`:
	```bash
	echo "COPY (SELECT * FROM opendata.public.nodes WHERE area = 13) TO STDOUT WITH CSV HEADER \g 'nodes.csv'" | psql -d opendata
	```

# Importing data
A simple SQL data (database dump) can be imported using the `psql` command:
```bash
psql -d <db name> -f <file name>
```

we can also import from stdin by omitting the `-f` parameter:
```bash
psql -d <db name> < <file name>

# or
<command> | psql -d <db name>
```


## Importing compressed SQL dump
To import a compressed SQL dump we need to know how the dump was compressed. 

- If it was compressed using the `pg_dump` with the `-Z` parameter, we use a `pg_restore` command:
	```bash
	pg_restore -d <db name> <file name>
	```

- If it was compressed using a compression tool, we need to pipe the output to the decompression tool and then to `psql`:
	```bash
	<decompression tool> < <file name> | psql -d <db name>
	```


## Importing data from csv
The easiest way to import data from csv is to use the `psql` `\copy` meta-command:
```bash
psql -d <db name> -c "\copy <table name> FROM <file name> CSV HEADER"
```
The syntax of this command and its parameters is almost identical to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command. Important parameters:

- `CSV`: the file is in CSV format
- `HEADER`: the first line of the file contains column names

Except simplicity, the `\copy` command has another advantage over the `COPY` command: it has the same access rights as the user that is currently logged in. The `COPY` command, on the other hand, has the access rights of the user that started the database server. 

The `COPY` command, however, has an advantage over the `\copy` command when we access a remote database. In that case, the `\copy` command would first download the whole file to the client and then upload it to the server. The `COPY` command, on the other hand, can be executed directly on the server, so the data are not downloaded to the client.


### Importing data from csv with columns than are not in the db table
The `COPY` (and `\copy`) command can be used to copy the input into a database table even if it contains only a subset of database table columns. However, it does not work the other way, i.e, all input columns have to be used. If only a subset of input columns needs to be used, or some of the input columns requires processing, we need to use some workaround. The prefered mathod depends on the characte of the data: 

- data do not match the table, but they are small: 
	1. load the data with pandas
	2. process the data as needed
	3. use `pandas.to_sql` to upload the data
- data do not match the table and they are large:
	1. preprocess the data with batch commands
	2. use `COPY` (or `\copy`) to upload the data
- data do not match the table and they are large *and dirty*: use the [`file_fdw`](https://www.postgresql.org/docs/current/file-fdw.html) module: 		
	1. create a table for SQL mapping with tolerant column types (e.g., text for problematic columns)
	2. select from the mapping to the real table


## Importing data from a shapefile
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

## Importing data from GeoJSON
For a single geometry stored in a GeoJSON file, the function [`ST_GeomFromGeoJSON`](http://postgis.net/docs/ST_GeomFromGeoJSON.html) can be used.

- just copy the geometry part of the file
- change the geometry type to match the type in db
- don't forget to surround the object with curly brackets

For the whole document, the `ogr2ogr` tool can be used.


# Exporting data
The data can be exported to SQL using the `pg_dump` command. The simplest usage is:
```bash
pg_dump -f <output file name> <db name>
```
Important parameters:

- `-s`: export only the schema, not the data

If we need to further process the data, we can use the stdout as an output simply by omitting the `-f` parameter:
```bash
pg_dump <db name> | <command>
```


## Exporting the database server configuration
To export the database server configuration, we can use the `pg_dumpall` command:
```bash
pg_dumpall -f <output file name>
```


## Compressing the SQL dump
To compress the SQL dump, we have two options:

- use the `pg_dump` command with the `-Z` parameter, e.g., `pg_dump <db name> -Z1 -f <output file name>` or
- pipe the output to a compression tool, e.g., `pg_dump <db name> | gzip > <output file name>`


## Exporting data to csv
When exporting large data sets, it is not wise to export them as an SQL dump. To export data to csv, we can use either:

- `psql` `\copy` command
- `COPY` command in SQL

The simplest way is to use the `\copy` command. However, it may be slow if we call psql from a client and we want to export the data to a file on the server, because the data are first sent to the client and then back to the server. 

The `COPY` command is the fastest way to export data to the server. However, by default, it can be tricky to use, as the sql server needs to have write access to the file. To overcome this problem, we can use the following workaround:

1. choose `STDOUT` as an output for the `COPY` command
2. at the end of the command, add `\g <file name>` to redirect the output to a file.

Example:
```bash
echo "COPY (SELECT * FROM opendata.public.nodes WHERE area = 13) TO STDOUT WITH CSV HEADER \g 'nodes.csv'" | psql -d opendata
```


# Information and statistics
To show the **table size**, run:
```PostgreSQL
SELECT pg_size_pretty(pg_total_relation_size('<table name>'));
```

To show the **version** of the PostgreSQL server, run:
```PostgreSQL
SELECT version();
```

To list all **extensions** for a database, run:
```PostgreSQL
psql -d <db name> -c "\dx"
```

To check if a **specific table** exists, run:
```PostgreSQL
SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = '<schema_name>' AND table_name = '<table_name>');
```


## Databases
To list all databases, we can use the `-l` parameter:
```bash
psql -l
```

To get more information about the databases, we can use the `\l+` meta-command.

To check if a specific database exists, we can use the following query:
```SQL
SELECT EXISTS (SELECT 1 FROM pg_database WHERE datname = '<db name>');
```



# Managing the database clusters
As a first step, it is always good to know which clusters are installed and running. To show this information, use the `pg_lsclusters` command.

## Starting, stopping, and restarting the cluster

Sometimes it is needed to restart the cluster. There are two commands:

- `pg_ctl restart`: restarts the cluster
- `pg_ctl reload`: reloads the configuration of the cluster

Always check which one is needed in each case. For both commands, the path to the `data` directory of the cluster is needed. We can specify it in two ways:

- using the `-D` parameter of the `pg_ctl` command
- setting the `PGDATA` environment variable


## Monitoring activity
To monitor the activity on Linux, we can use the [`pg_activity`](https://github.com/dalibo/pg_activity):
```bash
sudo -u postgres pg_activity -U postgres
```

For a detailed monitoring on all platforms, we can use the *[Cumulative Statistics System](https://www.postgresql.org/docs/current/monitoring-stats.html)*. It contains collections of statistics that can be accessed similarly to tables. The difference is that these collections are server-wide and can be accessed from any database or scheme. Important collections:

- [`pg_stat_activity`](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW): contains information about the current activity on the server

### `pg_stat_activity`
The `pg_stat_activity` collection contains information about the current activity on the server. Some activities belong to background processes it is therefore best to query the collection like:
```SQL
SELECT * FROM pg_stat_activity WHERE state IS NOT NULL;
```



## Kill a hanging query
To kill the query, run:
```sql
SELECT pg_cancel_backend(<PID>)
```
The `PID` can be obtained from the [database activity monitoring tool](#monitoring-activity).



## Creating new user
For creating a new user, we can use the [`createuser`](https://www.postgresql.org/docs/current/app-createuser.html) command. Important parameters:

- `-P` or `--pwprompt`: prompt for password. If not used, the user will be created without a password.


## Deleting database
To delete a database, we can use the [`dropdb`](https://www.postgresql.org/docs/current/app-dropdb.html) command: `dropdb <db name>`


## Granting privileges


### Grant privileges for a database
To give privileges for creating new tables and other objects in a database:
```SQL
GRANT ALL PRIVILEGES ON DATABASE <db name> TO <user name>;
```

To give privileges for existing objects, it is best to change the owner of the objects.



### Grant privileges for database schema
To grant all privileges for a database schema to a user, we can use the following command:
```SQL
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user name>;
```

To grant only the `SELECT` privilege, use:
```SQL
GRANT SELECT ON ALL TABLES IN SCHEMA public TO <user name>;
```




## Upgrading the database cluster
With PostgreSQL version 9.3 and later, we can upgrade easily even between major versions using the [`pg_upgrade`](https://www.postgresql.org/docs/current/pgupgrade.html) command. We can even skip versions, e.g., upgrade from 12 to 16. 

The process is described in the pg_upgrade manual, however, usually, most of the steps are not necessary as they apply only to very specific cases. On top of that, some aspects important for the upgrade are not mentioned in the manual.

The steps for a typical ubuntu/debian installation are:

1. stop the new cluster using `systemctl stop postgresql@<version>-main`
2. run the `pg_upgrade` command with `--check` to check the compatibility
3. stop the old cluster using `systemctl stop postgresql`
4. run the `pg_upgrade` command without `--check` to perform the upgrade
5. apply all actions recommended by the `pg_upgrade` output
1. change the `port` in the `/etc/postgresql/<version>/main/postgresql.conf` file of the new cluster to the original port (usually 5432)
6. start the new cluster using `systemctl start postgresql@<version>-main` an check if the connection works

The standard `pg_upgrade` command looks like this:
```bash
sudo -u postgres pg_upgrade --link -j <number of cores> -b <old bin dir> -d <old data dir> -D <new data dir> -o 'config_file=<old conf file>' -O 'config_file=<new conf file>'
```
Description:

- `--link`: links the old data directory to the new one instead of copying the data. Fastest migration method.
- `<old bin dir>`: The `bin` directory of the old cluster.
	- usually `/usr/lib/postgresql/<old version>/bin`
- `<old/new data dir>`: The `data` directory of the cluster.
	- usually `/var/lib/postgresql/<old/new version>/main`.
	- Can be found using `pg_lsclusters`
- `<old/new conf file>`: The path to the `postgresql.conf` file.
	- usually `/etc/postgresql/<old/new version>/main/postgresql.conf`

## Upgrading extensions
Some PostgreSQL extensions uses separate libraries. These are installed fro each version of the PostgreSQL server separately. If a library is not foun on the new cluster, it is detected by the `pg_upgrade` command automaticly. In that case, you have to install the library according to the instructions of the library provider.


## Managing access to the database
To manage access to the database, we can use the `pg_hba.conf` file. 

This file is located in the `data` directory of the PostgreSQL installation. Unfortunately, the location of the `data` directory is not standardized, and the variants are many. However, there is a remedy, just execute the following SQL command:
```SQL
SHOW hba_file
```

[Documentation](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)


### Lost Password to the Postgres Server
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


## Configuration
[Documentation](https://www.postgresql.org/docs/current/config-setting.html)

PostgreSQL server can be configured using *parameters*. The parameters itself can be set in multiple ways:

- default values are set in the configuration file stored in the `<postgres data dir>/postgresql.conf`.
- the values can be set at runtime using SQL
- the values can be set at runtime using shell commands

### Getting and setting parameters at runtime using SQL
to get the value of a parameter, we can use the [`SHOW`](https://www.postgresql.org/docs/current/sql-show.html) command or the `current_setting` function:
```PostgreSQL
SHOW <parameter name>;
SELECT current_setting('<parameter name>');
```

To set the value of a parameter, we can use the [`SET`](https://www.postgresql.org/docs/current/sql-set.html) command or the `set_config` function:
```PostgreSQL
SET <parameter name> TO <value>;
SELECT set_config('<parameter name>', '<value>', false);
```
If the third parameter of the `set_config` function is set to `true`, the value is set for the current transaction only.

### Logging
[Documentation](https://www.postgresql.org/docs/current/runtime-config-logging.html)

The logs are stored in the `<postgres data dir>/log` directory. 

By default, only errors are logged. To logg statements, we need to change the `log_statement` parameter. Valid values are:

- `none`: no statements are logged
- `ddl`: only DDL statements are logged
- `mod`: only statements that modify the database are logged
- `all`: all statements are logged


## Garbage collection and optimization
There is a shared command for both garbage collection (vacuum) and optimization (analyze) of the database. To execute it from the command line, use the [vacuumdb`](https://www.postgresql.org/docs/current/app-vacuumdb.html) command.  



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

## Known issues and workarounds

## Cannot delete a database due to DataGrip's own connections
Before deleting a database we need to close all DataGrip sessions connected to the database. We can do that in the sessions window.

### DataGrip displays objects that were deleted
Sometimes, DataGrip displays objects that were deleted. Additionally, it it displays errors when trying to refresh the view. Solution:

1. right-click on database connection (root object in the database explorer)
1. click on `Diagnostics` -> `Force refresh`



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




# Troubleshooting
If the db tools are unresponsive on certain tasks/queries, check if the table needed for those queries is not locke by some problematic query.

## Select PostgreSQL version
```SQL
SELECT version()
```

## Select PostGIS version
```SQL
SELECT PostGIS_version()
```

## `Tried to send an out-of-range integer as a 2-byte value`
This error is caused by a too large number of values in the insert statement. The maximum index is a 2-byte number (max value: 32767). The solution is to split the insert statement into smaller bulks.




