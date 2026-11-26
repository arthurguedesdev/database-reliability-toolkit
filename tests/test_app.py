from app import create_app


def test_liveness_without_database():
    app = create_app()
    response = app.test_client().get("/health/live")
    assert response.status_code == 200
    assert response.json == {"status": "alive"}

def test_database_version_integration():
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get("/api/v1/database/version")

    assert response.status_code == 200

    data = response.get_json()
    assert data["version"].startswith("17.")
