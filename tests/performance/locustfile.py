from locust import HttpUser, between, task


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health(self) -> None:
        self.client.get("/api/v1/health")

    @task
    def iss_position(self) -> None:
        self.client.get("/api/v1/space/iss-position")
