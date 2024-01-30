# Submiting a paper to Arxiv
Before submitting a preprint to arxiv, you should check whether the journal allows it, and if so, what version of the paper can be submitted to arxiv. Links:
- [Taylor & Francis](https://authorservices.taylorandfrancis.com/research-impact/sharing-versions-of-journal-articles/)


Steps on arxiv:
1. First page: details
    - Select arxive as the license type
1. Second page: files
    - Papers written in latex have to be uploaded as source files
1. Third page: check the printed pdf
    - check that the pdf looks good. Check for missing references (`?`), or figures.
1. Fourth page: Metadata
    - keep authors in the LaTeX encoding, this is the way how arxiv wants it

## Uploading LaTeX source to Arxiv
The procedure should be as follows:
1. delete any images not used in the paper
1. check that the pdf looks good
1. commit and push the changes to master branch
1. delete all journal classes, style files, etc. 
1. write a title footnote about how the article is a preprint/accepted manuscript
    - example: This is an Accepted Manuscript of an article published by Taylor & Francis in the Journal of Intelligent Transportation Systems on 4th December 2022, available online: https://www.tandfonline.com/doi/abs/10.1080/15472450.2022.2121651
1. compile the paper till no errors are present
1. pack source files into a zip archive
    - do not include any temporary files
    - include the compiled bibliography file (`.bbl`)
1. create a new git branch
1. commit to the new branch, push it to the remote

## Creating new version of a paper
In the menu, click `Replace`. Then, the process is the same as the new submission.