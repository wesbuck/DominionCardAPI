# Dominion Card API

Full-featured Dominion Card API using Django's REST framework. Includes a command function to ingest Dominion Card data from a CSV file.

## Getting Started

These instructions will get you a copy of the API server up and running on your local machine.

### Prerequisites

These tools are required before installation :

- [Python](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- pip

### Installing

Install required django tools: 

```
pip install djangorestframework
pip install django-filter
pip install httpie
```

Browse to the local directory containing the project files and execute the following commands:

```
python manage.py makemigrations
python manage.py migrate
python manage.py ingest_csv dominion_cards.csv
```

Note that you can import any properly-formatted data set by specifying a file other than `challenge_data.csv` when 
running the `ingest_csv` function.

### Create a User

You must generate a Token using username/password credentials in order to use this API. 
Create the username/password credentials using the `createsuperuser` function: 

```
python manage.py createsuperuser
```

Then enter the credentials you wish to use.

## Running the program

Start the program by executing:

```
python manage.py runserver
```

## Generate Authentication Token

An authentication token is required to interact with the API. 
Generate an authentication token by POSTING your username/password to 
`/get_auth_token/`.

More information is located in the 
[documentation](https://documenter.getpostman.com/view/5603098/RWguxcDR#474a6d68-c6b0-475a-b768-15e721cd5652).

## API Documentation

View the complete [documentation for this API](https://documenter.getpostman.com/view/5603098/RWguxcDR).

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE used
* [Postman](https://www.getpostman.com/) - API development testing & documentation

## Authors

* Wes Buck

