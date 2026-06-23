


#keys = ["access_level","age"]
#values = [5,25]
#employee = {}


#def add_employee(a, b):
#    for i in range(len(a)):
#        employee[a[i]] = b[i]

#add_employee(keys, values)

#print(employee)

remove_keys = ["access_level","age"]
employee = {"name":"John","email":"john@ecorp.com","access_level":5,"age":28}


#def remove_keys_from_employee(a, b):
#    new_employee = b.copy()
#    for i in a:
#        if i in b:
#            new_employee.pop(i)
#    return new_employee

#result = remove_keys_from_employee(remove_keys, employee)
#print(result)

#for key, value in result.items():
#    print(f"\n{key} : {value}")


for key in remove_keys:
    if key in employee:
        employee.pop(key)
print(employee)

