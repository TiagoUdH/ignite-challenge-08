import pytest
import requests
from itertools import product

from utils import is_none_param, parameter_check
from models.snack import Snack

BASE_URL = "http://127.0.0.1:5000/"

names_for_creation = [None, "Salada"]
descriptions_for_creation = [None, "Prato calórico"]
in_diet_for_creation = [None, False]

combinations_for_creation = list(product(names_for_creation, descriptions_for_creation, in_diet_for_creation))

existing_snack = None

@pytest.mark.parametrize("name, description, in_diet", combinations_for_creation)
def test_create_snack(name: (str | None), description: (str | None), in_diet: (bool | None)):
  invalid_expected_response = parameter_check(name, description, in_diet, "This field is required")
  
  new_snack_data = {}
    
  if not is_none_param(name):
    new_snack_data["name"] = name
      
  if not is_none_param(description):
    new_snack_data["description"] = description
      
  if not is_none_param(in_diet):
    new_snack_data["in_diet"] = in_diet
  
  response = requests.post(f"{BASE_URL}/snacks", json=new_snack_data)
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