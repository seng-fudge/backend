import json
from tests.http.test_app import test_app

'''
            ========================================================
                            history/customer tests
            ========================================================
'''

def test_invalid_token_customer_customer():
    with test_app.test_client() as app:
        resp = app.get("/history/customer",
            headers = {"token": "i promise i am a token"})

        assert resp.status_code == 403

def test_working_customer():
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


'''
            ========================================================
                            history/payment tests
            ========================================================
'''

def test_invalid_token_customer_payment():
    with test_app.test_client() as app:
        resp = app.get("/history/payment",
            headers = {"token": "i promise i am a token"})

        assert resp.status_code == 403

def test_working_payment():
    with test_app.test_client() as app:
        resp = app.post("/auth/register",
                        json={"email": "testemailcustomer2312@email.com", "password": "Password123"})

        token = json.loads(resp.data)['token']

        payment_details = {
            'dueDate' : "Tomorrow",
            'paymentType' : "Hard cold cash",
            'paymentId' : "Something idk",
            'paymentTerms' : "You must pay me or else"
        }

        resp = app.post("/history/payment",
            headers = {"token": token},
            json= payment_details)
        
        assert resp.status_code == 200

        resp = app.get("/history/payment",
            headers = {"token": token})

        assert resp.status_code == 200

        assert payment_details in json.loads(resp.data)['payments']