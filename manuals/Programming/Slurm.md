
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
- `-u <username>` filter just a specific user
- `--start` print the expected start time and the nodes planed to run the task
- `-w --nodelist` filter jobs running (but not planned) on specific nodes. The format for nodelist is `<name>[<range>]`, e.g., `n[05-06]`.

## [sinfo](https://slurm.schedmd.com/sinfo.html)
Prints information about the computer cluster.