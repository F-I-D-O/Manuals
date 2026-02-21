# Introduction

- [homepage](https://www.gurobi.com/)
- [Manual](https://docs.gurobi.com/projects/optimizer/en/current/)
- [Official Tutorials](https://support.gurobi.com/hc/en-us/articles/14165975461393-Tutorials-Getting-Started-with-the-Gurobi-APIs)

# Running Gurobi CLI
There are two gurobi command line tools:

- [`gurobi_cl`](https://www.gurobi.com/documentation/current/refman/grb_command_line_tool.html): for solving the optimization problems passed as a file
- `gurobi`: for running the interactive shell (ipython-like)



# Parallel Execution
The gurobi solver solves a problem in parallel by default, trying multiple solution methods at the same time (see the [official description](https://www.gurobi.com/documentation/9.5/refman/concurrent_optimizer.html)).

It is also possible to run multiple problems in parallel ([source](https://support.gurobi.com/hc/en-us/community/posts/360055837711-Solving-different-models-in-parallel-C-OpenMP-)), but each problem should be run in its own gurobi environment. Also, each environment should be configured to use only a single thread (e.g., in C++: `env.set(GRB_IntParam_Threads, 1);` ). 

The problem with this approach is that the CPU is usually not the bottleneck of the computation, the bottleneck is the memory ([source](https://groups.google.com/g/gurobi/c/JcUxe0YibZQ)). Therefore, solving multiple problems in parallel does not guarantee any speed up, it could be actually slower.

The performance could be most likely improved when running the problems in parallel on multiple machines (not multiple cores of the same machine). [Some advised to use MPI](https://support.gurobi.com/hc/en-us/community/posts/360077591892-Solving-thousands-of-QP-parallelly-on-a-machine-) for that.



# Model Parameters
[Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html)

In some (but not many) cases, we can improve the solution time by tuning the model parameters. The most important parameters are discussed here, for others, see the reference.


## Cuts
- [Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#cuts)

Cuts parameter affects the cutting plane generation.

Possible values:

- `-1`: automatic cuts (default)
- `0`: no cuts are generated
- `1`: moderate cut generation
- `2`: aggressive cut generation
- `3`: very aggressive cut generation

Thgis parameter can be overridden for a specific cut type through other parameters (e.g., `CliqueCuts` parameter).


## OutputFlag

- [Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#outputflag)

OutputFlag parameter is a toggle for the output of the solver (both in the console and in the log file).

Possible values:

- `0`: off
- `1`: on (default)

## PreCrush

- [Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#precrush)

PreCrush parameter affects the presolve behavior (see [Presolve](#presolve)).

- `0`: presolve creates models as reduced as possible (default)
- `1`: presolve preserve mapping between original and reduced model constraints. This setting is only useful if we want to add user-defined cuts.


## Presolve

- [Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#presolve)
- [Explanation](https://support.gurobi.com/hc/en-us/articles/360024738352-How-does-presolve-work)

The presolve heuristic works the following way:

1. A smaller model is created from the original model together with a mapping of the original variables to the smaller model variables.
    - this model is infeasible if and only if the original model is infeasible
    - if it has an optimal solution, it is the same as the optimal solution of the original model if the mapping is followed, and the solution values are the same
1. The smaller model is solved.
1. The solution of the smaller model is mapped back to the original model.

Possible parameters values:

- `-1`: automatic presolve (default)
- `0`: presolve is disabled
- `1`: conservative presolve
- `2`: aggressive presolve


# Undersanding Gurobi Logs
Typically, the Gurobi Solver logs in the following order:

1. Header message
    1. logging start message
    2. Output log path, if configured
    3. Gurobi version
    4. CPU info
2. Model info
3. Solution process info (depends on the model type, and configuration)
4. Solution info

## Solution Process Info
The solution process info depends on the model type, and configuration. For a typical MIP model, the process is:

1. Heuristic solution
1. Presolve
1. LP relaxation log
1. Integer solution log

### LP Log
Gurobi uses the [Barrier method](https://en.wikipedia.org/wiki/Interior-point_method) for solving LPs. The log in order contains (in order):

1. `Root barrier log...`
1. Ordering
1. Barrier statistics
1. Barrier iteration log


The barrier iteration log has the following columns:

- `Iter`: iteration number
- `Objective`: 
    - `Primal`: Objective value of the primal
    - `Dual`: Objective value of the dual
- `Residual`: 
    - `Primal`: Scaled measure of the primal feasibility error
    - `Dual`: Scaled measure of the dual feasibility error
- `Compl`: Scaled complementarity measure
- `Time`: Cumulative time

Under default setup, Gurobi typically stops iterating when values are as follows:

- both residuals are less than `1e-8`
- the `Compl` value is less than `1e-10`


# Gurobi in Python

- [Official Tutorial](https://support.gurobi.com/hc/en-us/articles/17278438215313-Tutorial-Getting-Started-with-the-Gurobi-Python-API)
- [Advanced Tutorial with dictionaries](https://support.gurobi.com/hc/en-us/articles/17307437899025-Tutorial-Getting-Started-with-the-Gurobi-Python-API-using-dictionaries)


## Tupledict
[Official Documentation](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tupledict.html#tupledict)

Tupledict is a dictionary that maps tuples to values, typically variables or constraints.

Typically, when we add multiple variables or constraints at once to the model, the returned object is a tupledict with indices matching the first arguments of the `addVars` or `addConstrs` methods.

To further modify the tupledict, we can use the array operators:

```Python
vdict = model.addVars(3, 2, name='v')
vdict[3, 0] = 1 # new variable outside of the index range above
```


## Variables
The variables are added using the [`addVar`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html#Model.addVar) method. The method has six arguments (all optional). Typically, we use the following three arguments:

- `vtype`: the type of the variable, one of the following:
    - `GRB.CONTINUOUS`: continuous variable (default)
    - `GRB.BINARY`: binary variable
    - `GRB.INTEGER`: integer variable
    - `GRB.SEMICONT`:
    - `GRB.SEMIINT`:
- `obj`: the objective function coefficient of the variable, default is `0`
- `name`: the name of the variable, default is `""`

Other than that, the arguments are:
- `lb`: the lower bound of the variable, default is `0`
- `ub`: the upper bound of the variable, default is `GRB.INFINITY`
- `column`: initial coefficients for the column (default is None)

The `addVar` method returns the created variable, representing it as a [`Var`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/var.html#Var) class instance.

### Add multiple variables at once
We can add multiple variables at once using the [`addVars`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html#Model.addVars) method.

The signature is the kind of similar to the `addVar` method, the biggest difference is that we have to supply an extra `indices` parameter that represents the index of the resulting variable collection. 

The `indices` parameter is a [variable length positional argument](Python%20Manual.md#variable-length-arguments). This means that we can enter any number of index arguments. The `addVars` method then creates a collection of variables that has the same number of dimensions as the number of index arguments, and each dimension will be indexed according to the corresponding index argument.

Each index may be specified as:

- A **single value**: in that case, the number marks the length of the dimension.
- A **list of values**: in that case, the list marks the values of the dimension.
- A **list of tuples**: in that case, each tuple specifies a single value for each dimension. This is useful when the index is sparse (contrary to the cartesian product of all indices).

Another special argument is the `name` argument. It is specified as constant, and the indices in the name are generated from the index arguments automatically.

Other `addVars` arguments can be set up in two ways:

- Using a scalar value: result in a constant value for all variables
- Using a collection proportional to the index:
    - list of values for one-dimensional index
    - dict with tuples as keys for multi-dimensional index

The 
    - 


The `addVars` method returns a [`tupledict`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tupledict.html#tupledict) object, which is a dictionary that maps the indices to the variables.


## Constraints
The constraints are added using the [`addConstr`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html#Model.addConstr) method. The method has two arguments:

- The *constraint expression*, and
- The name of the constraint

The name of the constraint is straightforward, it can be any ASCII string without spaces (so that we can export the model to LP format).

The constraint expression is, however, a complex topic, as:

- There are multiple types of constraints (e.g., linear, quadratic, indicator, integer, etc.), and
- Each type can be written in a variety of ways.

Here, we demonstrate various ways how to write a **linear constraint**. Other types of constraints are listed in the [TempConstr reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tempconstr.html#TempConstr) (a class representation of any constraint expression).

The linear constraint is in the form of `<Expression A> <Operator> <Expression B>`, where:

- `<Expression A>` and `<Expression B>` can be both constants or *linear expressions* and ,
- `<Operator>` is one of the following: `==`, `<=`, `>=`


### Add multiple constraints at once
We can add multiple constraints at once using the [`addConstrs`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html#Model.addConstrs) method. It has two arguments:

- The *generator*, and
- The name of the constraint

The name of the constraint is automatically generated similarly to the `addVars` method.

The generator is a Python generator function that produces a Gurobi constraint expression.



## Linear Expressions
The linear expression is represented by the [LinExpr](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/linexpr.html#LinExpr) class. There are several ways how to build a linear expression, here **sorted from slowest to fastest**:

- Using natural syntax:
    ```Python
    expr = x + 2*y + 3*z
    ```
    - this works because of operator overloading on the gurobi variable class
- using the [`quicksum`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/func_global.html#quicksum) Gurobi function
    ```Python
    expr = quicksum([1*x, 2*y, 3*z])
    ```
- using the [`add`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/linexpr.html#LinExpr.add) method:
    ```Python
    expr = LinExpr()
    expr.add(1, x)
    expr.add(2, y)
    expr.add(3, z)
    ```
- using the [`addTerms`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/linexpr.html#LinExpr.addTerms) method of the `LinExpr` class:
    ```Python
    expr = LinExpr()
    expr.addTerms([1, 2, 3], [x, y, z])
    ```
- using the [`LinExpr` constructor](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/linexpr.html#LinExpr.LinExpr):
    ```Python
    expr = LinExpr([1, 2, 3], [x, y, z])
    ```

### Creating a linear expression from a tupledict
Instead of creating linear expression from a list of variables and coefficients, we can use dedicated methods of the [`tupledict`](#tupledict) class that can be used to build a linear expression from a single variable type:

- [`sum()`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tupledict.html#tupledict.sum) for the sum of the variables.
- [`prod(coeffs)`](https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tupledict.html#tupledict.prod) for the product of the variables and coefficients, stored in a dictionary with the same indices as the tupledict.

For all these methods, we can use a pattern arguments. This argument limits the indices of the variables that are used in the expression. For example, in the expression bellow, we sum only the first row
```Python
var_dict = model.addVars(3, 2, name='v')
expr = var_dict.sum(0, '*') # sum of the first row: v[0, 0] + v[0, 1]
```







