# Codex

- [Homepage](https://openai.com/codex/)
- [GitHub](https://github.com/openai/codex)
- [CLI manual](https://developers.openai.com/codex/cli/features)

Codex is a command line LLM tool that uses ChatGPT API. Typically, it is run interactively in the terminal by executing `codex` command in the directory where the code is located. The important parameters are:

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

We can also use `@` to refer to files and directories. However, this functionality is currently limited, there is no way how to expand the suggestion deeper to the directory structure.