# Selectors
There are many CSS selectors:

- *element*: e.g. `div`, `span`, `p`, `a`, `img`, etc.
- *class*: `.<class>`
- *id*: `#<id>`
- *attribute*: `[<attribute>]`
- *any element*: `*`

## Combining selectors
Selectors are so powerful because we can combine them:

- *conjunction*: `<selector 1><selector 2>`: select elements that match `<selector 1>` and `<selector 2>`
    - `div.class`: select `<div>` with class `class`
- *inside* (`<space>`): `<selector 1> <selector 2>` select elements that match `<selector 2>` inside `<selector 1>`
- *adjacent* (`+`): e.g., `div + p` selects the first paragraph after a div
- *child* (`>`): e.g., `div > p` selects all paragraphs that are direct children of a div
- *parent* (`<`): e.g., `div < p` selects all divs that are direct parents of a paragraph
- [*contains* (`:has()`)](https://developer.mozilla.org/en-US/docs/Web/CSS/:has): e.g., `div:has(p)` selects all divs that contain a paragraph



## Pseaudo-classes
[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes)

Pseudo-classes are special properties that are added to elements by the browser. Typically, they result from a user action, or the active layout or state, but they are even pseudo-classes that can be derived purely from the HTML code.

To select elements with a pseudo-class, we use the `:<pseudo-class>` suffix, e.g., `:hover`,  `a:hover`...

Most used pseudo-classes:

- `:hover`: when the mouse is over the element
- `:root`: the root element of the document, typically the `<html>` element
- `:visited`: when the element (typically a link) has been visited



# Styling
[Mozilla reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties)


## Properties
The most common properties are:

- [`box-shadow`](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow): shadows around the element. There syntaxis:
    ```css
    `<offset-x> <offset-y> <blur radius> <spread-radius> instet <color>`
    ```
    - every value except `<offset-x>` and `<offset-y>` can be omitted.
    - the `<offset-x>` and `<offset-y>` values mark the end of the shadow to right (`<offset-x>`) and bottom (`<offset-y>`). If negative values are used, the shadow will be drawn at the opposite side, i.e, left and top.
    - default values:
    - the `<blur radius>` is the the radius of the blurring effect of the shadow. 0 means no blurring and sharp edge precisely at `<offset-x>` and `<offset-y>` The higher the value, the more blurred the shadow is, and also wider.
    - the `<spread-radius>` size of the shadow. 0 means size of the element, positive values means the shadow is bigger than the element, negative values means the shadow is smaller.
        - `<color>`: the color of the parent element
        - `<blur radius>`: 0
        - `<spread-radius>`: 0
- [`width`](https://developer.mozilla.org/en-US/docs/Web/CSS/width): the width of the element. In addition to [units](#units), we can use:
    - `auto`: the default value calculated by the browser. Depends on the type of the element, the context,...
    - `max-content`: based on the content, without any wrapping
    - `min-content`: based on the content, wrap at any opportunity
    - `fit-content`: min(max-content, max(stretch, min-content))
    - `stretch`: use all the available space in the parent element

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


# Media Queries
[Wikipedia](https://en.wikipedia.org/wiki/Media_query)

Media queries are used to change the style of the page based on the device characteristics. The syntax is:
```css
@media <media type> {
    <style>
}
```
where the `<style>` is the selector/styling to be applied, base on the rules specified in previous sections, and `<media type>` is the condition for which the media query applies.

The `<media type>` can be:

- `max-width`: the maximum width of the device


# CSS Variables (Custom Properties)
[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*)

Variables can be declared in modern CSS inside any selector using the syntax `--<variable-name>: <value>`. Later, the value of the variable can be used in any place matching the selector by writing `var(--<variable-name>)` instead of the literal value. Example:
```css
:root {
    --main-color: blue;
}

p {
    color: var(--main-color);
}
```