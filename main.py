import os; import hashlib;import random; import getpass; import sqlite3; from cryptography.fernet import Fernet; import base64

def title():
    print(r"    ____                 _       __               __   __  ___                                 ")
    print(r"   / __ \____ __________| |     / /___  _________/ /  /  |/  /___ _____  ____ _____ ____  _____")
    print(r"  / /_/ / __ `/ ___/ ___/ | /| / / __ \/ ___/ __  /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/")
    print(r" / ____/ /_/ (__  |__  )| |/ |/ / /_/ / /  / /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ /    ")
    print(r"/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     ")
    print(r"                                                                            /____/             ")
    print("\n")

# End to End password encryption -----------
def derive_key(password: str) -> Fernet:
    key = hashlib.sha256(password.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    return Fernet(fernet_key)
# database Userlogin ------------------------------
def setup_database():
    with sqlite3.connect("ACC_DB") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE,
            password TEXT,
            salt BLOB
        )
        """)
        connection.commit()

# Registeration -------------------------
def Register():
    with sqlite3.connect("ACC_DB") as connection:
        cursor = connection.cursor()

    User = input("What is you're User/Email: ")
    #getpass makes input invisble
    Password = getpass.getpass("What is you're password: ")
    salt = os.urandom(16)
    hashed_pw = hashlib.sha3_512(salt + Password.encode()).hexdigest()
    del Password

    try:
        cursor.execute(
            "INSERT INTO users (user, password, salt) VALUES (?, ?, ?)",
            (User, hashed_pw, salt)
        )
        connection.commit()
        create_user_db(User)
    except sqlite3.IntegrityError:
            print("User already exists.")

# Creation of user DB (saves pwds & accs) ------------
def create_user_db(username):
    db_filename = f"{username.strip()}.db"

    # Only create if it doesn’t exist
    if not os.path.exists(db_filename):
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                site_user TEXT,
                site_pass TEXT
            )
            """)
            conn.commit()
        print(f"Database created for {username}")


# login -----------------------------------------------

def login():
    with sqlite3.connect("ACC_DB") as connection:
        cursor = connection.cursor()
    User = input("Enter your User/Email: ")
    Password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT password, salt FROM users WHERE user = ?", (User,))
    result = cursor.fetchone()

    if result:
        stored_pw, salt = result

        hashed_input = hashlib.sha3_512(salt + Password.encode()).hexdigest()

        if hashed_input == stored_pw:
            print("Login successful!")
            return User, Password
        else:
            print("Incorrect password.")
            return False
    else:
        print("User not found.")

# Account Manager -------------------------------------

def user_system(username, user_password):
    os.system("clear")
    fernet = derive_key(user_password)
    db_filename = f"{username}.db"
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        while True:
            title()
            print("1. View All Accounts")
            print("2. Add Account")
            print("\n 0. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                cursor.execute("SELECT site_name, site_user, site_pass FROM passwords")
                rows = cursor.fetchall()
                if rows:
                    print("\nYour saved accounts:")
                    for row in rows:
                        site_name, site_user, e_site_pass = row
                        decrypted_pass = fernet.decrypt(e_site_pass).decode()
                        print(f"Site: {site_name}, User: {site_user}, Password: {decrypted_pass}")
                else:
                    print("No accounts saved yet.")

            elif choice == "2":
                site_name = input("Site name: ")
                site_user = input("Site username/email: ")
                site_pass = input("Site password: ")
                e_site_pass = fernet.encrypt(site_pass.encode())
                cursor.execute(
                    "INSERT INTO passwords (site_name, site_user, site_pass) VALUES (?, ?, ?)",
                    (site_name, site_user, e_site_pass)
                )
                conn.commit()
                print("Account saved.")

            elif choice == "0":
                break
            else:
                print("Invalid option, try again.")

# Account Login / creation --------------------
def acc_l_c():
    setup_database()

    while True:
        os.system("clear")
        title()
        print("1. Register")
        print("2. Login\n")
        print("0. Exit")

        input1 = input("Choose an option: ")

        if input1 == "1":
            Register()
        elif input1 == "2":
            user_data = login()
            if user_data:
                username, user_password = user_data
                user_system(username, user_password)
        elif input1 == "0":
            break
        else:
            print("no")   

# Password Generator
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def PasswordGen():
    print("Welcome to the Password Generator!")
    nr_letters= int(input("How many letters would you like in your password?\n")) 
    nr_symbols = int(input(f"How many symbols would you like?\n"))
    nr_numbers = int(input(f"How many numbers would you like?(1-4)\n"))

    s = random.choices(symbols, k=nr_symbols)
    n = random.choices(numbers, k=nr_numbers)
    l = random.choices(letters, k=nr_letters)

    combinding = s+n+l
    random.shuffle(combinding)
    print("Here is you're Password:")
    output = print("".join(combinding))
    clearinput = input("Press Enter to Return... ")
    if clearinput == "":
        os.system("clear")
        return StartMenu(), inputsys()

def StartMenu():
    print(r"    ____                 _       __               __   __  ___                                 ")
    print(r"   / __ \____ __________| |     / /___  _________/ /  /  |/  /___ _____  ____ _____ ____  _____")
    print(r"  / /_/ / __ `/ ___/ ___/ | /| / / __ \/ ___/ __  /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/")
    print(r" / ____/ /_/ (__  |__  )| |/ |/ / /_/ / /  / /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ /    ")
    print(r"/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     ")
    print(r"                                                                            /____/             ")
    print("\n")

    print("1. Sign In / Create Account")
    print("2. Generate Passwords \n")
    print("0. Exit")

os.system("clear")
StartMenu()

def inputsys():
    input1 = input("Choose an option: ")

    if input1 in ["1","2","0"]:
        os.system("clear")
    else:
        os.system("clear")
        
    #input system

    if input1 == "2":
        PasswordGen()
    elif input1 == "1":
        acc_l_c()
    elif input1 == "0":
        quit()
    else:
        title()
        print("1. Sign In / Create Account")
        print("2. Generate Passwords \n")
        print("0. Exit")
        print("Invalid Option, Pick Again")
        inputsys()
inputsys()


