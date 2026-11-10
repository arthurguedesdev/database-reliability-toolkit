from app import create_app


def test_liveness_without_database():
    app = create_app()
    response = app.test_client().get("/health/live")
    assert response.status_code == 200
    assert response.json == {"status": "alive"}
