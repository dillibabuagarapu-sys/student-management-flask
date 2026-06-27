import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-2DSPB68\\SQLEXPRESS;"
    "Database=StudentDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# CREATE TABLE (run once)
def create_table():
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects WHERE name='Students' AND xtype='U'
        )
        CREATE TABLE Students (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100),
            age INT,
            course NVARCHAR(100)
        )
    """)
    conn.commit()

# INSERT
def insert_student(name, age, course):
    cursor.execute(
        "INSERT INTO Students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()

# READ
def view_students():
    cursor.execute("SELECT * FROM Students")
    return cursor.fetchall()

# UPDATE
def update_student(id, name, age, course):
    cursor.execute(
        "UPDATE Students SET name=?, age=?, course=? WHERE id=?",
        (name, age, course, id)
    )
    conn.commit()

# DELETE
def delete_student(id):
    cursor.execute("DELETE FROM Students WHERE id=?", (id,))
    conn.commit()