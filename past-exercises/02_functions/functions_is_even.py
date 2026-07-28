

# Write is_even(n) that returns True/False.

# Write swap_first_last(my_list) that swaps the first and last elements for lists of any size.

# Write count_primes(limit) that counts how many primes exist from 2 to limit (using your is_prime).

#def is_even(n):
#    if n % 2 == 0:
#        return (f"This is: {True}")
#    else: return (f"This is: {False}")

#num= 4
#print(is_even(num))

#jordan_nums = int(input("What is your favorite number?:"))
#print(is_even(jordan_nums))




#def swap_first_last(my_list):
#    if len(my_list) < 2:
#        return my_list
#
#    my_list[0], my_list[-1] = my_list[-1], my_list[0]
#    return my_list


#user_input = input("Enter numbers separated by space: ")

#list_nums = []

#for num in user_input.split():
#    if len(user_input) < 2:
#        print("Please enter at least two numbers.")
#    else:
#        list_nums.append(int(num))

#result = swap_first_last(list_nums)

#print(f"Swapped list: {result}")


#def count_primes(limit):
#    primes = []
#    for num in range(2,limit):
#        is_prime = True
#        for i in range(2,int(num**0.5)+1):
#            if num % i == 0:
#                is_prime = False
#                break
#        if is_prime:
#            primes.append(num)
#    return primes


#value = int(input("Enter a limint for the prime numbers: "))
#result = count_primes(value)
#print(f"The total of numbers are: \n{result}")



#def add_item(item,items):
#    items.append(item)
#    return items

#my_list=[1,2,43,24,4]

#digist_to_add = int(input("How many numbers do you want to add?: "))

#for counter in range(digist_to_add):
#    nums_to_add = int(input("\n\nEnter a number to add: "))
#    result = add_item(nums_to_add,my_list)
#    print(f"\n\nThe number added is: \n|{nums_to_add}| \n\nand the list is now: \n{result}")
