from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# DB path (important for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")


# DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create table automatically (FIX FOR YOUR ERROR)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            course TEXT
        )
    """)

    conn.commit()
    conn.close()


# Run DB init on startup
init_db()


# Home + Search
@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search')

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    conn.close()

    return render_template('index.html', students=students)


# Add student
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Login (basic demo)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')


# Run server (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)