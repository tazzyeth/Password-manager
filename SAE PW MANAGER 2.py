# Import the modules we need for our program
import os             # For checking if files exist, working with file paths
import json           # For storing data in a structured format (better than plain text)
from datetime import datetime  # For adding timestamps

# This function shows ASCII art menu to the user
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
    print("1. Add credentials and resources")
    print("2. View stored credentials")
    print("3. Search credentials")     # Added this feature to make finding things easier
    print("4. Delete credentials")     # Added this so users can remove old entries
    print("5. Exit program")

# This function loads our saved passwords from the file
# Centralizing this logic makes the code cleaner and easier to maintain
def load_credentials():
    # First check if we have any saved passwords
    if os.path.exists("credentials.json"):
        try:
            # Try to read the file - using 'with' automatically closes the file after we're done
            with open("credentials.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file is corrupted or empty, just start fresh
            # This prevents crashes if the file gets messed up somehow
            print("Warning: Could not read credentials file. Starting with empty list.")
            return []
    else:
        # If the file doesn't exist yet, return an empty list to start with
        return []

# This function saves the passwords to the file
def save_credentials(credentials_list):
    # Save everything to a formatted JSON file
    # The indent=4 makes the file human-readable if opened in a text editor
    with open("credentials.json", "w") as file:
        json.dump(credentials_list, file, indent=4)
    # No need to manually close the file when using 'with' 

# This function adds a new password
def add_creds():
    # First it gets the existing passwords
    credentials_list = load_credentials()
    
    # It collects all the details and stores them in a dictionary
    
    # Get username - keep asking until it gets something valid
    while True:
        username = input("What's the username? ").strip()
        if username:  # Make sure it's not empty
            break
        print("Username can't be empty!")
    
    # Get the rest of the information
    password = input("What is the password? ")
    resource = input("What is the resource or website? ")
    # Added categories to help organize passwords
    category = input("What category does this belong to? (e.g., Work, Personal, Finance): ")
    
    # Add a timestamp - helpful to know when this entry was created
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a dictionary with all the credential info
    # This is much better than storing strings - we can easily access specific fields
    new_credential = {
        "username": username,
        "password": password,
        "resource": resource,
        "category": category,
        "date_added": timestamp
    }
    
    # Add this new credential to our list
    # Lists are great for collecting multiple items - we can easily add, remove, and iterate through them
    credentials_list.append(new_credential)
    
    # Save everything back to the file
    save_credentials(credentials_list)
    
    print("Your data has been saved.")
    print()  # Empty line for better readability

# This function displays all saved passwords to the user
def view_creds():
    # Get the saved passwords
    credentials_list = load_credentials()
    
    # Check if you have any passwords saved
    if credentials_list:
        # Organize credentials by category
        # We'll use a dictionary where each key is a category and the value is a list of credentials
        categories = {}
        
        # Loop through each credential and organize by category
        for cred in credentials_list:
            # Get the category or use "Uncategorized" if none was specified
            category = cred.get("category", "Uncategorized")
            
            # If this is the first credential in this category, create a new list
            if category not in categories:
                categories[category] = []
                
            # Adds this credential to the right category list
            categories[category].append(cred)
        
        # Now display everything, grouped by category
        for category, creds in categories.items():
            print(f"\n--- {category.upper()} ---")  # Section header for each category
            
            # Display each credential in this category
            for i, cred in enumerate(creds, 1):  # Start counting from 1 instead of 0
                print(f"{i}. Resource: {cred['resource']}")
                print(f"   Username: {cred['username']}")
                print(f"   Password: {cred['password']}")
                print(f"   Added on: {cred.get('date_added', 'Unknown')}")
                print()  # Empty line between entries
    else:
        print("No credentials stored yet.")
        print()

# This function lets users search for specific passwords
# helpful when the list gets long
def search_creds():
    # Get the saved passwords
    credentials_list = load_credentials()
    
    # Check if it has any passwords saved
    if not credentials_list:
        print("No credentials stored yet.")
        print()
        return  # Exit the function early if there's nothing to search
    
    # Get what the user wants to search for
    search_term = input("Enter search term (resource, username, or category): ").lower()
    
    # Look for matches - we'll collect them in a list
    matches = []
    
    # Check each credential to see if it matches
    for cred in credentials_list:
        # Convert everything to lowercase for case-insensitive search
        # Check if the search term is in any of the main fields
        if (search_term in cred["resource"].lower() or 
            search_term in cred["username"].lower() or 
            search_term in cred.get("category", "").lower()):
            # If it matches, add it to our results
            matches.append(cred)
    
    # Show the search results
    if matches:
        print(f"\nFound {len(matches)} matching credentials:")
        for i, cred in enumerate(matches, 1):
            print(f"{i}. Resource: {cred['resource']}")
            print(f"   Username: {cred['username']}")
            print(f"   Password: {cred['password']}")
            print(f"   Category: {cred.get('category', 'Uncategorized')}")
            print()
    else:
        print("No matching credentials found.")
        print()

# This function lets users delete passwords they don't need anymore
def delete_creds():
    # Get our saved passwords
    credentials_list = load_credentials()
    
    # Check if we have any passwords saved
    if not credentials_list:
        print("No credentials stored yet.")
        print()
        return  # Exit the function early if there's nothing to delete
    
    # Show all credentials so the user can choose which to delete
    print("Available credentials:")
    for i, cred in enumerate(credentials_list, 1):  # Start counting from 1 instead of 0
        print(f"{i}. Resource: {cred['resource']}, Username: {cred['username']}")
    
    # Get the user's choice - with error handling
    while True:
        try:
            selection = int(input("\nEnter the number of the credential to delete (0 to cancel): "))
            
            # Allow cancellation
            if selection == 0:
                print("Deletion cancelled.")
                return
                
            # Make sure the selection is valid
            if 1 <= selection <= len(credentials_list):
                break
                
            # If we get here, the number was out of range
            print(f"Enter a number between 1 and {len(credentials_list)}.")
            
        except ValueError:
            # This happens if they enter something that's not a number
            print("Please enter a valid number.")
    
    # Remove the selected credential
    # pop() is used to remove the item and get a reference to it
    deleted_cred = credentials_list.pop(selection - 1)  # -1 because our list is 0-indexed
    
    # Save the updated list
    save_credentials(credentials_list)
    
    # Confirm the deletion to the user
    print(f"Deleted credentials for {deleted_cred['resource']} ({deleted_cred['username']}).")
    print()

# This is the main function that runs the program
def main():
    # Keep running until the user chooses to exit
    while True:
        # Show the menu and get the user's choice
        menu()
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        # Do different things based on what they chose
        if choice == "1":
            add_creds()  # Add new credentials
        elif choice == "2":
            view_creds()  # View saved credentials
        elif choice == "3":
            search_creds()  # Search for specific credentials
        elif choice == "4":
            delete_creds()  # Delete credentials
        elif choice == "5":
            print("Exiting the program. Cheers mate!")
            break  # Exit the loop, ending the program
        else:
            # If they entered something invalid
            print("Invalid choice, choose a valid option.")
            print()

# This makes sure the program only runs 
# when executed directly not when imported by another program
if __name__ == "__main__":
    main()