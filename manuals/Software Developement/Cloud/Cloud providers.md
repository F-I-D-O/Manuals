# Amazon Web Services


# Google Cloud

- [Homepage](https://cloud.google.com/)
- [Documentation](https://cloud.google.com/docs)
- [Wikipedia](https://en.wikipedia.org/wiki/Google_Cloud_Platform)


Useful commands:

- **enable service for project**:
    ```bash
    gcloud services enable <service> --project <project>
    ```


## Google Cloud CLI

- [Homepage](https://cloud.google.com/cli)
- [Installation Guide](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [`gcloud` command reference](https://docs.cloud.google.com/sdk/gcloud/reference)

Google Cloud CLI is a set of tools to manage Google Cloud services from the command line.


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
In this case, we need to typr the password to the active google account.


## Google Cloud Console
[Web](https://console.cloud.google.com)

The Google Cloud Console is the web interface for Google Cloud services. It is the main place to manage resources, projects, billing, access control, etc.

The most important is the project selector in the top left corner.

Important sections:

- **Google Auth Platform**: Accessible from `menu` > `APIs & Services` > `OAuth consent screen`


### Google Auth Platform
Google Auth Platform is a service taht enables OAuth2 authentication for Google Cloud project clients.

- address: https://console.cloud.google.com/auth/
- access from console:  `menu` > `APIs & Services` > `OAuth consent screen`

Each client have the following properties:

- `Name`: the name in the Google Cloud Console
- `Type`: the type of the client, e.g., `Web application`
- `Client ID`: the client ID that will be used in the client application to connect with the right OAuth2 client
- `Client secret`: Privite identifier for the client: this makes sure that only the authorized apps can access the client


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