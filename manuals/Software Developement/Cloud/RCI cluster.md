# General

- [Form to get access to the RCI cluster](https://docs.google.com/forms/d/e/1FAIpQLSewws_V6-D567fkp6QZmr0GQlkzQrEoB6QquAgQkZu8so818Q/viewform)
- [Official instructions](https://login.rci.cvut.cz/wiki/how_to_start)
- [Storage manual and description of the partitions](https://login.rci.cvut.cz/wiki/storage)

## Usual command Usage

- You can watch your jobs with `squeue -u username`.
- You test/debug your program when running it with `srun` command
    - you usually don’t have to allocate resources when testing
    - To start an interactive shell, run: `srun -p cpufast --pty bash -i`
    - Set your main script file (sh) executable via `chmod +x <filename>` command 
    - Test your script in console
    - Cancel the job: `scancel <JOB ID>`
- You run your job with `sbatch` command with allocated resources
    - Example sbatch: `sbatch --mem=30G -t 60 -n30 -o /home/fiedlda1/Amodsim/log/ih.log /home/fiedlda1/Amodsim/rci_launchers/ih.sh`

# How to clone projects
Usually, you need to clone some of the SUM projects to start working on the RCI cluster. To do that:

1. Copy your key to `~/.ssh/`
2. Set file permissions to your ssh key safely
3. Modify `~/.ssh/config IdentityFile` to point to your key
4. Clone your project

# Specifics for java projects

1. Clone project on RCI cluster
2. Download binary maven from: http://maven.apache.org/download.cgi and export it to your home folder on the RCI cluster.
3. Prepare your bash script
    - Add `#!/bin/bash` to the first line
    - Change the environment variable `PATH` for your maven location with this command: `PATH=$PATH:/home/$USER/apache-maven-3.6.1/bin/`
    - Load all required software via ml command, definitely `ml Java`
    - Build, compile, run your project via `mvn` commands
    - Set your file executable via `chmod +x filename` command
    - Example run command: `mvn exec:exec -Dexec.executable=java -Dexec.args=’-classpath %classpath -Xmx30g  cz.cvut.fel.aic.amodsim.OnDemandVehiclesSimulation /home/kholkolg/amod-to-agentpolis/local_config_files/olga_vga_RCI.cfg’ -Dfile.encoding=UTF-8`
    - Example -  Bash script for amodsim project: 
4. Run your script with srun, sbatch etc. commands, I recommend first use srun, to check everything is set up ok and then use sbatch command, because if computational nodes are busy, your job will be added to the queue and you can do other work.

# Specifics for python projects

1. First load the appropriate version of python, e. G.: `ml Python/3.6.6-foss-2018b`
2. You can’t just install the packages with `sudo`, you have to install them to the user space instead:
    - Run `pip install --user packagename`

# Specifics for C++ projects

## Workflow options
As linux binaries are usually not portable. They are not compatible with older linux versions due to the infamous `glibc` incompatibility. There are three solutions to this problem:

| Method | Setup | Program Upgrade |
|---------|-------|--------|
| Compile the code on the RCI | Setup the compilation on RCI. | Copy the source code to RCI and recompile after every change |
| Use a [Singularity](https://en.wikipedia.org/wiki/Singularity_(software)) container | learn with singularity, create the container | Generate new container and copy it to the RCI |
| Build a compatible binary using a [modified toolchain](https://crosstool-ng.github.io/docs/introduction/) | learn with a toolchain generator, configure and generate the right toolchain | Copy the updated binary


## Building on RCI
In general the workflow is the same as on a local machine. The difference is that we do not have root access, so for all needed tools, we have to either  load them via `ml` command, or, if not available, install them in the user space. Typically, we need to load:

- git: `ml git`
- GCC: `ml GCC`
- CMake: `ml CMake`



# Specific for projects with gurobi

1. Load Gurobi with 
    - `ml Gurobi`
    - or `ml Gurobi/8.1.1-foss-2018b-Python-3.6.6` for a specific version
2. Be aware that this operation can reload other packages

## Gurobi and Java
It is necessary to install Gurobi to maven: `mvn install:install-file -Dfile=/mnt/appl/software/Gurobi/9.0.3-GCCcore-8.3.0-Python-3.7.4/lib/gurobi.jar -DgroupId=com.gurobi -DartifactId=gurobi -Dversion=1.0 -Dpackaging=jar`


## Gurobi and C++
As RCI use Linux as OS, we need to compile the Gurobi C++ libs with the same compiler as the one we use for compilation of our code (see C++ Workflow for more details). Note that **this is necessary even if the Gurobi seems to be compiled with the same copiler we use for compilation**.

Unlike in Linux installation we controll, we cannot build the C++ lib in the Gurobi installation folder. To make the Linking work, foloow these steps:

1. copy the `src` dir from the RCI Gurobi module located at `mnt/appl/software/Gurobi/<desired version>` to our home
2. run make located in `src/build`
3. copy the `libgurobi_c++.a` to the `lib` subfolder of your project
4. configure the searching for the C++ lib in `FindGUROBI.cmake` file:

    ```cmake
    # Find the Gurobi C library
    find_library(GUROBI_LIBRARY
        NAMES gurobi<version>
        HINTS ${GUROBI_DIR} $ENV{GUROBI_HOME}
        PATH_SUFFIXES lib
    )

    # Find the Gurobi C++ library
    find_library(GUROBI_CXX_LIBRARY
        NAMES gurobi_c++
        HINTS ${PROJECT_SOURCE_DIR}
        PATH_SUFFIXES lib
        NO_CMAKE_ENVIRONMENT_PATH
        REQUIRED
    )

    # Find the Gurobi C++ debug library. We don't need it on RCI, but it may be required in CMakelists.txt. Therefore, we supply the release version as a debug version.
    set(GUROBI_CXX_DEBUG_LIBRARY ${GUROBI_CXX_LIBRARY})

    ```

5. if the CMake cache is already generated, delete it.
6. Generate the CMake cache and build the project







# Commands
For command description, see Slurm manual.


Main params

- `--mem=<required memory>`
     - `<required memory>` is in megabytes by default, for gigabytes, we need to add G
- `-t <time>`
    - Time in minutes

# Task Explanations
`srun --pty bash -i`
    - `--pty` runs the first task and close output and error stream for everything except the first task
    - `bash`: what we want to run
    - `-i` Input setting, here followed by no param indicating that the input stream is closed
osed

# Access the RCI cluster using JetBrains Gateway
When connecting to the RCI cluster, we have to use the `login2` or `login3` nodes. The `login1` node has an outdated version of `glibc` which is not compatible with the JetBrains Gateway.


# Resource limits
The resource limits are described in the [RCI cluster documentation](https://login.rci.cvut.cz/wiki/jobs_changes). However, the limits:

- do not cover the amd partitions, and
- there is no information how to determine the role for a user.

Therefore, to know exactly the limits, **it is best to use the [`sacctmgr show`](./Slurm.md#sacctmgr) command**.


# Installing Linux packages
Without root access, we have cannot install packages using the package manager. However, we can manually install them to home. Steps:

1. Locate the repository of the package that contains the packages for Red Hat Linux (rpm)
2. Download the package
3. Extract the package using `rpm2cpio pv-*.rpm | cpio -idmv`
4. Move the extracted files to the desired location in the home folder
5. Add the `bin` folder of the package to the `PATH` environment variable






