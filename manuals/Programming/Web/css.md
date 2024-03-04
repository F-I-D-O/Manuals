# Selectors
basic selectors are:
- *element*: e.g., `p` selects all paragraphs
- *class*: e.g., `.intro` selects all elements with class `intro`
- *id*: e.g., `#first` selects the element with id `first` (ids are unique)

These basic selectors can be combined to form complex selectors the combination operators are:
- *inside* (`<space>`): e.g., `div p` selects all paragraphs inside a div
- *adjacent* (`+`): e.g., `div + p` selects the first paragraph after a div
- *child* (`>`): e.g., `div > p` selects all paragraphs that are direct children of a div
- *parent* (`<`): e.g., `div < p` selects all divs that are direct parents of a paragraph
- [*contains* (`:has()`)](https://developer.mozilla.org/en-US/docs/Web/CSS/:has): e.g., `div:has(p)` selects all divs that contain a paragraph

