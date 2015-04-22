import os

from locust import HttpLocust

from ecommerce import EcommerceTasks
from baskets import BasketsTasks


class EcommerceTest(EcommerceTasks):
    tasks = {
        BasketsTasks: 1,
    }


class EcommerceLocust(HttpLocust):
    """Representation of an HTTP "user".

    Defines how long a simulated user should wait between executing tasks, as well as which
    TaskSet class should define the user's behavior.
    """
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'EcommerceTest')]
    min_wait = 5000
    max_wait = 9000
