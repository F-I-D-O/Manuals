# Amazon Web Services


# Google Cloud

- [Homepage](https://cloud.google.com/)
- [Documentation](https://cloud.google.com/docs)
- [Wikipedia](https://en.wikipedia.org/wiki/Google_Cloud_Platform)

The main unit in Google Cloud is a *project*. Each Google user can have multiple projects.

The capabilities for each project are determined by the list of available *service*s.



## Google Cloud CLI

- [Homepage](https://cloud.google.com/cli)
- [Installation Guide](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [`gcloud` command reference](https://docs.cloud.google.com/sdk/gcloud/reference)
- [`gcloud` command cheat sheet](https://cloud.google.com/sdk/docs/cheatsheet)

Google Cloud CLI is a set of tools to manage Google Cloud services from the command line.

Most used subcommands:

- `gcloud auth`: authentication
- `gcloud info`: show information about the current configuration (installation, project, paths, etc.)
- `gcloud organizations`: see and manage organizations


### Filtering
[Official documentation](https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters)

Many commands in the gcloud CLI support filtering. The filter format is:
```bash
<field> <operator> <value>
```
The `<field>` can be one of the column names in the output + some hidden fields. To **see all available fields**, fetch one row from the command in the `YAML` format:
```bash
gcloud <command> --format=yaml --limit=1
```

Most used operators are:

- `:`: *simple command* equality 
- `=`: equal

#### Simple commands
Simple commands are dedicated google commands that matches the field if it's equal to the value or if it matches the value using a specially crafted logic.

The logic:

- `<value>` can end with `*`, in which case it matches any string that starts with `<value>`
- each dot (`.`) in `<field>` splits the field into multiple parts. Then, the `<value>`is matched against each consecutive subset of parts, and returns true if any of the subsets match.

the `<field>` `abc.def.ghi` can be matched by:

- `abc.def.ghi`
- `abc*`
- `abc.def*`
- `def.ghi`
- `def`
- `def*` 
- `xyz*`


### Projects
For managing projects, we use the `gcloud projects` subcommands.

To **list** the projects, run `gcloud projects list`.

To **create a project**, we call the [`create`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/create) subcommand:
```bash
gcloud projects create <project id>
```

### Services
To **enable service for project**:
    ```bash
    gcloud services enable <service> --project <project>
    ```

To *list or browse* services, use the `gcloud services list` command.


#### Listing and browsing services
[Reference](https://docs.cloud.google.com/sdk/gcloud/reference/services/list)

By default, the enabled services are listed for the active project. Important parameters:

- `--available`: list all available services instead of the enabled ones
- `--filter <filter>`: filter the output (see [Filtering](#filtering) for details)
- `--format <format>`: output format
- `--limit <limit>`: limit the number of rows
- `--project <project>`: list services for the specified project instead of the active project



## Authentication
There are two types of authentication in Google Cloud:

- Google Cloud CLI authentication:
    - used for Google Cloud CLI and few connected systems
    - `gcloud auth login`
- [Application Default Credentials](https://docs.cloud.google.com/docs/authentication/application-default-credentials): 
    - special credential systems for other Google Cloud services and external applications
    - `gcloud auth application-default login`


### Google Cloud CLI authentication
[Official documentation](https://docs.cloud.google.com/sdk/docs/authenticate)

The Google Cloud CLI authentication is used for the Google Cloud CLI and few connected systems.

Typically, we **authenticate** using the `gcloud auth login` command, which initiates the OAuth2 authentication flow (in web browser, using the Google account).

To **list** the active accounts, we can use the `gcloud auth list` command.

When working with multiple accounts, we need to first **select the account** for the following commands. To do that, run:
```bash
gcloud config set account <email>
```

Sometimes, a **reauthentication** is required, with a prompt like the following:
```text
Reauthentication required.
Please enter your password:
```
In this case, we need to type the password to the active google account.


## Google Cloud Console
[Web](https://console.cloud.google.com)

The Google Cloud Console is the web interface for Google Cloud services. It is the main place to manage resources, projects, billing, access control, etc.

The most important is the project selector in the top left corner.

Important sections:

- **IAM & Admin**: Main administration section. Accessible from `menu` > `IAM & Admin`
- **Google Auth Platform**: Accessible from `menu` > `APIs & Services` > `OAuth consent screen`


### IAM & Admin
In the IAM & Admin section, we can:

- manage service accounts


#### Service Accounts
Service accounts can be used to access some Google Cloud services. To use service account from local computer, we have to first authenticate to the service account using

- a key file, or
- Workload Identity Federation (WIF)

The key authentification is simple, just clikc `manage keys` > `add key` > `JSON` and save the key file.


### Google Auth Platform
[Official documentation](https://developers.google.com/workspace/guides/configure-oauth-consent)

Google Auth Platform is a service that enables OAuth2 authentication for Google Cloud project clients. Unlike other Google Cloud services, this one cannot be configured using the gcloud CLI, but only from the Google Cloud Console.

- address: https://console.cloud.google.com/auth/
- access from console:  `menu` > `APIs & Services` > `OAuth consent screen`

Typically, we need to specify three things:

- the project wide OAuth configuration
- the client for our application
- the test users

Most importantly, the **first thing to do is to select the right project** in the selector in the top left corner.

#### Application Configuration
The application configuration is initially empty and have to be filled by clicking on the `Get started` button.

All the fields are self-explanatory.

#### Adding a client
To add a client, go to `Clients` and click on the `Create client` button.

Each client have the following properties:

- `Name`: the name in the Google Cloud Console
- `Type`: the type of the client, e.g., `Web application`
- `Client ID`: the client ID that will be used in the client application to connect with the right OAuth2 client
- `Client secret`: Privite identifier for the client: this makes sure that only the authorized apps can access the client

#### Test users
To add test users, go to `Audiance` and in the `Test users` section, click on the `Add users` button.

## Google Cloud SQL
[Documentation](https://cloud.google.com/sql/docs)

Google Cloud SQL is a managed database service.


### Cloud SQL Proxy

- [Documentation](https://docs.cloud.google.com/sql/docs/postgres/sql-proxy#windows-64-bit)
- [GitHub](https://github.com/GoogleCloudPlatform/cloudsql-proxy)
- [How it Works](https://docs.cloud.google.com/sql/docs/mysql/sql-proxy)

Cloud SQL Proxy is a command line tool for connecting to Google Cloud SQL. It creates an encrypted tunnel to the Google Cloud SQL service, directly connecting to the correct instance based on the provided credentials.


#### Authentication
Both Google Cloud CLI and Application Default Credentials can be used for authentication:

- Application Default Credentials are used automatically, if set up
- Google Cloud CLI authentication can be used if the `-g` (or `--gcloud-auth`) flag is provided. Note that an active Google Cloud CLI session is required.


### Management from Google Cloud Console
The instances can be managed from `menu` > `Cloud SQL` > `Instances`.

When clicking on the instance from the list, we can manage the specific instance.