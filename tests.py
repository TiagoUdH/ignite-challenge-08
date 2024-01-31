import pytest
import requests
from itertools import product

from utils import is_none_param, parameter_check_for_creation, parameter_check_for_update
from models.snack import Snack

BASE_URL = "http://127.0.0.1:5000/"

names_for_creation = [None, "Salada"]
descriptions_for_creation = [None, "Prato calórico"]
in_diet_for_creation = [None, False]

combinations_for_creation = list(product(names_for_creation, descriptions_for_creation, in_diet_for_creation))

existing_snack = None

@pytest.mark.parametrize("name, description, in_diet", combinations_for_creation)
def test_create_snack(name: (str | None), description: (str | None), in_diet: (bool | None)):
  invalid_expected_response = parameter_check_for_creation(name, description, in_diet, "This field is required")
  
  request_body = {}
    
  if not is_none_param(name):
    request_body["name"] = name
      
  if not is_none_param(description):
    request_body["description"] = description
      
  if not is_none_param(in_diet):
    request_body["in_diet"] = in_diet
    
  response = requests.post(f"{BASE_URL}/snacks", json=request_body)
  response_json = response.json()
  
  if invalid_expected_response:
    invalid_expected_response["message"] = "Invalid snack data"
      
    assert invalid_expected_response == response_json
    assert response.status_code == 400
    
  else:
    assert response_json["message"] == "Snack registered successfully"
    assert response.status_code == 200
    
    snack_id = response_json["snack_id"]
    snack_created_at =response_json["created_at"]
    
    response = requests.get(f"{BASE_URL}/snacks/{snack_id}")
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json["id"] == snack_id
    assert response_json["created_at"] == snack_created_at
    
    global existing_snack
    existing_snack = response_json

names_for_update = [None, "Burguer"]
descriptions_for_update = [None, "Prato de poucas calorias"]
in_diet_for_update = [None, False]

combinations_for_update = list(product(names_for_update, descriptions_for_update, in_diet_for_update))
   
@pytest.mark.parametrize("name, description, in_diet", combinations_for_update)
def test_update_snack(name: (str | None), description: (str | None), in_diet: (bool | None)):
  request_body = {}
    
  if not is_none_param(name):
    request_body["name"] = name
      
  if not is_none_param(description):
    request_body["description"] = description
      
  if not is_none_param(in_diet):
    request_body["in_diet"] = in_diet
    
  response = requests.put(f"{BASE_URL}/snacks/{existing_snack["id"]}", json=request_body)
  response_json = response.json()
  
  assert response.status_code == 200
  assert response_json["message"] == "Snack updated successfully"
  
  response = requests.get(f"{BASE_URL}/snacks/{existing_snack["id"]}")
  response_json = response.json()
    
  expected_response = parameter_check_for_update(name, description, in_diet, existing_snack)
  
  assert response.status_code == 200
  assert response_json == expected_response
  
def test_get_snacks():
  response = requests.get(f"{BASE_URL}/snacks")
  response_json = response.json()
  
  assert response.status_code == 200
  
  for snack in response_json["snacks"]:
    assert "id" in snack
    assert "name" in snack
    assert "created_at" in snack
    assert "in_diet" in snack
    
    get_details_response = requests.get(f"{BASE_URL}/snacks/{snack["id"]}")
    get_details_response_json = get_details_response.json()
    
    assert get_details_response.status_code == 200
    
    del get_details_response_json["description"]
    
    assert get_details_response_json == snack
    
  assert response_json["snack_amount"] == len(response_json["snacks"])
  
def test_get_snack_details():
  response = requests.get(f"{BASE_URL}/snacks/{existing_snack["id"]}")
  response_json = response.json()
  
  assert response.status_code == 200
  assert response_json == existing_snack
  
def test_delete_snack():
  response = requests.delete(f"{BASE_URL}/snacks/{existing_snack["id"]}")
  response_json = response.json()
  
  assert response.status_code == 200
  assert response_json["message"] == "Snack deleted successfully"
  
  response = requests.get(f"{BASE_URL}/snacks/{existing_snack["id"]}")
  
  assert response.status_code == 404