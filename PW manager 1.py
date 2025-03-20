# import the os module
import os

# defining the function of the print menu
def menu():
        ascii_art = r"""
       __________  __      __     _____                                             
       \______   \/  \    /  \   /     \ _____    ____ _____     ____   ___________ 
        |     ___/\   \/\/   /  /  \ /  \\__  \  /    \\__  \   / ___\_/ __ \_  __ \
        |    |     \        /  /    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/|  | \/
        |____|      \__/\  /   \____|__  (____  /___|  (____  /\___  / \___  >__|   
                         \/            \/     \/     \/     \//_____/      \/       
        """
        print(ascii_art)
        print("--Menu--")
        print("1. add credentials and resources")
        print("2. view stored credentials")
        print("3. exit program")

# defining the function to add credentials
# this part of the code creates the function that will take user input and store it in the .txt file
# i used \n to print information on diferent lines so it is easier to read

def add_creds():
    username = input("What's the username?")
    password = input("What is the password?")
    resource = input("What is the resource or website?")

    if os.path.exists("credentials.txt"):
        DB = open("credentials.txt", "a")
    else:
        DB = open("credentials.txt", "w")

    DB.write(f"Username: {username},\n Password: {password},\n Resource: {resource}\n")
    DB.close()

    print("Your data has been saved.")
    print()

def add_creds():
    while True:
        username = input("What's the username? ").strip()
        if username:  # Check if username is not empty
            break
        print("Username cannot be empty!")
        
# defining the view creds function
# here i used imported modlue called os and used os.path.exists to check wether "credentials.txt" exists or not
# if it exists it is then opened in the next line

def view_creds():
    if os.path.exists("credentials.txt"):
        DB = open("credentials.txt", "r")
        for line in DB:
            print(line.strip())
        DB.close()
        print()
    else:
        print("No credentials stored yet.")
        print()

# defining the main function of the program we will call later
# i used a while loop, it takes the input from a user and makes a decision based on either 1,2,3 or else
# if else is chose (anything other than 1,2 or 3) it will print "Exiting the program. Cheers mate!"

def main():
    while True:
        menu()
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            add_creds()
        elif choice == "2":
            view_creds()
        elif choice == "3":
            print("Exiting the program. Cheers mate!")
            break
        else:
            print("Invalid choice, choose a valid option.")
            print()

# call the main function
main()
