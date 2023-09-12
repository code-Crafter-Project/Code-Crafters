# Import relevant libraries (these need to be installed)
import face_recognition
import sqlite3
import datetime

# Create a database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Initialize the list of available books
available_books = ["Book1", "Book2", "Book3"]

# Function to authenticate user using face recognition
def authenticate_face(image_path):
    # Load the known image of the user
    known_image = face_recognition.load_image_file("known_face.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Load the user's image for authentication
    user_image = face_recognition.load_image_file(image_path)
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    # Compare face encodings
    result = face_recognition.compare_faces([known_face_encoding], user_face_encoding)

    return result[0]

# Function to register a new user
def register_user(username, password, full_name, email):
    cursor.execute("INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?)",
                   (username, password, full_name, email))
    conn.commit()
    return "User registered successfully."

# Function to borrow a book
def borrow_book(user_id, book_title):
    # Check if the book is available
    cursor.execute("SELECT availability FROM books WHERE title=?", (book_title,))
    availability = cursor.fetchone()[0]
    
    if availability == 1:
        # Calculate due date (e.g., 14 days from now)
        due_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
        
        # Update book availability and due date
        cursor.execute("UPDATE books SET availability=0, due_date=? WHERE title=?", (due_date, book_title,))
        cursor.execute("INSERT INTO borrowed_books (user_id, book_title) VALUES (?, ?)", (user_id, book_title,))
        conn.commit()
        return "Book borrowed successfully. Due date: " + due_date
    else:
        return "Book not available."

# Function to return a book
def return_book(user_id, book_title):
    cursor.execute("SELECT availability FROM books WHERE title=?", (book_title,))
    availability = cursor.fetchone()[0]
    
    if availability == 0:
        # Update book availability
        cursor.execute("UPDATE books SET availability=1, due_date=NULL WHERE title=?", (book_title,))
        cursor.execute("DELETE FROM borrowed_books WHERE user_id=? AND book_title=?", (user_id, book_title,))
        conn.commit()
        return "Book returned successfully."
    else:
        return "Book already returned."

# Main program loop
while True:
    print("1. Authenticate\n2. Register User\n3. Borrow Book\n4. Return Book\n5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        image_path = input("Enter path to your image: ")
        if authenticate_face(image_path):
            print("Authentication successful.")
        else:
            print("Authentication failed.")

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        full_name = input("Enter full name: ")
        email = input("Enter email: ")
        print(register_user(username, password, full_name, email))

    elif choice == "3":
        user_id = input("Enter your user ID: ")  # Assuming you have a way to retrieve the user ID
        book_title = input("Enter book title to borrow: ")
        import GUI
        from GUI import open_gui
        
        open_gui()
        print(borrow_book(user_id, book_title))

    elif choice == "4":
        user_id = input("Enter your user ID: ")
        book_title = input("Enter book title to return: ")
        import GUI
        from GUI import open_gui
        
        open_gui()
        print(return_book(user_id, book_title))

    elif choice == "5":
        break

# Close the database connection
conn.close()
