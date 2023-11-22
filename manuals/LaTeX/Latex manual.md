
# Document structure
The document structure is well documented [on wikibooks](https://en.wikibooks.org/wiki/LaTeX/Document_Structure). The basic structure is:
```latex
\documentclass[<options>]{<class>}
...
\begin{document}
    ...
\end{document}
```

# Escape characters
LaTeX uses man6y special characters which needs to be escaped. Unfortunatelly, there is no single escape character, instead, there are many. The following table lists the most common escape characters:

| Character | Escape sequence |
| --- | --- |
| `[` | `{[}` |
| `]` | `{]}` |


# Text formatting

## Subscript and superscript
In math mode, the subscript and superscript are created using the `_` and `^` characters. In text mode, we need to use a special commands: `\textsubscript` and `\textsuperscript`. Example:
```latex
H\textsubscript{2}O
```



# Floats
The following environments are floats:
- `figure`
- `table`
- `algorithm`

## Placement
Any float takes the position as a first argument. The following positions are available:
- `h`: here
- `t`: top
- `b`: bottom
- `p`: special dedicated page per float
- `!`: ignore nice positioning and put it according to the float specifiers

The placement algorithm then iterate pages starting from the page where the float is placed. For each page, it tries to find a place for the float according to the float specifiers (in the same order as they appear in the float position argument). In case of success, the procedure stops and place the float. If the procedure fails for all pages, the float is placed at the end. 

Sources:
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX/Floats,_Figures_and_Captions#Figures)
- [Overleaf](https://www.overleaf.com/learn/latex/Positioning_images_and_tables#The_figure_environment)

### Default placement
The default placement differs between environments and also classes. For example for article class, the default placement for `figure` and `table` is `tbp` ([see SO](https://tex.stackexchange.com/questions/172782/what-are-the-default-placement-options-for-a-floating-figure-in-latex)).


## Tables
The float environment for tables is `table`. However, the rows and columns are wrapped in another environment. The default inner enviroment is `tabular`, however, there are *many* other packages that extends the functionality. In practice, there are currently three inner environments to consider:
- `tabular`: the default environment that is sufficient for simple tables
- `tabulary`: the environment that allows to create columns with automatic width. If the main or only issue of the table is that it needs to fit a specific width, this is the environment to use.
- `tblr`: the `tblr` environment from the [`tabulararray`](https://ctan.org/pkg/tabularray) package is the most up to date tabular environment that support many features. Also, it splits the table presentation from the table content, which can make generating tables from code easier. The only downside is that **it does not support automatic column width**. 


### Column types
The column types are specified in the argument of the `tabular` or equivalent environment. The following column types are available by default:
- `l`: left aligned
- `c`: centered
- `r`: right aligned
- `p{width}`: paragraph column with specified width

Other column types can be provided by the inner environment package or by the user.


### Simple tables with tabular environment
The usual way to create a table in the `tabular` environment is:
```latex
\begin{table}[h]
    \centering % center the content of the table environment
    \begin{tabular}{|c|c|}
        ... rows and columns
    \end{tabular}
    \caption{My table}
    \label{tab:my_table}
\end{table}
```



### Columns with automatic width: `tabulary`
By default, laTeX does not support automatic width for columns, i.e., sizing the columns by their content. To enable this feature, we can use the `tabulary` package, which provides the `tabulary` environment (which is a replacement for the `tabular` environment). The columns with automatic width are specified by the `L`, `C`, `R` column types. 

Note that the new column types can be combined with the standard column types. In that case, the standard columns will have width according to their content, and the rest of the space will be distributed among the new column types. 


### Configure the space between columns
In most packages, the space between columns is configured using the `\tabcolsep` variable. Example:
```latex
\setlength{\tabcolsep}{10pt}
```

However, in the `tblr` environment, the space between columns is configured using the `leftsep` and `rightsep` keys. Example:, 
```latex
\begin{tblr}
{
    colspec={llllrr},
    leftsep=2pt, 
    rightsep=2pt
}
```
By default, the `leftsep` and `rightsep` are set to `6pt`.

### Export google sheets to latex tables
There is ann addon called [LatexKit](http://caenrigen.tech/LatexKit/) which can be used for that.


### Footnotes in tables
In tables and table captions, the `\footnote` command does not work correctly. Also, it is not desirable to have the footnote at the bottom of page, instead, we want the footnote to be at the bottom of the table. To achieve this, we use a special environment:
- `threeparttable`: if we are using the `tabular` or `tabulary` environment
- `talltblr`: if we are using the `tblr` environment

#### Using the `threeparttable`
The `threeparttable` environment is used as follows:
```latex
\begin{table}[h]
    \centering
    \caption{My table}
    \label{tab:my_table}
    \begin{threeparttable}
        \begin{tabular}{|c|c|}
            one$^a$ & two$^b$ \\
            ... other rows and columns
        \end{tabular}
        \begin{tablenotes}
            \item $^a$footnote 1
            \item $^b$footnote 2
        \end{tablenotes}
    \end{threeparttable}
\end{table}
```

#### Using the `talltblr`
The `talltblr` environment is used as follows:
```latex
\begin{table}[h]
    \centering
    \caption{My table}
    \label{tab:my_table}
    \begin{talltblr}[
        label = none,
        note{a} = {footnote 1},
        note{b} = {footnote 2}
    ]{
        colspec={|c|c|},
    }
        one\TblrNote{a} & two\TblrNote{b} \\
        ... other rows and columns
    \end{talltblr}
\end{table}
```

Notice the `label = none` option. Without it, the table numbering is raised again, resulting in the table being numbered twice. 



# Math
[wiki](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

To use math, we need the `amsmath` package. 

The math commands only works in math mode which can be entered in one of the many math environments. 


## If/else variants
For that, we use the `cases` environment. Example:
```latex
\begin{equation}
    f(x) = 
    \begin{cases}
        0 & \quad \text{if } x < 0 \\
        1 & \quad \text{if } x \geq 0
    \end{cases}
\end{equation}
```

## Problem and similar environments
[wiki](https://en.wikibooks.org/wiki/LaTeX/Theorems)

The environments for special math text blocks are not included in the `amsmath` package. Instead, we can define them manually using the `\newtheorem` command. Example:
```latex
\newtheorem{problem}{Problem}

\begin{problem}
    This is a problem.
\end{problem}
```



# Footnotes
The footnote is created using the `\footnote{}` command. 

## Override footnote numbering
To override the footnote numbering (e.g. to repeat the same number twice), we can use the `\setcounter` command. Example:
```latex
\setcounter{footnote}{1} # set the footnote counter to 1
```


# Bibliography
See more on [SE](https://tex.stackexchange.com/questions/25701/bibtex-vs-biber-and-biblatex-vs-natbib).

For bibliography management, whole toolchain is usually needed, including:
- a tool that generates the bibliography file (e.g. Zotero, Mendeley, ...)
- a latex package that cares about the citations style (e.g. biblatex, natbib, or default style)
- the real bibliography processer that generates and sorts the bibliography (e.g. bibtex, biber, ...)

However, not all combinations of theses tools are possible. For understanding the pipeline and the possible combinations, see the following figure:

![bibliography toolchain](LaTeX_Bibliography_processing.png "bibliography toolchain")

When choosing what package to use in latex, we have to take care that we:
- have the bibliography file in the right format (`.bib` for all pipelines, but the content differs)
- have the style in the right format (`.bst` for default or natbib, `.bbx` for biblatex)

By default, we should use the biblatex - Biber pipeline. Howevver, there are some circumstances where we need to use bibtex, for example, if we need to use a style that is not available for biblatex (as [there is no conversion tool](https://tex.stackexchange.com/questions/174676/how-to-use-custom-bibstyle-with-biblatex)). The styles available for biblatex are listed [on CTAN](https://ctan.org/topic/biblatex).


## Latex document configuration

### Biblatex styling
Basic setup:
```latex
\usepackage[style=numeric]{biblatex}
...
\addbibresource{bibliography.bib}
...
\printbibliography
```
The style parameter is optional. The styles available for biblatex are listed [on CTAN](https://ctan.org/topic/biblatex).


#### Handle overflowing URLs in bibliography
Sometimes, the links overflow the bibliography. To fix this, we can use the following commands:
```latex
\setcounter{biburllcpenalty}{100}
\setcounter{biburlucpenalty}{100}
\setcounter{biburlnumpenalty}{100}

\biburlnumskip=0mu plus 1mu\relax
\biburlucskip=0mu plus 1mu\relax
\biburllcskip=0mu plus 1mu\relax
```



### Default and natbib styling
Basic setup:
```latex
\bibliographystyle{plain}
...
\bibliography{bibliography}
```
Note that we do not have to use any package to use basic cite commands. Also note, that **the `\bibliographystyle` command is mandatory**. Finally, we do not need to specify the extension of the bibliography file.

#### Natbib
The bibtex bibliography management system is quite old and does not support many features. To overcome this, we can use the `natbib` package:
```latex
\usepackage{natbib}
```



# Splitting the document into multiple files
There are two ways to split the document into multiple files:
- `\input{file}`
- `\include{file}`

The `\include` is intended for chapters or other large parts of the document. It has the following properties:
- it starts a new page before and after the included file
- it does not allow nesting
- there is a special command `\includeonly{file1,file2,...}` which allows to include only the specified files. This is useful for large documents where we want to compile only a part of the document. Without this command we would need to search for the include command and comment it out.

The `\input` command is intended for smaller parts of the document. Contrary to the `\include` command, there is no special behavior involved. Instead, the content of the file is simply pasted at the place of the `\input` command. 



# Speedup Techniques
The compilation of large documents can be slow. There are several techniques to speed up the compilation:
- split the document into multiple files and use `\includeonly` to include only the relevant files
- precompiling the preamble
- using draft mode

## Precompiling the preamble
The preamble is the part of the document before the `\begin{document}` command. It contains the document configuration, packages, etc. Because the included packages are usually large, the compilation of the preamble can be slow. To speed up the compilation, we can precompile the preamble and use the precompiled preamble in the main document. This can be done using the `mylatexformat` package. The usage is as follows:

1. At the beginning of the preamble, add the following comment: `%&<format name>`. This will tell the compiler to use the specified format. The `<format name>` can be arbitrary, but it is recommended to use the same name as the main document.
1. To spare some preamble content from being precompiled (dynamic content), add a command `\endofdump` after the content that should not be precompiled. 
1. run the following command:
    ```PowerShell
    pdflatex --ini -jobname="<format name>" "&pdflatex" mylatexformat.ltx <format name>.tex
    ```

Afther this, the compilation of the main document should be faster. For more information, see the [package documentation](https://ctan.org/pkg/mylatexformat) or the [SO question](https://tex.stackexchange.com/questions/79493/ultrafast-pdflatex-with-precompiling/377033#377033).


# Miscelaneous tasks
## Balancing columns in two-column documents
To balance the columns at the end of the document, we can use the `flushend` package. Just add `\usepackage{flushend}` to the preamble.



# Common problems

## Ugly font in pdf
This can be cause by the missing  vector fonts. If the vector fonts are missing, the bitmap fonts are used instead. 
1. To check if this is the cause, zoom in on the pdf. If the text is blurry, the bitmap fonts are used.
1. To fix this, install the vector fonts.
    - On Windows, install the cm-super package through MikTeX.