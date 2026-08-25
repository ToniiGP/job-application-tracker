def test_login_success(client):
    client.post(
        "/users/register",
        json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "TestPassword123!",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    

def test_login_wrong_password(client): 
     client.post(
            "/users/register",
            json={
                "email": "loginuser2@example.com",
                "username": "loginuser2",
                "password": "TestPassword123!",
            },
        )
    
     response = client.post(
            "/auth/login",
            data={
                "username": "loginuser2@example.com",
                "password": "TestPassword122",
            },
        )
    
     assert response.status_code == 401
     
     
def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "SomePassword123!",
        },
    )

    assert response.status_code == 401
    
    
def test_users_me_with_valid_token(client): 
    client.post(
        "users/register", 
        json={
            "email": "meuser@example.com",
            "username": "meuser",
            "password": "TestPassword123!",
        }, 
        
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "meuser@example.com",
            "password": "TestPassword123!",
        },
    )
    
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "meuser@example.com"
    assert data["username"] == "meuser"
    
    
def test_users_me_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401