#Contar cuántos:
#tengan solo letras
#longitud >= 3


nombres = ["Juan", "Ana", "Luis", "Al", "Pedro123"]


resultado = sum(1 for n in nombres if n.isalpha() and len(n) >= 3)
print (resultado)