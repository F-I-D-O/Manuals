# TOML Format

- [Official Website](https://toml.io)
- [Wikipedia](https://en.wikipedia.org/wiki/TOML)

TOML is a configuration that use a superset of the INI format. It uses key-value pairs to store the configuration, with possible structuring using sections.

Extensions over INI format:

- support of subsections

Comments are supported using the `#` character.

There are two types of values:

- **strings**: `"string"` or `'string'`
- **numbers**: `123`, `123.456`, `123e456`
- **booleans**: `true`, `false`
- **dates**: `2021-01-01`
- **times**: `12:34:56`
- **datetimes**: `2021-01-01T12:34:56`
- **arrays**: `[1, 2, 3]`
- **tables**: `{key = "value"}`

# Sections
Sections are marked by square brackets: `[section]`. Subsections can be created using the dot notation: `[section.subsection]`.


# Visual studio code support
Unfortunately, **TOML is not supported by default in Visual Studio Code** [[source](https://github.com/microsoft/vscode/commit/f2f8b7cb08d80184d1df76234b236760ae9a72f5)]. 