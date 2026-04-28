# Workflow
JavaScript is originally a browser scripting language. However, today, many other environments use it. Here we describe the following stack:

- Environment: [Node.js](https://nodejs.org/)
- Package manager: [npm](https://www.npmjs.com/)


# Node.js
[wikipedia](https://en.wikipedia.org/wiki/Node.js)

# npm

- [wikipedia](https://en.wikipedia.org/wiki/Npm_(software))
- [official website](https://www.npmjs.com/)
- [official documentation](https://docs.npmjs.com/cli/v11/commands)

npm is the package manager for Node.js. To **install or update** a package, use the [`install`](https://docs.npmjs.com/cli/v11/commands/npm-install) command as:

```bash
npm install <package specification>
```
The `<package specification>` can be:

- a package name, e.g. `npm install express`
    - this can also contain a scope, e.g. `npm install @openai/codex`



Important options are:

- `-g`, `--global`: install the package globally. On Linux, this requires `sudo` permissions.