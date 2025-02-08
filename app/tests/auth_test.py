from .utils import client
import pytest


@pytest.mark.usefixtures("reset_database")
class TestAuthEndpoints:
    def test_login(self):
        response = client.post(
            "/api/login",
            json={
                "email": "default@example.com",
                "password": "123456",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            },
        )
        assert response.status_code == 200
