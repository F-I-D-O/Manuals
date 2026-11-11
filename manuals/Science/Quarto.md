# Introduction

- [Wikipedia](https://en.wikipedia.org/wiki/Quarto_(software))
- [Official Website](https://quarto.org)

Quarto is a software for scientific writing. Its format is based on jupyter notebooks and markdown, and its putpose is close the LaTeX, i.e., to provide scientific documentation. Unlike LaTeX, Quarto enables interactive documents, and the figure and table elements can be generated inline.

The Quarto files have the extension `.qmd`.


# VS Code Integration

Quarto has an official VS Code extension that provides support for editing `.qmd` files, rendering documents, and previewing outputs. You can install it from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=quarto.quarto).

There are two ways how to rander the preview of a Quarto documents:

- **In-editor preview**: initiated by clicking the preview button
    - does not watch the changes, you need to click the button again after each change, similarly to TeX editors.
- **Live in-browser preview**: initiated by `quarto preview` command in the terminal, which watches for changes and updates the preview automatically.


# YAML Header
Each document can have a YAML header that specifies metadata and configuration options for the document. Mosst importantl fields are:

- `title`: the title of the document
- `format`: dictionary specifying the output format configuration. Each key represents a format (e.g., `html`, `pdf`), and its value is a dictionary of options for that format.

## Format Options
Some options are shared across formats, most notably:

- `toc`: true or false, indicating whether to include a table of contents in the output.


# Math
[Tutorial](https://quarto.org/docs/authoring/markdown-basics.html#equations)

Math can be wrapped in `$...$` for inline math or `$$...$$` for display math. Note that for inline math, the **`$` cannot have spaces surrounding it from inside** - in that case, it will not be recognized as math.