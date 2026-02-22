"""Tests for FastAPI routes in src.main."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_home_returns_200_and_html(client: TestClient) -> None:
    """GET / returns 200 and HTML with FinAdv."""
    response = client.get("/")
    assert response.status_code == 200
    assert "FinAdv" in response.text


def test_toggle_theme_light_to_dark(client: TestClient) -> None:
    """POST /theme/toggle with no cookie sets theme=dark and HX-Refresh."""
    response = client.post("/theme/toggle")
    assert response.status_code == 204
    assert "theme=dark" in response.headers.get("set-cookie", "")
    assert response.headers.get("hx-refresh") == "true"


def test_toggle_theme_dark_to_light(client: TestClient) -> None:
    """POST /theme/toggle with theme=dark cookie sets theme=light."""
    client.post("/theme/toggle")  # light -> dark, sets cookie on client
    response = client.post("/theme/toggle")  # dark -> light
    assert response.status_code == 204
    assert "theme=light" in response.headers.get("set-cookie", "")
