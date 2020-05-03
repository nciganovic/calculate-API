# calculate-API

Python REST API for simple calculations, made with Django REST Framework

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
Python 3.8.x
```

### Installing

Create virtual environment inside project

```
virtualenv -p python env
```

Activate virtual envirnment

```
source env/bin/activate
```

Install all dependencies 

```
pip install -r requirements.txt
```

Running local server in directory where is manage.py file (second calculateAPI folder)

```
python manage.py runserver <port-number>
```

## Users
In order to login as admin go to: http://127.0.0.1:6767/admin/

Admin user:

```
username: admin
password: 123456789
```

Basic user:

```
username: test_user_1
password: 123456789nc
```

## Routes


#### POST /add 

expects either Array of integers (comma-separated integers) or one integer as the body of the POST request.


#### GET /calculate

calculates the sum of all elements that exist in the array, saves it and returns it. If parameter all is provided, then call returns all calculated sums.


#### POST /reset

saves array and calculations, give it some ID, and empties array and all calculations from memory. 

#### GET /history

returns JSON with the next structure: 

```
[{“id”: <id of element>, “array”: <array of numbers>, “calculations”: <array of all calculations for given array of numbers>} …]
```

if parameter id is provided call returns just JSON for that id.

```
{“id”: <id of element>, “array”: <array of numbers>, “calculations”: <array of all calculations for given array of numbers>}
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

## Other technologies

* [Postman](https://www.postman.com/) - Tool for making HTTP requests
