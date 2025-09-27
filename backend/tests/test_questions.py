from http import HTTPStatus


def test_list_questions_initially_empty(client):
    resp = client.get("/questions/")
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == []


def test_create_and_get_question(client):
    payload = {"text": "Что такое FastAPI?"}
    resp = client.post("/questions/", json=payload)
    assert resp.status_code == HTTPStatus.CREATED
    q = resp.json()
    assert q["id"] > 0
    assert q["text"] == payload["text"]

    q_id = q["id"]
    resp2 = client.get(f"/questions/{q_id}")
    assert resp2.status_code == HTTPStatus.OK
    data = resp2.json()
    assert data["id"] == q_id
    assert data["text"] == payload["text"]
    assert data.get("answers") == []


def test_get_question_not_found(client):
    resp = client.get("/questions/999999")
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json()["detail"] == "Question not found"


def test_delete_question_cascade_answers(client):
    q_resp = client.post("/questions/", json={"text": "Задача"})
    q_id = q_resp.json()["id"]
    for i in range(3):
        a_resp = client.post(
            f"/questions/{q_id}/answers/",
            json={"user_id": "user1", "text": f"ответ {i}"},
        )
        assert a_resp.status_code == HTTPStatus.CREATED

    got = client.get(f"/questions/{q_id}")
    assert got.status_code == HTTPStatus.OK
    assert len(got.json()["answers"]) == 3

    d = client.delete(f"/questions/{q_id}")
    assert d.status_code == HTTPStatus.NO_CONTENT

    nf = client.get(f"/questions/{q_id}")
    assert nf.status_code == HTTPStatus.NOT_FOUND


