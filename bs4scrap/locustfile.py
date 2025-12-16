from locust import HttpUser, task, between

class MovieUser(HttpUser):
    wait_time = between(1, 3)  # simulate realistic user delays

    @task
    def load_home(self):
        self.client.get("/")

    @task
    def load_reservation(self):
        self.client.get("/reservation")

    @task
    def load_films(self):
        self.client.get("/films")

    @task
    def load_archives(self):
        self.client.get("/archives")

    @task
    def load_about(self):
        self.client.get("/a-propos")

    @task
    def load_contact(self):
        self.client.get("/contact")
