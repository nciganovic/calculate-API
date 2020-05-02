# calculate-API

Python REST API for simple calculations, made with Django REST Framework

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
Python 3.8.x
```

### Installing

Create and activate virtual environment inside project

```
virtualenv -p python env
```

Install all dependencies 

```
pip install -r requirements.txt
```

Running local server in directory where is manage.py file (second calculateAPI folder)

```
python manage.py runserver <port-number>
```

## Running the tests

In order to test whole flow of the app run

```
python manage.py test
```

File that will be run with this command is inside calculateApi/main/tests.py

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST Framework](https://www.django-rest-framework.org/) - REST framework
