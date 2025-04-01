import sqlite3
import os

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT,
        major TEXT,
        starting_year INTEGER,
        total_attendance INTEGER,
        standing TEXT,
        year INTEGER,
        last_attendance TEXT,
        image BLOB
    )
''')

# The 'data' list contains tuples for each student's information. 
# Each tuple includes the student's ID, name, major, starting year, total attendance, 
# standing, year, last attendance date (e.g., '2023-10-15 12:37:00'), and an additional value (None).
data = [
    ("id", "name", "major", "starting_year", "total_attendance", 
     "standing", "year", "last_attendance", None),
]

cursor.executemany("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

image_folder = "Images"  # Folder with pictures

for student_id, _, _, _, _, _, _, _, _ in data:
    image_path = os.path.join(image_folder, f"{student_id}.png")  # Image file path
    
    if os.path.exists(image_path):  
        with open(image_path, 'rb') as f:
            image_data = f.read()

        cursor.execute("UPDATE students SET image = ? WHERE id = ?", (image_data, student_id))

conn.commit()
conn.close()

print("SQLite database created, students and images added.")