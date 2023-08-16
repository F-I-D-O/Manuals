# Local testing
1. Install Ruby
2. Download dependencies using `bundle` command
3. Run `bundle exec jekyll serve` to start local server

# Directory structure
Jekyll has a predefined directory structure. The important directories are:
- `_posts`: Contains all the posts. The file name should be in the format `YYYY-MM-DD-title.md`.
- `_pages`: Contains all the pages. The file name should be in the format `title.md`.
- `_config.yml`: Contains the configuration of the site.

# Configuration
The configuration can be set in `_config.yml` file. Impotant options are:

# Markdown
## Code blocks
Markdown code blocks are supported by Jekyll. The syntax is:
~~~markdown
```language
code
\```
~~~
Note that for Jekyll, **the language name is case sensitive**. For example, `java` is correct, but `Java` is not. This is in contrast to GitHub markdown, where the language name is case insensitive.


# Plugins
Jekyll functionality can be extended using plugins. Plugins are Ruby gems, which should be added to the Gemfile and also to the `_config.yml` file.

Note that **GitHub Pages supports only a limited number of plugins**. The list of supported plugins can be found [here](https://pages.github.com/versions/).