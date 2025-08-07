import pytest
from backend.app import create_app, db
from backend.models import User
from backend.config import TestingConfig

@pytest.fixture
def test_client():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
        
def test_successful_registration(test_client):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "123456",
        "role": "learner"
    }
    
    response = test_client.post('/auth/register', json=payload)
    json_data = response.get_json()
    
    assert response.status_code == 201
    print("Response JSON:", json_data)
    assert "data" in json_data
    assert json_data["data"]["email"] == "newuser@example.com"
    
def test_duplicate_username(test_client):
    user = User(username="duplicateuser", email="first@example.com", role="LEARNER")
    user.set_password("secret")
    db.session.add(user)
    db.session.commit()
    
    payload = {
        "username": "duplicateuser",
        "email": "other@example.com",
        "password": "123456",
        "role": "LEARNER"
    }
    
    response = test_client.post('/auth/register', json=payload)
    json_data = response.get_json()
    print("Response JSON:", json_data)
    
    assert response.status_code == 400
    assert json_data["message"] == "Username already exists"
    
def test_duplicate_email(test_client):
    user = User(username="uniqueuser", email="duplicate@example.com", role="LEARNER")
    user.set_password("secret")
    db.session.add(user)
    db.session.commit()
    
    payload = {
        "username": "otheruser",
        "email": "duplicate@example.com",
        "password": "1234",
        "role": "LEARNER"
    }
    
    response = test_client.post('/auth/register', json=payload)
    json_data = response.get_json()
    
    assert response.status_code == 400
    assert json_data["message"] == "Email already exists"
    
def test_invalid_payload(test_client):
    payload = {
        "username": "invaliduser",
        "role": "LEARNER"
    }
    
    response = test_client.post('/auth/register', json=payload)
    json_data = response.get_json()
    
    assert response.status_code == 400
    assert "message" in json_data
    
def test_successful_login(test_client):
    # Create user first
    user = User(username="loginuser", email="login@example.com", role="LEARNER")
    user.set_password("mypassword")
    db.session.add(user)
    db.session.commit()
    
    payload = {
        "email": "login@example.com",
        "password": "mypassword"
    }
    
    response = test_client.post("/auth/login", json=payload)
    json_data = response.get_json()
    print("LOGIN SUCCESS:", json_data)
    
    assert response.status_code == 200
    assert "access_token" in json_data["data"]
    assert json_data["data"]["user"]["email"] == "login@example.com"
    assert json_data["message"] == "Login successful"
    
def test_login_wrong_password(test_client):
    user = User(username="wrongpass", email="wrongpass@example.com", role="LEARNER")
    user.set_password("correctpassword")
    db.session.add(user)
    db.session.commit()
    
    payload = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    
    response = test_client.post("/auth/login", json=payload)
    json_data = response.get_json()
    print("WRONG PASSWORD:", json_data)
    
    assert response.status_code == 401
    assert json_data["message"] == "Invalid email or password"
    