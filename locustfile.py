import requests
from locust import HttpLocust, TaskSet


def login(l):
    auth = requests.auth.HTTPBasicAuth("admin", "adminadmin")
    l.client.post("/api/auth/", auth=auth)


def products(l):
    l.client.get("/api/v1/products/")


class UserBehavior(TaskSet):
    tasks = {login: 1, products: 2}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
