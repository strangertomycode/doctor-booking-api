import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


class APIClient:
    def __init__(self):

        self.token = None

    def set_token(self, token):

        self.token = token

    @property
    def headers(self):

        if self.token:
            return {"Authorization": f"Bearer {self.token}"}

        return {}

    def get(self, endpoint, params=None):

        return requests.get(
            f"{BASE_URL}{endpoint}",
            headers=self.headers,
            params=params,
        )

    def post(self, endpoint, data=None):

        return requests.post(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=self.headers,
        )

    def patch(self, endpoint, data=None):

        return requests.patch(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=self.headers,
        )
