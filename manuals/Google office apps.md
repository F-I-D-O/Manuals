# Google sheets

## Data types
This is how we can create various data types in Google Sheets:

- **Dropdown list**: `Insert` -> `Dropdown`

## Date and time

To refer to the current date, we can use the `TODAY()` function.


## Conditional formatting
To apply conditional formatting to a range of cells, select the range and go to `Format` -> `Conditional formatting`. The rules are sorted from highest to lowest priority. Rule types:

- **Value is (lower, equal, greater) than...**
- **Date is (older, equal, newer) than...**
    - but not for complex date operations
- **Custom formula** for complex conditions
    - `=AND(E2>=TODAY(); E2<=TODAY()+90)`: date in the next three months


## Subscript and superscript
There is no direct way to format text as subscript or superscript. The easiest way is to copy the subscript/superscript characters from and paste them into the cell. A source for that can be the [wiki page for Unicode subscript and superscript](https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts).


# Google docs

## Troubleshooting
### Can't open a document on Android
This can sometime happen for large documents. The solution is to open the Google Docs application settings and clear both the cache and the app data.