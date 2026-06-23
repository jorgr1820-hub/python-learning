# Listas + loops + menor sin min()

#Dada nums = [4, -2, 7, 0], encontrá el menor usando un loop (incluye negativos y 0).

#Encontrá el mayor sin max().

#Contá cuántos son positivos, negativos y ceros (en 3 contadores, sin listas extra).

#Sacá el promedio (media) sin usar librerías.

nums = [4, -2, 7, ]
num_lowest = nums[0]
num_highest = nums[0]
for index in nums:
    if index < num_lowest:
        num_lowest = index
    elif index > num_highest:
        num_highest = index


possitive = 0
negative = 0
ceros = 0 
for x in nums:
    if x == 0:
        ceros += 1 
    elif x > 0:
        possitive += 1 
    else:
        negative += 1         


total = 0 
for t in nums:
    total += t


media = total / len(nums)



print(f"The lowest number is: {num_lowest} and the hights is:{num_highest}")
print (f"The total of positive is: {possitive}")
print (f"The total of negative is: {negative}")
print (f"The total of ceros is: {ceros}")
print(f"The media is:{media}")
