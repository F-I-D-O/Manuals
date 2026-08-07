<https://www.mkdocs.org/>

update steps:

1. generate navigation: `python .\generate_nav.py
1. generate site: `mkdocs build`
1. deploy: `mkdocs gh-deploy`



# Configuration
The configuration is done in the `mkdocs.yml` file. The most important options are:

- `site_name`: the name of the site
- `nav`: the navigation structure
- [`exclude_docs`](https://www.mkdocs.org/user-guide/configuration/#exclude_docs): a list of documents to exclude from the site

# Known limitations
MkDocs use the [Python-Markdown](https://python-markdown.github.io/) parser which does not follow the CommonMark specification. Therefore, some markdown elements may not work as expected:

- lists has to be separated by an empty line, otherwise they will be rendered as simple text.


# Troubleshooting

## Left sidebar overlaps the main content
This can be caused by too long words in the left sidebar. To fix this, find the problematic header and split the long word.
