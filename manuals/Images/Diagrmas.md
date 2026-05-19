# Diagrams with D2

- [Homepage](https://d2lang.com/)
- [GitHub](https://github.com/terrastruct/d2)
- [Tutorial](https://d2lang.com/tour/)

D2 is a system that can usea D2 declarative format as input and export it to a several formats, including `png`, `svg`, `pdf`, `html`, and `md`.

## Installation
[Official documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md)

### Windows
[Official documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md#windows)

The Windows `msi` installer can be downloaded from the [Releases page](https://github.com/terrastruct/d2/releases). Note that the installer has no configuration options, so it may appear as faulty, but it is working.


## CLI
The basic usage of d2 is to run it in command line: `d2 <input file>`. This command will compile the file to svg. Most useful options are:

- `--watch`, `-w`: This will automatically start a server where the generated `svg` file is displayed. It will also watch the file for changes and reload the web page with the new diagram.
- `--scale`: Scale the output. Default is `-1`, which means fit the whole `svg` to the screen.