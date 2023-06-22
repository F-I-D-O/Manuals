

First download [binaries for Windows](https://www.gyan.dev/ffmpeg/builds/).

# Converting a Video to Gif Image
Example:
```
ffmpeg -i .\screen_recording1618479593603.mp4 -r 15 -vf "scale=512:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -ss 00:00:03 -to 00:00:06 simod_showcase.gif
```

To change the speed, we can use an `-itsscale` inut option:

```
ffmpeg  -itsscale 0.2 -i .\screen_recording1618479593603.mp4 -r 15 -vf "scale=838:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -ss 00:00:00 -to 00:00:15 simod_showcase.gif
```

Detailed description on [SE](https://askubuntu.com/questions/648603/how-to-create-an-animated-gif-from-mp4-video-via-command-line)
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyNjU3NDQxNjksNzMwOTk4MTE2XX0=
-->