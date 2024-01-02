
# Configuration
The git configuration is stored in the `.gitconfig` file in the user's home directory. It can be edited by editing the file directly, or by calling `git config` command. 

To display the active configuration in the command line, call:
```
git config --list
```

We can also show whether the configuration results from the system, user or local configuration file:
```
git config --list --show-origin
```

# Basic Tasks

## Rewrite remote with local changes without merging

````
git push -f
````

## Go back to branch:

````
git revert --no-commit 0766c053..HEAD

````

## Untrack files, but not delete them locally:

```
git rm --cached <FILEPATH>
```

usefull params:
- `-r`: recursive - deletes content of directories
- `-n` dry run


# Reverting
When we want to revert  something using git there are multiple options depending on the situation. The commands are:
- [`git checkout`](https://git-scm.com/docs/git-checkout) for overwriting local files with version from a specified tree (also for switching branches) and
- [`git reset`](https://git-scm.com/docs/git-reset)

The following table shows the differences between the commands:
| Command | revrerts commits | overwrite local changes | 
| --- | --- | --- |
| `git checkout <commit>` | no | yes |
| `git reset --soft <commit>` | yes | no |
| `git reset --hard <commit>` | yes | yes |

### Using `git checkout`
To reset an individual file, call: `git checkout <filepath>`, to reset all files, call: `git checkout .`. By default, the local files will be overwrtitten by the head. To specify a specific commit, put another positional argument before `<filepath>`: `git checkout <commit> <filepath>`. 




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

## Revert merge:

````
git revert -m 1
````

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

# Repository Migration

https://github.com/piceaTech/node-gitlab-2-github