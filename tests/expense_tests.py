def test_no_expenses_list(test_client, init_database, second_user_token):
    response = test_client.get(
        "/expenses/", headers={"Authorization": f"Bearer {second_user_token}"}
    )
    assert response.status_code == 200
    assert response.json == []


def test_expenses_list(test_client, init_database, default_user_token):
    response = test_client.get(
        "/expenses/", headers={"Authorization": f"Bearer {default_user_token}"}
    )
    assert response.status_code == 200
    assert len(response.json) > 0


def test_full_expense(test_client, init_database, default_user_token):
    create_expenses_res = test_client.post(
        "/expenses/",
        json={"title": "test1", "amount": 100},
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert create_expenses_res.status_code == 201
    assert create_expenses_res.json["title"] == "test1"
    assert create_expenses_res.json["amount"] == 100

    create_expenses_res_id = create_expenses_res.json["id"]
    response = test_client.get(
        f"/expenses/{create_expenses_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert response.status_code == 200
    assert response.json["title"] == "test1"
    assert response.json["amount"] == 100

    update_expenses_res = test_client.patch(
        f"/expenses/{create_expenses_res_id}",
        json={"title": "test2", "amount": 200},
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert update_expenses_res.status_code == 200
    assert update_expenses_res.json["title"] == "test2"
    assert update_expenses_res.json["amount"] == 200

    delete_expenses_res = test_client.delete(
        f"/expenses/{create_expenses_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )
    assert delete_expenses_res.status_code == 204
    assert None == delete_expenses_res.json
