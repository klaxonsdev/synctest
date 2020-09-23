import requests

mainURL="http://127.0.0.1:5000/api"

submit_data = {
    "name": "TEST_UNIT",
    "address": "from_apitest.py",
    "city": "PHONEBOOK",
    "phonenumber": 123
                }

contact_list = [
    {
        "address":"APP.DB",
        "city":"PHONEBOOK",
        "id":1,
        "name":"TEST_UNIT",
        "phonenumber":123
    },
    {
        "id": 2,
        "name": "TEST_UNIT",
        "address": "from_apitest.py",
        "city": "PHONEBOOK",
        "phonenumber": 123
    }
    ]

contact_data_1 = {
    "id": 1,
    "name": "TEST_UNIT",
    "address": "APP.DB",
    "city": "PHONEBOOK",
    "phonenumber": 123
                }

contact_data_2 = {
    "id": 2,
    "name": "TEST_UNIT",
    "address": "from_apitest.py",
    "city": "PHONEBOOK",
    "phonenumber": 123
                }

contact_data_3 = {
    "id": 3,
    "name": "TEST_UNIT",
    "address": "from_apitest.py",
    "city": "PHONEBOOK",
    "phonenumber": 123
                }

put_data = {
    "name": "TEST_UNIT_UPDATE",
    "address": "from_apitest.py_UPDATE",
    "city": "PHONEBOOK_UPDATE",
    "phonenumber": 123
            }       

updated_contact_data_2 = {
    "id": 2,
    "name": "TEST_UNIT_UPDATE",
    "address": "from_apitest.py_UPDATE",
    "city": "PHONEBOOK_UPDATE",
    "phonenumber": 123
                        }

response = requests.put(mainURL + "/phonebook/2", json=contact_data_2) #set contact #2 

def test_Phonebook_JSON():
     response = requests.get(mainURL + "/phonebook")
     assert response.headers["Content-Type"] == "application/json"

def test_phonebook_GET_all_Contacts():
    response = requests.get(mainURL + "/phonebook")
    response_body = response.json()
    assert response_body == contact_list

def test_phonebook_POST_Contacts():
    response = requests.post(mainURL + "/phonebook", json=submit_data)
    assert response.status_code ==200

def test_compare_POSTED_Contact(): #Comparing contact #2 with existing data from DB
    response = requests.get(mainURL + "/phonebook/3")
    response_body = response.json()
    assert response_body == contact_data_3

def test_phonebook_GET_Contact_id_1(): #Get response Contact #1
    response = requests.get(mainURL + "/phonebook/1")
    response_body = response.json()
    assert response.status_code ==200

def test_compare_Contact_id_1(): #Comparing contact #1 with existing data from DB
    response = requests.get(mainURL + "/phonebook/1")
    response_body = response.json()
    assert response_body == contact_data_1

def test_UPDATE_Contact_id_2(): #Update and compare contact #2 with existing data from DB
    response = requests.put(mainURL + "/phonebook/2", json=put_data)
    response_body = response.json()
    assert response_body == updated_contact_data_2

def test_DELETE_Contact_id_3(): #Comparing contact #3 with existing data from DB
    response = requests.delete(mainURL + "/phonebook/3")
    response_body = response.json()
    assert response_body == contact_data_3
    response = requests.get(mainURL + "/phonebook/3")
    response_body = response.json()
    assert response_body == {}