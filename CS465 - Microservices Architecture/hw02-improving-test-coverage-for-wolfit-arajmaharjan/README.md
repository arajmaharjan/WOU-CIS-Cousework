## First Things First: Python 3 and SQLite

Before you clone and try to get the sample app working, you'll need a valid Python 3 (3.8 or newer) installation ([Python downloads](https://www.python.org/downloads/)).

Next, make sure you have a working [SQLite3](https://www.sqlite.org/) engine installed. On MacOS or Linux it is probably already installed. You should also install the [DB Browser for SQLite](https://sqlitebrowser.org/) as this will help you inspect schemas and data. 

## Clone this repository to your local dev environment

Your command will look something like this:

``` sh
$ git clone https://github.com/wou-cs/wolfit.git
```

In addition, you probably want to connect this local repo to your own remote, detaching from the master repository.

``` sh
$ cd wolfit
$ git remote set-url origin https://new.url.here
```

## Configure your settings files

You will create two settings files, one for development and one for test. These files will provide a [Flask secret key](https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key) and a name for your development and test databases. The development database is a *sandbox* that you can use for interactive play and testing. It will retain data and allow you to interact with the app. The test database will get torn down and recreated **every time you run the test suite**.

* Create your own dev.settings and test.settings files (do not check these into Git). Start by copying the `example.settings` file.

``` sh
$ cp example.settings dev.settings
$ cp example.settings test.settings
```
* Each will contain two environment variables:

``` py
SECRET_KEY = "your generated secret key"
BLOG_DATABASE_NAME = 'wolfit_XYZ.db'
```

* [Generate your own secret key](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask). Best practice is to *not* check secrets like this into Git, hence the reason `dev.settings` and `test.settings` are in the `.gitignore` file.
* Configure your pipenv environment and download required Python modules. Start by getting pipenv itself working using [these instructions](https://pipenv.readthedocs.io/en/latest/). Then, in the working directory containing the clone of this app:

``` sh
$ pipenv install
$ pipenv shell
```

Once you have requisite libraries installed, you will *always* need to start your development session by entering the `pipenv shell`.

## Set the WOLFIT_SETTINGS environment variable

Now that you have your local settings files, we need to tell the Wolfit app which one to use before we setup the database. This variable is set automatically when you run `rundev.sh`, `runtests.sh`, and `cov.sh`. We need to set it manually now for the following steps:

``` sh
$ export WOLFIT_SETTINGS=$(pwd)/dev.settings
```

## Build / migrate the database

``` sh
$ flask db upgrade
```

You should see all of the migrations being applied to your development database. Ignore any "unsupported ALTER" warnings: we are using a non-production quality database (SQLite) that doesn't support the full SQL language.

## Run tests

``` sh
$ ./runtests.sh
```

## Run dev server (local web server)

``` sh
$ ./rundev.sh
```


## Test Coverage

To look at test coverage, simply run:

``` sh
$ ./cov.sh
```

## Load up some sample posts from Reddit

A great way to load up content into this Reddit clone is to copy some submissions from Reddit to your local sandbox. There's a script to perform this called `load_reddit_posts.py`, but in order to run it you'll need to configure the PRAW API with a praw.ini file. Create such a file in the root of your project, and add these entries:

``` ini
[DEFAULT]
client_id=<your client ID>
client_secret=<your secret>
user_agent=python:edu.wou.<your user ID at WOU>
```

You will get your ID and secret by [creating an app under your Reddit profile](https://www.reddit.com/prefs/apps).

Follow these steps:

1. Click the "create app" at the bottom of the [Reddit apps page](https://www.reddit.com/prefs/apps).
2. Give it a name you will recognize, such as "Load posts for Wolfit".
3. Select the script option.
4. Fill in this for the redirect API: `http://www.example.com/unused/redirect/uri`
5. Client the "create app" button.
6. Under your app name you will see a client ID that looks something like this: `R2jyWgoETNkBfQ`
7. You will also see your secret shown. Copy both the client ID and the secret into your praw.ini file.

Then you can load up some sample posts:

``` sh
$ python load_reddit_posts
```

You can optionally give the name of a subreddit as the first parameter. By default the script will load from [`/r/learnpython`](https://www.reddit.com/r/learnpython/).

*Note* -- This is script is not terribly resilient and may fail with some title and body formatting issues because of the source data from Reddit. Still, it should load *some* posts allowing you have some data to work with. You can point the tool at other subreddits as well - just run `python load_reddit_posts.py --help` to see how to do this.
