


print("    ____                 _       __               __   __  ___                                 ")
print("   / __ \____ __________| |     / /___  _________/ /  /  |/  /___ _____  ____ _____ ____  _____")
print("  / /_/ / __ `/ ___/ ___/ | /| / / __ \/ ___/ __  /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/")
print(" / ____/ /_/ (__  |__  )| |/ |/ / /_/ / /  / /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ /    ")
print("/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     ")
print("                                                                            /____/             ")


username_C = input("Create a Username for the Access")
password_C = input("Create a Password for Access")

def UserAuth(username_C, password_C):

if username == True and password == True:
    print("Access Granted.")
elif:
    username or password == false
    print("Access Denied.")
else:
    return print("Access Denied")

if UserAuth == True:
    print("")

#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the Password Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?(1-4)\n"))

s = random.choices(symbols, k=nr_symbols)
n = random.choices(numbers, k=nr_numbers)
l = random.choices(letters, k=nr_letters)

combinding = s+n+l
random.shuffle(combinding)
output = print("".join(combinding))













Name = input('Whom should I sign this to: ')
filename = input('Where shall I save it: ')


def Creating_File(filename):

    with open(filename, 'w') as file:
        file.write(f"Hi {Name},\n")
        file.write("We hope you enjoy learning Python with us!\n")
        file.write("\nBest,\n")
        file.write("The3 3I337 AP Computer Science Team")


def file_Contents_Confirm(filename):

    open(filename, 'r')
    filecontains = filename.read()
    print(filename)
    filename.close()

Creating_File(filename)
file_Contents_Confirm(filename)