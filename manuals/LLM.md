# AGENTS.md
[Official website](https://agents.md/)

Agents.md is a standard for LLM agent rules that work in most of the LLM tools. It is a markdown file that is read by the agent to determine basic rules.

The file can be used for:

- **project-specific rules** - in this case, the file belongs to the project root directory
- **user-specific rules** - in this case, refer to the LLM tool documentation. Typically, the file should be placed in a provider-specific subdirectory in the user's home directory.

# Codex

- [Homepage](https://openai.com/codex/)
- [GitHub](https://github.com/openai/codex)
- [Official manual](https://developers.openai.com/codex/)
- [CLI manual](https://developers.openai.com/codex/cli/features)

Codex is a command line LLM tool that uses ChatGPT API. It requires [Node.js](./Programming/Web/JavaScript.md#nodejs) to be installed. Ster that, it can be installed using `npm i -g @openai/codex` (requires administrator permissions).


## The `codex` command
Typically, it is run interactively in the terminal by executing `codex` command in the directory where the code is located. The important parameters are:

- `--add-dir`: add and additional directory to be accessible for codex. This can sometimes fail, in that case, use the [configuration file](#configuration) to add the directory.

There are also some subcommands:

- `resume`: resume the previous session. The first argument is the name (hash) of the session to resume.
    - We can use `--last` instead of the hash to resume the last session, or 
    - we can skip the argument completely to get a list of all available sessions and choose one to resume interactively.


## Interactive mode
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

- [Official manual](https://developers.openai.com/codex/config-basic)
- [Configuration Reference](https://developers.openai.com/codex/config-reference)

The configuration is determined by (ordered from the highest to the lowest priority):

- command line arguments
- project-specific configuration: `.codex/config.toml`
- user-specific configuration: `~/.codex/config.toml`


### `config.toml`
The most important configuration keys are:

- `sandbox_mode`: the sandbox mode to use. Valid values are:
    - `read-only`: approval required for all edits
    - `workspace-write`: most files in the workspace are editable (except for `.codex`, `.git`, and similar files)
    - `danger-full-access`: No sandboxing

There can be several sections in the `config.toml` file:

- `[sandbox_workspace_write]`: the configuration for the `workspace-write` sandbox mode. Most important keys are:
    - `writable_roots`: the directories that are writable in the `workspace-write` sandbox mode. Array of strings.

## Notifications
By default, codex CLI sends notifications using the `OSC 9` (see [Operating System Command (OSC) Escape Sequences](./Programming/Common.md#terminal-control-escape-sequences)) escape sequence. This sequence is not supported by all terminals, including the Windows Terminal. Therefore, as a fallback, the CLI sends a `BEL` control code (see [Single characters (C0 control codes)](./Programming/Common.md#terminal-control-escape-sequences)) to send an alert sound.

To get a notification in Windows Terminal without a sound, Windows Terminal can be configured to react to the `BEL` control code by flashing the window or the taskbar icon (see [Windows Terminal Configuration](./Windows/Windows%20Manual.md#windows-terminal-configuration)).


## Rules
[Official documentation](https://developers.openai.com/codex/guides/agents-md)

Rules are defined in `AGENTS.md` file. The user-specific global rules are stored in `~/.codex/AGENTS.md` file.