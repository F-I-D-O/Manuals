# Running Gurobi CLI
There are two gurobi command line tools: 
- [`gurobi_cl`](https://www.gurobi.com/documentation/current/refman/grb_command_line_tool.html): for solving the optimization problems passed as a file
- `gurobi`: for running the interactive shell (ipython-like)


# Parallel Execution
The gurobi solver solves a problem in parallel by default, trying multiple solution methods at the same time (see the [official description](https://www.gurobi.com/documentation/9.5/refman/concurrent_optimizer.html)).

It is also possible to run multiple problems in parallel ([source](https://support.gurobi.com/hc/en-us/community/posts/360055837711-Solving-different-models-in-parallel-C-OpenMP-)), but each problem should be run in its own gurobi environment. Also, each environment should be configured to use only a single thread (e.g., in C++: `env.set(GRB_IntParam_Threads, 1);` ). 

The problem with this approach is that the CPU is usually not the bottleneck of the computation, the bottleneck is the memory ([source](https://groups.google.com/g/gurobi/c/JcUxe0YibZQ)). Therefore, solving multiple problems in parallel does not guarantee any speed up, it could be actually slower.

The performance could be most likely improved when running the problems in parallel on multiple machines (not multiple cores of the same machine). [Some advised to use MPI](https://support.gurobi.com/hc/en-us/community/posts/360077591892-Solving-thousands-of-QP-parallelly-on-a-machine-) for that.


