
#This program returns the string saved on the variable "string" backwards

string = "hola mundo"


def backwards(a):
    reversed_txt = ""
    for index in range(len(a)-1,-1,-1):
        reversed_txt += a[index]
    return reversed_txt

print(backwards(string))


