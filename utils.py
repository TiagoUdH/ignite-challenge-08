from models.snack import Snack

def is_none_param(param: any) -> bool:
  return True if param is None else False

def parameter_check_for_creation(name: (str | None), description: (str | None), in_diet: (bool | None), message: str):
    is_none_param1 = is_none_param(name)
    is_none_param2 = is_none_param(description)
    is_none_param3 = is_none_param(in_diet)
    
    response = {}
    
    if is_none_param1:
      response["name"] =  message
      
    if is_none_param2:
      response["description"] =  message
      
    if is_none_param3:
      response["in_diet"] = message
        
    return response
  
def parameter_check_for_update(name: (str | None), description: (str | None), in_diet: (bool | None), snack: Snack):
    is_none_param1 = is_none_param(name)
    is_none_param2 = is_none_param(description)
    is_none_param3 = is_none_param(in_diet)
    
    if not is_none_param1:
      snack["name"] =  name
      
    if not is_none_param2:
      snack["description"] =  description
      
    if not is_none_param3:
      snack["in_diet"] = in_diet
        
    return snack
