
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from markupsafe import escape

app = Flask(__name__)
DATABASE = "students.db"


# Create database and students table
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("home.html")


# About page
@app.route("/about")
def about():
    return "<h1>About</h1><a href='/'>Back to Home</a>"


# Contact page
@app.route("/contact")
def contact():
    return "<h1>Contact</h1><a href='/'>Back to Home</a>"


# Register a new student
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    course = request.form.get("course", "").strip()

    if not all([name, email, phone, course]):
        return "Please fill in all fields.", 400

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO students (name, email, phone, course)
        VALUES (?, ?, ?, ?)
    """, (name, email, phone, course))

    conn.commit()
    conn.close()

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registration Successful</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Registration Successful!</h1>
        <p style="text-align:center;">Student saved successfully.</p>
        <p style="text-align:center;">
            <a href="/">Register another student</a>
        </p>
        <p style="text-align:center;">
            <a href="/students">View all students</a>
        </p>
    </body>
    </html>
    """


# View and search students by name only
@app.route("/students")
def students():
    search = request.args.get("search", "").strip()

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if search:
        records = conn.execute("""
            SELECT id, name, email, phone, course
            FROM students
            WHERE name LIKE ?
            ORDER BY id
        """, (f"%{search}%",)).fetchall()
    else:
        records = conn.execute("""
            SELECT id, name, email, phone, course
            FROM students
            ORDER BY id
        """).fetchall()

    conn.close()

    rows = ""

    for student in records:
        rows += f"""
        <tr>
            <td class="id-column">{student['id']}</td>
            <td>{escape(student['name'])}</td>
            <td>{escape(student['email'])}</td>
            <td>{escape(student['phone'])}</td>
            <td>{escape(student['course'])}</td>
            <td class="actions">
                <a href="/edit/{student['id']}">Edit</a>

                <form action="/delete/{student['id']}"
                      method="POST"
                      onsubmit="return confirm('Are you sure you want to delete this student?');">
                    <button type="submit" class="delete-btn">Delete</button>
                </form>
            </td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="6" style="text-align:center;">
                No students found with that name.
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registered Students</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Registered Students</h1>

        <form method="GET" action="/students" class="search-form">
            <label for="search">Search by Student Name</label>

            <input
                type="text"
                id="search"
                name="search"
                placeholder="Enter student name"
                value="{escape(search)}"
            >

            <button type="submit">Search</button>
            <a href="/students" class="show-all-link">Show All Students</a>
        </form>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Course</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <p style="text-align:center;">
            <a href="/">Back to Registration</a>
        </p>
    </body>
    </html>
    """

# Edit student details
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()

        if not all([name, email, phone, course]):
            conn.close()
            return "Please fill in all fields.", 400

        conn.execute("""
            UPDATE students
            SET name = ?, email = ?, phone = ?, course = ?
            WHERE id = ?
        """, (name, email, phone, course, student_id))

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    if student is None:
        return "Student not found.", 404

    name = escape(student["name"])
    email = escape(student["email"])
    phone = escape(student["phone"])
    course = student["course"]

    courses = {
        "ECE": "Electronics and Communication (ECE)",
        "CSE": "Computer Science (CSE)",
        "EEE": "Electrical and Electronics (EEE)",
        "ME": "Mechanical Engineering (ME)"
    }

    options = ""

    for code, label in courses.items():
        selected = "selected" if course == code else ""
        options += (
            f'<option value="{code}" {selected}>'
            f'{label}</option>'
        )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Edit Student</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Edit Student</h1>

        <form method="POST">
            <label for="name">Full Name:</label>
            <input id="name" name="name" value="{name}" required>

            <label for="email">Email:</label>
            <input id="email" type="email" name="email"
                   value="{email}" required>

            <label for="phone">Phone Number:</label>
            <input id="phone" name="phone" value="{phone}" required>

            <label for="course">Course:</label>
            <select id="course" name="course" required>
                {options}
            </select>

            <button type="submit">Save Changes</button>
            <p><a href="/students">Cancel</a></p>
        </form>
    </body>
    </html>
    """


# Delete a student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# Run the application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
