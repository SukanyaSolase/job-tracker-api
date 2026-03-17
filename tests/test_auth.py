def test_register_and_login(client):
    # Register
    r = client.post("/auth/register", json={"email": "a@b.com", "password": "Test@1234"})
    assert r.status_code in (201, 409)

    # Login
    r = client.post(
        "/auth/login",
        data={"username": "a@b.com", "password": "Test@1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # Access protected route
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "a@b.com"