#This program sum the total of numbers on the list
#and print the total 


num_list = [2,1,4,5,6,30]

def sum_num(a):
    total = 0
    for index in a:
        total += index
    print(total)

sum_num(num_list)    
