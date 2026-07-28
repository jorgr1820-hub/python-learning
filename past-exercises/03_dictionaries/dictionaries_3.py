#This program will read the key and then remove 
# the values listed on list_of_keys




list_of_keys = ["access_level", "age"]
employee = {
    "name": "John",
    "email": "john@ecorp.com",
    "access_level": 5,
    "age": 28
    }


for key in list_of_keys:
    if key in employee:
        employee.pop(key)


for key,value in employee.items():
    print(key , ":" , value)