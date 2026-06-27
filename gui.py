from tkinter import *
from tkinter import ttk, messagebox
from db import *

root = Tk()
root.title("Student Management System")
root.geometry("650x450")

# ===== Input Fields =====
Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(root)
name_entry.grid(row=0, column=1)

Label(root, text="Age").grid(row=1, column=0, padx=10, pady=5)
age_entry = Entry(root)
age_entry.grid(row=1, column=1)

Label(root, text="Course").grid(row=2, column=0, padx=10, pady=5)
course_entry = Entry(root)
course_entry.grid(row=2, column=1)

# ===== Table =====
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Course"), show="headings")

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# ===== Functions =====

def clear_fields():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    course_entry.delete(0, END)


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    rows = view_students()
    for row in rows:
        tree.insert("", END, values=(row[0], row[1], row[2], row[3]))


def add_data():
    name = name_entry.get().strip()
    age = age_entry.get().replace(",", "").strip()
    course = course_entry.get().strip()

    if not name or not age or not course:
        messagebox.showerror("Error", "All fields required!")
        return

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number!")
        return

    insert_student(name, int(age), course)
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student added!")


def update_data():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a record")
        return

    values = tree.item(selected, "values")
    age = age_entry.get().replace(",", "").strip()

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be number!")
        return

    update_student(int(values[0]), name_entry.get(), int(age), course_entry.get())
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Updated successfully!")


def delete_data():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a record")
        return

    values = tree.item(selected, "values")

    confirm = messagebox.askyesno("Confirm", "Delete this record?")
    if confirm:
        delete_student(int(values[0]))
        refresh_table()
        clear_fields()
        messagebox.showinfo("Deleted", "Record deleted!")


def select_data(event):
    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    if not values:
        return

    clear_fields()

    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    course_entry.insert(0, values[3])


tree.bind("<ButtonRelease-1>", select_data)

# ===== Buttons =====
Button(root, text="Add", width=12, command=add_data).grid(row=3, column=0, pady=10)
Button(root, text="Update", width=12, command=update_data).grid(row=3, column=1)
Button(root, text="Delete", width=12, command=delete_data).grid(row=3, column=2)
Button(root, text="Refresh", width=12, command=refresh_table).grid(row=3, column=3)

refresh_table()

root.mainloop()