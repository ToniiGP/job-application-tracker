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
    

def test_update_application(client): 
    client.post(
        "/users/register",
        json={
            "email" : "test123@gmail.com", 
            "username" : "test123", 
            "password" : "Test123!"
        },
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username" : "test123@gmail.com", 
            "password" : "Test123!"
        },
    )
    
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    
    application = client.post(
        "/applications",
        headers=headers, 
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        }, 
    )
    
    assert application.status_code == 201
    
    application_id = application.json()["id"]
    
    response = client.patch(
        f"/applications/{application_id}",
        headers=headers,
        json={
            "job_title" : "Junior Developer"
        },
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == application_id
    assert data["company_name"] == "Google"
    assert data["job_title"] == "Junior Developer"
    assert data["status"] == "Wishlist"
    

def test_delete_application(client): 
    client.post(
            "/users/register",
            json={
                "email" : "test123@gmail.com", 
                "username" : "test123", 
                "password" : "Test123!"
            },
        )
        
    login_response = client.post(
        "/auth/login",
        data={
            "username" : "test123@gmail.com", 
            "password" : "Test123!",
            },
        )
        
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    headers = {
            "Authorization" : f"Bearer {token}"
        }
        
    application = client.post(
        "/applications",
        headers=headers, 
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        }, 
    )
        
    assert application.status_code == 201
        
    application_id = application.json()["id"]
    
    deleted = client.delete(
        f"/applications/{application_id}",
        headers=headers 
    )
    
    assert deleted.status_code == 200
    assert deleted.json()["message"] == "Application deleted successfully"
    
    response = client.get(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert response.status_code == 404
    
def test_create_application_without_token(client):
    application = client.post(
        "/applications/",
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        },
    )

    assert application.status_code == 401


def test_user_cannot_access_another_users_application(client): 
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
    
    assert login_response.status_code == 200
    
    user1_token = login_response.json()["access_token"]
    
    headers = {
            "Authorization": f"Bearer {user1_token}"
    }
    
    
    application = client.post(
        "/applications/",
        headers=headers,
        json={
                "company_name": "Microsoft",
                "job_title": "Backend Engineer",
                "status": "Applied",
        },
    )
    
    assert application.status_code == 201
    
    application_id = application.json()["id"]
    
    client.post(
        "/users/register",
        json={
            "email": "listuser2@example.com",
            "username": "listuser2",
            "password": "TestPassword123!",
        },
    )
        
    login_response2 = client.post(
        "/auth/login",
        data={
            "username": "listuser2@example.com",
            "password": "TestPassword123!",
        },
    )
    
    assert login_response2.status_code == 200
        
    user2_token = login_response2.json()["access_token"]
        
    headers2 = {
            "Authorization": f"Bearer {user2_token}"
    }
    
    response = client.get(
        f"/applications/{application_id}",
        headers=headers2,
    )

    assert response.status_code == 404
    

def test_user_cannot_update_another_users_application(client):
    client.post(
        "/users/register",
        json={
            "email": "owner@example.com",
            "username": "owner",
            "password": "TestPassword123!",
        },
    )

    owner_login = client.post(
        "/auth/login",
        data={
            "username": "owner@example.com",
            "password": "TestPassword123!",
        },
    )

    assert owner_login.status_code == 200

    owner_token = owner_login.json()["access_token"]

    owner_headers = {
        "Authorization": f"Bearer {owner_token}"
    }

    application = client.post(
        "/applications/",
        headers=owner_headers,
        json={
            "company_name": "Microsoft",
            "job_title": "Backend Engineer",
            "status": "Applied",
        },
    )

    assert application.status_code == 201

    application_id = application.json()["id"]

    client.post(
        "/users/register",
        json={
            "email": "other@example.com",
            "username": "otheruser",
            "password": "TestPassword123!",
        },
    )

    other_login = client.post(
        "/auth/login",
        data={
            "username": "other@example.com",
            "password": "TestPassword123!",
        },
    )

    assert other_login.status_code == 200

    other_token = other_login.json()["access_token"]

    other_headers = {
        "Authorization": f"Bearer {other_token}"
    }

    response = client.patch(
        f"/applications/{application_id}",
        headers=other_headers,
        json={
            "job_title": "Hacked Title"
        },
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_application(client):
    client.post(
        "/users/register",
        json={
            "email": "owner2@example.com",
            "username": "owner2",
            "password": "TestPassword123!",
        },
    )

    owner_login = client.post(
        "/auth/login",
        data={
            "username": "owner2@example.com",
            "password": "TestPassword123!",
        },
    )

    assert owner_login.status_code == 200

    owner_token = owner_login.json()["access_token"]

    owner_headers = {
        "Authorization": f"Bearer {owner_token}"
    }

    application = client.post(
        "/applications/",
        headers=owner_headers,
        json={
            "company_name": "Google",
            "job_title": "Software Engineer",
            "status": "Wishlist",
        },
    )

    assert application.status_code == 201

    application_id = application.json()["id"]

    client.post(
        "/users/register",
        json={
            "email": "other2@example.com",
            "username": "otheruser2",
            "password": "TestPassword123!",
        },
    )

    other_login = client.post(
        "/auth/login",
        data={
            "username": "other2@example.com",
            "password": "TestPassword123!",
        },
    )

    assert other_login.status_code == 200

    other_token = other_login.json()["access_token"]

    other_headers = {
        "Authorization": f"Bearer {other_token}"
    }

    response = client.delete(
        f"/applications/{application_id}",
        headers=other_headers,
    )

    assert response.status_code == 404