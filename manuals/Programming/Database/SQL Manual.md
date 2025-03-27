SQL is a standard for relational databases. There is no complete implementation of the standard. The standard is not free, you have to pay for it. Therefore, it is sometimes hard to say what exactly is SQL and what is not.


# Operators
**Comparison** operators:

- `=`: equal
- `<>` or `!=`: not equal
- `>`: greater than
- `<`: less than
- `>=`: greater or equal
- `<=`: less or equal

**String** operators:

- `||`: concatenation
- `LIKE`: pattern matching


# Literals
In SQL, there are three basic types of literals:

- **numeric**: `1`, `1.2`, `1.2e3`
- **string**: `'string'`, `"string"`
- **boolean**: `true`, `false`

When we need a constant value for other types, we usually use either a constructor function or a specifically formatted string literal.

**String literals can also span multiple lines**, we do not need any operator to split the line (unlike in Python and despite the JetBrains IDEs adds a string concatenation operator automatically on newline).



# WITH
Statement for defining variables pointing to temporary data, that can be used in the related `SELECT` statement. Usage:
```sql
WITH <var> 
AS (<sql that assigns data to var>) 
<sql that use the variable>
```
Note that the **variable has to appear in the FROM clause**!

Multiple variables in the `WITH` statement ahould be delimited by a comma:
```SQL
WITH <var>  AS (<sql that assigns data to var>),
	<var 2> AS (<sql that assigns data to var 2>)
<sql that use the variables>
```


# SELECT
Most common SQL statement, syntax:
```SQL
SELECT <EXPRESSION> [AS <ALIAS>][, <EXPRESSION 2> [AS <ALIAS 2> ...]]
```
The most common expression is just a column name.

## Selecting row number
We can select row numbers using the function `ROW_SELECT()` in the `SELECT` statement:
```SQL
SELECT 
	...
	ROW_NUMBER() OVER([<PARTITIONING AND NUMBERING ORDER>]) AS <RESULT COLUMN NAME>,
	...
```
Inside the `OVER` statement, we can specify the order of the row numbering. Note however, that this does not order the result, for that, we use the `ORDER BY` statement. If we want the rown numbering to correspond with the row order in the result, we can left the `OVER` statement empty.


## Select unique rows
To select unique rows, we can use the `DISTINCT` keyword:
```sql
SELECT DISTINCT <column name> FROM ...
```


## Count selecting rows
The `count()` function can be used to count the selection. The standard syntax is:
```sql
SELECT count(1) FROM ...
```

### Count distinct
To count distinct values in a selection we can use:
```sql
SELECT count(DISTINCT <column name>) FROM...
```




## Select from another column if the specified column is NULL
We can use a replacement column using the `coalesce` function:
```sql
SELECT coalesce (<primary column>, <secondary column>)
```
The secondary column value will be used if the primary column value in the row is `NULL`.


## `UNION`
`UNION` and `UNION ALL` are important keywords that enables to merge query results verticaly, i.e., appending rows of one query to the results set of another.

The difference between them is that `UNION` discards duplicate rows, while `UNION ALL` keeps them

The `UNUION` statement appends one `SELECT` statement to another, but some statements that appears to be part of the `SELECT` needs to stay outside (i.e., be specified just once for the whole union), namely `ORDER BY`, and `LIMIT`. In contrast, the `GROUP BY` and `HAVING` statement stays inside each individual select.


## Select hardcoded values
For selecting hardcoded values, we can use the `VALUES` statement. The syntax is:
```sql
VALUES (<column 1>, <column 2>, ...), (<column 1>, <column 2>, ...), ...
```
Full example of selecting hardcoded values:
```sql
SELECT * FROM (VALUES (1, 'a'), (2, 'b')) AS t (id, label)
```


# JOIN
Classical syntax:
```SQL
JOIN <table name> [[AS] <ALIAS>] ON <CONDITION>
```
The alias is obligatory if there are duplicate names (e.g., we are joining one table twice)

## Types

- `INNER` (default): when there is nothing to join, the row is discarded
- `[LEFT/RIGHT/FULL] OUTER`: when there is nothing to join, the missing values are set to null
- `CROSS`: creates cartesian product between tables


## OUTER JOIN
The OUTER JOIN has three subtypes

- `LEFT`: joins right table to left, fills the missing rows on right with null
- `RIGHT`: joins left to right, fills the missing rows on left with null  	
- `FULL`: both `LEFT` and `RIGHT` `JOIN` is performend


## Properties

- When there are multiple matching rows, all of them are matched (i.e., it creates duplicit rows)
- If you want to filter the tables *before* join, you need to specify the condition inside `ON` caluse


## Join Only One Row

### Joining a specific row
Sometimes, we want to join only one row from many fulfilling some condition. One way to do that is to use a subquery:

```sql
SELECT * FROM a
JOIN (
	SELECT * FROM b ORDER BY column_in_b DESC LIMIT 1
)
```
This query joins table `b` to table `a`, using the row with the highest `column_in_b`. 

Note however, that all rows from `a` will be joined to the same row from `b`.  To use a different row from `b` depending on `a`, we need to look outside the subquery to filter out `b` according to `a`. **The folowing query, which should do exactly that, is invalid**:

```sql
SELECT * FROM a
JOIN (
	SELECT * FROM b 
	WHERE column_in_b <= a.column_in_a 
	ORDER BY column_in_b DESC 
	LIMIT 1
)
```

The problem here is that the subquery cannot refer the tables outside in, in the preceeeding `FROM` clause. Luckily, in the most use db systems, there is a magical keyword `LATERAL` that enables exacly that:

```sql
SELECT * FROM a
JOIN LATERAL (
	SELECT * FROM b 
	WHERE column_in_b <= a.column_in_a 
	ORDER BY column_in_b DESC 
	LIMIT 1
)
```

### Join random row
To join a random row, we can use the `RANDOM` function in ordering, e.g.:
```sql
SELECT * FROM a
JOIN (
	SELECT * FROM b ORDER BY RANDOM() LIMIT 1
)
```

However, this subquery is evaluated just once, hence we have the same problem as with the first example in this section:  **to every row in `a`, we are joining the same random row from `b`**. 

To force the db system to execute the subquery for each row in `a`, we need to refer `a` in the subquery, even with some useless filter (and of course we need a `LATERAL` join for that):

```sql
SELECT * FROM a
JOIN LATERAL(
	SELECT * FROM b WHERE a.column_in_a IS NOT NULL ORDER BY RANDOM() LIMIT 1
)
```


### Joining any row find active nodes
Sometimes, we need to join any matching row from B to find a set of active (referenced) rows in A. For example, we need to find a set of custommers with pending orders. 

IF the average number of matches in B is low, we proceed with normal join and then aggregate the results or use `DISTINCT`. However, sometimes, the average number of matching rows in B can be very high (e.g., finding all countries with at least one MC Donald). For those cases, the `LATERAL` join is again the solution:
```SQL
SELECT *
	FROM zones
	JOIN LATERAL (
		SELECT id AS request_id 
		FROM demand
		WHERE zones.id = demand.destination
		LIMIT 1
	) demand ON TRUE
```

For more information about the trade offs of this solution, check the [SO answer](https://stackoverflow.com/a/34715134/1827955)



## Getting All Combinations of Rows
This can be done using the `CROSS JOIN`, e.g.:
```sql 
SELECT * FROM table_a CROSS JOIN table_b
```

The proble arises when you want to filter one of the tables before joining, because **`CROSS JOIN` does not support the `ON` clause** (see more in [the Oracle docs](https://docs.oracle.com/javadb/10.8.3.0/ref/rrefsqljcrossjoin.html)).

Then you can use the equivalent `INNER JOIN`:
```
SELECT * FROM table_a INNER JOIN table_b ON true
```
Here you replace the true value with your intended condition.


## Inverse JOIN
Sometimes, it is useful to find all rows in table A that has no match in table B. The usual approach is to use LEFT JOIN and filter out non null rows after the join:
```SQL
SELECT ... FROM tableA
	LEFT JOIN tableB
WHERE tableB.id is NULL
```


## Joining a table on multiple options
There are situations, where we want to join a single table on multiple possible matches. For example, we want to match all people having birthday or name day the same day as some promotion is happanning. The foollowing query is a straighrorward solution:
```SQL
SELECT *
FROM promo
	JOIN people ON promo.date = people.birthaday OR promo.date = people.name_day
```
However, as we explain in the performance chapter, using OR in SQL is almost never a good solution. The usual way of gatting rid of `OR` is to use `IN`:
```SQL
SELECT *
FROM promo
	JOIN people ON promo.date IN(people.birthaday, people.name_day)
```
Nevertheless, this query can still lead to problems, despite being more compact. When we use any complex condition while joining tables, we risk poor performance. In general, it is better to use just simple column-to-column matches, even when there are more joins as a result. If you have performance problems, consult the "Replacing `OR`" section in the "Performance Optimization" chapter.





# GROUP BY
[wiki](https://en.wikipedia.org/wiki/Group_by_(SQL))

`GROUP BY` is used to aggregate data. Usual syntax:
```SQL
GROUP BY <LIST OF COLUMNS>
```
Note that we need to use some aggreagte function for all columns in the `SELECT` clause that are not present in the `GROUP BY` list. On the other hand, we can use columns not present in the `SELECT` in the `GROUP BY` statement.

## Using aggregate functions for the whole result set while using `GROUP BY`
If a query contains a `GROUP BY` statement, all aggregate functions (e.g., `count`, `avg`) are applied to groups, i.e., for each row of the result set. If we need to apply an aggregate function to the whole result set while using `GROUP BY`, we need to specify it using the `OVER` statement:
```SQL
SELECT count(1) OVER () as result_count
...
```
This will add a coulumn with a total count to each row of the result. If we do not need the actual groups, but only the distinct count, we can use a `LIMIT` statement.

## Get any row from each group
Sometimes, we need a value from a non-grouped column, but we do not care which one. The reson can be, for example, that we no that the values are the same for all rows in the group. There is no dedicated aggregation for this case, but we can use some simple ones as `MIN` or `MAX`.


# Window functions
Sometimes, we would need an aggregate function that somehow use two different columns (e.g., value of col A for the row where col B is largest). For that, we cannot use the classical aggregation, but we rather have to use a [*window function*](https://en.wikipedia.org/wiki/Window_function_(SQL)).

A window function is a function that for each row returns a value computed from one or multiple rows. 

Syntactically, we recognize a window function by the `OVER` clause that determines the rows used as an input for the function. Functions with the same name can exist as aggregate and window functions.

Window functions are evaluated after the `GROUP BY` clause and aggregate functions.


## Specifiing the range

- `()`: the whole result set
- `(PARTITION BY <column set>)`: the rows with the same values for that set of columns
We can also order the result for the selected range using `ORDER BY` inside the parantheses.

In some SQL dialects (e.g., PostgreSQL), there are even more sophisticated ways how to specify the range for the window functions.



# ORDER BY
By default, there is no guarantee that the result will be in any particular order. To sort the result, we need to add an `ORDER BY` statement at the end of the query:
```SQL
ORDER BY <LIST OF COLUMNS>
```





# `INSERT`
Standard syntax for the [`INSERT`](https://en.wikipedia.org/wiki/Insert_(SQL)) statement is
```sql
INSERT INTO <table>
(<col_1>, <col_2>,...)
VALUES (<val_1>, <val_2>,...)
```

If we fill all columns and we are confident with the column ordering, we can omit columns:

```sql
INSERT INTO <table>
VALUES (<val_1>, <val_2>,...)
```

Sometimes, we need to handle the eroro cases, e.g., the case when the record already exists. The solutions for these cases are, however, database specific. 


## INSERT SELECT
If we want to duplicate the records, we can use:
```sql
INSERT INTO <table> 
SELECT * FROM <table>  
[WHERE  <condition>]
```

If we need to fill some columns ourselfs:
```sql
INSERT INTO <table> (<col_1>, <col_2>,...)
SELECT <col_1>, <any expression> FROM <anything suported by select>  
[WHERE  <condition>]
```


# UPDATE
`UPDATE` query has the following structure:
```sql
UPDATE table_name
SET column1 = value1, column2 = value2...., columnN = valueN
WHERE <condition>
```
Unfortunately, the statement is ready to update *N* records with *one* set of values, but not to update *N* records with *N* set of values. To do that, we have only an option to select from another table: 

```sql
UPDATE table_name
SET column1 = other_table.column1  
FROM other_table WHERE other_table.id = table_name.id
```

**Don't forget the `WHERE` clause** here, otherwise, you are matching the whole result set returned by the `FROM` clause to each row of the table.

## Use the table for updating itself
If we are abou to update the table using date stored in int, we need to use aliases:
```SQL
UPDATE nodes_ways new SET way_id = ways.osm_id
FROM nodes_ways old
JOIN ways ON old.way_id = ways.id AND old.area = ways.area
WHERE new.way_id = old.way_id AND new.area = old.area AND new.position = old.position
```



# `DELETE`
To delete records from a table, we use the [`DELETE`](https://en.wikipedia.org/wiki/Delete_(SQL)) statement:
```sql
DELETE FROM <table_name> WHERE <condition>
```

If some data from another table are required for the selection of the records to be deleted, the syntax varies depending on the database engine. 



# `EXPLAIN`
Sources

- [official documentation](https://www.postgresql.org/docs/current/sql-explain.html) 
- [official cosumentation: usage](https://www.postgresql.org/docs/current/using-explain.html)
- https://docs.gitlab.com/ee/development/understanding_explain_plans.html

## Remarks:

- to show the actual run times, we need to run `EXPLAIN ANALYZE`

## Nodes
Sources

- [Plan nodes source code](https://gitlab.com/postgres/postgres/blob/master/src/include/nodes/plannodes.h)
- [PG documentation with nodes described](https://www.pgmustard.com/docs/explain)

Node example:
```

->  Parallel Seq Scan on records_mon  (cost=0.00..4053077.22 rows=2074111 width=6) (actual time=398.243..74465.389 rows=7221902 loops=2)
	Filter: ((trip_length_0_1_mi = '0'::double precision) AND (trip_length_1_2_mi = '0'::double precision) AND (trip_length_2_3_mi = '0'::double precision) AND (trip_length_3_4_mi = '0'::double precision) AND (trip_length_4_5_mi = '0'::double precision))
	Rows Removed by Filter: 8639817
	Buffers: shared hit=157989 read=3805864
```
Description:
In first parantheses, there are expected values:

- `cost` the estimated cost in arbitrary units.  The format is *startup cost..total cost*, where startup cost is a flat cost of the node, an init cost, while total cost is the estimated cost of the node. Averege per loop.
- `rows`: expected number of rows produced by this node. Averege per loop.
- `width` the width of each row in bytes

In the second parantheses, there are measured results:

- `actual time`: The measured execution time in miliseconds. The format is *startup time..total time*. 
- `rows` The real number of rows returned. 

The `Rows Removed by the Filter` indicates the number of rows that were filtered out.
The `Buffers` statistic shows the number of buffers used. Each buffer consists of 8 KB of data.

# Keys
Keys serves as a way of identifying table rows, they are **unique**.
There are many type of keys, see [databastar article](https://www.databasestar.com/database-keys/) for the terminology overview.

## Primary key
Most important keys in ORM are primary keys. Each table should have a single primary key. A primary key has to be non null.

When choosing primary key, we can either

- use a uniqu combination of database colums: a *natural key*
- use and extra column: *surogate key*

If we use a natural key and it is composed from multiple columns, we call it a *composite key*

The following table summarize the adventages and disadvantages of each of the solutions:
Area | Property | Natural key | Composite key | Surrogate key |
|-|-|-|-|-|
| usage | SQL joins | **easy** | hard | **easy** |
|| changing natural key columns | hard | hard | **easy** |
| Performance | extra space | **none** | A lot if there are reference tables, otherwise none | one extra column |
|| space for indexes | **normal** | extra | **normal**
|| extra insertion time | **no** | A lot if there are reference tables, otherwise none | yes |
|| join performance | suboptimal due to sparse values | even more sub-optimal due to sparse values | **optimal**

From the table above, we can see that using natural keys should be considered only if rows can be identified by a single column and we have a strong confidence in that natural id, specifically in its uniquness and timelessnes. 


## Non-primary (UNIQUE) keys
Sometimes, we need to enforse a uniqueness of a set of columns that does not compose a primary key (e.g., we use a surogate key). We can use a non primary key for that.

One of the differences between primary and non-primary keys is that non-primary keys can be null, and each of the null values is considered unique.



# Indices
Indices are essential for speeding queries containing conditions (including conditional joins).

The basic syntax for creating an index is:
```sql
CREATE INDEX <index name> ON <table name>(<column name>);
```

## Show Table Indices
MySQL:
```sql
SHOW INDEX FROM <tablename>;
```

PostgreSQL
```sql
SELECT * FROM pg_indexes WHERE tablename = '<tablename >';
```

### Show Indices From All Tables
MySQL:
```sql
SELECT DISTINCT TABLE_NAME, INDEX_NAME
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = '<schemaname>';
```


# CREATE TABLE
The syntax is:
```SQL
CREATE TABLE <TABLE NAME> (
	<COLUNM 1 NAME> <COLUNM 1 TYPE>,
	...
	<COLUNM N NAME> <COLUNM N TYPE>
	[, PRIMARY KEY (<LIST OF KEY COLUMNS>)]
)
```
The primary key is optional, but usually, any table should have one. Each row has to have a unique primary key. An index is created automatically for the list of primary key columns.


# ALTER TABLE
## Add column generated from other columns
SQL:
```sql
ALTER TABLE <table name> ADD <column name> AS (<generator expression>);
```

In MySQL we have to add the data type:
```sql
ALTER TABLE <tablename> ADD <columnname> <datatype> AS (<generator expression>);
```

In PostgreSQL, the syntax is quite different:
```sql
ALTER TABLE <tablename> ADD <columnname> <datatype> GENERATED ALWAYS AS (<generator expression>) STORED
```
The advantage of the Postgres approach is that the column is set as generated, therefore it is generated for the new rows automatically.



# Procedures and functions
In SQL there are two constructs that are able to encapsulate SQL statements to increase resusability and readability: functions and procedues. The main difference between these two is that functions are intended to be called inline from SLQ statements, while procedures cannot be used in SQL statements and instead, they are used as a wrapper of a set of SQL statement to be called repeatedly with different arguments. The extensive summary of the different capabilities of functions and procedures is on [SO](https://stackoverflow.com/questions/1179758/function-vs-stored-procedure-in-sql-server).

## Calling a procedure
The keyword for calling a procedure differs between database system, refer to the documentation for your system for the right keyword.


## Creating a procedure
The syntax for calling a procedure differs between database system, refer to the documentation for your system for the right syntax.


## Parameters
Procedures and functions can have parameters similar to parameters in programming languages. We can use those parameters in the body of a function/procedure equally as a column or constant.

Parameters can have **default values**, suplied after the `=` sign. We can test whether a default argument was supplied by testing the parameter for the default value.


# Views
Views are basically named SQL queries stored in database. The queries are run on each view invocation, unles the view is materialized.

The syntax is:
```SQL
CREATE VIEW <VIEW NAME> AS <QUERY>
```

## Modifying the view
The view can be modified with `CREATE OR REPLACE VIEW`, however, [existing columns cannot be changed](https://dba.stackexchange.com/questions/586/cant-rename-columns-in-postgresql-views-with-create-or-replace). If you need to change existing columns, drop the view first.


# Schemas
Schema in SQL is a container or namespace for tables, views, and other database objects. This means that we can have multiple objects with the same name in different schemas. 

**The SQL schema should not be confused with the database schema, which is a logical structure of the database.**

Sadly, the concept of SQL schema is not standardized across different database systems. The following table shows how SQL schema is implemented in different systems:

| Database System | Schema concept | default schema |
|-|-|-|
| MySQL | Databases are used as schemas | - |
| PostgreSQL | Multiple schemas in a single database as per the SQL standard | public |
| Oracle | Each user has an associated schema (user = schema) | user name |
| SQL Server | Multiple schemas in a single database as per the SQL standard | dbo |



# Performace Optimization
When the query is slow, first inspect the following checklist:

- Do not use `OR` or `IN` for a set of columns (see replacing `OR` below).
- Check that all column and combination of columns used in conditions (`WHERE`) are indexed.
- Check that all foreign keys are indexed.
- Check that all joins are simple joins (column to column, or set of columns to a matching set of columns).

If nothing from the above works, try to start with a simple query and add more complex pars to find where the problem is. 

If decomposing the query also does not bing light into the problem, refer to either one of the subsections below, or to the external sources.

Also, note that **some IDEs limits the number of returned rows automatically, which can hide serious problems** and confuse you. Try to remove the limit when testing the performance this way.


## Replacing `OR` 
We can slow down the query significantly using `OR` or `IN` statements if the set of available options is not constant (e.g., `IN(1, 2)` is okish, while `IN(origin, destination)` can have drastic performance impact).

To get rid of these disjunctioncs, we can use the `UNION` statement, basically duplicating the query. The resulting query will be double in size, but much faster:

```SQL
SELECT people.id
FROM promo
	JOIN people ON promo.date IN(people.birthaday, people.name_day);

-- can be revritten as

SELECT *
FROM promo
	JOIN people ON promo.date = people.birthaday
UNION 
SELECT *
FROM promo
	JOIN people ON promo.date = people.name_day
GROUP BY people.id
```


## A specific join makes the query slow
If a single join makes the query slow, there is a great chance that the index is not used for the join. Even if the table has an index on the referenced column(s), the join can still not use it if we are joining not to the table itself but to:

- a subquery,
- a variable created with a `WITH` statement,
- a view,
- or temborary table

created from the indexed table. You can solve the situation by creating a *materialized* view or temporary table instead, and adding inedices to the table manualy. Specifically, you need to split the query into multiple queries:

1. delete the materialized view/table if exists
1. create the materialized view/table
1. create the required indices
1. perform the actual query that utilizes th view/table

Of course we can skip the first three steps if the materialized view is constant for all queries, which is common during the testing phase.


## Slow `DELETE`
When the delete is slow, the cause can be the missing index on the child table that refers to the table we are deleting from.

Other possible causes are listed in the [SO answer](https://stackoverflow.com/questions/10901299/delete-statement-in-sql-is-very-slow).


## Sources
[Database development mistakes made by application developers](https://stackoverflow.com/questions/621884/database-development-mistakes-made-by-application-developers/621891#621891)


