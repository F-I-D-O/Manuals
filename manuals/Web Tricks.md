# Exporting cookies from a browser

## Edge

1. Open the developer tools (F12)
2. Go to the `Application` tab -> `Cookies` 
3. Select rows you want to export, `Ctrl` + `C` to copy
4. Paste the cookies into a file 
5. Paste this header:
    ```
    Name	Value	Domain	Path	Expires	Max-Age	Size	HttpOnly	Secure	SameSite	Partition Key	Site Cross Site	Priority
    ```
6. And save
7. Optionally, to convert the cookies to the Netscape format, use a [converting script](https://github.com/F-I-D-O/tools/blob/master/cookies_to_netscape.py).





# Download all photos from `rajce.cz`
```JavaScript
$("#photoList img").each(function () {var a = $(this).closest("a"); if (a.length){$(document.body).append("<img src='" + a.attr("href") + "' \/>");}});$("body>*:not(img)").remove();
```