from http import HTTPStatus


def _make_question(client, text: str = "Q"):
    return client.post("/questions/", json={"text": text}).json()["id"]


def test_create_answer_for_existing_question(client):
    q_id = _make_question(client, "Тестовый вопрос")
    resp = client.post(
        f"/questions/{q_id}/answers/",
        json={"user_id": "u1", "text": "Мой ответ"},
    )
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.json()
    assert data["question_id"] == q_id
    assert data["user_id"] == "u1"
    assert data["text"] == "Мой ответ"


def test_cannot_create_answer_for_missing_question(client):
    resp = client.post(
        "/questions/999999/answers/",
        json={"user_id": "u2", "text": "N/A"},
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json()["detail"] == "Question not found"


def test_get_and_delete_answer(client):
    q_id = _make_question(client)
    created = client.post(
        f"/questions/{q_id}/answers/",
        json={"user_id": "u3", "text": "Ответ"},
    ).json()

    a_id = created["id"]

    got = client.get(f"/answers/{a_id}")
    assert got.status_code == HTTPStatus.OK
    assert got.json()["id"] == a_id
    assert got.json()["question_id"] == q_id

    d = client.delete(f"/answers/{a_id}")
    assert d.status_code == HTTPStatus.NO_CONTENT

    nf = client.get(f"/answers/{a_id}")
    assert nf.status_code == HTTPStatus.NOT_FOUND


def test_multiple_answers_by_same_user_allowed(client):
    q_id = _make_question(client)
    for i in range(2):
        resp = client.post(
            f"/questions/{q_id}/answers/",
            json={"user_id": "same", "text": f"ans {i}"},
        )
        assert resp.status_code == HTTPStatus.CREATED

    q = client.get(f"/questions/{q_id}").json()
    user_ids = [a["user_id"] for a in q["answers"]]
    assert user_ids == ["same", "same"]


