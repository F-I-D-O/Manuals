# Workflow
JavaScript is originally a browser scripting language. However, today, many other environments use it. Here we describe the following stack:

- Environment: [Node.js](https://nodejs.org/)
- Package manager: [npm](https://www.npmjs.com/)


# Node.js

- [wikipedia](https://en.wikipedia.org/wiki/Node.js)
- [official website](https://nodejs.org/)

To install `node.js`, download the `.msi` installer from the official website. During the installation, **do not check the option to install necessary dependencies like Python, Visual Studio, etc.** This will install everything again as a Chocolatey package, even if you already have them installed.

# npm

- [wikipedia](https://en.wikipedia.org/wiki/Npm_(software))
- [official website](https://www.npmjs.com/)
- [official documentation](https://docs.npmjs.com/cli/v11/commands)

`npm` is the package manager included in Node.js. The most common subcommands are:

- `install`: install or update a package
- `uninstall`: uninstall a package
- `run`: run a script from the package (defined in the `package.json` file)


## Installing packages with `npm install`
To **install or update** a package, use the [`install`](https://docs.npmjs.com/cli/v11/commands/npm-install) command as:

```bash
npm install <package specification>
```
The `<package specification>` can be:

- a package name, e.g. `npm install express`
    - this can also contain a scope, e.g. `npm install @openai/codex`

Important options are:

- `-g`, `--global`: install the package globally. On Linux, this requires `sudo` permissions.


## Running scripts with `npm run`
[official documentation](https://docs.npmjs.com/cli/v11/commands/npm-run)

This can run scripts specified in the `scripts` field of the `package.json` file. 