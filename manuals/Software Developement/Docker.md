# Introduction

- [Homepage](https://www.docker.com/)
- [Documentation](https://docs.docker.com/)
- [Getting Started](https://docs.docker.com/get-started/)

Docker is the most popular containerization platform. Docker images can be run in multiple environments, including:

- Docker Desktop: a graphical user interface for running Docker containers on a local machine
- Docker Engine: a server that runs Docker containers
- Docker Sandbox: a lightweight virtual machine for running sandboxed environments
- and many more

Each setup is typically specified by a `YAML` file called *Compose file*.


## Docker Desktop

[Docker Desktop](https://www.docker.com/products/docker-desktop/)

Docker Desktop is a GUI program for running Docker containers on a local machine. The subcommand for it is `docker desktop`. The most important subcommands are:

- `docker desktop start`: starts the Docker Desktop application
- `docker desktop stop`: stops the Docker Desktop application
- `docker desktop restart`: restarts the Docker Desktop application


## Compose File

- [Documentation](https://docs.docker.com/compose/intro/compose-application-model/#the-compose-file)
- [Reference](https://docs.docker.com/reference/compose-file/)

The Compose file is a file named `compose.yaml` that specifies the services to be run. The top level elements of the file are:

- `name`: the name of the project
- `services`: most important part: the list of services to be run
- [`volumes`](https://docs.docker.com/reference/compose-file/volumes/): the list of Docker volumes (paths in a Docker filesystem) shared between multiple services


### Services

- [Documentation](https://docs.docker.com/reference/compose-file/services/)
- [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/)
- [Compose Deployment Specification](https://docs.docker.com/reference/compose-file/deploy/)

In Docker, a *service* is a definition of a computing resource within a computing infrastructure which can be replaced, updated, or scaled independently of the other components of the computing infrastructure.

Each service can be backed by one or more *containers*.

In the Compose file, a service is defined by a key value pair, where the key is the name of the service and the value is an object that specifies the configuration of the service.

Each service may either use an existing *image* of a container, specified under the `image` key, or create a custom image defined in the `build` section.

Important service object keys:

- [`build`](https://docs.docker.com/reference/compose-file/services/#build): configuration of the build process. If `image` is not specified, or the specified image does not exist, the build process is executed on `docker compose up`. 
- [`depends_on`](https://docs.docker.com/reference/compose-file/services/#depends_on): an array of service names that this service depends on. This control the starting order - the service basically waits for all the services listed in the `depends_on` array to be started.
- [`environment`](https://docs.docker.com/reference/compose-file/services/#environment): [environment variables](https://docs.docker.com/compose/environment-variables/) set in the container
- [`env_file`](https://docs.docker.com/reference/compose-file/services/#env_file): an environment file or array of files to load into the container. The environment files contain a list of environment variables, and are alternative to the `environment` key for the case when there are many environment variables.
- [`entrypoint`](https://docs.docker.com/reference/compose-file/services/#entrypoint): defines how the container can be run as an executable. Overrides the `ENTRYPOINT` instruction in the Dockerfile.
- [`healthcheck`](https://docs.docker.com/reference/compose-file/services/#healthcheck): configuration of a set of commands that must run successfully to determine whether the container is in a healthy state, or some error has occurred
- [`image`](https://docs.docker.com/reference/compose-file/services/#image): name of the image to use
- [`ports`](https://docs.docker.com/reference/compose-file/services/#ports): port mapping between host and container. See more in the [Ports](#ports) section.
- [`profiles`](https://docs.docker.com/reference/compose-file/services/#profiles): an array of profile names that should start the service. By default, every profile starts every service.
- [`volumes`](https://docs.docker.com/reference/compose-file/services/#volumes): host drives or folders to be mounted in the container


#### Ports

- [Compose File Documentation](https://docs.docker.com/reference/compose-file/services/#ports)
- [Detailed Port Mapping Configuration](https://docs.docker.com/engine/network/port-publishing/)

The ports section sepcifies the port mapping between the host (running OS) and the container. Without this configuration, the container is unreachable from the host (without using the container IP, which is only available on a Linux server host).

There are two syntaxes for the ports section:

- short syntax, e.g.:
    ```yaml
    ports:
      - `127.0.0.1:8080:8080` 
- long syntax, e.g. :
    ```yaml
    ports:
      - name: web
        target: 8080
        host_ip: 127.0.0.1
        published: "8080"
        protocol: tcp
        app_protocol: http
        mode: host
    ```

**Important security note**: if the host IP address is set to `0.0.0.0` (default), It means that the specified container port is accessible from any IP address, not just from the host. Moreover, on Linux, Docker also overrides firewall rules for this port, breaching another level of security. Therefore, for a typicall local testing environment, it is recommended to always set the host IP to `127.0.0.1`.

##### Short Syntax
[Documentation](https://docs.docker.com/reference/compose-file/services/#short-syntax-3)

The format of the short syntax is: `[<host>:]<container>[/<protocol>]`. Here:

- `<host>` is in the format of `[<host_ip>:]<port or range>`. By default, the host is `0.0.0.0`, which means that the container is accessible from any IP address.
- `<container>` is a container port or a range of ports
- `<protocol>` is the protocol to use, either `tcp` or `udp`. Default is `tcp`.


#### Volumes
[Documentation](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes)

Volumes are specified in the `volumes` section of the Compose file. It is a list of mappings between the host paths and the container paths. Similar to the ports, there are two syntaxes:

- short syntax, e.g.:
    ```yaml
    volumes:
      - `/home/user/data:/app/data`
- long syntax, e.g.:
    ```yaml
    volumes:
      - type: bind
        source: /home/user/data
        target: /app/data
    ```

##### Short Syntax
[Documentation](https://docs.docker.com/reference/compose-file/services/#short-syntax-5)

The short syntax has a format of `<volume>:<container_path>[:<access_mode>]`. 

- The `<volume>` is either the name of the volume specified in the top level `volumes` section, or a path to a file or directory in the host machine.
- The `<access mode>` can be:
    - `rw`: read and write access
    - `ro`: read-only access
    - `z` or `Z`: SELinux specific access types


#### Health Check

- [Compose File Documentation](https://docs.docker.com/reference/compose-file/services/#healthcheck)

The healthcheck section specifies the configuration of a detection system for the container status. Most important keys are:

- `test`: an array of commands, out of which all must succeed for the container to be considered healthy
- `retries`: the number of times to retry the healthcheck
- `interval`: interval between retries


### Build
[Documentation](https://docs.docker.com/reference/compose-file/build/)

The `build` section specifies the configuration of the build process, which itself is optional, as we can use pre-built images (with the `image` key).

We can

- either specify the build section as a path pointing to a directory with a `Dockerfile` file, or
- fully specify the build process in the `build` section.


## Docker File

- [Documentation](https://docs.docker.com/build/concepts/dockerfile/)
- [Reference](https://docs.docker.com/reference/dockerfile/)

A *Dockerfile* is a text file literally named `Dockerfile` that specifies how a Docker image is built. It uses a custom set of commands specific to Docker.

Most used commands are:

- [`ARG`](https://docs.docker.com/engine/reference/builder/#arg): defines an argument that can be used when running `docker build`
- [`COPY`](https://docs.docker.com/engine/reference/builder/#copy): copies files into the image
- [`ENTRYPOINT`](https://docs.docker.com/engine/reference/builder/#entrypoint): defines how the container can be run as an executable
- [`EXPOSE`](https://docs.docker.com/engine/reference/builder/#expose): specifies a port on which the container will listen
- [`FROM`](https://docs.docker.com/reference/dockerfile/#from): sets the base image this image is built on
- [`RUN`](https://docs.docker.com/reference/builder/#run): executes a command in the image
- [`WORKDIR`](https://docs.docker.com/reference/builder/#workdir): sets the working directory for the image. Basically, it sets CWD for the following commands.


## Docker Compose

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Compose CLI Documentation](https://docs.docker.com/compose/intro/compose-application-model/#cli)
- [Docker Compose CLI Reference](https://docs.docker.com/reference/cli/docker/compose/)

Docker Compose is a core tool for managing containers. It is used for starting, stopping, and building containers, for viewing the status of running containers, or one a single command in a container.

The basic subcommands are:

- `docker compose up`: starts the containers
- `docker compose down`: stops the containers
- `docker compose logs`: shows the logs of the containers
- `docker compose ps`: shows the status of the containers


### `docker compose up`
[Reference](https://docs.docker.com/reference/cli/docker/compose/up/)

This command starts the services defined in the Compose file. The most important options are:

- `-d`, `--detach`: starts the services in the background. Without this option, the terminal application switches from the host shell to the container shell, displaying the logs of the container. When the services are detached, we can inspect the output with the `docker compose logs` command.
- `--wait`: only return the control to the host shell after all services are started. Only meaningful if the `--detach` option is used.




