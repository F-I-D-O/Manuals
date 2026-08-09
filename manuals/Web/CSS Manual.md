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



# Styling
[Mozilla reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties)


## Units
For many properties, we have to specify the unit. The most common units are:

- `px`: pixel
- `em`: 
- `%`: percent
- `vw`: viewport width
- `vh`: viewport height

If the value is `0`, we can omit the unit.

For shorhand properties setting multiple sides at once (e.g., `border`, `margin`, `padding`), we can set:

- all sides to same value: `<property>: <value>`
- same top and bottom, same left and right: `<property>: <top-bottom value> <left-right value>`
- all sides separately: `<property>: <top> <right> <bottom> <left>`


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

