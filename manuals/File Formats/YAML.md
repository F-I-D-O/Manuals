YAML is a simple markup language that uses the syntax that can be easily read by non-programmers.

Important links:

- [YAML official website](https://yaml.org/)

The YAML files should have a `.yaml` extension [[source](https://yaml.org/faq.html)].


# String Literals
[documentation](https://yaml.org/spec/1.2.2/#scalars)

There are three styles of string literals in YAML:

- [*plain style*](https://yaml.org/spec/1.2.2/#plain-style) (`plain style literal`): for most simple strings
- [*single-quoted style*](https://yaml.org/spec/1.2.2/#single-quoted-style) (`'single quoted literal'`): for strings that should be interpreted literally
- [*double-quoted style*](https://yaml.org/spec/1.2.2/#double-quoted-style) (`"double quoted literal"`): for strings with escape sequences

Below is a table of the properties of the different styles:

| Style | Character Limitations | Character Escapes |
| ------- | ---------------------- | ------------------ |
| Plain | Any printable character except `\|`, `>`, `&`, `#`, `?`, `[`, `]` | None |
| Single | Any printable character | `'` must be written as `''` |
| Double | Any valid text character, including non-printable characters like `\n`, `\r`, `\t`, `\f`, `\b` | `"` must be written as `\"`, `\` must be written as `\\` |


All three styles can be used for multi-line strings, if we don't need to preserve the newlines:

```yaml
my_string: 
  This is a multiline string.
  Beware that the that all lines are trimmed and the whole string is then folded. 
```

**White space characters are interpreted as follows:**

1. all lines are trimmed (leading and trailing whitespace is removed)
2. [*flow folding*](https://yaml.org/spec/1.2.2/#flow-folding) is applied, which means that all line break sequences are replaced by a single space.


## Literal Style
[documentation](https://yaml.org/spec/1.2.2/#literal-style)

If we want to preserve all the whitespace characters, we can use the [*literal style*](https://yaml.org/spec/1.2.2/#literal-style):

```yaml
my_string: |
  This is a literal style string.
  It will be preserved as is.
```

Inside the literal style string, all characters are preserved as is, including white space characters (this is the difference to the *single-quoted style*, where trimming and flow folding is applied).


## Folded Style
[documentation](https://yaml.org/spec/1.2.2/#folded-style)

Folding style is similar to the literal style, but it does not preserve the newlines, unless the line is whitespace only.

```yaml
my_string: >
  This is a folded style string.
  This is still a single line.

  This is a new line.
```

The result is:
```text
This is a folded style string. This is still a single line. 
This is a new line.
```

# Characters with special meaning in YAML
[documentation](https://yaml.org/spec/1.2.2/#53-indicator-characters)

The following characters have special meaning in YAML: ``{, }, [, ], &, *, #, ?, |, -, <, >, =, !, %, @, :, ` `` and `,`. In strings, these characters should be quoted. They have to be avoided in keys.