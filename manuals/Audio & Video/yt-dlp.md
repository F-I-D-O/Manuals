# Introduction
[home](https://github.com/yt-dlp/yt-dlp)

To install, just run: `pip install yt-dlp`

useful parameters:

- `-x`, `--extract-audio`: extract only the audio from the video



# Possible problems

## [youtube] H8QQHGupPrs: Sign in to confirm your age.
This means that this video is age restricted. Signing in with a Google account is required. With yt-dlp, there are two options:

- using a browser with non-encrypted cookies (e.g. Firefox) and passing the `--cookies-from-browser` argument to yt-dlp
- exporting cookies from the browser with encrypted cookies (Chrome, Edge, Opera, ...) and passing the `--cookies` argument to yt-dlp


## ERROR: [youtube] MbXLBIlR0oE: The page needs to be reloaded.
This is an [open issue](https://github.com/yt-dlp/yt-dlp/issues/16212#issuecomment-4041111155). Basically, yt-dlp currently (2026-03-12) cannot download YouTube videos that are age restricted. 