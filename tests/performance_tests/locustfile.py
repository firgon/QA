from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    club = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    @task(1)
    def home(self):
        self.client.get("/")

    @task(1)
    def point_display(self):
        self.client.get('/point-display')

    @task(1)
    def show_summary(self):
        self.client.get(f'/showSummary/{self.club["name"]}')

    @task(1)
    def book(self):
        self.client.get('/book/Spring%20Festival%202023/Iron%20Temple')

