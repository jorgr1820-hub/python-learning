#This program merges 2 lists (Keys,Values)
#and creates a dictionary using the elements on the list
#to print a single list including one element form the first list, and
#one from the second one.



list_a = ["first_name", "last_name", "role"]
list_b = ["Jordan", "Guzman", "Software Engineer"]

dictionary = dict(zip(list_a , list_b))
print(dictionary)