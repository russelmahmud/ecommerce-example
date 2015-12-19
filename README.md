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


## Load Test
[Locust](http://docs.locust.io/en/latest/what-is-locust.html) tool has been used for load testing.
We have added only 2 examples to show how we can write and test locally. Locust can be also used in
production and distributed environment. 

To run the Locust server:

**`$ locust --host=http://localhost:8000`**

**Open up Locust’s web interface(http://localhost:8089/)**

![alt tag](http://docs.locust.io/en/latest/_images/webui-splash-screenshot.png)
