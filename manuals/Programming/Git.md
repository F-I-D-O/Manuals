Revert local changes (uncommited):
```
git checkout <pathspec>
```


Rewrite remote with local changes without merging

````
git push -f
````

Go back to branch:

````
git revert --no-commit 0766c053..HEAD

````

# Untrack files, but not delete them locally:

```
git rm --cached <FILEPATH>
```

usefull params:
- `-r`: recursive - deletes content of directories
- `-n` dry run

# Reset individual files
To reset an individual file, call: `git checkout <filepath>`

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

# Repository Migration

https://github.com/piceaTech/node-gitlab-2-github