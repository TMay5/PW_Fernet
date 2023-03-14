from cryptography.fernet import Fernet

def load_key():
    file = open("key.key", "rb") #rb - read in bytes mode
    key = file.read()
    file.close()
    return key

master_pwd = input("What is the master password? ")
key = load_key() + master_pwd.encode() #encode converts to bytes
fer = Fernet(key)


#generates our key - ran only once
#def write_key():
#   key = Fernet.generate_key()
#    with open("key.key", "wb") as key_file:  #wb - write in bytes mode
#       key_file.write(key)



def view():
    with open("passwords_storage.txt", "r") as f: 
        for line in f.readlines():
            data = line.rstrip() #.rstrip() - removes the return from the \n line break after printing data
            user, passw = data.split(" | ") #.split() - finds a character in a str and returns it as a list; repeats for each instance found
            print("User:", user, "/ Pasword:", fer.decrypt(passw.encode()).decode()) #prints UN + decrypted PW


#with - auto-closes the file after we're done with it
#modes "w", "r", "a"; w - write (overrides existing data); r - read mode; a - adds to next available line of file / creates a file if there is none
def add():
    name = input("Account Name: ")
    pwd = input("Password: ")
    with open("passwords_storage.txt", "a") as f: 
        f.write(name + " | " + fer.encrypt(pwd.encode()).decode() + "\n") #stores UN + encrypts PW in bytes; converts back to a non-byte str in order to store



while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ")
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue
