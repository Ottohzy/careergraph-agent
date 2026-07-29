from fastapi.testclient import TestClient

from careergraph.api import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_create_candidate() -> None:
    candidate_data = {
        "name": "Zhuoyu Hao",
        "skills": [
            {
                "name": "Python",
            }
        ],
        "experiences": [],
    }

    response = client.post(
        "/api/candidates",
        json=candidate_data,
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["name"] == "Zhuoyu Hao"
    assert response_data["skills"] == [
        {
            "name": "Python",
        }
    ]
    assert isinstance(response_data["candidate_id"], int)


def test_get_existing_candidate() -> None:
    create_response = client.post(
        "/api/candidates",
        json={
            "name": "Test Candidate",
            "skills": [],
            "experiences": [],
        },
    )

    candidate_id = create_response.json()["candidate_id"]

    response = client.get(
        f"/api/candidates/{candidate_id}"
    )

    assert response.status_code == 200
    assert response.json()["candidate_id"] == candidate_id
    assert (
        response.json()["name"]
        == "Test Candidate"
    )


def test_get_missing_candidate() -> None:
    response = client.get(
        "/api/candidates/999999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Candidate not found.",
    }


def test_create_candidate_with_invalid_skills() -> None:
    response = client.post(
        "/api/candidates",
        json={
            "name": "Invalid Candidate",
            "skills": "Python",
            "experiences": [],
        },
    )

    assert response.status_code == 422