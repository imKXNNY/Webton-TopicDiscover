# tests/backend/integration/test_app.py
def test_api_topics(client, mocker):
    mocker.patch("app.find_uncovered_topics", return_value=["topic1", "topic2"])
    response = client.get("/api/topics")
    assert response.status_code == 200
    assert response.json["data"] == ["topic1", "topic2"]


def test_api_error_handling(client, mocker):
    mocker.patch("app.find_uncovered_topics", side_effect=Exception("Test Error"))
    response = client.get("/api/topics")
    assert response.status_code == 500
    assert "Test Error" in response.json["message"]
