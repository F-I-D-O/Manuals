# Using the debugger
Pycharm has a build in debugger, however, there are some tricky problems described below.

## Breaking on Exception
Breaking on exception is one of the most important debugger tools. However, there are some problems with Pycharm exception debugging.

### Breake on Termination vs on Raise
By default, the program breakes on termination (unhandled exception). This is usually a correct configuration. However, in jupyter, all exceptions are caught to not break the jupyter itself. Therefore, **in jupyter, all exceptions are ignored by the debugger if the breakpoins are set to break on termination.**

To break on exceptions in jupyter, we have to breake on raise. By this setting, however, we stop even on expected/handeled exceptions, stoping potentially on hundereds breakpoints in library code.

Another issue is with the setting itself. **To propagate the change between breaking on raise/termination, we have to deactivate and then activate again the exception breakpoints, otherwise, the setting is ignored.**


# Profiling
Pycharm has a built-in profiler with a very simple use:

1. Select three dots next to the debug button and click on `Profile <script name>`
1. Wait some time to warm up and get to the important parts of the code
1. in the left panel, select `create snapshot`
1. Explore the results

The built-in profiler is statistical and provides only aggregated results for each function. To get line-by-line results we need a [line_profiler](https://github.com/pyutils/line_profiler) package.


## Line Profiling
The [line_profiler](https://github.com/pyutils/line_profiler) package provides line-by-line profiling of the code. Unfortunately, the [corresponding PyCharm plugin](https://plugins.jetbrains.com/plugin/16536-line-profiler) is currently broken and [does not work with latest PyCharm version (2025.2)](https://gitlab.com/line-profiler-pycharm/line-profiler-pycharm-plugin/-/issues?show=eyJpaWQiOiIyOSIsImZ1bGxfcGF0aCI6ImxpbmUtcHJvZmlsZXItcHljaGFybS9saW5lLXByb2ZpbGVyLXB5Y2hhcm0tcGx1Z2luIiwiaWQiOjE3MTY3MDk4Nn0%3D).


