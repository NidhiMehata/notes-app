import uuid
from datetime import datetime

from models.note import Note


def create_user(client, email=None, password="password123"):
    if email is None:
        email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/users/",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    return response.json()


def login_user(client, email="test@example.com", password="password123"):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_authenticated_user(client, email=None, password="password123"):
    if email is None:
        email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    create_user(client, email, password)
    token = login_user(client, email, password)
    return token


# -------------------------------------------------------------------
# CREATE NOTE
# -------------------------------------------------------------------


def test_create_note_success(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "My Note",
            "content": "This is my note",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "My Note"
    assert data["content"] == "This is my note"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_note_without_authentication(client):
    response = client.post(
        "/notes",
        json={
            "title": "My Note",
            "content": "This is my note",
        },
    )

    assert response.status_code == 401


def test_create_note_missing_title(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "content": "This is my note",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_create_note_missing_content(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "My Note",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_create_note_empty_body(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={},
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_create_note_empty_title(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "",
            "content": "Some content",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201


def test_create_note_empty_content(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "My Note",
            "content": "",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201


# -------------------------------------------------------------------
# GET ALL NOTES
# -------------------------------------------------------------------


def test_get_all_notes_success(client):
    token = create_authenticated_user(client)

    client.post(
        "/notes",
        json={
            "title": "Note 1",
            "content": "Content 1",
        },
        headers=auth_headers(token),
    )

    client.post(
        "/notes",
        json={
            "title": "Note 2",
            "content": "Content 2",
        },
        headers=auth_headers(token),
    )

    response = client.get(
        "/notes",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 2

    # API explicitly orders by created_at descending.
    assert notes[0]["title"] == "Note 2"
    assert notes[1]["title"] == "Note 1"


def test_get_all_notes_without_authentication(client):
    response = client.get("/notes")

    assert response.status_code == 401


def test_get_all_notes_returns_empty_list_for_new_user(client):
    token = create_authenticated_user(client)

    response = client.get(
        "/notes",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json() == []


def test_user_cannot_see_another_users_notes(client):
    token_1 = create_authenticated_user(
        client,
        email="user1@example.com",
    )

    client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Private content",
        },
        headers=auth_headers(token_1),
    )

    token_2 = create_authenticated_user(
        client,
        email="user2@example.com",
    )

    response = client.get(
        "/notes",
        headers=auth_headers(token_2),
    )

    assert response.status_code == 200
    assert response.json() == []


# -------------------------------------------------------------------
# GET SINGLE NOTE
# -------------------------------------------------------------------


def test_get_note_success(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "My Note",
            "content": "My content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "My Note"
    assert data["content"] == "My content"


def test_get_nonexistent_note(client):
    token = create_authenticated_user(client)

    response = client.get(
        "/notes/999999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note with id 999999 does not exist"


def test_get_note_without_authentication(client):
    response = client.get("/notes/1")

    assert response.status_code == 401


def test_user_cannot_get_another_users_note(client):
    token_1 = create_authenticated_user(
        client,
        email="user-get@example.com",
    )

    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Private content",
        },
        headers=auth_headers(token_1),
    )

    note_id = create_response.json()["id"]

    token_2 = create_authenticated_user(
        client,
        email="user-get-2@example.com",
    )

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers(token_2),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Note with id {note_id} does not exist"


# -------------------------------------------------------------------
# UPDATE NOTE
# -------------------------------------------------------------------


def test_update_note_title(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original title",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Updated title",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "Updated title"
    assert data["content"] == "Original content"


def test_update_note_content(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original title",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "content": "Updated content",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Original title"
    assert data["content"] == "Updated content"


def test_update_note_title_and_content(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original title",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Updated title",
            "content": "Updated content",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["content"] == "Updated content"


def test_update_note_with_empty_body(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original title",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={},
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Original title"
    assert data["content"] == "Original content"


def test_update_nonexistent_note(client):
    token = create_authenticated_user(client)

    response = client.patch(
        "/notes/999999",
        json={
            "title": "Updated",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note with id 999999 does not exist"


def test_update_note_without_authentication(client):
    response = client.patch(
        "/notes/1",
        json={
            "title": "Updated",
        },
    )

    assert response.status_code == 401


def test_user_cannot_update_another_users_note(client):
    token_1 = create_authenticated_user(
        client,
        email="user-update@example.com",
    )

    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Private content",
        },
        headers=auth_headers(token_1),
    )

    note_id = create_response.json()["id"]

    token_2 = create_authenticated_user(
        client,
        email="user-update-2@example.com",
    )

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Hacked",
        },
        headers=auth_headers(token_2),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Note with id {note_id} does not exist"


def test_update_note_with_null_title_only(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original title",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": None,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Original title"
    assert data["content"] == "Original content"


# -------------------------------------------------------------------
# DELETE NOTE
# -------------------------------------------------------------------


def test_delete_note_success(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "To be deleted",
            "content": "Delete me",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200


def test_delete_nonexistent_note(client):
    token = create_authenticated_user(client)

    response = client.delete(
        "/notes/999999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note with id 999999 does not exist"


def test_delete_note_without_authentication(client):
    response = client.delete("/notes/1")

    assert response.status_code == 401


def test_deleted_note_cannot_be_fetched(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "To be deleted",
            "content": "Delete me",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    assert delete_response.status_code == 200

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Note with id {note_id} does not exist"


def test_deleted_note_does_not_appear_in_all_notes(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "To be deleted",
            "content": "Delete me",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    response = client.get(
        "/notes",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json() == []


def test_user_cannot_delete_another_users_note(client):
    token_1 = create_authenticated_user(
        client,
        email="user-delete@example.com",
    )
    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Private content",
        },
        headers=auth_headers(token_1),
    )

    note_id = create_response.json()["id"]

    token_2 = create_authenticated_user(
        client,
        email="user-delete-2@example.com",
    )
    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token_2),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Note with id {note_id} does not exist"

    # Verify the original owner can still access it.
    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers(token_1),
    )

    assert response.status_code == 200


# -------------------------------------------------------------------
# NOTE TIMESTAMPS
# -------------------------------------------------------------------


def test_note_timestamps_are_returned_as_iso_datetimes(client):
    token = create_authenticated_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "Timestamp test",
            "content": "Testing timestamps",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()

    created_at = datetime.fromisoformat(data["created_at"])
    updated_at = datetime.fromisoformat(data["updated_at"])

    assert created_at.tzinfo is not None
    assert updated_at.tzinfo is not None


def test_update_changes_note_content(client):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Original",
            "content": "Original content",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]
    original_updated_at = create_response.json()["updated_at"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "content": "Changed content",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "Changed content"
    assert data["updated_at"] >= original_updated_at


# -------------------------------------------------------------------
# DATABASE / SOFT DELETE
# -------------------------------------------------------------------


def test_delete_sets_is_deleted_in_database(client, db_session):
    token = create_authenticated_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Soft delete",
            "content": "Check database",
        },
        headers=auth_headers(token),
    )

    note_id = create_response.json()["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    note = db_session.get(Note, note_id)

    assert note is not None
    assert note.is_deleted is True
