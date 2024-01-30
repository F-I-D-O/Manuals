So far we have three LaTeX toolchains that has proven to work well:

- **Overleaf**: Cloud tool that is stable and very good for collaboration. 
- **Texmaker + MiKTex**: Traditional desktop setup.
- **VSCode + Latex Workshop + MikTeX/Tinytex**: Modern desktop setup. The main advantage is that VSCode has the best Copilot support from all the editors, which is a huge time saver.

# VSCode + Latex Workshop + MikTeX/Tinytex
## Installation
The installation of VSCode and [Latex Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) (VSCode extension) is straightforward, so we cover only the installation of MikTeX/[Tinytex](https://github.com/rstudio/tinytex) here.


### MikTeX
The installation of MikTeX is straightforward. MikTeX installs all the required packages on the fly, so there is no need to install them manually. 

The only thing that we need to do manually is to install [Perl](https://www.perl.org) which is needed for the [latexmk](https://mg.readthedocs.io/latexmk.html) tool. There are two Perl distributions for Windows: [ActivePerl](https://www.activestate.com/products/perl/) and [Strawberry Perl](https://strawberryperl.com). This LaTeX toolchain has been only tested with Strawberry Perl. The installation of Strawberry Perl is straightforward: there is an executable installer. Do not forget to add it to the `PATH` variable.

Do not forget to restart VSCode after the installation of MikTeX and Perl.


### Tinytex
[Official installation guide](https://yihui.org/tinytex/#installation)

1. Install Tinytex using the shell script for the respective OS. The links to the scripts are in the installation guide.
2. Add the executable path of Tinytex to the PATH variable. 


#### Installing additional packages
Unlike MiKTex, Tinytex does not install required packages on the fly. Instead, it only shows an error in the log. To install a missing package, run the following command:
```
tlmgr install <package name>
```


## Latex Workshop Configuration and Usage
[wiki](https://github.com/James-Yu/LaTeX-Workshop/wiki)

### Syncing between PDF and source
To jump from PDF to source, use the binding configured in: `Settings` > `Latex Workshop` > `View` > `Pdf` > `Internal` > `SyncTeX: Keybinding`.

To jump from source to PDF, use the binding configured in: `Keyboad Shortcuts` > `Latex Workshop: SynTeX from cursor`. Unfortunately, mouse cannot be used here due to [VSCode limitations](https://github.com/microsoft/vscode/issues/3130).
