def is_none_param(param: any) -> bool:
  return True if param is None else False

def parameter_check(name: (str | None), description: (str | None), in_diet: (bool | None), message: str):
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
