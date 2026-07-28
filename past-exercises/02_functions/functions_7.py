#The program receives a list with random numbers, validates if the
# number is prime, and then returns a list with prime numbers only


def is_prime(num):
    if num <= 1:
        return False
    
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    
    return True


def filter_primes(lst):
    primes = []
    
    for num in lst:
        if is_prime(num):
            primes.append(num)
    
    return primes


nums = [1, 5, 67, 43, 15, 9, 87]
result = filter_primes(nums)
print(result)