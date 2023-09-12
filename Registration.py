# Import relevant libraries (these need to be installed)
import face_recognition
import sqlite3

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

# Function to borrow a book
def borrow_book(book_title):
    if book_title in available_books:
        available_books.remove(book_title)
        cursor.execute("INSERT INTO borrowed_books (title) VALUES (?)", (book_title,))
        conn.commit()
        return "Book borrowed successfully."
    else:
        return "Book not available."


# Function to return a book
def return_book(book_title):
    if book_title in available_books:
        return "Book already returned."
    else:
        available_books.append(book_title)
        cursor.execute("DELETE FROM borrowed_books WHERE title=?", (book_title,))
        conn.commit()
        return "Book returned successfully."

# Main program loop
while True:
    print("1. Authenticate\n2. Borrow Book\n3. Return Book\n4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        image_path = input("Enter path to your image: ")
        if authenticate_face(image_path):
            print("Authentication successful.")
        else:
            print("Authentication failed.")

    elif choice == "2":
        book_title = input("Enter book title to borrow: ")
        print(borrow_book(book_title))
        import GUI
        from GUI import open_gui
        
        open_gui()

    elif choice == "3":
        book_title = input("Enter book title to return: ")
        print(return_book(book_title))
        import GUI
        from GUI import open_gui
        
        open_gui()

    elif choice == "4":
        break
