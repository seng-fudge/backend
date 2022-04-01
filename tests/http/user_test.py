import json
from tests.http.test_app import test_app
'''
            ========================================================
                            get_user_data tests
            ========================================================
'''

def test_bad_token_get_user_data():
    with test_app.test_client() as app:
        resp = app.get("/user/data",
            headers = {"token": "i promise i am a token"})

        assert resp.status_code == 403

def test_no_data_uploaded_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200

        data = json.loads(resp.data)

        resp = app.get("/user/data", headers = {"token": data["token"]})
        assert resp.status_code == 204

def test_working_get_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        
        data = json.loads(resp.data)
        token = data["token"]
        
        sent_data = {
                "businessName" : "Fudge",
                "contactName" : "Some Guy",
                "electronicMail" : "some.guy@mail.com",
                "supplierID" : 42,
                "street" : "street rd",
                "city" : "city",
                "postcode" : "2000",
                "country" : "Australia",
                "currency" : "AUD"
            }

        resp = app.post(
            "/user/data",
            headers = {"token": token},
            json = sent_data
        )
        assert resp.status_code == 200

        data = json.loads(resp.data)

        resp = app.get("/user/data", headers = {"token": token})
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert data['electronicMail'] == "some.guy@mail.com"



'''
            ========================================================
                            post_user_data tests
            ========================================================
'''
def test_missing_data_post_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        resp = app.post(
            "/user/data",
            headers = {"token": data["token"]},
            json = {
                "businessName" : "Fudge",
                "electronicMail" : "some.other.guy@mail.com",
                "supplierID" : 42,
                "street" : "street rd",
                "city" : "city",
                "postcode" : "2000",
                "country" : "Australia",
                "currency" : "AUD"
            }
        )
        assert resp.status_code == 400
        resp = app.get("/user/data", headers = {"token": data["token"]})
        assert resp.status_code == 200
        data = json.loads(resp.data)

        assert data['electronicMail'] != "some.other.guy@mail.com"

def test_bad_email_post_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        token = data["token"]

        #get original data
        resp = app.get("/user/data", headers = {"token": token})
        assert resp.status_code == 200
        orig_data = json.loads(resp.data)

        sent_data = {
                "businessName" : "Fudge",
                "contactName" : "Some Guy",
                "electronicMail" : "obvi not an email",
                "supplierID" : 1,
                "street" : "street rd",
                "city" : "city",
                "postcode" : "2000",
                "country" : "Australia",
                "currency" : "AUD"
            }
        resp = app.post(
            "/user/data",
            headers = {"token": token},
            json = sent_data
        )
        assert resp.status_code == 400

        #ensure that no data was changed
        resp = app.get("/user/data", headers = {"token": token})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert orig_data == data

def test_working_post_user_data():
    with test_app.test_client() as app:

        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200

        sent_data = {
                "businessName" : "Fudge",
                "contactName" : "Some Guy",
                "electronicMail" : "some.guy@mail.com",
                "supplierID" : 42,
                "street" : "street rd",
                "city" : "city",
                "postcode" : "2000",
                "country" : "Australia",
                "currency" : "AUD"
            }

        data = json.loads(resp.data)
        token = data["token"]

        resp = app.post(
            "/user/data",
            headers = {"token": token},
            json = sent_data
        )
        assert resp.status_code == 200

        # ensure data was changed
        resp = app.get("/user/data", headers = {"token": token})
        assert resp.status_code == 200
        data = json.loads(resp.data)

        assert data == sent_data


def test_all_types_bad_data_post_user_data():
    with test_app.test_client() as app:
        resp = app.post("/auth/login",
                json={"email": "email4@email.com", "password": "Password123"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        token = data["token"]

        sent_data = {
                "businessName" : "Fudge",
                "contactName" : "Some Guy",
                "electronicMail" : "some.guy@mail.com",
                "supplierID" : 1,
                "street" : "street rd",
                "city" : "city",
                "postcode" : "2000",
                "country" : "Australia",
                "currency" : "AUD"
            }

        sent_data["businessName"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["businessName"] = "Fudge"

        sent_data["contactName"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["contactName"] = "Some Guy"

        sent_data["electronicMail"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["electronicMail"] = "some.guy@mail.com"

        sent_data["supplierID"] = "im supposed to be an int"
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["supplierID"] = 42

        sent_data["street"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["street"] = "street rd"

        sent_data["city"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["city"] = "city"

        sent_data["postcode"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["postcode"] = "2000"

        sent_data["country"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["country"] = "Australia"

        sent_data["currency"] = 42
        resp = app.post("/user/data",headers = {"token": token},json = sent_data)
        assert resp.status_code == 400
        sent_data["currency"] = "AUD"

