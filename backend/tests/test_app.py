from fastapi.testclient import TestClient

from school_accounting.config import Settings
from school_accounting.main import create_app


def test_app_starts_and_health_succeeds() -> None:
    app = create_app(Settings(app_env="test"))
    with TestClient(app) as client:
        assert app.state.session_factory is not None
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_settings_load_test_mode(monkeypatch) -> None:
    monkeypatch.setenv("SCHOOL_ACCOUNTING_APP_ENV", "test")
    assert Settings(_env_file=None).app_env == "test"
