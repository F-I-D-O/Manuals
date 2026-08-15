# Introduction
[home](https://github.com/yt-dlp/yt-dlp)

To install, just run: `pip install yt-dlp`

useful parameters:

- `-x`, `--extract-audio`: extract only the audio from the video
- `--js-runtimes`: enable non default JavaScript runtimes. Only Deno is enebeld without this option, but others (e.g. Node) must be enabled.
    - Example: `--js-runtimes node`
    - Only required for certain YouTube operations


# Configuration
[Official documentation](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#configuration)

Among the many layers of configuration, the user configuration is most tyical. It can be located in several places, e.g.: `~/yt-dlp.conf`.

The format of the file is simple, just command line options, each on a separate line. Lines starting with `#` are comments, empty lines are ignored.


# Possible problems

## [youtube] H8QQHGupPrs: Sign in to confirm your age.
This means that this video is age restricted. Signing in with a Google account is required. With yt-dlp, there are two options:

- using a browser with non-encrypted cookies (e.g. Firefox) and passing the `--cookies-from-browser` argument to yt-dlp
- exporting cookies from the browser with encrypted cookies (Chrome, Edge, Opera, ...) and passing the `--cookies` argument to yt-dlp


### Exporting cookies from the browser
Because YouTube frequently rotates the cookies, the only option how to get persistent cookies is to export them from within the in-private/incognito mode of the browser. So the steps are:

1. close all incognito/private windows and open a new one
1. go to the YouTube website and log in
1. got to https://www.youtube.com/robots.txt
1. export the cookies (see the [Manual](../Web%20Tricks.md#exporting-cookies-from-a-browser))


## ERROR: [youtube] MbXLBIlR0oE: The page needs to be reloaded.
This is an [open issue](https://github.com/yt-dlp/yt-dlp/issues/16212#issuecomment-4041111155). Basically, yt-dlp currently (2026-03-12) cannot download YouTube videos that are age restricted. 