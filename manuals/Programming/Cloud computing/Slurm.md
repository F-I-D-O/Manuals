# Introduction and basic terms
Slurm is a job scheduler for HPC clusters. It is used to manage the resources and to run the tasks. Because it uses a different terminology than typical users are used to, we start with a short introduction to the basic terms:

- *Association*: a record of a Slurm user. It consists of four fields:
    - *User*: the Linux user name
    - *Cluster*: the name of the HPC cluster
    - *Partition*: the name of the partition on the cluster
    - *Account*: the *bank account* of the user used to schedule the jobs.
- [*TRES (Trackable Resource)*](https://slurm.schedmd.com/tres.html): a resource that can be tracked by Slurm. It is used to limit the resources that a job can use. Most important TRES are:
    - cpu: number of CPUs
    - [*GRES (Generic Resource)*](https://slurm.schedmd.com/gres.html): other computing resources, e.g., GPUs.




# Commands

## [`srun`](https://slurm.schedmd.com/srun.html)
Run the task in the current shell in blocking mode, i.e., the console will be blocked till the task finishes. This command is only useful if we expect that the resources will be available immediatelly and the task will finish quickly. Otherwise, we should use `sbatch`.


Params:

- `--pty` runs the in terminal mode. Output and error streams are closed for everything except the first task.
- `-i` Input setting. If followed by no param, it indicates that the input stream is closed.

## [sbatch](https://slurm.schedmd.com/sbatch.html)
Request the execution of a task, with the required resources specified as `sbatch` parameters. The plain call with all resources defaulted is:
```bash
sbatch <bash script>
```

Note that the `<bash script>` here realy needs to be a bash script, it cannot be an arbitrary command or executable.

Important parameters:

- `-n, --ntasks`: maximum number of tasks/threads that will be allocated by the job
    - default is one task per node
- `-N, --nodes`: number of allocated nodes. 
    - default: minimum nodes that are needed to allocate resources according to other parameters (e.g., `--ntasks`, `--mem`).
- `--mem` maximum memory that will be allocated by the job. The suffix G stands for gigabytes, by default, it uses megabytes. Example: `--mem=40G`.
- `-t, --time`: time limit. possible formats are `<minutes>`, `<minutes:seconds>`, `<hours:minutes:seconds>`, `<days-hours>`, `<days-hours:minutes>`, and `<days-hours:minutes:seconds>`. 
    - default: partition time limit
- `-p`, `--partition=`: partition name
- `-o`, `--output=`: job's output file name. The default name is `slurm-<JOB ID>.out`

## [squeue](https://slurm.schedmd.com/squeue.html)

- `--me` filter just my jobs
- `-u <username>` filter just a specific user
- `--start` print the expected start time and the nodes planed to run the task
- `-w --nodelist` filter jobs running (but not planned) on specific nodes. The format for nodelist is `<name>[<range>]`, e.g., `n[05-06]`.


## [sinfo](https://slurm.schedmd.com/sinfo.html)
Prints information about the computer cluster.


## [scancel](https://slurm.schedmd.com/scancel.html)
The `scancel` command cancels the execution of a job specified by the ID (firsta argument). 

To instead cancel jobs by name, use the `--name` option. Note however, that **full name has to be specified and no wildcards are allowed**. To cancel all jobs with a certain name, we have to mess with various linux commands instead:

```bash
squeue --me | awk '/smod_cha/ {print $1}' | xargs scancel
```


## [sacctmgr](https://slurm.schedmd.com/sacctmgr.html)
The `saccmgr` command is for viewing and modifying Slurm account information. The most important command for users is `show` (or `list`, which is equivalent). 

### `sacctmgr show` (`sacctmgr list`)

The `show <entity>` subcommand is used to display information about Slurm *entities*. Based on the `<entity>` argument, it shows different information.

If we want to **display just some columns**, we can use the `format` argument:

```bash
sacctmgr show associations format=Cluster,Account,User,QOS
```

If we want to **filter rows**, we can use the *specifications* arguments that differ for each entity:

```bash
sacctmgr show associations Users=user1
```

The most important entities are:

- `associations`: associations between users and accounts, quality of service (QOS), etc. 
    - The important columns are:
        - `Cluster`: the name of the cluster
        - `Account`: the bank account
        - `User`: the Linux user name
        - `QOS`: the quality of service that is in effect for the association
    - The important [specifications](https://slurm.schedmd.com/sacctmgr.html#SECTION_SPECIFICATIONS-FOR-ASSOCIATIONS) are:
        - `Users`: display associations for a specific user
- `qos`: quality of service: limits and priorities for each group-queue combination
    - The important columns are:
        - `Name`: the name of the QOS
        - `Priority`: the priority of the QOS
        - `Preempt`: list of QOS names that can be preempted by this QOS
        - `MaxTRES`: maximum [TRES](#introduction-and-basic-terms) each job can use
        - `MaxTRESPerUser`: maximum [TRES](#introduction-and-basic-terms) each user can use, specified for each TRES separately
            - `cpu`: maximum number of CPUs
        - `MaxJobsPU`: maximum number of running jobs per user
        - `MaxSubmitPerUser`: maximum number of jobs that can be submitted by a user
- `tres`: [Trackable Resources](#introduction-and-basic-terms)







# Determining why the job was killed
Usually, the error message is at the end of the output file. Message meaning:

- `Detected 1 oom_kill event in ...`: oom stands for out of memory. The job was killed because it exceeded the memory limit.