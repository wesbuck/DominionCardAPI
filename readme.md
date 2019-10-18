# Dominion Card API

Full-featured Dominion Kingdom Card API using Django's REST framework. 
This API is intended to power companion apps for the board game Dominion and allows you to quickly 
and easily obtain card sets and card details for the Kingdom Cards used to play the game.

[API functions](https://documenter.getpostman.com/view/5603098/RWguxcDR) include:
* Obtain a set of 10 unique random Dominion Kingdom Cards
* Retrieve a list of Dominion Kingdom Cards based on filter criteria (name, cost, etc.)
* Add custom Dominion Kingdom Cards
* Get the information for a single Dominion Kingdom Card (random or specified)

This app includes a command function to ingest Dominion Kingdom Card data from a provided CSV file.

## Getting Started

These instructions will get you a copy of the API server up and running on your local machine.

### Prerequisites

These tools are required before installation :

- [Python 3](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- [pip](https://pip.pypa.io/en/stable/)

### Installing

Install required django tools: 

```
pip3 install djangorestframework
pip3 install django-filter
pip3 install httpie
```

Browse to the local directory containing the project files and execute the following commands:

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py ingest_csv dominion_cards.csv
```

Note that you can import any properly-formatted data set by specifying a file other than `dominion_cards.csv` when 
running the `ingest_csv` function.

### Create a User

You must generate a Token using username/password credentials in order to use this API. 
Create the username/password credentials using the `createsuperuser` function: 

```
python3 manage.py createsuperuser
```

Then enter the credentials you wish to use.

## Running the program

### Development

Test run the program on your local machine by executing:

```
python3 manage.py runserver
```

### Production

It is likely that you will need to add the server URL to `ALLOWED_HOSTS` in `DominionCardAPI/settings.py`:

```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

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
[documentation](https://documenter.getpostman.com/view/5603098/RWguxcDR#474a6d68-c6b0-475a-b768-15e721cd5652).

### Disable Authentication

You can disable the requirement for authentication by commenting out lines 81 & 82 of `DominionCardAPI/settings.py`:

```
#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
#    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
```

## API Documentation

View the complete [documentation for this API](https://documenter.getpostman.com/view/5603098/RWguxcDR).

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE used
* [Postman](https://www.getpostman.com/) - API development testing & documentation

## Authors

* Wes Buck

