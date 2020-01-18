# Dominion Card API

[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/release/wesbuck/DominionCardAPI)](https://github.com/wesbuck/DominionCardAPI/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/wesbuck/DominionCardAPI.svg?branch=master)](https://travis-ci.org/wesbuck/DominionCardAPI)
[![codecov](https://codecov.io/gh/wesbuck/DominionCardAPI/branch/master/graph/badge.svg)](https://codecov.io/gh/wesbuck/DominionCardAPI)

Full-featured Dominion Kingdom Card API written in Python using Django's REST framework. 
This API is intended to power companion apps for the board game Dominion and allows you to quickly 
and easily obtain card sets and card details for the Kingdom Cards used to play the game.

[API functions](https://documenter.getpostman.com/view/5603098/RWguxcDR) include:
* Obtain a set of 10 unique random Dominion Kingdom Cards
* Retrieve a list of Dominion Kingdom Cards based on filter criteria (name, cost, etc.)
* Add custom Dominion Kingdom Cards
* Get the information for a single Dominion Kingdom Card (random or specified)
* Get the complete list of all Dominion Kingdom Cards

This app includes a command function to ingest Dominion Kingdom Card data from a provided CSV file.

## Getting Started

These instructions will get you a copy of the API server up and running on your local machine.

### Prerequisites

Make sure [Python](https://www.python.org/downloads/) version 3.7 or newer is installed. Python 3.8 is recommended.

You will also need the `virtualenv` package if you want to work in a Virtual Environment (recommended):
```
pip install virtualenv 
```

### Installing

Clone the repository and browse to the local directory containing the project files:
```
git clone https://github.com/wesbuck/DominionCardAPI
cd DominionCardAPI
```

If you want to work in a Virtual Environment (recommended), create it and activate it:

```
virtualenv venv
source venv/bin/activate (for Linux, Mac)
source venv/Scripts/activate (for Windows)
```

Install required packages (or do it the [old fashioned way](#manually-install-packages)):

```
pip install -r requirements.txt
```

Make a local copy of the `DominionCardAPI/settings.py` file by executing the following:
```
cp DominionCardAPI/settings-sample.py DominionCardAPI/settings.py
```

Execute the following commands to prepare the database:
```
python manage.py migrate
python manage.py ingest_csv dominion_cards.csv
```

>NOTE: You can import any properly-formatted data set by specifying a file other than `dominion_cards.csv` when running the `ingest_csv` function.

### Create a User

You must generate a Token using username/password credentials in order to use this API. 
Create the username/password credentials using the `createsuperuser` function: 
```
python manage.py createsuperuser
```

Then enter the credentials you wish to use.

## Development

You likely want to activate the Virtual Environment each time you work on the project with `source venv/Scripts/activate` for Windows or `source venv/bin/activate` for Linux and Mac.

You can leave the Virtual Environment with the `deactivate` command.

### Running the program

Test run the program on your local machine by executing:
```
python manage.py runserver
```

### Adding Packages

If you add a package (using `pip install [package-name]`) to this app, ensure it also gets added to `requirements.txt` file:
```
pip freeze > requirements.txt
```

### Flush Database
If you need to ingest the CSV file again, you should first flush the database:
```
python manage.py flush
```

### VS Code

If you plan to use VS Code with the Python extension installed, you'll also want to install `pylint-django`:
```
pip install pylint-django
```
And add this to your `settings.json`:
```
"python.linting.pylintArgs": [
    "--load-plugins=pylint_django"
]
```
## Testing

This app uses `pytest` with `pytest-django` to run automatic testing. You can run the test suite with the command:
```
pytest
```

### Generate Test Data

To recreate the `test_data.json` file, run:
```
python manage.py dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 4 > tests/test_data.json
```
> NOTE: You will likely need to update the tests in `tests/test_api.py` to work with your updated database data.

To recreate the `test_users.json` file, run:
```
python manage.py dumpdata auth.User --indent 4 > tests/test_users.json
```
> NOTE: You will likely need to update the tests in `tests/test_auth.py` to work with your updated user data.

### Continuous Integration

Continuous integration (CI) testing is provided by [Travis CI](https://travis-ci.org/) and is automatically run upon each git check-in and merge.

## Production

You should change `DEBUG` from `True` to `False` in `DominionCardAPI/settings.py` before deploying for production.

It is likely that you will need to add the server URL to `ALLOWED_HOSTS` in `DominionCardAPI/settings.py`:
```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

### Static Files

You will likely need to make static files (css, etc) available to make the API look properly pretty in the browser. If you use the default URL for static files, just uncomment line 133 (under `STATIC_URL = '/static/'`) of `DominionCardAPI/settings.py`:

```
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

If you change `STATIC_URL` to something other than `/static/` then you will need to update `STATIC_ROOT` accordingly.

Run the following command to prepare the files:
```
python manage.py collectstatic
```

### Apache

If you are using Apache, it is likely that you will need to change the name of the root directory of this project to something other than `DominionCardAPI` (this will solve "ImportError: No module named DominionCardAPI.settings" error in the Apache error.log).

Additionally, if using Apache, you will likely need to configure mod_wsgi to pass the required headers through to the application. Add the following to either server config (e.g. `/etc/apache2/apache.conf`), virtual host, directory or .htaccess:
```
WSGIPassAuthorization On
```

## Generate Authentication Token

An authentication token is required to interact with the API. 
Generate an authentication token by POSTING your username/password to 
`/get_auth_token/`.

More information is located in the 
[documentation](https://documenter.getpostman.com/view/5603098/RWguxcDR).


## Optional

### Disable Authentication

You can choose to disable the requirement for authentication by commenting out lines 81 & 82 of `DominionCardAPI/settings.py`:
```
#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
#    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
```
### Manually Install Packages

If you don't want to use the `requirements.txt` option [detailed above](#installing), you can manually install the python packages using these instructions.

Install [django](https://www.djangoproject.com/download/):
```
pip install Django==3.0
```

Install required django tools: 
```
pip install djangorestframework
pip install django-filter
pip install httpie
```

## API Documentation

View the complete [documentation for this API](https://documenter.getpostman.com/view/5603098/RWguxcDR).

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE used for initial project creation
* [Postman](https://www.getpostman.com/) - API development testing & documentation
* [VS Code](https://code.visualstudio.com/) - The code editor used for continued development

## Authors

* [Wes Buck](https://github.com/wesbuck)

