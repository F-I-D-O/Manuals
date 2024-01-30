

First download [binaries for Windows](https://www.gyan.dev/ffmpeg/builds/).

# Converting a Video to Gif Image
Example:
```
ffmpeg -ss 00:00:03 -to 00:00:06 -i .\screen_recording1618479593603.mp4 -r 15 -vf "scale=512:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" simod_showcase.gif
```

Used options:
- `-ss 00:00:03`: start at 3 seconds
- `-to 00:00:06`: end at 6 seconds
- `-r 15`: set the frame rate to 15 fps
- `-vf "scale=512:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"`: set the size of the image to 512px width, and split the video into two streams: one for generating the palette, and one for using the palette

Note that the order of the options is important. For example, if we put `-ss` after `-i`, then the video will be cut after the specified time, but the whole video will be loaded into memory before that.

To change the speed, we can use an `-itsscale` inut option:

```
ffmpeg  -itsscale 0.2 -i .\screen_recording1618479593603.mp4 -r 15 -vf "scale=838:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -ss 00:00:00 -to 00:00:15 simod_showcase.gif
```

Detailed description on [SE](https://askubuntu.com/questions/648603/how-to-create-an-animated-gif-from-mp4-video-via-command-line)

A **text** can be then added to the video using online tools, e.g. [ezgif](https://ezgif.com/add-text).
