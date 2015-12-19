## Dependencies
 * [python 2.7](https://www.python.org/downloads/)
 * [pip](http://www.pip-installer.org/en/latest/installing.html)
 * [virtualenv](http://www.virtualenv.org/en/latest/)

## Create a virtualenv to isolate our package dependencies locally
virtualenv env
source `env/bin/activate`  # On Windows use `env\Scripts\activate`


## Set Up
  `$ ./setup.sh`
  
## Run Tests
   `$ ./manage.py test`
   
## Test Coverage
   `$ coverage run --source='.' manage.py test`
   
   `$ coverage report`

## Run server
  `$ ./manage.py runserver`
  
  server running at **http://localhost:8000**
  
  admin panel(admin:adminadmin): **http://localhost:8000/admin/**

#### [API Documentation](https://github.com/russelmahmud/ecommerce-example/wiki)
