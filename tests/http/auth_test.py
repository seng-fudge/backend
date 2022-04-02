import json
from tests.http.test_app import test_app
'''
            ========================================================
                            auth register tests
            ========================================================
'''


def test_invalid_email_register():
    with test_app.test_client() as app:
        resp = app.post("/auth/register",
                        json={"email": "email", "password": "Password123"})

        assert resp.status_code == 400


def test_invalid_password_register():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "Password"})

        assert resp.status_code == 400

        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "password123"})

        assert resp.status_code == 400

        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "PASSWORD123"})

        assert resp.status_code == 400

        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "Passw23"})

        assert resp.status_code == 400


def test_working_register():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "Password123"})

        assert resp.status_code == 200
        assert "token" in json.loads(resp.data)


def test_email_already_registered_register():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/register", json={"email": "email2@email.com", "password": "Password123"})

        assert resp.status_code == 200

        resp = app.post(
            "/auth/register", json={"email": "email2@email.com", "password": "Password123"})

        assert resp.status_code == 400


'''
            ========================================================
                            auth login tests
            ========================================================
'''


def test_invalid_email_login():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                        json={"email": "email", "password": "Password123"})

        assert resp.status_code == 400


def test_invalid_password_login():
    with test_app.test_client() as app:
        app.post(
            "/auth/register", json={"email": "email3@email.com", "password": "Password123"})

        resp = app.post("/auth/login",
                        json={"email": "email3@email.com", "password": "Password321"})
        assert resp.status_code == 400


def test_working_login():
    with test_app.test_client() as app:
        app.post(
            "/auth/register", json={"email": "email4@email.com", "password": "Password123"})

        resp = app.post("/auth/login",
                        json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        assert "token" in json.loads(resp.data)

'''
            ========================================================
                            auth login tests
            ========================================================
'''

def test_bad_token_logout():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/logout",
            headers={"token":"I am totally a token i promise good sir"}
        )
        assert resp.status_code == 403
def test_working_logout():
    with test_app.test_client() as app:
        app.post(
            "/auth/register", json={"email": "email4@email.com", "password": "Password123"}
        )

        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200

        data = json.loads(resp.data)
        token = data["token"]

        resp = app.post(
            "/auth/logout",
            headers={"token":token}
        )
        assert resp.status_code == 200

        resp = app.post(
            "/auth/logout",
            headers={"token":token}
        )
        assert resp.status_code == 403

'''
            ========================================================
                            auth remove tests
            ========================================================
'''


def test_invalid_token_remove():
    with test_app.test_client() as app:
        resp = app.delete("/auth/remove", headers={"token": "Token is wrong"})
        assert resp.status_code == 403


def test_working_remove():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/register", json={"email": "email6@email.com", "password": "Password123"})

        assert resp.status_code == 200

        data = json.loads(resp.data)

        resp = app.delete("/auth/remove", headers={"token": data["token"]})
        assert resp.status_code == 200

        resp = app.delete("/auth/remove", headers={"token": data["token"]})
        assert resp.status_code == 403

        resp = app.post("/auth/login",
                        json={"email": "email6@email.com", "password": "Password321"})
        assert resp.status_code == 400
