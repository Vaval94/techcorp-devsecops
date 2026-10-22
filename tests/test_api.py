import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_orders_nominal(monkeypatch):
    monkeypatch.setenv("SIMULATE_FAILURE", "false")
    assert client.get("/orders").status_code == 200


def test_orders_simulated_failure(monkeypatch):
    monkeypatch.setenv("SIMULATE_FAILURE", "true")
    assert client.get("/orders").status_code == 500


def test_metrics_exposed():
    body = client.get("/metrics").text
    assert "techcorp_http_requests_total" in body and "techcorp_build_info" in body
