# Codex

- [Homepage](https://openai.com/codex/)
- [GitHub](https://github.com/openai/codex)
- [Official manual](https://developers.openai.com/codex/)
- [CLI manual](https://developers.openai.com/codex/cli/features)

Codex is a command line LLM tool that uses ChatGPT API. It requires [Node.js](./Programming/Web/JavaScript.md#nodejs) to be installed. Ster that, it can be installed using `npm i -g @openai/codex` (requires administrator permissions).


## The `codex` command
Typically, it is run interactively in the terminal by executing `codex` command in the directory where the code is located. The important parameters are:

- `--add-dir`: add and additional directory to be accessible for codex.

In the interactive mode, all text is interpreted as a single message, except:

- special keystrokes:
    - `Enter` (or `Ctrl+J`): send the message
    - `Ctrl+C`:
        - if during message creation, delete the message,
        - if during execution, cancel the execution and return to the interactive mode,
        - otherwise, exit to the terminal.
    - `Ctrl+Z`: exit to terminal.
- special commands starting with `/`:
    - `/model`: set the model to use.
    - `/status`: show information about the current session, including model, sandbox mode, accessible directories, remaining tokens, etc.
    - `/exit`: exit the interactive mode and return to the terminal.

We can also use `@` to refer to files and directories. However, this functionality is currently limited, there is no way how to expand the suggestion deeper to the directory structure.


## Configuration
[Official manual](https://developers.openai.com/codex/config-basic)

The configuration is determined by (ordered from the highest to the lowest priority):

- command line arguments
- project-specific configuration: `.codex/config.toml`
- user-specific configuration: `~/.codex/config.toml`

The most important configuration keys are:

- `sandbox_mode`: the sandbox mode to use. Valid values are:
    - `read-only`: approval required for all edits
    - `workspace-write`: most files in the workspace are editable (except for `.codex`, `.git`, and similar files)
    - `danger-full-access`: No sandboxing