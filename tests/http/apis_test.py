import json
from tests.http.test_app import test_app

def test_conenct_invalid_token_apis():
    with test_app.test_client() as app:
        resp = app.post("/apis/connect",
            headers={"token": "Invalid_token"})

        assert resp.status_code == 403

def test_connect_working_apis():
    with test_app.test_client() as app:
        app.post("/auth/register", json={"email": "email4@email.com", "password": "Password123"})

        resp = app.post("/auth/login",
                        json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200

        data = json.loads(resp.data)
        token = data["token"]

        resp = app.post("/apis/connect",
            headers={"token":token})

        assert resp.status_code == 200
        
        assert "send_token" in json.loads(resp.data)
        
        resp = app.post("/apis/disconnect",
            headers={"token":token})
        
        assert resp.status_code == 200