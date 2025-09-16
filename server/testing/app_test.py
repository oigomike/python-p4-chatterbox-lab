def test_create_message(client):
    res = client.post("/messages", json={"body": "Hello", "username": "Mike"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["body"] == "Hello"
    assert data["username"] == "Mike"

def test_get_messages(client):
    res = client.get("/messages")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)

def test_update_message(client):
    # Create first
    res = client.post("/messages", json={"body": "Old", "username": "Mike"})
    msg_id = res.get_json()["id"]

    # Update
    res = client.patch(f"/messages/{msg_id}", json={"body": "New"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["body"] == "New"

def test_delete_message(client):
    # Create first
    res = client.post("/messages", json={"body": "To delete", "username": "Mike"})
    msg_id = res.get_json()["id"]

    # Delete
    res = client.delete(f"/messages/{msg_id}")
    assert res.status_code == 204
