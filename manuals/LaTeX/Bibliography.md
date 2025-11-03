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

By default, we should use the Biblatex - Biber pipeline. However, there are some circumstances where we need to use bibtex, for example, if we need to use a style that is not available for biblatex (as [there is no conversion tool](https://tex.stackexchange.com/questions/174676/how-to-use-custom-bibstyle-with-biblatex)). The styles available for biblatex are listed [on CTAN](https://ctan.org/topic/biblatex).


# Latex document configuration

## Biblatex styling
[official biblatex documentation](https://linorg.usp.br/CTAN/macros/latex/contrib/biblatex/doc/biblatex.pdf)

Basic setup:
```latex
\usepackage[style=numeric]{biblatex}
...
\addbibresource{bibliography.bib}
...
\printbibliography
```
The style parameter is optional. The styles available for biblatex are listed [on CTAN](https://ctan.org/topic/biblatex).

The style can be further customized by:

- editing the processed bibliography data (`\DeclareSourcemap` command)
- editing the bibliography printing 
    - using `\AtEveryBibitem` command to edit the bibliography item as a whole or content of specific fields
    - using `\DeclareFieldFormat` or `\renewbibmacro` command to edit the formatting of a bibliography field


### Customizing the bibliography printing
The bibliography printing can be customized:

- using the `\AtEveryBibitem` command to edit the bibliography item as a whole or content of specific fields:
    ```latex
    \AtEveryBibitem{
        \clearfield{urldate} % remove the url date
    }
    ```
    - Inside the `\AtEveryBibitem` we typically use the following macros:
        - `\clearfield{<field>}`: remove the field from the bibliography item. Be aware that by doing this, we edit the model, i.e., the field cannot be used in subsequent commands.
        - `\togglefalse{bbx:<field>}`: disable the printing of the field.
- using `\DeclareFieldFormat` or `\renewbibmacro` command to edit the formatting of a bibliography field:
    ```latex
    \DeclareFieldFormat{title}{\textbf{#1}} % make the title bold
    ```
    - the difference between `\DeclareFieldFormat` and `\renewbibmacro` is that the former is used to declare format for a bibliography field, while the latter changes an existing macro that prints the field. It is not an easy task to determine which one is applicable in a given situation, as it depends on the field we want to format, but also on the applied bibliography style.
    - Inside the `\DeclareFieldFormat` and `\renewbibmacro` we typically use the following macros:
        - `\printfield{<field>}`: print the field, styled according to the bibliography style.
        - `\thefield{<field>}`: print the field value.

There are some biblatex macros that can help us to controll the flow inside our customization commands. These can be used inside `\AtEveryBibitem`, but also inside `\DeclareFieldFormat` and `\renewbibmacro`. Most useful are:

- `\iffieldundef{<field>}{<true>}{<false>}`: if the field is undefined, execute the true branch, otherwise execute the false branch.
- `\ifhyperref{<true>}{<false>}`: if the `hyperref` package is loaded, execute the true branch, otherwise execute the false branch. With this, we can compile without error even if the `hyperref` package is not loaded.


### Customizing the bibliography data
The bibliography data can be customized using the `\DeclareSourcemap` command. Example:
```latex
\DeclareSourcemap{
    \maps{
        \map{
            \step[fieldset=urldate, null] % remove the url date
        }
    }
}
```

Inside the `\map` command, we can use conditional statements:

- `\pernottype{<type>}`: execute the following steps only if the entry type is not `<type>`

In each step, we can use multiple conditions, e.g:
```latex
\DeclareSourcemap{
    \maps{
        \map{
            \step[
                fieldset=urldate, fieldvalue={2022-01-01}, null] % remove the url date if it is 2022-01-01
        }
    }
}
```


### Handle overflowing URLs in bibliography
Sometimes, the links overflow the bibliography. To fix this, we can use the following commands:
```latex
\setcounter{biburllcpenalty}{100}
\setcounter{biburlucpenalty}{100}
\setcounter{biburlnumpenalty}{100}

\biburlnumskip=0mu plus 1mu\relax
\biburlucskip=0mu plus 1mu\relax
\biburllcskip=0mu plus 1mu\relax
```




## Default and natbib styling
Basic setup:
```latex
\bibliographystyle{plain}
...
\bibliography{bibliography}
```
Note that we do not have to use any package to use basic cite commands. Also note, that **the `\bibliographystyle` command is mandatory**. Finally, we do not need to specify the extension of the bibliography file.

### Natbib
The bibtex bibliography management system is quite old and does not support many features. To overcome this, we can use the `natbib` package:
```latex
\usepackage{natbib}
```


# Commands for citing
There are multiple commands for citing, each resulting in a different output. The two most important variants are in-text citation and parenthetical citation:

- In-text citation: the citation is part of the text.
    - IEEE: *this was proven by Smith et al. [1]*
    - APA: *this was proven by Smith et al., 2019*
- Parenthetical citation: the citation is not part of the text.
    - IEEE: *this has been proven before [1]*
    - APA: *this has been proven before (Smith et al., 2019)*

Unfortunately, the commands for these two variants are not consistent across the bibliography packages. The following table summarizes the commands for the two variants:
| Package | In-text citation | Parenthetical citation | Full citation |
| --- | --- | --- | --- |
| Biblatex | `\textcite{<key>}` | `\cite{<key>}` (`\parencite` for APA) | `\fullcite{<key>}` |
| Natbib | `\cite{<key>}` | `\citep{<key>}` | `\bibentry{<key>}` (requires the [`bibentry`](https://ctan.org/pkg/bibentry) package) |

There are more citation commands resulting in different styles for each bibliography styling package, and each of these packages can be also configurated for even more customized look. For more information, see the following links:

- [Natbib styles](https://www.overleaf.com/learn/latex/Natbib_citation_styles)

## Adittional details for citation (page number, chapter, ... )
To add additional details to the citation, we can use the optional argument of the citation command:
```latex
\cite[page~123]{key}
```


## Adding a reference to the bibliography without citing it
For this, we use the `\nocite` command. Example:
```latex
\nocite{key}
```


# Bibliography entries
There are many types of bibliography entries, each of them with different fields. to make things even more complicated, these entries does not match the entry types in Zotero. To make it easier, many use-cases are covered in the table below:

| Use-case | Biblatex | Zotero |
| --- | --- | --- |
| Book | `@book` | `Book` |
| Book chapter | `@incollection` | `Book Section` |
| Conference paper | `@inproceedings` | `Conference Paper` |
| Journal article | `@article` | `Journal Article` |
| Report | `@report` | `Report` |
| Thesis | `@thesis` | `Thesis` |
| Web page | `@online` | `Web Page` |
| Legal document | `@legal` | Unavailable. Use `Report` instead. |

Other sources:

- [Biblatex documentation](https://mirrors.nic.cz/tex-archive/macros/latex/contrib/biblatex/doc/biblatex.pdf)
- [Zotero documentation](https://www.zotero.org/support/kb/item_types_and_fields)
- [Zotero legal types](https://www.zotero.org/support/kb/legal_citations)


