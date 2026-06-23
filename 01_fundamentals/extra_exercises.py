#list_Xs = []
#my_list =[]
#number = 0
#no_list_Xs =[]

#x_number = int(input("Enter how many numbers your list will have?: "))

#for counter in range(1, x_number+1):
#    number = int(input(f"Enter your number #{counter}:"))
#    my_list.append(number)

#f_number = int(input("What is the number you are looking for? : "))

#for index in len(my_list):
#    if index == f_number:
#        list_Xs.append(index)

#if list_Xs > 0 :
#    print(f"The number you were looking for was {f_number}, and it shows up {len(list_Xs)+1} on the list")
#else:
#    print(f"The number you were looking for was {f_number}, and it shows up 0 times on the list")




#####################################################################


#number_list = []
#quantity = 0
#number = None
#while True:
#    try:
#        while quantity == 0:
#            quantity = int(input("How many numbers your list will have: "))
#            if quantity <= 0:
#                print("Must be at least 1. Try again!")
#            else:
#                break
#        for counter in range(quantity):
#            while True:
#                try:
#                    number = int(input(f"Enter value #{counter+1}: "))
#                    number_list.append(number)
#                    break
#                except ValueError:
#                    print("Wrong value type. Try again!")
#        break
#    except ValueError:
#        print("Wrong value type. Try again!")

#positives = []
#negatives = []
#zeros = []
#for index in number_list:
#    if index > 0:
#        positives.append(index)
#    elif index == 0:
#        zeros.append(index)
#    else:
#        negatives.append(index)

#p = len(positives)
#n = len(negatives)
#z = len(zeros)

#if n == 0 and z == 0:
#    print(f"All numbers are positive")
#elif p > 0 and z > 0 and n == 0:
#    print(f"The list has {p} positive numbers and {z} ceros")
#elif n > 0 and z > 0 and p == 0:
#    print(f"The list has {n} negative numbers and {z} ceros")
#elif z > 0 and p == 0 and n == 0:
#    print(f"The list only has {z} ceros")
#elif z == 0 and p > 0 and n > 0:
#    print(f"The list has {p} positive numbers and {n} negative numbers")
#else:
#    print(f"The list has {p} positive numbers, {n} negative numbers and {z} ceros")


########################################################################



#nums = [4, 7, -2, 10, 3]
#menor = nums[0]

#for n in range(1,len(nums)):
#    if n < menor:
#        menor = nums[n]
#print(f"El numero menor es {n}")

######################################################################

#import statistics

#number_list = []
#quantity = 0
#while True:
#    try:
#        while quantity <= 1:
#            quantity = int(input("How many numbers your list will have: "))
#            if quantity <= 1:
#                print("Must enter at least two values")
#                continue
#            else:
#                break
#        for counter in range(quantity):
#            while True:
#                try:
#                    number = int(input(f"Enter value #{counter+1}: "))
#                    number_list.append(number)
#                    break
#                except ValueError:
#                    print("Wrong value type. Try again!")
#        break
#    except ValueError:
#        print("Wrong value type. Try again!")

#avg = statistics.mean(number_list) ##sum(number_list) / len(number_list)
#mtavg_list = []

#for index in number_list:
#    if index > avg:
#        mtavg_list.append(index)

#print("\nResults:",
#      f"\nThe average is {avg:.2f}",
#      f"\nThe numbers that are higher than the average are: {mtavg_list}"
#    )



#####################################################################################
total_of_words = []
words = []



