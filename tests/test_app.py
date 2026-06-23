import pytest


pytestmark = pytest.mark.anyio


async def test_get_activities_returns_seed_data(client):
    response = await client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]
    assert isinstance(payload["Chess Club"]["participants"], list)


async def test_signup_adds_new_participant(client):
    email = "new.student@mergington.edu"

    signup_response = await client.post(
        f"/activities/Chess Club/signup?email={email}")
    activities_response = await client.get("/activities")

    assert signup_response.status_code == 200
    assert signup_response.json(
    )["message"] == f"Signed up {email} for Chess Club"
    assert email in activities_response.json()["Chess Club"]["participants"]


async def test_signup_rejects_duplicate_participant(client):
    existing_email = "michael@mergington.edu"

    response = await client.post(
        f"/activities/Chess Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()[
        "detail"] == "Student already signed up for this activity"


async def test_signup_rejects_unknown_activity(client):
    response = await client.post(
        "/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


async def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"

    delete_response = await client.delete(
        f"/activities/Chess Club/participants/{email}")
    activities_response = await client.get("/activities")

    assert delete_response.status_code == 200
    assert delete_response.json(
    )["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities_response.json()[
        "Chess Club"]["participants"]


async def test_unregister_rejects_unknown_participant(client):
    response = await client.delete(
        "/activities/Chess Club/participants/notfound@mergington.edu")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == "Participant not found in this activity"


async def test_unregister_rejects_unknown_activity(client):
    response = await client.delete(
        "/activities/Unknown Club/participants/student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
