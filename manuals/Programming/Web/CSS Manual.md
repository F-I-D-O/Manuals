# Selectors
There are many CSS selectors:

- HTML element: e.g. `div`, `span`, `p`, `a`, `img`, etc.
- ID: `#<id>`
- Class: `.<class>`
- Attribute: `[<attribute>]`
- Any element: `*`

## Combining selectors
Selectors are so powerful because we can combine them:

- `<selector 1> <selector 2>`: select elements that match `<selector 2>` inside `<selector 1>`
- `<selector 1><selector 2>`: select elements that match `<selector 1>` and `<selector 2>`
    - `div.class`: select `<div>` with class `class`
- `<selector 1> > <selector 2>`: select elements that match `<selector 2>` as a direct child of `<selector 1>`


# Layout options

## Grid Layout
For complex pages. See the [tutorial](https://css-tricks.com/snippets/css/complete-guide-grid/).

## Flex Layout
For simpler pages. See the [tutorial](https://css-tricks.com/snippets/css/a-guide-to-flexbox/).
Note that setting `max_width: 100%` for child elements of flex items does not work frequenly, so it's better to specify `max_witdth` ([SO](https://stackoverflow.com/questions/21103622/auto-resize-image-in-css-flexbox-layout-and-keeping-aspect-ratio)).

## Oldschool Layout
Oldschool layout use floats.

## Very Oldschool Layout
With tables...

