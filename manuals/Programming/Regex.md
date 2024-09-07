# Symbol meaning

- `.` any character
- `[xyz]` one of these characters   
- `[c-j]` any character between `c` and `j`. We can combine this and the previou syntax, e.g.: `[az0-4jsd]`. Note that the minus sign is interpreted as a range only if it is between two characters.
- `[^c-g]` `^` means negation: anything except the following set of characters. Note that the negation(`^`) sign needs to be the first character in the bracket.
- `\`: escape character. 
- `|` means OR. It has the lowest precedence, so it is evaluated last.
- `?`lazy quantifier. It will try to match as few characters as possible (i.e., previous pattern will try to match only till the next patern matches).

`?R` recursive pattern. 

## Quantifiers

- `*`: zero or more 
- `+`: one or more
- `?` zero or one
- `{<from>, <to>}` between `from` and `to` times. If `to` is omitted, it means infinity. If `from` is omitted, it means zero. If there is only one number, it means exact count. If both are omitted, it means one. 

## Anchors

- `^x` must start with x
- `x$` must end with x

## Groups and Lookarounds

- `()` capture group. We can refer to it later, either in the regex, or in the result of the match, depending on the programming language. 
    - The nubering starts from 1, the 0 group is usually the whole match.
    - in the regex we refer to group using `\1`, `\2`, etc.
- `(?:)` non-caputing group. It is useful when we want to use the quantifiers on a group, but we don't want to capture it.
- `(?=)` positive lookahead. It will try to match the pattern, but it will not consume it.
- `(?!)` negative lookahead. It is useful when we want to match a pattern, but we don't want to consume it.
- `(?<=)` positive lookbehind. Same as positive lookahead, but it looks behind.
- `(?<!)` negative lookbehind. Same as negative lookahead, but it looks behind.



# Principles
## Non-capturing groups
Non-capturing groups are groups that helps to specify the match but they are not captured. They are useful when we want to use the group content to specify the match, but we don't want to capture/consume the group. Some of them can be replaced, but usually with a more complicated regex.

All of the non-capturing groups start with `(?` and end with `)`. The `?` is followed by a character that specifies the type of the group. The most common are:

- `?:` non-capturing group
- `?=` positive lookahead
- `?!` negative lookahead
- `?<=` positive lookbehind
- `?<!` negative lookbehind

The actual content of the group is specified between the group type specifier (e.g., `?=`) and the closing bracket (`)`). Example:
```Regex
(?=d)a
```
This regex will match `a` only if it is followed by `d`. The `d` will not be consumed.

Note that **some regex engines don't support variable length lookbehind**. To overcome this, we can use the following tricks:

- use multiple lookbehinds with fixed length
- construct a more complicated regex that will match the same thing
- place a marker with one regex replace and then use the lookbehind to match the marker



# Examples

## Any whitespace
```Regex
/[\x{00a0}\s]/u
```

## Non-breaking space
```Regex
((?!&nbsp;)[^\s\x{00a0}])
```

## Transform Google sheet to latex table
```Regex
najít ([^\r\n]*)\r\n([^\r\n]*)\r\n([^\r\n]*)\r\n([^\r\n]*)\r\n
nahradit \1 & \2 & \3 & \4 \\\\\r\n
```

## CSV to Latex

Search:
```Regex
 ([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),([^,\r\n]*)\n
```
Replace
```Regex
 \1 & \2 & \3 & \4 & \5 & \6 & \7 \\\\\r\n
```

## Name regex
```Regex
([AÁBCČDEFGHIJKLMNOPQRŘSŠTUÚVWXYZŽ]{1}[aábcčdďeéěfghchiíjklmnňoópqrřsštťuúůvwxyýzžw]+ *){2,3}
```



# Archive

## vasdomovnik
najít 
```Regex
[0-9]+[ ]*([^\r\n]*)[\r\n]+
```
nahradit `'\1'`,

## sloupce na pole php
najít 
```Regex
([^\r\n]*)([\r\n])+
```
nahradit `'\1' => ''\2,`

## Pogamut - jen logy od jednoho bota
```Regex
\(TeamCTF[^2][^\r\n]*\r\n 
```
nahradit za prázdno




