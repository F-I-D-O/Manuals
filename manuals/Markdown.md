- [Available elements with syntax](https://commonmark.org/help/)
- [Linter](https://github.com/DavidAnson/markdownlint)
- [VSCode Linter specifics](https://github.com/DavidAnson/vscode-markdownlint)
- [CommonMark specification](https://spec.commonmark.org/0.31.2/)

# Elements

## Links
Links can be added to a markdown file by using the following syntax:
```markdown
[Link text](http://example.com)
```

There are also simple links where the URL is used as the link text, these are called *[autolinks](https://spec.commonmark.org/0.31.2/#autolink)*
```markdown
<http://example.com>
```

If the link contains spaces, it must be enclosed in angle brackets:
```markdown
[Link text](<some link with spaces>)
```

### Local links
We can also create local links to headings in the same document:
```markdown
[Link text](#<heading>)
```
Here, `<heading>` is the heading text 

- in lowercase,
- with spaces replaced by hyphens,
- with all special characters removed,
- two or more hyphens are replaced by one hyphen,
- and, in case of a heading with the same text, a number is added at the end.


## Images
Images can be added to a markdown file by using the following syntax:
```markdown
![Alt text](/path/to/image.png)
```


# Standardization
The only standard for markdown is the [CommonMark specification](https://commonmark.org). However, this specification was created ten years after the original markdown was introduced and therefore there are many implementations of markdown does not follow the CommonMark specification. The following implementations follow the CommonMark specification:

- [Markdown-it](https://markdown-it.github.io/)

The following implementations do not follow the CommonMark specification:

- [Python-Markdown](https://python-markdown.github.io/)

## Linter
There is a [linter](https://github.com/DavidAnson/markdownlint) for markdown available also as a [VSCode extension](https://github.com/DavidAnson/vscode-markdownlint).

The linter can be configured:

- in the `.markdownlint.jsonc` or `markdownlint.yaml` file in the root of the project
- a file with the same name in the home directory
- in the settings of the VSCode extension (`markdownlint.config`)

By default, the linter will check more than 50 rules. Not all of them are based on the CommonMark specification and therefore it may be useful to disable some of them. We can do this by adding the following to the configuration file:
```json
{
    "MD013": false
}
```

# Handling of special characters

To use backticks (`` ` ``) in code, use double backticks:
```markdown
``code with `backticks` inside``
```

# HTML Content
If we want some object that cannot be created by markdown syntax (e.g., a table with merged cells), we can use HTML content. HTML content can be directly inserted into the markdown file, without being wrapped in special tags [[source](https://daringfireball.net/projects/markdown/syntax#html)].
