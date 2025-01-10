from locust import HttpUser, task, between


class MyWebsiteTest(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Initialiser les données de test
        self.client.post("/show_summary", data={"email": "kate@shelifts.co.uk"})

    @task(3)
    def load_homepage(self):
        self.client.get("/")

    @task(2)
    def book_competition(self):
        self.client.get("/book/Spirit%20of%20the%20Season/Iron%20Temple")

    @task(1)
    def point_display(self):
        self.client.get("/clubs_points")

    @task(1)
    def purchase_places(self):
        self.client.get("/reset_data")

        response = self.client.post(
            "/purchase_places",
            data={
                "competition": "Spirit of the Season",
                "club": "Iron Temple",
                "places": 2,
            }
        )
        if response.status_code != 200:
            print(f"Failed to purchase places: {response.status_code} - {response.text}")
