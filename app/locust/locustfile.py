from locust import HttpUser, between, task
import time

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """result = self.client.post("/api/v1/auth/", {
            "username": "root",
            "password": "1234"
        })
        print(f"statuscode: {result.status_code}")
        print(f"raw: {result.raw}")
        print(f"result: {result.json()}")"""
        #self.client.headers = {'Authorization': 'Token '+result.json().get("token")}
        self.client.headers = {'Authorization': 'Token e2d4404ba1bcc893c74a709695e5cb905a05268909891a6150636c9a182d9f2f'}

    @task
    def list_systems(self):
        self.client.get("/api/v1/systems/")

    @task
    def add_system(self):
        self.client.post("/api/v1/systems/", json={
            "name": f"locust-system-{time.time()}",
            "host": f"locust-host-{time.time()}"
        })
        self.client.get("/api/v1/systems/")
