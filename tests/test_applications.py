def get_token(client, email="user@test.com", password="Test@1234"):
    client.post("/auth/register", json={"email": email, "password": password})
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return r.json()["access_token"]


def test_create_and_list_applications(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    payload = {
        "company": "Google",
        "role": "Software Engineer",
        "status": "APPLIED",
        "link": "https://careers.google.com",
        "notes": "test",
    }
    r = client.post("/applications", json=payload, headers=headers)
    assert r.status_code == 201
    app_id = r.json()["id"]

    # List
    r = client.get("/applications", headers=headers)
    assert r.status_code == 200
    assert any(a["id"] == app_id for a in r.json())

    # Filter
    r = client.get("/applications?status=APPLIED", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1