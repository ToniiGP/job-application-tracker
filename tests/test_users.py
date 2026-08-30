
def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "testuser@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data
    

def test_register_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "username": "firstuser",
        "password": "TestPassword123!",
    }

    first_response = client.post(
        "/users/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/register",
        json={
            "email": "duplicate@example.com",
            "username": "seconduser",
            "password": "AnotherPassword123!",
        },
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "A user with this email already exists."
    )


def test_register_duplicate_username(client): 
    user_data = {
        "email" : "example1@gmail.com",
        "username" : "duplicateuser",
        "password" : "Examplepass1",
    }
    
    first_response = client.post(
        "/users/register", 
        json=user_data,
    )
    
    assert first_response.status_code == 201 
    
    second_response = client.post(
        "/users/register", 
        json={
            "email" : "example2@gmail.com", 
            "username" : "duplicateuser",
            "password" : "Examplepass2",
        }  
    )
    
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "A user with this username already exists."
     )