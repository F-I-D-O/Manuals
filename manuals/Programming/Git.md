# Basics
The structure of a single git repository is displayed in the following picture:
![Git Repository Structure](Git%20Scheme.png)

Explanation of the picture:

- The **working tree** or working directory is the directory where the files are stored, typically the root directory of the project where the `.git` directory is located.
- The **index** or staging area is a cache of all changes that are marked (*staged*) for the next commit. To stage a change, we need to call `git add` command. Only files in the index are committed when we call `git commit`.
- The **HEAD** is a pointer to the last commit in the current branch. 

The following scheme shows the operations that can be performed between the working tree, index, HEAD and the remote repository (blue arrows represent the typical workflow):
![Git Operations](Git%20Operations.png)


# Configuration
The git configuration is stored in the `.gitconfig` file in the user's home directory. It can be edited by editing the file directly, or by calling `git config` command.

To display the active configuration in the command line, call:
```bash
git config --list
```

We can also show whether the configuration results from the system, user or local configuration file:
```bash
git config --list --show-origin
```

# Basic Tasks

## Rewrite remote with local changes without merging

```bash
git push -f
```

## Go back to branch

```bash
git revert --no-commit 0766c053..HEAD
```

## Untrack files, but not delete them locally:

```bash
git rm --cached <FILEPATH>
```

usefull params:

- `-r`: recursive - deletes content of directories
- `-n` dry run


# Remote Repositories
[Git Basics manual](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

Normally, we have a single remote repository, which is typically called `origin`. In this repository, we share the code with other developers. In this case we don't have to care about the remote repository handling, because the remote is automatically set to the repository we cloned from.

However, sometimes we need to work with multiple remote repositories. In this case, we have to add remotes manually and also specify the remote repository when we push or pull.

To **add a remote**, we call:

```bash
git remote add <remote name> <URL>
```
Where the remote and `<URL>` is is the link we use to clone the repository.

To **list remotes**, we call:

```bash
git remote -v
```

Then we need to specify the remote when we want to use a command that interacts with the remote repository and we want to use a remote other than the default one. For example, to push to a remote repository, instead of just `git push`, we call:

```bash
git push <remote name> <branch name>
```


# Reverting
When we want to revert  something using git there are multiple options depending on the situation. The commands are:

- [`git checkout`](https://git-scm.com/docs/git-checkout) for overwriting local files with version from a specified tree (also for switching branches) and
- [`git reset`](https://git-scm.com/docs/git-reset) for reverting commits and effectively rewriting the history.
- [`git read-tree`](https://git-scm.com/docs/git-read-tree): similar to checkout, but does not require a cleanup before

The following table shows the differences between the commands:

| Command | revrerts commits | overwrite local changes |  delete files committed after `<commit>` |
| --- | --- | --- | --- |
| `git checkout <commit>` | no | yes | no |
| `git read-tree -m -u <commit>` | no | yes | yes |
| `git reset --soft <commit>` | yes | no | no |
| `git reset --hard <commit>` | yes | yes | yes |

To decide between the commands, the first consideration should be whether we want to preserve the history or not:

- we want to reach a specific state in the history and commit the changes as a new commit -> use `git checkout` or `git read-tree`
- we want to reach a specific state in the history and discard all changes after that point -> use `git reset`

## Keep the history
If we want to keep the history, there are still two options:

- we want to revert the whole working tree and also delete all files that were committed after the specified commit -> use `git read-tree -m -u <commit>`
- we want to revert the whole working tree, but keep all files that were committed after the specified commit -> use `git checkout <commit>`
- we want to revert only some files -> use `git checkout <commit> <filepath>`

### Using `git checkout`
To reset an individual file, call: `git checkout <commit> <filepath>`, to reset all files, call: `git checkout <commit> .`. 

If the `<commit>` parameter is ommited, the local files will be overwritten by the HEAD.  


## Drop the history
Dropping the history can be useful in many cases. For example, we may commit some changes to the master, but then we realize that they belong to a branch. A simple solution is to create a branch, and then reset the master to the previous commit.

Note that if the wrong history was already pushed to the remote, we need to fix the history on the remote as well. This is done by force pushing:

```
git push -f
```




# Wildcards
Can be used in gitignore and also in some git commands. All described in the [Manual](https://git-scm.com/docs/gitignore#_pattern_format). Usefull wildcards:

- `**/` in any directory
- `/**` everything in a directory


# Removing files from all branches, local and remote 

Removing files from history can be done using multiple tools:

1. [bfg repo cleaner](https://rtyley.github.io/bfg-repo-cleaner/) is the simplest tool. It can only select files by filename or size, but that is sufficient in most cases. 
2. [git filter-repo](https://github.com/newren/git-filter-repo/) is a more sophisticated successor to BFG. It can do almost anything possible. Nevertheless, it is less intuitive to operate, and it is harder to analyze its result.
3. The [`filter-branch`](https://git-scm.com/docs/git-filter-branch) command is the original tool for filtering git history. It is slow and problematic, so it should be used only if the above two tools are not available.  

**No matter of the used tool, before you begin:**

1. commit and push from all machines,
2. backup the repository

**Similarly, at the end:**

- **It is important not to merge (branch or conflitcs) that originated before the cleanup** on other machines. Otherwise, the deleted file can be reintroduced to the history.
- Pull on other machines.
- **Add the file to gitignore** so that it wont be commited again

## BFG
With BFG, **only a file with specific filename can be deleted**. It is not possible to use exact file path. To remove file by its name:

1. remove the file locally
2. clone the whole repo again with the `--mirror` option
3. on the mirrored repo, run the cleaner: `bfg --delete-files <FILENAME>`
4. run the git commands that appears at the end of the bfg output
5. run git push

## Git filter-repo
The git filter-repo can be installed using pip: `pip install git-filter-repo`.

To remove file by its path:

1. run the command: `git filter-repo --invert-paths --force --dry-run --path <PATH TO THE FILE TO BE REMOVED>`
2. inspect the changes in `.git/filter-repo` directory:
	- Compare the files in KDiff3
	- To skip the lines  starting with `original-oid`, 
		1. go to the file selection dialog
		2. click Configure
		3. to the line-matching preprocessor command, add: `sed 's/original-oid .*//'`
3. add remote again: `git remote add origin <REPO SSH ADDRESS>`
4. force push the comman to the remote `git push origin --force --all`
	- If the push is rejected by the remote hook, the master branch is probably protected. It has to be unprotected first in the repository config. 

[git filter-repo manual](https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html)

[More information on github](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)


## filter-branch

````
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch <FILE>' --prune-empty --tag-name-filter cat -- --all
````

# Merging

Syntax:

```
git merge <params> <commit>
```

Merge can be aborted at any time by calling `git merge --abort`. This resets the state of the repository.

## Resolving Conflicts
Sometimes, the same file is changed on the same line in both branches we are merging. This is called a conflict. In this case, the conflicting content is marked with conflict markers:
```
<<<<<<< HEAD
This is the content of the file in the current branch
=======
This is the content of the file in the branch we are merging
>>>>>>> branch-a
```

We can resolve the conflict manually by editing the file, but more often, we want to use a merge tool. To do that, we can call:
```
git mergetool
```
The mergetool should be first configured, as the default one (vimdiff) is not very user friendly. To configure the mergetool, we edit the git configuration. The appropriate section is `mergetool`. It has a lot of options, but for typical mergetool, is enough to set the name, as the `mergetool` command for that specific merge tool is preconfigured in recent versions of git. Example of the `.gitconfig` file configured for KDiff3:
```
...
[mergetool "kdiff3"]
...
```

[More information on git mergetool](https://git-scm.com/docs/git-mergetool)


### Debugging mergetool
Sometimes, this error can occur after calling `git mergetool`:
```
git-mergetool--lib "command not found"
```
This means that the mergetool is misconfigured. Inspect the `mergetool` section in the `.gitconfig` file to find the error.


## Merging Moved Files

Sometimes, it's necessary to tweak the command to help it locate the moved files. What can help:

- `-X rename-threshold=25`: Changing the threshold is important for languages that changes the file content when moving it with automatic refactoring (especially important for Java files, which usually have tons of imports)
- `-X ignore-space-change`

## Revert merge

```bash
git revert -m 1
```

Note that when the merge is reverted, the changes cannot be merged again, because they predates the revert!

# Update
On windows, run: `git update-git-for-windows`

# Pull Requests
Pull requests are a way to propose changes to the repository. The principle is as follows:

1. Create a branch for the changes
2. Commit the changes to the branch and push it to the remote
3. Create a pull request on the remote, that suggest to merge the branch into the master branch

There are two possible scenarios:

- We have the permission to create a branch in the repository: in this case, we can create the branch directly on the remote
- We do not have the permission to create a branch in the repository: in this case, we have to:
	1. Fork the repository
	2. Clone the fork
	3. Create the branch locally in the fork
	4. Commit and push the changes to the fork
	5. Create a pull request from the fork to the original repository

##  Update pull request
If there are changes requested by the reviewer or we just forgot to add something, we can update the pull request by pushing the updates to the PR branch. The pull request will be automatically updated.


# GitHub

## Creating a GitHub Release
To create a release:

1. In the repository, under the `Releases` heading, click `Create a new release`
1. Click on the `Choose a tag` dropdown
1. Select an existing tag or create a new one by filling the text field with the tag name and clicking `Create new tag` button
1. Fill the `Release title` and `Description` fields
1. Click `Publish release`


## GitHub CLI
Github has a CLI tool that can be used to interact with the repository. The tool can be installed from the [GitHub CLI page](https://cli.github.com/). The main command is `gh`.

Typically, we need to authenticate the tool first by calling [`gh auth login`](https://cli.github.com/manual/gh_auth_login). There are two options for authentication:

- browser authentication (default)
- token authentication: suitable for automation
	- only the old token type can be used, the fine-grained tokens are not supported yet


### Token Authentication
To authenticate using a token, we first need to create a token:

1. Go to `Settings` -> `Developer settings` -> `Personal access tokens`
1. Click `Tokens (classic)`
1. Click `Generate new token` -> `Generate new token (classic)`
1. Fill the token description and select the scopes
1. Click `Generate token`

Then we can authenticate using the token. We can either

- suply the token to the `gh auth login` command:
	```PowerShell
	gh auth login -h github.com -p ssh --skip-ssh-key --with-token <TOKEN>
	```
- or set the environment variable `GH_TOKEN` to the token value and call commands without authentication.


### Managing realeases
Required permissions:

- `public_repo` if the repository is public
- `repo` if the repository is private

To **create** a release, we can the [`gh release create`](https://cli.github.com/manual/gh_release_create) command:
```PowerShell
gh release create <TAG> --repo <REPO> --title <TITLE> --generate-notes
```
Here, the `<REPO>` is the full url of the repository, e.g. `git@github.com:F-I-D-O/Future-Config.git`

To **delete** a release, we can call the [`gh release delete`](https://cli.github.com/manual/gh_release_delete) command:
```PowerShell
gh release delete <TAG> --repo <REPO> --cleanup-tag -y
```



## Repository Migration

https://github.com/piceaTech/node-gitlab-2-github