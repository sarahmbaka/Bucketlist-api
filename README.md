# bucketlist-api

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3ae3f9985c1e43eaae3b7206de7f5d9f)](https://www.codacy.com/app/sarahmbaka/bucketlist-api?utm_source=github.com&utm_medium=referral&utm_content=sarahmbaka/bucketlist-api&utm_campaign=badger)
[![Build Status](https://travis-ci.org/sarahmbaka/bucketlist-api.svg?branch=develop)](https://travis-ci.org/sarahmbaka/bucketlist-api)  ||  [![Coverage Status](https://coveralls.io/repos/github/sarahmbaka/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/sarahmbaka/bucketlist-api?branch=develop)


API documentation : http://docs.bucketlists1.apiary.io/

## What is a Bucketlist?

A Bucketlist is a number of experiences or achievements that a person hopes to have or accomplish during their lifetime.

## Bucketlist Application

Bucketlist app is an application that  allows users  to record and share things they want to achieve 
or experience before reaching a certain age meeting the needs of keeping track of their dreams and goals.

## Installation

Clone this repo:

```
$ git clone https://github.com/sarahmbaka/Bucketlist.git
```

Navigate to the `bucketlist-api` directory:

```
$ cd bucketlist-api
```

Create a virtual environment:

> Use [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Install the required dependencies:
```
$ pip install -r requirements.txt
```

Install postgres:
```
brew install postgresql
type psql in terminal.
On postgres interactive interface, type CREATE DATABASE bucketlist_db;
```

Create a .env file and add the following:
```
source name-of-virtual-environment/bin/activate
export FLASK_APP="run.py"
export SECRET="a-secret-key"
export DATABASE_URL="postgresql://localhost/bucketlist_db"
```

Then run:
```
source .env
```

Launch the program:
```
python run.py
```

### API Endpoints

| Methods | Resource URL | Description | Public Access |
| ---- | ------- | --------------- | ------ |
|POST| `/auth/login` | Logs a user in| TRUE |
|POST| `/auth/register` |  Register a user | TRUE |
|POST| `/bucketlists/` | Create a new bucket list | FALSE |
|GET| `/bucketlists/` | List all the created bucket lists | FALSE |
|GET| `/bucketlists/<bucketlist_id>/` | Get single bucket list | FALSE |
|PUT| `/bucketlists/<bucketlist_id>/` | Update this bucket list | FALSE |
|DELETE| `/bucketlists/<bucketlist_id>/` | Delete this single bucket list | FALSE |
|POST| `/bucketlists/<bucketlist_id>/items/` | Create a new item in bucket list | FALSE |
|GET| `/bucketlists/<bucketlist_id>/items/` | List items in this bucket list | FALSE |
|GET| `/bucketlists/<bucketlist_id>/items/<item_id>/` | Get single bucket list item | FALSE |
|PUT|`/bucketlists/<bucketlist_id>/items/<item_id>/` | Update a bucket list item | FALSE |
|DELETE|`/bucketlists/<bucket_id>/items/<item_id>/` | Delete an item in a bucket list | FALSE 


### Testing

To test, run the following command:
```
nosetests
```
