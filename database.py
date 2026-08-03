import sqlite3

# Connect to Database
conn = sqlite3.connect("students.db")

# Create Cursor
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    attendance REAL,

    study_hours REAL,

    internal_marks REAL,

    assignment_marks REAL,

    previous_marks REAL,

    predicted_score REAL,

    grade TEXT,

    risk TEXT

)
""")

print("✅ Database Created Successfully")
print("✅ Students Table Created Successfully")

# Save Changes
conn.commit()

# Close Connection
conn.close()