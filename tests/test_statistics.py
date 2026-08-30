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


def create_application(
    client,
    headers,
    company_name,
    job_title,
    status,
    date_applied=None,
):
    application_data = {
        "company_name": company_name,
        "job_title": job_title,
        "status": status,
    }

    if date_applied is not None:
        application_data["date_applied"] = date_applied

    response = client.post(
        "/applications/",
        headers=headers,
        json=application_data,
    )

    assert response.status_code == 201

    return response


def test_statistics_summary(client):
    headers = register_and_login(
        client,
        "statsuser@example.com",
        "statsuser",
    )

    create_application(
        client,
        headers,
        "Google",
        "Software Engineer",
        "Wishlist",
    )

    create_application(
        client,
        headers,
        "Microsoft",
        "Backend Engineer",
        "Applied",
    )

    create_application(
        client,
        headers,
        "Amazon",
        "Software Engineer",
        "Technical Interview",
    )

    create_application(
        client,
        headers,
        "Apple",
        "Developer",
        "Offer",
    )

    create_application(
        client,
        headers,
        "Meta",
        "Backend Engineer",
        "Rejected",
    )

    response = client.get(
        "/statistics/summary",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_applications"] == 5
    assert data["wishlist"] == 1
    assert data["applied"] == 1
    assert data["interviewing"] == 1
    assert data["offers"] == 1
    assert data["rejected"] == 1
    assert data["total_interviews"] == 0


def test_applications_over_time(client):
    headers = register_and_login(
        client,
        "timeline@example.com",
        "timelineuser",
    )

    create_application(
        client,
        headers,
        "Google",
        "Software Engineer",
        "Applied",
        "2026-06-10",
    )

    create_application(
        client,
        headers,
        "Microsoft",
        "Backend Engineer",
        "Applied",
        "2026-06-20",
    )

    create_application(
        client,
        headers,
        "Amazon",
        "Software Engineer",
        "Applied",
        "2026-07-05",
    )

    create_application(
        client,
        headers,
        "Apple",
        "Developer",
        "Applied",
        "2026-08-01",
    )

    response = client.get(
        "/statistics/applications-over-time",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    assert data[0]["month"] == "2026-06"
    assert data[0]["count"] == 2

    assert data[1]["month"] == "2026-07"
    assert data[1]["count"] == 1

    assert data[2]["month"] == "2026-08"
    assert data[2]["count"] == 1


def test_statistics_are_user_specific(client):
    user1_headers = register_and_login(
        client,
        "statsowner@example.com",
        "statsowner",
    )

    create_application(
        client,
        user1_headers,
        "Google",
        "Software Engineer",
        "Applied",
    )

    create_application(
        client,
        user1_headers,
        "Microsoft",
        "Backend Engineer",
        "Offer",
    )

    user2_headers = register_and_login(
        client,
        "statsother@example.com",
        "statsother",
    )

    create_application(
        client,
        user2_headers,
        "Amazon",
        "Developer",
        "Rejected",
    )

    response = client.get(
        "/statistics/summary",
        headers=user2_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_applications"] == 1
    assert data["wishlist"] == 0
    assert data["applied"] == 0
    assert data["interviewing"] == 0
    assert data["offers"] == 0
    assert data["rejected"] == 1
    assert data["total_interviews"] == 0