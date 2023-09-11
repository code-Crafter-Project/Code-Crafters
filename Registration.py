import sqlite3
import datetime

# Create a database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Initialize the list of available books
available_books = ["Book1", "Book2", "Book3"]

# Function to register a new user
def register_user(username, password, full_name, email):
    try:
        cursor.execute("INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?)",
                       (username, password, full_name, email))
        conn.commit()
        return "User registered successfully."
    except Exception as e:
        return f"Error: {e}"

# Function to borrow a book
def borrow_book(user_id, book_title):
    try:
        cursor.execute("SELECT availability FROM books WHERE title=?", (book_title,))
        availability = cursor.fetchone()[0]
        
        if availability == 1:
            due_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
            cursor.execute("UPDATE books SET availability=0, due_date=? WHERE title=?", (due_date, book_title,))
            cursor.execute("INSERT INTO borrowed_books (user_id, book_title) VALUES (?, ?)", (user_id, book_title,))
            conn.commit()
            return f"Book '{book_title}' borrowed successfully. Due date: {due_date}"
        else:
            return "Book not available."
    except Exception as e:
        return f"Error: {e}"

# Function to return a book
def return_book(user_id, book_title):
    try:
        cursor.execute("SELECT availability FROM books WHERE title=?", (book_title,))
        availability = cursor.fetchone()[0]
        
        if availability == 0:
            cursor.execute("UPDATE books SET availability=1, due_date=NULL WHERE title=?", (book_title,))
            cursor.execute("DELETE FROM borrowed_books WHERE user_id=? AND book_title=?", (user_id, book_title,))
            conn.commit()
            return f"Book '{book_title}' returned successfully."
        else:
            return "Book already returned."
    except Exception as e:
        return f"Error: {e}"

# Main program loop
while True:
    print("1. Authenticate\n2. Register User\n3. Borrow Book or  Return Book\n4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        # Implement authentication here
        pass

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        full_name = input("Enter full name: ")
        email = input("Enter e2mail: ")
        print(register_user(username, password, full_name, email))
        

    elif choice == "3":
        user_id = input("Enter your user ID: ")
        book_title = input("Enter book title to borrow: ")
        print(borrow_book(user_id, book_title))

        import GUI
        from GUI import open_gui
        
        open_gui()

    elif choice == "4":
        break

# Close the database connection
conn.close()
