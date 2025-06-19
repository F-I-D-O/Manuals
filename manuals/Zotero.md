# Installation
It’s important to do these steps in exactly this order. **Connecting to the Zotero account before setting up file sync from owncloud can result in article loss** due to low space in the Zotero cloud account!

1. Install and set up ownCloud
1. Install Zotero
1. Log in to Zotero account and sync data from cloud
    1. `Zotero Preferences` -> `Sync`
    1. In `Data Syncing Section`, connect to Zotero account
        - **after successful connection, do not leave settings or confirm the setup!**
    1. in `File Syncing section` that just appeared:
        1. check `Sync attachment files in My Library using` and select WebDAV 
        1. set URL: `owncloud.cesnet.cz/remote.php/webdav`
        1. set username: `fiedlda1@fel.cvut.cz`
        1. set password: `<owncloud webdav password>`
        1. click `Verify Server`
    1. leave settings and click the sync button
1. Install BetterBibLatex plugin (from file)


# Set up the LaTeX \cite Command Drag’n’drop
Two things need to be set up correctly in the Preferences:

- `Better BibTeX` -> `QuickCopy/drag-and-drop citations` -> `QuickCopy format needs to be set to LaTeX`
- `Export` -> `Default format needs to be Better BibTeX Citation Key Quick Copy`

# Integration with Local Projects

# Automatic Better BibTex Export

1. right-click on your library
1. `Export Library`
1. Choose `Better BibLatex` format and check `keep updated`
1. Save the file to your desired location

# Integration with Overleaf
There are two basic options:

- Pin the keys using better bibtex and use the standard Overleaf Zotero integration
- Upload the bibliography file manually to your repo

Despite it may seem strange, the first option requires more maintenance, as the keys have to be pinned manually, which can be done in bulk, but new items in your library are not pinned automatically. Therefore, we will use the second option.

In order to get automatic upload work, we need to set two things:

- `BetterBibTex` automatic export of the Zotero library to file (see Automatic Better BibTex Export)
- Automatic upload of the file to Overleaf (see next section)

# Automatic Upload of the Bibliography File to Overleaf
Again, there are two options on how to sync your local reference file with Overleaf: Git and Cloud sync. Git has an advantage of keeping the history, but the auto-commit and push hook can be a distraction, and in the case of multiple repositories, it can be also very slow. The cloud sync is simpler and faster but requires manual refresh in overleaf (just like the built-in Zotero integration).

## Cloud Sync Direct Link Integration

1. Choose a cloud storage provider that supports direct download links (GoogleDrive, DropBox, Owncloud…)
1. export your references to the folder you have in sync with cloud storage 
1. Share the reference file by link and copy a direct download link to clipboard
1. In Overleaf, click the upload button, choose from external URL and paste the direct download link to the URL field
1. if your library changes, select the reference file and click on the refresh button

## Cloud Sync Dropbox Integration

## Git


