from flask import Flask, render_template, request, redirect, session, send_file
from db import insert_student, view_students, update_student, delete_student

from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table

import os

app = Flask(__name__)
app.secret_key = "secret123"

USERNAME = "admin"
PASSWORD = "1234"

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = "admin"
            return redirect("/")
        return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


def check_login():
    return "user" in session


@app.route("/")
def index():
    if not check_login():
        return redirect("/login")

    students = view_students()
    total_students = len(students)
    total_courses = len(set([s[3] for s in students]))

    return render_template("index.html",
                           students=students,
                           total_students=total_students,
                           total_courses=total_courses)


# ADD
@app.route("/add", methods=["GET", "POST"])
def add():
    if not check_login():
        return redirect("/login")

    if request.method == "POST":
        insert_student(
            request.form["name"],
            int(request.form["age"]),
            request.form["course"]
        )
        return redirect("/")

    return render_template("add.html")


# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    if not check_login():
        return redirect("/login")

    delete_student(id)
    return redirect("/")


# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if not check_login():
        return redirect("/login")

    if request.method == "POST":
        update_student(
            id,
            request.form["name"],
            int(request.form["age"]),
            request.form["course"]
        )
        return redirect("/")

    student = [s for s in view_students() if s[0] == id][0]
    return render_template("edit.html", student=student)


# 📊 EXPORT TO EXCEL (✅ FIXED)
@app.route("/export/excel")
def export_excel():
    if not check_login():
        return redirect("/login")

    students = view_students()

    wb = Workbook()
    ws = wb.active
    ws.title = "Students"

    ws.append(["ID", "Name", "Age", "Course"])

    for s in students:
        ws.append(list(s))   # ✅ IMPORTANT FIX

    file_path = "students.xlsx"
    wb.save(file_path)

    return send_file(file_path, as_attachment=True)


# 📄 EXPORT TO PDF
@app.route("/export/pdf")
def export_pdf():
    if not check_login():
        return redirect("/login")

    students = view_students()

    file_path = "students.pdf"

    data = [["ID", "Name", "Age", "Course"]]
    for s in students:
        data.append(list(s))

    pdf = SimpleDocTemplate(file_path)
    table = Table(data)
    pdf.build([table])

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)