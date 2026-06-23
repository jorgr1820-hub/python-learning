#product = input("Enter the product")
#product_price = float(input("What is the price $?"))
#final_price = float
#if product_price < 100:
#    final_price = product_price - (product_price * 0.02)
#else:
#   final_price = product_price - (product_price * 0.10)

#print(f"Your final price for {product} is {final_price}")   







#time = int(input ("Enter the time in seconds:"))
#if time < 600:
#    result = 600 - time
#    print(f"Your time is lower, the total of sec missing are: {result}")
#elif time == 600:
#    print("Your time is: Equal")
#else:
#    print("Your time is Higher")    







#number = int(input("Enter the number"))
#total = 0 
#for counter in range (number+1):
#    total += counter

#print (f"Your total is: {total}")







#import random
#number = 0

#magic_number = random.randint(1,10)
#while number != magic_number:
#    try:    
#        number = int(input("Enter a number between 1 to 10:"))
#        if number == magic_number:
#            print("Correct Number") 
#        elif number < 1 or number >10:
#            print("Out of Range, enter a number between 1 to 10")
#        else:
#            print("Incorrect, try again") 
#    except ValueError:
#        print("Enter a valid inter")          


#number1= int(input("Enter first number:"))
#number2= int(input("Enter second number:"))
#number3= int(input("Enter third number:"))
#if number1 == 30 or number2 == 30 or number3 == 30 or  number1 + number2 + number3 == 30:
#    print("Correct")
#else:
#    print("Incorrect")







#number = float(input("Enter the temperature in Celsius:"))
#fahrenheit =  (number * 9 / 5) + 32
#kelvin = number + 294.5

#print(f"The tempeture in Fahrenheit is {fahrenheit}, and {kelvin} in Kelvin")





total = 0
number = int(input("Enter a number beteween 1 to 10:"))

for multiplier in range (1,12 + 1):
    total= multiplier+number
    print(total)