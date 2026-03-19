# Using the debugger
Pycharm has a build in debugger, however, there are some tricky problems described below.

## Breaking on Exception
Breaking on exception is one of the most important debugger tools. However, there are some problems with Pycharm exception debugging.

### Breake on Termination vs on Raise
By default, the program breakes on termination (unhandled exception). This is usually a correct configuration. However, in jupyter, all exceptions are caught to not break the jupyter itself. Therefore, **in jupyter, all exceptions are ignored by the debugger if the breakpoins are set to break on termination.**

To break on exceptions in jupyter, we have to breake on raise. By this setting, however, we stop even on expected/handeled exceptions, stoping potentially on hundereds breakpoints in library code.

Another issue is with the setting itself. **To propagate the change between breaking on raise/termination, we have to deactivate and then activate again the exception breakpoints, otherwise, the setting is ignored.**


# Profiling
Profiling in Python is surprisingly difficult compared to other languages. There is no all-in-one profiler for Python, and most of the profilers fail to analyze complex code and thus are unreliable. The table below summarizes the situation:

| Profiler | Reliable | Granularity | Call Graph | Mode | Code Modif. Required | Scrip must finish | <div style="width: 200px;">Notes</div> |
| -- | -- | -- | -- | -- | -- | -- | -- |
| [cProfile](#cprofile) | Yes | function-level | No | Det. | No | Yes | Included in the standard library. Mostly useful as a backend for other profilers |
| [PyCharm](#pycharm-profiler) | Partially | function-level | incomplete and confusing | Det. | No | No | Built-in profiler in PyCharm. By default, it uses cProfile as a backend. |
| [line_profiler](#line-profiler) | Yes | line-level | No | Det. | Yes | Yes | |
| [pyinstrument](#pyinstrument) | Yes | function-level | Yes | Sampling | No | Yes | Both command line and HTML GUI |
| [py-spy](https://github.com/benfred/py-spy) | ? | function-level | No | Sampling | No | Yes | Broken on Windows |
| [Scalene](#scalene) | No | line-level | No | Sampling | No | Yes | Absolutely random results |


Typically, **the best profiling approach is**:

1. find the functions that are taking the most time using pyinstrument
1. If we need to find specific lines of a function, use line_profiler for just that specific function identified as a bottleneck using pyinstrument


## pyinstrument

- [GitHub](https://github.com/joerick/pyinstrument)
- [Documentation](https://pyinstrument.readthedocs.io/en/stable/home.html)

The pyinstrument profiler is the most reliable profiler that provides a call tree. Usage

1. Run the profiler: `pyinstrument <script> <script arguments>`.
    - the results are displayed immediately in the terminal
2. Explore the results: `pyinstrument --load-prev <previous profile name>`. Parameters:
    - `--show-all`: show all functions, including library functions
    - `-r`: render variant. Possible values:
        - `html`: HTML output

## Line Profiler
[GitHub](https://github.com/pyutils/line_profiler)

The line_profiler package provides line-by-line profiling of the code. Unfortunately, the [corresponding PyCharm plugin](https://plugins.jetbrains.com/plugin/16536-line-profiler) is currently broken and [does not work with latest PyCharm version (2025.2)](https://gitlab.com/line-profiler-pycharm/line-profiler-pycharm-plugin/-/issues?show=eyJpaWQiOiIyOSIsImZ1bGxfcGF0aCI6ImxpbmUtcHJvZmlsZXItcHljaGFybS9saW5lLXByb2ZpbGVyLXB5Y2hhcm0tcGx1Z2luIiwiaWQiOjE3MTY3MDk4Nn0%3D), so we have to use the command line interface.

The usage is: 

1. decorate functions of interest with @profile decorator
2. run the profiler: `kernprof -l -v <script> <script arguments>`

## PyCharm Profiler
[official documentation](https://www.jetbrains.com/help/pycharm/profiler.html)

Pycharm has a built-in profiler with a very simple use:

1. Select three dots next to the debug button and click on `Profile <script name>`
1. Wait some time to warm up and get to the important parts of the code
1. in the left panel, select `create snapshot`
1. Explore the results

Each snapshot contains the following tabs:

- `Flame Graph`: Frequently broken - absolutely incorrect visualization.
- `Call Tree`: Again frequently broken
- `Method list`: Can be broken as well
- `Statistics`: This view comes directly from the cProfile backend and is the only reliable view in PyCharm.
- `Call Graph`: Typically both incorerect and totally visually broken.

The built-in profiler provides only aggregated results for each function. To get line-by-line results we need a [line_profiler](https://github.com/pyutils/line_profiler) package.


## cProfile
[Official documentation](https://docs.python.org/3/library/profile.html)

Usage: `python -m cProfile <script> <script arguments>`

This way, everything is outputed to the terminal, which is not very convenient, as the list of functions may be too long. One option is to redirect the output to a file and then read the top. But there is also a GUI option using `snakeviz` package:

```bash
pip install snakeviz
python -m cProfile -o profile.prof <script> <script arguments>
snakeviz profile.prof
```

Individual outputs columns:

- `ncalls`: number of calls
- `tottime`: total time spent in the function. The most important column to look at.
- `percall`: time spent in the function per call
- `cumtime`: total time spent in the function including the time spent in the called functions. This is the column by which the list of functions is sorted.
- `percall`: time spent in the function per call including the time spent in the called functions.
- `filename:lineno(function)`: filename, line number, and function name


## Scalene
[GitHub](https://github.com/plasma-umass/scalene)

Scalane is a profiler that allegedly provides CPU, memory, and GPU profiling, all with minimal performance impact. The reality is however, that the profiler results are quite random, not at all showing all the function calls, totally failing to identify the bottlenecks.

Usage: `scalene run <script> --- <script arguments>`. Important parameters:

- `--cpu-only`: only CPU profiling
- `--profile-all`: profile all files. By default, only the main script is profiled (even more useless)

To display the results, use `scalene view`.