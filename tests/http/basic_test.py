from tests.http.test_app import test_app

'''
            ========================================================
                            basic endpoint test
            ========================================================
'''

def test_functional():
    with test_app.test_client() as app:
        resp = app.get("/")
        assert resp.status_code == 200