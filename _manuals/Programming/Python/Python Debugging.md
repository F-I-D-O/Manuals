
Pycharm has a build in debugger, however, there are some tricky problems described below.

# Breaking on Exception
Breaking on exception is one of the most important debugger tools. However, there are some problems with Pycharm exception debugging.

## Breake on Termination vs on Raise
By default, the program breakes on termination (unhandled exception). This is usually a correct configuration. However, in jupyter, all exceptions are caught to not break the jupyter itself. Therefore, **in jupyter, all exceptions are ignored by the debugger if the breakpoins are set to break on termination.**

To break on exceptions in jupyter, we have to breake on raise. By this setting, however, we stop even on expected/handeled exceptions, stoping potentially on hundereds breakpoints in library code.

Another issue is with the setting itself. **To propagate the change between breaking on raise/termination, we have to deactivate and then activate again the exception breakpoints, otherwise, the setting is ignored.**


## 

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA3ODU4MjE2Niw5MDU2MDA5NzgsNzMwOT
k4MTE2XX0=
-->