fido7382


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
1. create the sequence:
	```SQL
	CREATE SEQUENCE <SEQUENCE NAME> OWNED BY <TABLE NAME>.<COLUMN NAME>;
	```
1. adjust the value of the sequence:
	```SQL
	SELECT setval(pg_get_serial_sequence('<TABLE NAME>', '<COLUMN NAME>'), max(<COLUMN NAME>)) FROM <TABLE NAME>;
	```
1. set the column to be incremented by the sequence:
	```SQL
	ALTER TABLE <TABLE NAME>
	ALTER COLUMN <COLUMN NAME> SET DEFAULT nextval('<SEQUENCE NAME>');
	```


## Strings
[official documentation](https://www.postgresql.org/docs/current/datatype-character.html)

The most important string type is `text`, it is a variable unlimited length string, like we know it from programming languages.

Other types are:

- `name`: An internal type for database object names. It is limited to 63 characters.

There are many string function available, including the `format` function that works similarly to the C format function. For all functions, check the [documentation](https://www.postgresql.org/docs/9.1/functions-string.html).


## Arrays

- [arrays](https://www.postgresql.org/docs/current/arrays.html)
- [array functions and operators](https://www.postgresql.org/docs/8.4/functions-array.html)

Arrays are **declared** as `<type>[]`, e.g., `integer[]`. The type can be any type, including composite types.

Array **literals** are declared using we use single quatation and curly brackets, e.g., `'{1, 2, 3}'`. For the same purpose, we can use the `ARRAY` constructtor sytax: `ARRAY[1, 2, 3]`. If we use the `ARRAY` constructor with an empty array, we have to specify the type of the array, e.g., `ARRAY[]::integer[]`. 

To compute array **length**, use `array_length(<array>, 1)` where `1` stands for the first dimension. Note that **most of the array functions return `NULL` if the array is empty.**


To check that some value match at least some member of the array, we use `ANY`:
```SQL
SELECT ...
FROM tab
WHERE tab.a = ANY(<array>)
```

### Working with the array members individualy
For using the members of an array in the `SELECT` or `JOIN`, we have to first split the array using the `unnest` function. This function transforms the result set to a form where there is a separate row for each member of the array (a kind of inverse operation to group by).

If we want to also keep the array index, we can use the `WITH ORDINALITY` expression, as shown in the [manual](https://www.postgresql.org/docs/current/functions-srf.html) or on [SO](https://stackoverflow.com/questions/8760419/postgresql-unnest-with-element-number).


### Converting a result set (query result) to an array
There are two ways to convert a result set to array in PostgreSQL:

- If we want to convert the whole result set to a single array, we use the [array constructor](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-ARRAY-CONSTRUCTORS):
	```SQL
	SELECT array(<query>);
	```
- If the query aggregates the rows and we want to create an array for each group, we use the `array_agg` function (see [aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html#FUNCTIONS-AGGREGATES)):
	```SQL
	SELECT array_agg(<column name>) FROM <table name>;
	```
	- note that counterintuitively, **the `array_agg` function returns `NULL` if the result set is empty, not an empty array.**


### Creating an array to a result set
The opposite operation to the section above is to convert an array to a result set. This can be done using the `unnest` function:
```SQL
SELECT unnest(<array>) AS <column name>;
```


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

Schemas in PostgreSQL are implemented as namespaces according to the SQL standard. They are intended to organize the database objects into logical groups. Unfortunately, they cannot be nested, so they can hardly be used as a replacement for namespaces/packages/modules in programming languages.


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

### `IF NOT EXISTS` modifier
An important modifier is the `IF NOT EXISTS` clause that prevents errors when the object already exists. This is very useful if we want to update the database schema that is in the development phase with some automated script without the need to drop the database every time. However, this modifier is not available for all objects. It is available for:

- `TABLE`
- `INDEX`
- `SEQUENCE`
- `VIEW`
- `MATERIALIZED VIEW`
- `PROCEDURE`
- `FUNCTION`
- `TRIGGER`
- `SCHEMA`

However, it is not available for:

- `DATABASE`
- `USER`
- `CONSTRAINT`

For these objects, we have to use some workaround. There are three options in general:

1. check if the object exists before creating it ([SO example with Constraint](https://stackoverflow.com/a/6804058/1827955))
2. delete the object before creating it
3. catch the error and ignore it ([SO example with Constraint](https://stackoverflow.com/a/32526723/1827955))



# Procedures and functions
To store a set of SQL commands for later use, PostgreSQL provides two options: procedures and functions. Both are similar and can use SQL, PL/pgSQL, or other languages supported by PostgreSQL. The key differences are:

- functions return a value, while procedures do not. However, procedures can return a value using an `OUT` parameter.
- functions can be called in SQL queries, while procedures require a separate `CALL` statement.
	- functions: `... SELECT <function name>(<function arguments>) ...`
	- procedures: `CALL <procedure name>(<procedure arguments>);`
- procedures can manage transactions, while functions cannot.


## Syntax
Both functions and procedures have the following syntax:

```SQL
CREATE OR REPLACE <FUNCTION/PROCEDURE> <name> (<parameters>)
<return definition - only for functions>
LANGUAGE <language name>
AS
<body>
```
where `<body>` can be both a delimited string:

```SQL
AS $$
<function content>
$$
```

OR an active SQL body, if we use SQL language (since PostgreSQL 14):

```SQL
BEGIN ATOMIC
	<sql statements>
END
```

There are some differences between those syntaxes (e.g., the second one works only for SQL and is evaluated/checked for validity at the time of creation), but in most cases, they are interchangable.

The `<function content>` depends on the language used:

- for SQL, it is a set of SQL statements
- for PL/pgSQL, it is a *block*. See the [functions and procedures](#functions-and-procedures) section of the PL/pgSQL chapter.


## Functions
To call a function, we use the `SELECT` statement:
```SQL
SELECT * FROM <function signature>
```

To create a function, we use the [CREATE FUNCTION statement](https://www.postgresql.org/docs/12/sql-createfunction.html).

Unlike for procedures, we need to specify a return type for function, either as an `OUT`/`INOUT` parameter, or using the `RETURNS` clause. To return tabular data, we use [`TABLE`](https://www.postgresql.org/docs/current/xfunc-sql.html#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE) return type:
```SQL
RETURNS TABLE(<param 1 name> <param 1 type>, ..., <param n name> <param n type>)
```

### Returning data
[Documentation](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING)

When using SQL language, we can return the data just by executing a `SELECT` statement:
```SQL
CREATE OR REPLACE FUNCTION <function name> (<parameters>)
LANGUAGE SQL
AS
$$
SELECT ...
$$
```

When using PL/pgSQL, we have to use the `RETURN` statement. To make it even more complicated, there are three versions of the `RETURN` statement:

- `RETURN <expression>`: This one is for:
	- returning a single scalar value
	- return from function with return type `void`. In this case, the `<expression>` is empty.
- `RETURN NEXT <expression>` and `RETURN QUERY <query>`: These are for returning a set of rows.

As the `RETURN NEXT` and `RETURN QUERY` do not terminate the function, we can mix them with the `RETURN` statement. Additionally, the `RETURN QUERY` can be used multiple times in a single function and therefore, it is valid to use all three versions in a single function.


#### `RETURN NEXT` and `RETURN QUERY`
[Documentation](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING-RETURN-NEXT)

For returning a set of rows (`table` or `setof` type) in `PL/PgSQL` , we have to use the `RETURN NEXT` or `RETURN QUERY` statement. Besides the fact that these statements are used for returning a set of rows, there is another important difference between them and the `RETURN` statement: **they do not terminate the execution of the function**. This is useful as sometimes, we need to do some cleanup after selecting the rows to be returned from function, or we need to build the result in a loop. In classical programming languages, we use variables for this purpose. In `PG/plSQL`, we can also use the [`RETURN NEXT` and `RETURN QUERY`](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-RETURNING) constructs. Example:

```SQL 
RETURN QUERY SELECT ...;
DROP TABLE target_ways;
RETURN;
```

The `RETURN QUERY` differs from `RETURN NEXT` in following ways:

- its argument is a query, not an expression. Therefore we can use it directly with the `SELECT` statement, instead of using a variable.
- it appends the result of the query to the result set. Therefore, it can be used multiple times in a single function.
- it cannot be used for returning a single value even if the query returns a single value. If we have a single value return type and need to do some postprocessing between selecting the value and returning from the function, we have to use a variable instead.


## Procedures
To exectue a stored procedure, use:
```SQL
CALL <procedure name>(<procedure arguments>);
```

To create a procedure, use the [`CREATE PROCEDURE` command](
https://www.postgresql.org/docs/current/sql-createprocedure.html). The syntax is as follows:
```SQL
CREATE PROCEDURE <name> (<params>)
LANGUAGE <language name>
<procedure body>
```



## Function and procedure parameters
The definition of parameters of functions and procedures are composed of three parts:

1. mode: `IN`, `OUT`, or `INOUT` (optional, default is `IN`)
2. name: the name of the parameter (optional, default for `OUT` parameters generated)
3. type: the type of the parameter

Unlike in programing languages, there is no implicit type cast of the program arguments, including literals. Therefore, we need to cast all parameters explicitely, as in the following example:

```SQL
CREATE OR REPLACE PROCEDURE compute_speeds_for_segments(target_area_id smallint)
...

CALL compute_speeds_for_segments(1::smallint);
```


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


## Organizing functions and procedures
A natural task that emerge if there is a lot of functions and procedures is to organize them into packages. Unfortunately, PostgreSQL does not support any such feature. The closest thing is a schema, however, schemas are not suitable for this purpose, as they cannot be nested.



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



# PL/pgSQL
[PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html) is a procedural language available in PostgreSQL databases. It can be used inside:

- functions
- procedures
- `DO` command

## Blocks
[Documentation](https://www.postgresql.org/docs/8.1/plpgsql-structure.html)

The base components of PL/pgSQL is a *block*. It's syntax is as follows:
```SQL
DECLARE
	<variable declarations>
BEGIN
	<statements>
END
```
Here, the `DECLARE` part is optional.

In a block, each statement or declaration ends with a semicolon.

We can nest the blocks, i.e., we can put a block inside another block, between the `BEGIN` and `END` keywords. In this case, we put a semicolon after the inner block. Only the outer block that contains the whole content of the function/procedure/`DO` command does not require a semicolon.

## Variables
In PL/PgSQL, all variables must be [*declared*](https://www.postgresql.org/docs/current/plpgsql-declarations.html) before assignmant in the `DECLARE` block which is before the sql body of the function/procedure/`DO`. The syntax is:
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

Nothe that **`:=` is also a valid assignment operator**. There is no difference between `=` and `:=` in plpgsql. The `:=` operator is sometimes preferred to avoid confusion with the `=` operator used for comparison. 


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

Note that the behavior of the assignment may not be intuitive:

- **if the `SELECT` statement returns no rows, the variable is set to `NULL`**
- if the `SELECT` statement returns more than one row, an error is raised


## Functions and procedures

The syntax of a PL/pgSQL function content is a *block*


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

Note that `NULL` values are treated the same as in SQL: **if the condition evaluates to `NULL`, the branch is not executed**. This is different from other programming languages, where `NULL` is treated as `false`.

## Logging
[documentation](https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html).

Basic logging can be done using the `RAISE` command:
```SQL
RAISE NOTICE 'Some message';
```

We can add parameters by using the `%` placeholder:
```SQL
RAISE NOTICE 'Some message %', <expression>;
```

Only scalar expressions are allowed as parameters. If we need to log multiple rows, we have to use a loop:
```SQL
FOR row IN SELECT ... LOOP
	RAISE NOTICE 'Some message %, %', row.column_1, row.column_2;
END LOOP;
```


## Executing functions

In SQL, any function is executed using the `SELECT` statement:
```SQL
SELECT * FROM <function name>(<function arguments>); -- for functions with return value

SELECT <function name>(<function arguments>); -- for functions returning void or if we do not care about the return value
```

In PL/pgSQL, the second syntax where the return value is not used is not allowed. Instead, we have to use the `PERFORM` statement:
```SQL
PERFORM <function name>(<function arguments>);
```

## Exceptions
In PL/pgSQL, we can have both exceptions raised by the database and exceptions that are manually raised in user code.


### Handling exceptions
[Documentation](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-ERROR-TRAPPING)

In PL/pgSQL, we can handle exceptions by extending the block with the `EXCEPTION` part. The syntax is as follows:
```SQL
BEGIN
	...
EXCEPTION
	WHEN <exception condition> THEN
		<exception handling>
END
```

The list of valid exception names can be found in the [documentation](https://www.postgresql.org/docs/current/errcodes-appendix.html). The most common exceptions are:


- `P0001`, `raise_exception`: A user-raised exception that does not specify the SQLSTATE.
- `00000`, `successful_completion`: The normal completion of a statement. No exception should ever be raised with this SQLSTATE.

The `<exception handling>` part can be any valid PL/pgSQL code. It can contain multiple statements and can be nested.

The `<exception condition>` can have three forms:

- `WHEN <exception name>`: catches the exception with the specified name
- `WHEN SQLSTATE '<SQLSTATE>'`: catches the exception with the specified SQLSTATE
- `WHEN OTHERS`: catches all exceptions that are not caught by the previous `WHEN` clauses

There can be many `WHEN` clauses in a single `EXCEPTION` block. If there is no matching `WHEN` clause for the exception, the exception is propagated as if there was no `EXCEPTION` block at all.

Note that the **code `00000` cannot be caught by the `WHEN '00000'` clause. Such condition is interpreted as `WHEN OTHERS`**.

When handling an exception, we can use two special built-in variables:

- `SQLSTATE`: the SQLSTATE of the exception - a five-character code that specifies the exception type
- `SQLERRM`: the error message of the exception

### Raising exceptions
[Documentation](https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html)

To raise an exception, we use the `RAISE` statement, the same as for logging. The difference is in the level parameter, which we must set to `EXCEPTION` (default):
```SQL
RAISE EXCEPTION 'Some message'; -- exception
RAISE 'Some message'; -- exception
RAISE <another level> 'Some message'; -- just a message
```




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



# PgRouting
[documentation](https://docs.pgrouting.org/latest/en/index.html)


[PgRouting](https://pgrouting.org/) is a PostgreSQL extension focused on graph/network manpulation. It contains functions for:

- finding the strongly connected components: [`pgr_strongComponents`](https://docs.pgrouting.org/latest/en/pgr_strongComponents.html#index-0)
- [graph contraction/simplification](https://docs.pgrouting.org/latest/en/contraction-family.html): [`pgr_contraction`](https://docs.pgrouting.org/latest/en/pgr_contraction.html)
- creating vertices from edges: [`pgr_createVerticesTable`](https://docs.pgrouting.org/latest/en/pgr_createVerticesTable.html)


## Finding strongly connected components
The function [`pgr_strongComponents`](https://docs.pgrouting.org/latest/en/pgr_strongComponents.html#index-0) finds the strongly connected components of a graph. The only parameter of the script is a query that should return edge data in the folowing format:

- `id`, 
- `source`,
- `target`, 
- `cost`,
- `reverse_cost`.

The first three parameters are obvious. The cost parameter does not have any effect. **You should provide a negative `reverse_cost`, othervise, the edge will be considered as bidirectional!**


## Creating vertices from edges
The function [`pgr_createVerticesTable`](https://docs.pgrouting.org/latest/en/pgr_createVerticesTable.html) creates a table of vertices from a table of edges. The function has the following parameters:

- `edges_table`: the name of the table with edges. It must be a standard table, temporary tables are not supported.
- `the_geom`: the name of the geometry column in the `edges_table`
- `source`: the name of the source column in the `edges_table`
- `target`: the name of the target column in the `edges_table`

The return value is `OK` if the function was successful and `FAIL` if it was not.

The created vertices table is named `<edges_table>_vertices_pgr` and contains the following columns:

- `id`: the id of the vertex
- `the_geom`: the geometry of the vertex
- `cnt`: the number of edges that are connected to the vertex
- `chk`: an integer that indicates if the vertex might have a problem. 
- `ein`: the number of incoming edges
- `eout`: the number of outgoing edges

Note that **only the `id`, and `the_geom` columns are filled with data. The other columns are filled with `NULL`.** 

To fill the `cnt` and `chk` columns, we can use the [`pgr_analyzeGraph`](https://docs.pgrouting.org/latest/en/pgr_analyzeGraph.html) function. 

To fill all columns, we need to use the [`pgr_analyzeOneway`](https://docs.pgrouting.org/latest/en/pgr_analyzeOneway.html) function. However, this function is cumbersome to use, as it requires a lot of parameters.



# Testing with PgTAP
[Official documentation](https://pgtap.org/documentation.html)

[PgTAP](https://pgtap.org/) is the only testing framework for PostgreSQL.

## Installation

### Linux
If you are using Linux, you may (depending on your distribution) be able to use you distribution’s package management system to install pgTAP. For instance, on Debian, Ubuntu, or Linux Mint pgTAP can be installed with the command: `sudo apt-get install pgtap`

On other systems pgTAP has to be downloaded and built. First, download pgTAP from [PGXN](https://pgxn.org/dist/pgtap/) (click the green download button in the upper-right). Extract the downloaded zip file, and (at the command line) navigate to the extracted folder.

To build pgTAP and install it into a PostgreSQL database, run the following commands:

``` sh
make
make install
make installcheck
```

### Windows
To install pgtap for PostgreSQL on Windows, follow these steps:

1. Clone the [pgtap repository](https://github.com/theory/pgtap)
2. Open PowerShell (`pwsh`) as an Administrator
    - it is necessary to copy files into the `ProgramFiles` directory.
1. run the [`pgtap_install.ps1`](https://gist.github.com/F-I-D-O/7752c29590f2867ce502590453ed04e7) script as an administrator with the following command:
    ``` PowerShell
    pgtap_install.ps1 <path to pgtap clone>
    ```
    - This script will copy the necessary files to the PostgreSQL installation directory.

These instructions were adapted from [issue#192](https://github.com/theory/pgtap/issues/192#issuecomment-960033060) of the pgtap repository.


## Basic Usage - Test scripts
The easiest way to write tests in PgTAP is to write procedural SQL scripts that contain the tests. The basic test can look like this:
```SQL
BEGIN; -- Start a transaction

-- Specify that we plan to run 2 tests
SELECT plan(2);

-- Test 1: Check if basic arithmetic works as expected
SELECT is(1 + 1, 2, '1 + 1 equals 2');

-- Test 2: Verify string concatenation
SELECT is('Hello ' || 'World', 'Hello World', 'String concatenation works');
--

-- Run the tests and return results
SELECT * FROM finish();

ROLLBACK; -- Rollback the transaction
```

here, we create two assertions using the `is` function from the `pgtap` library. Then, we run the tests using the `finish` function. The whole test is wrapped in a transaction, so the database is not modified by the test.

To execute the test, we can:

- run the test SQL directly in the SQL console or with the `psql` command
- use the `pg_prove` command to run the test from the command line

## `pg_prove`
The `pg_prove` is a Perl test runner that can be used to run the pgtap tests. We need to install it first using `cpanm TAP::Parser::SourceHandler::pgTAP`.

Then, we can use it as:
```bash
pg_prove -d <db name> -U <user name> <test file>
```


## Test as functions
Instead of writing the tests in a procedural SQL script, we can write them as functions (**but not procedures!**). This can help as organizing tests and also to prepare the data for the tests.

There is also a runner function [`runtests`](https://pgtap.org/documentation.html#runtests) that can be used to run multiple tests at once:
```SQL
SELECT * FROM runtests();
```

This function has four variants:

- `runtests()`,
- `runtests(<schema>)`,
- `runtests(<pattern>)`, and
- `runtests(<schema>, <pattern>)`.

The `schema` parameter is used to specify the schema where the tests are searched. The `pattern` parameter is used to specify the pattern that the test names must match. The pattern uses the same syntax as the `LIKE` operator in SQL.

### Fixtues
Sometimes, we need to call some functions before and after the tests. We can indeed call these functions in from the test functions, but in case we need to run the same functions for multiple tests, it is desirable to automate this process using fixtures. The `runtests` function supports fixtures, it recognize them by the prefix. Again, only functions, not procedures are supported. The following fixtures are supported:

- `startup`: runs before the tests
- `setup`: runs before each test
- `teardown`: runs after each test
- `shutdown`: runs after the tests

Unfortunatelly, the **fixture search does not reflect the `<pattern>`**. Therefore, all fixtures in the schema are always run. To overcome this, we have to supply a custom function for executing the tests.


## Test assertions
PgTAP provides a set of functions that works as test assertions. Notable functions are:

- `ok(<condition>, <message>)`: checks if the `<condition>` is true
	- the `<message>` is optional
- [`throws_ok(<sql>, <error_code>, <error_message>, <message>)`](get_ways_in_target_area_): checks if the `<sql>` throws an exception 
	- all parameters except the `<sql>` are optional


# XML
[documentation](https://www.postgresql.org/docs/current/functions-xml.html)

PostgreSQL has a built-in support for XML. 

Important functions:

- [`xpath(<path>, <text>, <namespace bindings>)`](https://www.postgresql.org/docs/current/functions-xml.html#FUNCTIONS-XML-PROCESSING-XPATH): returns an array of XML nodes that match the given `<path>` evaluated on the given `<text>`. 

Besides functions, there is a powerful [`XMLTABLE` expression](#xmltable) that can be used to extract tabular data from XML documents.


## Handling XML namespaces
All XML methods in PostgreSQL require the namespace bindings to be specified, as per the XPath standard. The only exception is when work with XML documents that do not use namespaces.

We specify the namespace bindings as an array of arrays, where each inner array has two elements: the prefix and the namespace URI. Example:
```SQL
SELECT xpath(
	'/ns:root/ns:child', 
	'<root xmlns:ns="http://example.com/ns"><child>...</child></root>', 
	ARRAY[ARRAY['ns', 'http://example.com/ns']]);
```

Note that the namespace prefixes specified in the bindings are completely unrelated to the prefixes used in the XML document. They may be the same, but they do not have to be. 

Also don't forget that XPath requires the namespace prefixes even for the default namespace. 



## `XMLTABLE`
[Documentation](https://www.postgresql.org/docs/current/functions-xml.html#FUNCTIONS-XML-PROCESSING-XMLTABLE)

`XMLTABLE` expression can extract tabular data from XML documents. The syntax is as follows:
```SQL
XMLTABLE(
	[XMLNAMESPACES(<namespace bindings>),]
	<xpath expression>, PASSING <xml document expression> 
	COLUMNS
		<column name> <data type> PATH <xpath relative expression>,
		...
		<column name> <data type> PATH <xpath relative expression>
)
```

If the XML document contains namespaces, we have to specify the namespace bindings in the `XMLNAMESPACES` clause. The `<namespace bindings>` is a comma-separated list of namespace bindings in the format `<namespace URI> AS <prefix>`. Example:
```SQL
 XMLNAMESPACES(
	'http://graphml.graphdrawing.org/xmlns' AS dns,
	'http://www.yworks.com/xml/yfiles-common/3.0' AS y
)
```
The `<xpath expression>` is an XPath expression that specifies the path to the XML nodes from which we want to extract data. The `<xpath relative expression>` is then another XPath expression that is relative to the `<xpath expression>` and specifies the path to the XML nodes or attributes used to fill a specific column.

The `<xml document expression>` is an expression that evaluates to an XML document. Typically, it is a column in the select statement, or a subquery. Example:
```SQL
SELECT some_element FROM xml_documents, XMLTABLE(
	XMLNAMESPACES(...),
	'/dns:graph/dns:node' PASSING xml_document.xml_data
	COLUMNS some_element TEXT PATH ...
) FROM xml_documents WHERE id = 1;
```

Note that the *`XMLTABLE`* expression may only be used in the `FROM` clause. Therefore, if we, for example, need to join the result of the `XMLTABLE`, instead of using: 
```SQL
JOIN XMLTABLE(...)
```
we have to use:
```SQL
JOIN (SELECT <columns> FROM XMLTABLE(...))
```



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




