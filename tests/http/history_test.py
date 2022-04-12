import json
from tests.http.test_app import test_app

'''
            ========================================================
                            history/customer tests
            ========================================================
'''

def test_invalid_token_customer():
    with test_app.test_client() as app:
        resp = app.get("/history/customer",
            headers = {"token": "i promise i am a token"})

        assert resp.status_code == 403

def test_working():
    with test_app.test_client() as app:
        resp = app.post("/auth/register",
                        json={"email": "testemailcustomer@email.com", "password": "Password123"})

        token = json.loads(resp.data)['token']

        customer_details = {
                'buyerReference' : "231",
                'customerName' : "Bob",
                'businessName' : "Bobs grocceries",
                'email' : "email@email.com",
                'streetAddress' : "21 Street",
                'additionalStreetAddress' : "",
                'city' : "Sydney",
                'postcode' : "1234",
                'country' : "Australia"
            }

        resp = app.post("/history/customer",
            headers = {"token": token},
            json= customer_details)
        
        assert resp.status_code == 200

        resp = app.get("/history/customer",
            headers = {"token": token})

        assert resp.status_code == 200

        assert customer_details in json.loads(resp.data)['customers']