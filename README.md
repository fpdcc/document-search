# Forest Preserve of Cook County Document Search

Search and management interface for spatial documents, built for the Forest Preserve of Cook County.

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Before you start, you'll need a local settings file for development. If you're
on the Blackbox keyring for this repo, you can decrypt a canonical settings
file that is encrypted and stored in the `configs` directory. See [the
Blackbox documentation](https://github.com/StackExchange/blackbox) for
details on how to install and use Blackbox, and run this command to decrypt
the settings file once you have Blackbox set up:

```
blackbox_cat configs/local_settings.dev.py.gpg > docsearch/local_settings.dev.py
```

If you're not on the keyring for this repo, copy and edit the example settings file:

```
cp docsearch/local_settings.example.py docsearch/local_settings.dev.py
```

Next, build containers:

```
docker compose build
```

Run the app:

```
docker compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.

Create a superuser to view the application:

```
docker compose run --rm app ./manage.py createsuperuser
```

### Loading initial data

Initial data is available in separate repos, called `document-search-data`, that are
kept private in order to respect the privacy of entities mentioned in the
metadata. One repo is hosted on a private DataMade github repo, and another on AWS CodeCommit in the Forest Preserves AWS account.

To get that data, the easiest options are to:
- Clone it from [DataMade's private repo of the data](https://github.com/datamade/document-search-data), and copy that into a directory called `/data` in the root of your local environment.
- Ask a fellow dev to send you a zipped version of the `/data` directory from the root of their local environment and unzip it in a similar directory in your environment. 

If neither option is possible, you can also follow these [instructions for cloning CCFP's version of the same repo on AWS](#cloning-document-search-data) and return here when done.

Once you have initial `/data/` locally, load it using GNU Make:

```
docker compose -f docker-compose.yml -f data/docker-compose.yml run --rm app make all
```

To get documents to show up on the frontend, you'll need to create the search index. Start by bringing up Solr in one shell if it hasn't been started by the container itself:

```
docker compose up solr
```

Then, in another shell, run the `rebuild_index` command:

```
docker compose run --rm app ./manage.py rebuild_index
```

Voila, you now have Licenses, and Titles, and Books, oh my!

#### Cloning `document-search-data` from AWS
To gain access to cloning `document-search-data`, you'll need to add yourself to the SSH keys for CodeCommit.

First, log in to AWS using the credentials in Bitwarden titled "CCFP Forest Preserve of Cook County AWS creds". Make sure you're on the "us-east-1" regional version of the site after logging in.

Find the detail page for the "datamade" IAM user, click "Security credentials", and scroll down to "SSH public keys for AWS CodeCommit". Note that a max of 5 users can be added to the "datamade" user at once. You may choose to perform this action on a new user.

From here, follow [step 3 in the AWS docs to add your ssh key](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html?icmpid=docs_acc_console_connect#setting-up-ssh-unixes-keys), making sure to create an `rsa` formatted key. Then follow [step 4 in those same docs to clone the repo](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html?icmpid=docs_acc_console_connect#setting-up-ssh-unixes-connect-console).

Last, copy the contents of that repo to a subdirectory of this repo called `/data/`:

```
cp -R ./document-search-data/ ./document-search/data/
```

For additional guidance on configuring your local environment to work with AWS CodeCommit. see the [official AWS docs](https://docs.aws.amazon.com/codecommit/latest/userguide/getting-started-cc.html).

### Running tests

Run tests with Docker Compose:

```
docker compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

## Deployment

This repo is configured to deploy in the following ways:

| environment | deploys on                |
| ----------- | ------------------------- |
| staging     | commit to `master` branch |
| production  | tagged commit or release  |

Push to production using the following commands:
```bash
git tag <new-tag-name>  # create new tag
git tag  # list all tags to confirm creation
git push origin —-tags  # push all local tags, including the new one
```

In both cases, Travis CI will run tests before triggering a new deployment with AWS CodeDeploy.
