import pytest
from app import create_app, db
from config import TestingConfig
from models import User

# ---------------- Test Fixtures
@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# ---------------- Helper function to create a new user
def create_user(username, email, role, password="pass1234"):
    u = User(username=username, email=email, role=role.upper() if role.islower() else role)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u

# ---------------- Helper function to log in a user
def login(client, email, password):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    data = resp.get_json()
    assert resp.status_code == 200, f"Login failed: {data}"
    return data["data"]["access_token"]

# ---------------- Helper function to generate auth headers
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

# ---------------- Test admin has access to all routes
def test_admin_has_access_to_all_routes(client):
    with client.application.app_context():
        create_user("admin1", "admin1@example.com", "ADMIN", "secret")
    token = login(client, "admin1@example.com", "secret")

    # any-auth
    r1 = client.get("/protected/any-auth", headers=auth_headers(token))
    assert r1.status_code == 200

    # employer-only (admin should pass)
    r2 = client.get("/protected/employer-only", headers=auth_headers(token))
    assert r2.status_code == 200

    # admin-only
    r3 = client.get("/protected/admin-only", headers=auth_headers(token))
    assert r3.status_code == 200

# ---------------- Test employer cannot access admin-only
def test_employer_cannot_access_admin_only(client):
    with client.application.app_context():
        create_user("emp1", "emp1@example.com", "EMPLOYER", "secret")
    token = login(client, "emp1@example.com", "secret")

    # any-auth
    r1 = client.get("/protected/any-auth", headers=auth_headers(token))
    assert r1.status_code == 200

    # employer-only
    r2 = client.get("/protected/employer-only", headers=auth_headers(token))
    assert r2.status_code == 200

    # admin-only (should be 403)
    r3 = client.get("/protected/admin-only", headers=auth_headers(token))
    assert r3.status_code == 403
    body = r3.get_json()
    assert body["message"].startswith("Forbidden")

# ---------------- Test learner cannot access employer or admin-only
def test_learner_cannot_access_employer_or_admin_only(client):
    with client.application.app_context():
        create_user("learner1", "learner1@example.com", "LEARNER", "secret")
    token = login(client, "learner1@example.com", "secret")

    # any-auth
    r1 = client.get("/protected/any-auth", headers=auth_headers(token))
    assert r1.status_code == 200

    # employer-only (403)
    r2 = client.get("/protected/employer-only", headers=auth_headers(token))
    assert r2.status_code == 403

    # admin-only (403)
    r3 = client.get("/protected/admin-only", headers=auth_headers(token))
    assert r3.status_code == 403

# ---------------- Test unauthenticated user receives 401
def test_unauthenticated_is_401(client):
    r = client.get("/protected/any-auth")
    assert r.status_code == 401  # jwt_required should handle
