# Count how many names:
# have only letters
# have length >= 3


names = ["Juan", "Ana", "Luis", "Al", "Pedro123"]

result = sum(1 for n in names if n.isalpha() and len(n) >= 3)
print(result)
