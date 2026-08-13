# Amazon Web Services


# Google Cloud

- [Homepage](https://cloud.google.com/)
- [Documentation](https://cloud.google.com/docs)
- [Wikipedia](https://en.wikipedia.org/wiki/Google_Cloud_Platform)


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