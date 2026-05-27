# Github Workflows
[Official documentation](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)

Github workflows are automated workflows working on Github servers. Each repository can have multiple workflows, each stored in a separate `YAML` file in the `<repository root>/.github/workflows` directory.

The structure of a workflow is:

- the workflow is triggered by a specific *event*
- the workflow run one or more *jobs*
    - each job runs one or more *steps*


## Events
Events can be:

- triggered by a repository change
- triggered from outside using a `repository_dispatch` event
- scheduled for a specific time
- executed manually


## The workflow file

- [Reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Tutorial](https://docs.github.com/en/actions/tutorials/create-an-example-workflow#understanding-the-workflow-file)

The workflow file is a `YAML` file stored in the `<repository root>/.github/workflows` directory. The most important keys are:

- `name` (optional): the name of the workflow in the UI
- `on`: the event that triggers the workflow
- `jobs`: the jobs to run. It is an object, where each key is a job name, and the associated value is an object defining the job.


### Job definition object
The job definition object has the following structure:

- `runs-on`: the *runner* to use to run the job. 
- `steps`: the array of steps to run. 

### Step definition object
Each step is an object with the following structure:

- `name` (optional): the name of the step in the UI
- `uses`: the action to use to run the step, specified as `<actor owner>/<action name>@<version>`
- `run`: the command to run. An alternative to `uses` if there is no action available for the task.
- `with`: configuration object for the action.


## Actions
Actions are predefined scripts available in the [Github Actions catalog](https://github.com/actions). With actions, we can perform standard tasks with little effort.

The most important actions are:

- `checkout@v6`: checks out the repository to the `runner`'s working directory. This has to be the first action for any step that needs the content of the repository.


## Secrets
[Tutorial](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

For sensitive data that we do not want to store in the repository, we can use secrets system. The principle is as follows:

1. we define secrets in `Settings -> Secrets and variables -> Actions`
1. we refer to the secrets in the workflow file using the `${{ secrets.<secret name> }}` syntax.


# FTP Deploy Github Action
[Github](https://github.com/SamKirkland/FTP-Deploy-Action)

This GitHub action allows to automatically deploy a website to an FTP server. The action string is `SamKirkland/FTP-Deploy-Action@v4.4.0`.

Important configuration parameters are:

- `server`: the FTP server address
- `username`: the FTP username
- `password`: the FTP password
- `local_dir`: the local directory to deploy
- `server_dir`: the remote directory to deploy to