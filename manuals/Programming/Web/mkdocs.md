<https://www.mkdocs.org/>

update steps:

1. generate navigation: `python .\generate_nav.py
1. generate site: `mkdocs build`
1. deploy: `mkdocs gh-deploy`

# Known limitations
MkDocs use the [Python-Markdown](https://python-markdown.github.io/) parser which does not follow the CommonMark specification. Therefore, some markdown elements may not work as expected:

- lists has to be separated by an empty line, otherwise they will be rendered as simple text.


# Troubleshooting

## Left sidebar overlaps the main content
This can be caused by too long words in the left sidebar. To fix this, find the problematic header and split the long word.
