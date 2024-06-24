[quick start](https://docs.midjourney.com/docs/quick-start)

The basic command is `/imagine`. The format is:
```
\imagine <description> <parameters>
```
The `<description` describes the content of the image in human language. The `<parameters>` of the comand determines what we expect from the image.  

# `/imagine` parameters

## Aspect ratio
[official documentation](https://docs.midjourney.com/docs/aspect-ratios)

For aspect ratio, we use `--ar` or `--aspect` parameter. The format is `<width>:<height>`. Both `<width>` and `<height>` must be integers. 

## Version
[official documentation](https://docs.midjourney.com/docs/model-versions)

For version, we use `--version` parameter. 


## Using image input
[official documentation](https://docs.midjourney.com/docs/image-prompts)

The format for impage input prompt is:
```
\imagine <image url> <prompt> <params>
```

We can also adjust the weight of the image input with `--iw` parameter. 


# Choosing the right variant to vary or upscale
After successful generation, emojis can be use to either upscale one of the four generated images, or to vary the image. The order is top-left, top-right, bottom-left, bottom-right.


# Showing user information
[official documentation](https://docs.midjourney.com/docs/info)

To show user information, use the `/info` command in any channel (the response will be private). 


# Showing all generated images
All generated images can be seen at https://www.midjourney.com/imagine