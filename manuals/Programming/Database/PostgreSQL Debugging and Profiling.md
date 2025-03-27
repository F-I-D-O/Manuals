# Interpreting Error Messages
If there is an error in a function, the line number of the error refers to the line number in the function body (from the opening quotes), not including the function declaration. 

# Debugging
There is a debugger included in PostgreSQL. However its support in IDEs is limited: 

- DataGrip: No built-in support.
    - there is a [plugin](https://plugins.jetbrains.com/plugin/18419-postgresql-debugger) but it is outdated.
- pgAdmin: There is a [debugger](https://www.pgadmin.org/docs/pgadmin4/latest/debugger.html).


## Debugging with pgAdmin
[oficial documentation](https://www.pgadmin.org/docs/pgadmin4/latest/debugger.html)

First, it is necessary to activate the debugger on the server:

1. Open the `postgresql.conf` file
2. Set the `shared_preload_libraries` parameter to `<PostgreSQL installation directory>/lib/plugin_debugger`
3. Restart the server

Then, the debugger extension must be installed on target database:

```sql
CREATE EXTENSION pldbgapi;
```

Now, we can debug a function:

1. Right-click on the function in the `pgAdmin` tree and select `Debugging` > `Set Breakpoint`
1. Call the function, the debugger will stop at the breakpoint