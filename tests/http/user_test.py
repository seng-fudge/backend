import json
from app import init_app
test_app = init_app()
'''
            ========================================================
                            get_user_data tests
            ========================================================
'''


def test_working_get_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        resp = app.get("/user/data", headers = {"token": data["token"]})
        data = json.loads(resp.data)
        assert data['electronicMail'] == "email4@email.com"
