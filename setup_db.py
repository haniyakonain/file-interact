import sqlite3
from datetime import datetime

# Create a connection to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

# Create the documents table with proper fields including file_size
cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        file_path TEXT NOT NULL,
        text_content TEXT NOT NULL,
        file_size INTEGER NOT NULL
    )
""")

# Function to insert the document data into the database
def insert_document(filename, file_path, text_content, file_size):
    upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO documents (filename, upload_date, file_path, text_content, file_size)
        VALUES (?, ?, ?, ?, ?)
    """, (filename, upload_date, file_path, text_content, file_size))
    
    conn.commit()

# Example usage of inserting a document
filename = 'example.pdf'
file_path = '/path/to/example.pdf'
text_content = 'This is a sample text content extracted from the PDF.'
file_size = 102400  # Example size in bytes (100 KB)

# Insert the document into the database
insert_document(filename, file_path, text_content, file_size)

# Commit the changes and close the connection
conn.commit()
conn.close()
