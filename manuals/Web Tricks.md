# Download all photos from `rajce.cz`
```JavaScript
$("#photoList img").each(function () {var a = $(this).closest("a"); if (a.length){$(document.body).append("<img src='" + a.attr("href") + "' \/>");}});$("body>*:not(img)").remove();
```