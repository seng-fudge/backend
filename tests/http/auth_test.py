import json
from tests.http.fixtures import test_app


def test_invalidEmail_register():
    with test_app.test_client() as app:
        resp = app.post("/auth/register",
                        json={"email": "email", "password": "Password123"})

        assert resp.status_code == 400


def test_invalidPassword_register():
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


def test_emailAlreadyRegistered_register():
    with test_app.test_client() as app:
        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "Password123"})

        assert resp.status_code == 200

        resp = app.post(
            "/auth/register", json={"email": "email@email.com", "password": "Password123"})

        assert resp.status_code == 400

