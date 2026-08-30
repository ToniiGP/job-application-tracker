def register_and_login(client, email, username):
    client.post(
        "/users/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPassword123!",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_application(client, headers):
    response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_interview(client, headers, application_id):
    response = client.post(
        f"/applications/{application_id}/interviews",
        headers=headers,
        json={
            "stage": "Recruiter Screen",
            "interviewer": "Sarah",
            "notes": "Initial recruiter call",
        },
    )

    assert response.status_code == 201

    return response


def test_create_interview(client):
    headers = register_and_login(
        client,
        "createinterview@example.com",
        "createinterview",
    )

    application_id = create_application(client, headers)

    interview = client.post(
        f"/applications/{application_id}/interviews",
        headers=headers,
        json={
            "stage": "Recruiter Screen",
            "interviewer": "Sarah",
            "notes": "Initial recruiter call",
        },
    )

    assert interview.status_code == 201

    data = interview.json()

    assert data["stage"] == "Recruiter Screen"
    assert data["interviewer"] == "Sarah"
    assert data["notes"] == "Initial recruiter call"
    assert "id" in data


def test_get_interviews_for_application(client):
    headers = register_and_login(
        client,
        "listinterviews@example.com",
        "listinterviews",
    )

    application_id = create_application(client, headers)

    interview1 = client.post(
        f"/applications/{application_id}/interviews",
        headers=headers,
        json={
            "stage": "Recruiter Screen",
            "interviewer": "Sarah",
            "notes": "First interview",
        },
    )

    assert interview1.status_code == 201

    interview2 = client.post(
        f"/applications/{application_id}/interviews",
        headers=headers,
        json={
            "stage": "Technical Interview",
            "interviewer": "Mike",
            "notes": "Technical round",
        },
    )

    assert interview2.status_code == 201

    response = client.get(
        f"/applications/{application_id}/interviews",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    returned_ids = [interview["id"] for interview in data]

    assert interview1.json()["id"] in returned_ids
    assert interview2.json()["id"] in returned_ids


def test_get_single_interview(client):
    headers = register_and_login(
        client,
        "singleinterview@example.com",
        "singleinterview",
    )

    application_id = create_application(client, headers)

    interview = create_interview(
        client,
        headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    response = client.get(
        f"/interviews/{interview_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == interview_id
    assert data["stage"] == "Recruiter Screen"
    assert data["interviewer"] == "Sarah"
    assert data["notes"] == "Initial recruiter call"


def test_update_interview(client):
    headers = register_and_login(
        client,
        "updateinterview@example.com",
        "updateinterview",
    )

    application_id = create_application(client, headers)

    interview = create_interview(
        client,
        headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    response = client.patch(
        f"/interviews/{interview_id}",
        headers=headers,
        json={
            "stage": "Technical Interview",
            "interviewer": "Mike",
            "notes": "Moved to technical round",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == interview_id
    assert data["stage"] == "Technical Interview"
    assert data["interviewer"] == "Mike"
    assert data["notes"] == "Moved to technical round"


def test_delete_interview(client):
    headers = register_and_login(
        client,
        "deleteinterview@example.com",
        "deleteinterview",
    )

    application_id = create_application(client, headers)

    interview = create_interview(
        client,
        headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    response = client.delete(
        f"/interviews/{interview_id}",
        headers=headers,
    )

    assert response.status_code == 200

    verify_response = client.get(
        f"/interviews/{interview_id}",
        headers=headers,
    )

    assert verify_response.status_code == 404


def test_create_interview_without_token(client):
    response = client.post(
        "/applications/1/interviews",
        json={
            "stage": "Recruiter Screen",
            "interviewer": "Sarah",
            "notes": "Should not work",
        },
    )

    assert response.status_code == 401


def test_user_cannot_create_interview_for_another_users_application(client):
    owner_headers = register_and_login(
        client,
        "interviewowner@example.com",
        "interviewowner",
    )

    application_id = create_application(
        client,
        owner_headers,
    )

    other_headers = register_and_login(
        client,
        "interviewother@example.com",
        "interviewother",
    )

    response = client.post(
        f"/applications/{application_id}/interviews",
        headers=other_headers,
        json={
            "stage": "Recruiter Screen",
            "interviewer": "Sarah",
            "notes": "Should not be allowed",
        },
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_interview(client):
    owner_headers = register_and_login(
        client,
        "accessowner@example.com",
        "accessowner",
    )

    application_id = create_application(
        client,
        owner_headers,
    )

    interview = create_interview(
        client,
        owner_headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    other_headers = register_and_login(
        client,
        "accessother@example.com",
        "accessother",
    )

    response = client.get(
        f"/interviews/{interview_id}",
        headers=other_headers,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_interview(client):
    owner_headers = register_and_login(
        client,
        "updateowner@example.com",
        "updateowner",
    )

    application_id = create_application(
        client,
        owner_headers,
    )

    interview = create_interview(
        client,
        owner_headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    other_headers = register_and_login(
        client,
        "updateother@example.com",
        "updateother",
    )

    response = client.patch(
        f"/interviews/{interview_id}",
        headers=other_headers,
        json={
            "notes": "I should not be able to change this"
        },
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_interview(client):
    owner_headers = register_and_login(
        client,
        "deleteowner@example.com",
        "deleteowner",
    )

    application_id = create_application(
        client,
        owner_headers,
    )

    interview = create_interview(
        client,
        owner_headers,
        application_id,
    )

    interview_id = interview.json()["id"]

    other_headers = register_and_login(
        client,
        "deleteother@example.com",
        "deleteother",
    )

    response = client.delete(
        f"/interviews/{interview_id}",
        headers=other_headers,
    )

    assert response.status_code == 404

    verify_response = client.get(
        f"/interviews/{interview_id}",
        headers=owner_headers,
    )

    assert verify_response.status_code == 200
    
    