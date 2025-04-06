
# Standard Library 

## Standards
Unlike C++ standards that are released every 3 years, C standard releases are not regular, and they are less frequent. Moreover, the support of the new features is only poorly documented. The  [C compiler support on cppreference](https://en.cppreference.com/w/c/compiler_support) only covers the C99 and C23 standards. Therefore, it is better to consult the documentation of each individual compiler:

- GCC:
    - [C99 Status](https://gcc.gnu.org/c99status.html)
    - [C11 Status](https://gcc.gnu.org/wiki/C11Status)

The [standards](https://en.wikipedia.org/wiki/ANSI_C) are:

- C89: The original standard, sometimes referred to as ANSI C.
- C95: wchars, alternative logical operators
- C99: `long long` and other new types, variable-length arrays, removed several dangerous features from C89 like implicit int or implicit function declaration.
- C11: improved unicode support, cross-platform multithreading, atomic types
- C17: only address defects from C11
- C23: `auto`, new string functions, `typeof` standardized

## String functions

### Copying strings
For copying strings, there are the following functions:

- [`strcpy`](https://en.cppreference.com/w/c/string/byte/strcpy): `strcpy(<destination>, <source>)` copies the string `source` to `destination`.
- [`strncpy`](https://en.cppreference.com/w/c/string/byte/strncpy): `strncpy(<destination>, <source>, <count>)` copies at most `count` characters from `source` to `destination`.
    - note that this function was never intended to be used for copying strings as we know them today, but rather for copying old fixed-length strings. It is unsafe even for the C standards and **should not ever be used.** ([source](https://software.codidact.com/posts/281518/281519#answer-281519))

Additionally, the optional part of the C11 standard introduced more secure versions of the string functions, with the suffix `_s`:

- [`strncpy_s`](https://en.cppreference.com/w/c/string/byte/strncpy)

However, **the `_s` functions should be avoided as they are not supported by some major compilers ([e.g. GCC](https://gcc.gnu.org/wiki/C11Status)).** Some rational why these functions are problematic can be found in:

- the document [Field Experience With Annex K](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm).
- this [Codidact answer](https://software.codidact.com/posts/281518/281519#answer-281519)
- This [reddit post](https://www.reddit.com/r/C_Programming/comments/12mm7ta/can_someone_explain_annex_k_to_me_and_why_it_is/)
- This [StackOverflow answer](https://stackoverflow.com/a/373911/1827955)

