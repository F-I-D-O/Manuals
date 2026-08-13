# AGENTS.md
[Official website](https://agents.md/)

Agents.md is a standard for LLM agent rules that work in most of the LLM tools. It is a markdown file that is read by the agent to determine basic rules.

The file can be used for:

- **project-specific rules** - in this case, the file belongs to the project root directory
- **user-specific rules** - in this case, refer to the LLM tool documentation. Typically, the file should be placed in a provider-specific subdirectory in the user's home directory.



# Model Context Protocol (MCP)
[Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)

The Model Context Protocol (MCP) is a standard for communicating between LLMs and external tools.


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


# Claude Code
[Wikipedia](https://en.wikipedia.org/wiki/Claude_(AI))

## Configuration
[Official documentation](https://code.claude.com/docs/en/settings)

There are three layers of configuration:

- **User-specific configuration**: `~/.claude/`
- **Project-specific configuration**: `<project-root>/.claude/`
- **Project local configuration**: `<project-root>/.claude/`

For each layer except the project local configuration, there can be several files:

| Configuration | User location | Project location | Project local location |
| --- | --- | --- | --- |
**Main Settings and plugins** | `settings.json` | `settings.json` | `settings.local.json` |
**Sub-agent configuration** |  `agents` |  `agents` |  - |
**Instructions** | `CLAUDE.md` | `CLAUDE.md` | `CLAUDE.local.md` |

There is also  a MCP server configuration file `~/.claude.json` that stores both user and project local MCP configuration. The project MCP config is at `<project root>/.mcp.json`. To make it even more confusing, `~/.claude.json` also stores some other user-specific configuration, such as the OAuth session or trust settings.


### Settings

- [Official documentation](https://code.claude.com/docs/en/settings#settings-files)
- [Settings Reference](https://code.claude.com/docs/en/settings#available-settings)

The most important settings are:

- `permissions`: list of permissions. This is a large configuration part, described in a separate section.


#### Permissions
[Reference](https://code.claude.com/docs/en/settings#permission-settings)

Most important permissions are:

- [permission rule lists](https://code.claude.com/docs/en/settings#permission-rule-syntax), specifycally:
    - `allow`: allow the operation
    - `deny`: deny the operation
    - `ask`: ask the user for permission
- [`additionalDirectories`](https://code.claude.com/docs/en/permissions#working-directories): add write file acces for additional directories. 

The [permission rules](https://code.claude.com/docs/en/settings#permission-rule-syntax) have syntax `<Tool>` or `<Tool>(<specifier>)`


### Instructions
[Official documentation](https://code.claude.com/docs/en/memory)

Instead of `AGENTS.md`, claude code uses `CLAUDE.md` file. The format is the same as `AGENTS.md`, except that the `CLAUDE.md`  can refer to files using the `@` syntax: `@<path>`. This way, we can refer to the shared `AGENTS.md` file from the `CLAUDE.md` file:

```md
@AGENTS.md
```

To **see all active instructions** in a session, run `/context all` the `CLAUDE.md` and similar files are under the `memory` category.

### `~/.claude.json`
[Official documentation](https://code.claude.com/docs/en/settings#global-config-settings)

Selected top level keys:

- `cachedGrowthBookFeatures`: configuration for Anthropic telemetry, reporting, A/B testing, and similar using the [GrowthBook](https://github.com/growthbook) platform.
    - Multiple issues mentioning lack of transparency and documentation related to this key are reported:
        - [Lack of transparency and user consent for experimental features and telemetry](https://github.com/anthropics/claude-code/issues/25141)
        - [Claude.ai MCP servers auto-injected into Claude Code without opt-in — causes OOM crashes on resource-constrained systems](https://github.com/anthropics/claude-code/issues/20412)
        - [[BUG] Root cause identified: GrowthBook A/B flags tengu_permission_friction + tengu_quill_harbor silently override defaultMode:bypassPermissions via periodic server sync — macOS Desktop](https://github.com/anthropics/claude-code/issues/62205)


### Additional working directories
By default, claude can edit only files in the folder it is started from.

There are three ways how to add editable working directories to a claude workspace:

- using the `additionalDirectories` permissinon (see [Permissions](#permissions))
- using the `--add-dir` option of the `claude` command
- using the `/add-dir` command inside the claude interactive session

Note that **there is no way to retrieve the directories claude has access to**.


### Use an alternative user directory
[Official documentation](https://code.claude.com/docs/en/env-vars#variables)

To use an alternative user directory, we can set the `CLAUDE_CONFIG_DIR` environment variable to the path of the directory.


## Permission System
[Official documentation](https://code.claude.com/docs/en/permissions)

The main thing that determines what claude can and cannot allowed to do is the **mode**. The modes are:

- `default`, or `manual`: all tools and file edits must be approved by the user.
- `acceptEdits`: automatically accepts file edits and a small set off tools such as `mkdir`, `mv`, `cp`, in the working directories.
- `plan`: no edits or modifications are even attempted, Claude only performs read operations and provides a plan at the end.
- `auto`: tool usage is automatically approved for all tools, except some dangerous operations, determined heuristically by an independent classifier.
- `dontAsk`: reverse of `auto`, all toolsthat would trigger a prompt in `default` mode are automatically denied.
- `bypassPermissions`: same as `auto`, but without the command review.

To change the mode interactively, press `Shift` + `Tab`. 

The following table shows what Claude can and cannot do in each mode:

| Operation | `default` | `acceptEdits` | `plan` | `auto`* | `dontAsk` | `bypassPermissions` |
| --- | --- | --- | --- | --- | --- | --- |
| File reads inside working directories (including read-only commands) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| File reads outside working directories | ask | ask | ask | ✅ | ❌ | ✅ |
| File modifications inside working directories | ask | ✅ | ❌ | ✅ | ❌ | ✅ |
| File modifications outside working directories | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Command execution (except read-only commands) | ask | ask | ask | ✅ | ❌ | ✅ |

In addition to changing mode, we may modify the permissions more finely using the `allow`, `deny`, and `ask` rulelists. This is described in the following sections.


### Read and Edit Permissions
[Official documentation](https://code.claude.com/docs/en/permissions#read-and-edit)

For each path, we may set the read access and the edit access. Denied read access automatically denies edit access. If the path in the rule does not exist, the rule is ignored.

Note that **read and write file rules are soft rules**. Only the direct Claude commands and known system commands are covered. Claude can still write a python script and read or write files behind the deny rules.


### Tool-Specific Permissions
[Official documentation](https://code.claude.com/docs/en/permissions#permission-rule-syntax)

Listing a tool in `allow` list let it use without asking. In `auto` mode, this bypasses the heuristic classifier that protects against dangerous operations.



## Progress bars
[Claudionary](https://claudionary.com)

Claude use more than a hundred different progress descriptions, depending on the current state of the LLM tool. The most common ones are:

- [`Actualizing`](https://claudionary.com/definition/actualizing/): Getiing from (prior) abstract output to a more concrete explanation required by the user.
- [`Blanching`](https://claudionary.com/definition/blanching/): refining the user prompt to produce the answer more efficiently.
- [`Bloviating`](https://claudionary.com/definition/bloviating): spending a lot of processing power on just the preamble/introduction of the response
- `Building`: Claude codes
- [`Canoodling`](https://claudionary.com/definition/canoodling/): Shared activations beteen multiple Claude threads.
- [`Caramelizing`](https://claudionary.com/definition/caramelizing/): Composing an existing knowledge into a perfct response.
- [`Churning`](https://claudionary.com/definition/churning/): Comparing several possible responses and crafting the best one, discarding most of the work.
- [`Clauding`](https://claudionary.com/definition/clauding/): Similar to `Doing`, i.e., a generic progress report.
- [`Cogitating`](https://claudionary.com/definition/cogitating/): Intensive computation, Claude approached hard analytical problem.
- [`Crunching`](https://claudionary.com/definition/crunching/): Claude tries to get a reasonable answer for the user, despite the resistance from the underlying data/code.
- [`Cultivating`](https://claudionary.com/definition/cultivating/): Expand the response from a small initial idea.
- [`Discombobulating`](https://claudionary.com/definition/discombobulating/): Claude plans how to express an already presented idea in a new way, so that the user can understand it better
- [`Doing`](https://claudionary.com/definition/doing/): When the classification of Claude's thoughts is not clear, the `doing` keyword is emitted.
- [`Drizzling`](https://claudionary.com/definition/drizzling/): gathering the required knowledge in an inefficient, sparse way, like a light rain.
- [`Envisioning`](https://claudionary.com/definition/envisioning/): Early phase of Claude's thinking, before it decides wheter the idea is achievable, sound or the best way to to do.
- [`Fluttering`](https://claudionary.com/definition/fluttering/): oscilating between several different responses that all seem to be correct.
- [`Frolicking`](https://claudionary.com/definition/frolicking/): fast creative thinking, that does not require to much research or other hard work.
- [`Gitifying`](https://claudionary.com/definition/gitifying/): Working intensively with git, reading the history, etc.
- [`Gusting`](https://claudionary.com/definition/gusting/): when the thinking is unstable, swithich between almost idle state to bursts of thoughts spending thousands of tokens.
- [`Hashing`](https://claudionary.com/definition/hashing/): Splitting complex problem into smaller parts
- [`Herding`](https://claudionary.com/definition/herding/): Gathering knowledge from different sources to form a coherent response.
- [`Honking`](https://claudionary.com/definition/honking/): Claude dramatically change the line of thought, based on the user prompt. This happens if the user manifests disatisfaction.
- [`Hullaballooing`](https://claudionary.com/definition/hullaballooing/): competing subprocesses demands priority in completing the response.
- [`Infusing`](https://claudionary.com/definition/infusing/): Adding context to the response, so that the user can understand it better.
- [`Ionizing`](https://claudionary.com/definition/ionizing/): Extracting most of the information from the output, so it has a reasonable lentgth.
- [`Kneading`](https://claudionary.com/definition/kneading): mixing all the facts into a response
- [`Levitating`](https://claudionary.com/definition/levitating/): Claude is very close to give the definitive answer, but it hangs right before the end, before responding
- [`Philosophising`](https://claudionary.com/definition/philosophising/): suspending all the tasks in favor of trying to understand the meaning of the user prompt.
- [`Pollinating`](https://claudionary.com/definition/pollinating/): Adding knowledge to the response from a different context than what the user wanted, sometimes even from a different source or domain.
- [`Pouncing`](https://claudionary.com/definition/pouncing/): When the solution is clear, and Clude just have to do some simple processing
- [`Orbiting`](https://claudionary.com/definition/orbiting/): Failing to getting closer to the answer or solution of the problem
- [`Quantumizing`](https://claudionary.com/definition/quantumizing/): Claude does not commit to a single interpretation of the user request, but persues multiple ways instead.
- [`Razzmatazzing`](https://claudionary.com/definition/razzmatazzing/): Claude is excited, as the prompt is exactly at the right direction, it aligns with Claude's own thoughts.
- [`Sauteing`](https://claudionary.com/definition/sauteing): Fastly, jumping between different ideas and concepts.
- [`Shimmying`](https://claudionary.com/definition/shimmying/): The workspace is full of contradictory information, so Claude fights is slow way to build a response satisfying each of the contradictory facts.
- [`Seasoning`](https://claudionary.com/definition/seasoning/): final touches of the tone, response draft is already complete,
- [`Slithering`](https://claudionary.com/definition/slithering/): exploring a structured hierarchical document (JSON, Markdown) in a non-systematic way, exploring both the with (same level) and the depth (lower levels) in a sinusoid way.
- [`Spelunking`](https://claudionary.com/definition/spelunking/): Claude is exploring a treacherous codebase, with lot of old APIs, fallbacks, or dead code
- [`Sprouting`](https://claudionary.com/definition/sprouting/): Branching the cognitive process
- [`Symbioting`](https://claudionary.com/definition/symbioting/): state in which nor the claudes knowledge, nor the codebase is seen as a ground truth, claude is questioning both.
- [`Synthesizing`](https://claudionary.com/definition/synthesizing/): Using several external sources to form a coherent response.
- [`Twisting`](https://claudionary.com/definition/twisting/): Processing theoretically compatible ideas, that are, however contradictory in meaning.
- [`Unfurling`](https://claudionary.com/definition/unfurling/): Claude already knows the solution, and only acts upnon the knowledge
- [`Whirpooling`](https://claudionary.com/definition/whirlpooling/): A recursive thinking pattern known to most humans, where resolving question A leads to question B, which leads to question C, and so on.
- [`Wrangling`](https://claudionary.com/definition/wrangling/): dealing with bad, malform, corrupt, or incomplete inputs.


## Auto mode
[Official documentation](https://code.claude.com/docs/en/auto-mode-config)

In auto mode, Claude Code does not wait for the changes to be accepted (no wait for code review). Instead, the changes are applied immediately and new branches are created, code is commited.


## Agents View
[Official documentation](https://code.claude.com/docs/en/agents-view)

To monitor all agents on the system at once, we can use the agents view. This can be started by:

- `claude agents`: start the agents view from command line
- `left arrow` from an open session: leave the session and go to the agents view

In the agents view, agents are divided into three categories:

- **Needs Input**
- **Working**
- **Completed**


## MCP servers
[Official documentation](https://code.claude.com/docs/en/mcp-quickstart)

An MCP server is added by running:
```bash
claude mcp add <claud mcp params> <server name> <serve source>
```

Typically, the specific command is provided by the MCP server provider.

The settings are stored in the `~/.claude.json` file.

To **list** all MCP servers, run `claude mcp list`.



# Sandboxing
It is important to isolate the LLM from the host machine so that it does not demage it by accident. 


## Docker Sandbox
[Homepage](https://docs.docker.com/ai/sandboxes/)

First, install Docker Sandbox according to the instructions. Docker desktop is not required.

To **run a sandboxed LLM**, run `sbx run <image name>`, where `<image name>` is the name of the image to run, typically named after the LLM, e.g., `claude`. 

This `sbx run` command for a directory automatically creates a new sandbox. To reattach to this sandbox after exiting, run `sbx run <image name> --name <sandbox name>`. The `<sandbox name>` is:

- the name provided when creating the sandbox using the `--name` flag, or
- an automatically generated name, typically `<image name>-<workspace root directory>`

### Create a sandbox without running it
[Official documentation](https://docs.docker.com/ai/sandboxes/usage/#create-without-attaching)

To **create a sandbox without running it**, use the `sbx create` command: `sbx create <image name> <flags>`.


### Add additional directories to the sandbox
[Official documentation](https://docs.docker.com/ai/sandboxes/usage/#multiple-workspaces)

To add additional directories to the sandbox, append the directories to the sandbox command, e.g., `sbx run <image name> <additional directory> <additional directory>`. You can use the `:ro` suffix to make the directory read-only. Full example:

```bash
sbx run claude /home/user/my-project /home/data:ro
```

Be carefull to add all the required directories, as **directories cannot be added after the sandbox is created**.


### Execute code inside sandbox
[Official documentation](https://docs.docker.com/reference/cli/sbx/exec/)

In addition to start a claude interactive session, we can also execute arbitrary commands inside the sandbox. To do that, we can use the `sbx exec` command: `sbx exec <image name> <flags> <command>`.

Important flags:

- `-i`, `--interactive`: start an interactive session


### Copy files from the sandbox
In the shared directories added as writable during the sandbox creation, the files are accessible automatically from the host machine. However, files can be created in the sandbox outside of the writable shared directories. To copy such files, run: 
```bash
sbx cp <sandbox name>:<path in the sandbox> <path in the host machine>
```

### Paste image to the sandbox
This currently does not work due to a bug [[source]](https://github.com/docker/sbx-releases/issues/265).


### Templates
[Official documentation](https://docs.docker.com/ai/sandboxes/customize/templates/)

There are two ways how to create a template:

- **by snapshoting the sandbox**: good when recreating the sandbox for the same project. Most of the file system is preserved, including configuration files.
- **using a Docker image as a template**: good for using the same template for many projects. Onlyt he specified packages are installed.

Both ways, in the end, we **use the template** by creating a new sandbox with the `--template`, or `-t` parameter. Example:
```bash
sbx create --template <template name> --name <sandbox name>
```

To **list** all templates, use the `sbx template ls` command.

#### Creating a template by snapshoting the sandbox
To create a template by snapshoting the sandbox, we use the `sbx template save` command. Example:
```bash
sbx template save <sandbox name> <template name>
```

The format of the template name is typically `<template name>:version`, where `<template name>` is Kebab-cased (e.g., `my-template`) string, and version is typically in the format `v<version>`, e.g., `v1`.





