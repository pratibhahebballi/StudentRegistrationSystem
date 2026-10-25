# Student Registration System

## Project Description
The Student Registration System is a beginner-friendly web application developed using Python Flask. It allows users to register students and manage their records through a simple web interface.

## Features
- Register new students
- Store student details in an SQLite database
- View all registered students
- Search students by name
- Edit student information
- Delete student records
- Input validation for required fields

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS

## Project Structure
```text
StudentRegistrationSystem/
├── app.py
├── students.db
├── requirements.txt
├── README.md
├── templates/
│   └── home.html
└── static/
    └── style.css
```

## Installation and Setup
1. Install Python on your computer.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment if one is not already available.
4. Install the required package:

   `pip install -r requirements.txt`

## Running the Application
Open the VS Code terminal in the project folder and run:

`python app.py`

Open this address in your browser:

`http://127.0.0.1:5000/`

## Testing
Test student registration with valid details, check blank-field validation, view the student list, search by name, edit a record, and delete a test record.

## Conclusion
This project demonstrates basic Flask routing, HTML forms, GET and POST requests, input validation, and SQLite database operations.
