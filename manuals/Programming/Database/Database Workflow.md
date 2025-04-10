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


# Visual Studio Code
A limited support for PostgreSQL is available as an extension in VS Code.

Limitations:

- syntax highlighting works only for basic SQL commands, no support for, e.g., PL/pgSQL. [[source]](https://github.com/Borvik/vscode-postgres/issues/167)
- outline view does not work for SQL files



# PostgreSQL
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

### Configuration with `postgresql.conf`
all the properties are there, we typically just need to uncomment them. 

Be awere of these syntactic rules:

- the `#` character is used for comments
- for directonary paths, use `/` as the path separator, never use `\`
- wrap paths in single quotes, not double quotes

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