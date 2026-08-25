def test_create_application(client):
    
    client.post(
        "/users/register",
        json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "TestPassword123!",
        },
    )
    
    login_response = client.post(
    "/auth/login",
        data={
            "username": "loginuser@example.com",
            "password": "TestPassword123!",
        },
    )

    token = login_response.json()["access_token"]
    
    application = client.post(
        "/applications/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company_name" : "Google", 
            "job_title" : "SE", 
            "status" : "Wishlist", 
        },
    )
    
    assert application.status_code == 201
    data = application.json()

    assert data["company_name"] == "Google"
    assert data["job_title"] == "SE"
    assert data["status"] == "Wishlist"
    assert "id" in data
    
    
def test_get_applications(client):
    client.post(
        "/users/register",
        json={
            "email": "listuser@example.com",
            "username": "listuser",
            "password": "TestPassword123!",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "listuser@example.com",
            "password": "TestPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post(
        "/applications/",
        headers=headers,
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        },
    )

    client.post(
        "/applications/",
        headers=headers,
        json={
            "company_name": "Microsoft",
            "job_title": "Backend Engineer",
            "status": "Applied",
        },
    )

    response = client.get(
        "/applications/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["company_name"] == "Google"
    assert data[1]["company_name"] == "Microsoft"
    

def test_get_single_application(client):
    client.post(
        "/users/register",
        json={
            "email": "singleuser@example.com",
            "username": "singleuser",
            "password": "TestPassword123!",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "singleuser@example.com",
            "password": "TestPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    created_application = client.post(
        "/applications/",
        headers=headers,
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        },
    )

    application_id = created_application.json()["id"]

    response = client.get(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["company_name"] == "Google"
    assert data["job_title"] == "Software Engineer"
    assert data["status"] == "Wishlist"
    

    
    