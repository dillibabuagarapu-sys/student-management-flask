import sqlite3

# Create DB connection
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()


# INSERT
def insert_student(name, age, course):
    cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
    conn.commit()


# VIEW
def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


# UPDATE
def update_student(id, name, age, course):
    cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?", (name, age, course, id))
    conn.commit()


# DELETE
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()