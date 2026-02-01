import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: remove test user
    client.delete(f"/activities/{activity}/participants/{email}")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_delete_participant():
    email = "deleteuser@mergington.edu"
    activity = "Programming Class"
    # Add user first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_delete_participant_not_found():
    response = client.delete("/activities/Chess Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404
