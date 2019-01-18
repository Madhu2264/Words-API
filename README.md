## Prerequisites

* [Download](https://www.docker.com/community-edition#download)
* [MacOS](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

## Setting up

In the root directory.

```sh
docker-compose up
```

This creates a setup with a postgres server (hostname: postgres) containing a database.

To remove the servers later:

```sh
docker-compose down
```

### Connecting to postgres

If you happen to have the postgres client tools installed (not required for this assignment)

```sh
psql -h localhost -p 5432 -U postgres
```

### Words API

The data returned by the api should be camelCased, however the data in the database should be snake_cased.

The requirements for this project are:

* Create an endpoint /import, which calls the [http://dataservice/harrypotter] API and stores the results in the database.The import should be idempotent, so when the endpoint gets called twice the get harrypotter and import procedure should run only once (the first time).
* Create an endpoint /wordscount which returns an object that has each unique word with the count of how often it's used in the database
* Create an endpoint /wordcount/{word} which returns a single word count
* Create an endpoint /matchword/{pattern} which displays all the word which has the given string as a substring

