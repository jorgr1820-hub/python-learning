#Imprimí del 1 al 10 usando range.
#Imprimí del 10 al 1 usando range con paso negativo.
#Imprimí solo los pares del 0 al 20.
#Dado un string s = "Pizza con piña", imprimí los índices y caracteres: 0:P, 1:i,


for index in range(10 + 1):
    print(f"Here are the range from 1 to 10 {index}")



for index in range(-1, -11, -1):
    print(f"Here are the range from 1 to 10 {index}")


for index in range(1,20):
    if index % 2 == 0:
        even = index
        print(even)


s = "Pizza con piña"
indexes = [0,1]
for i in indexes:
    print(f"{i}:{s[i]}")


