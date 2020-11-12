
from chalice.test import Client
from app import app


"""
Unit testcases are created based on chalice testing framework
https://aws.github.io/chalice/topics/testing.html#rest-apis

To run test cases download pytest and run below command
"pip install pytest"
"pytest -s test/test_app.py" (-s gives more logging info)

"""

def test_index():
     with Client(app) as client:
         app.log.info("Printing response body from test_index")
         response = client.http.get('/')
         app.log.info(response.body)
         assert response.status_code == 200


def test_urlLookupWithOutQueryParameters():
    with Client(app) as client:
         app.log.info("Printing response body from test_urlLookupWithOutQueryParameters")
         response = client.http.get('/urlLookUp')
         app.log.info(response.body)
         assert response.status_code == 400

def test_urlLookupWithOutURLQueryParameter():
    with Client(app) as client:
         app.log.info("Printing response body from test_urlLookupWithOutURLQueryParameter")
         response = client.http.get('/urlLookUp?query1=http://www.google.co.in/news')
         app.log.info(response.body)
         assert response.status_code == 400

def test_urlLookupWithMalformedURI():
    with Client(app) as client:
         app.log.info("Printing response body from test_urlLookupWithMalformedURI")
         response = client.http.get('/urlLookUp?url=www.google.co.in/news')
         app.log.info(response.body)
         assert response.status_code == 400


def test_urlLookup200ResponseDeny():
    with Client(app) as client:
         app.log.info("Printing response body from test test_urlLookup200ResponseDeny")
         response = client.http.get('/urlLookUp?url=http://www.google.co.in/news')
         app.log.info(response.body)
         assert response.status_code == 200

def test_urlLookup200ResponseAllow():
    with Client(app) as client:
         app.log.info("Printing response body from test test_urlLookup200ResponseAllow")
         response = client.http.get('/urlLookUp?url=http://www.google.com/news')
         app.log.info(response.body)
         assert response.status_code == 200