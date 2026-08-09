from flask import Flask, render_template, request
import sqlite3
import joblib

app = Flask(__name__)

# Load Machine Learning Model
model = joblib.load("model.pkl")


# ---------------- HOME ----------------

@app.route("/")
def home():

    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
    """)

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        student=student
    )

# ---------------- PREDICT ----------------

@app.route("/predict", methods=["GET", "POST"])
def predict():

    result = None

    if request.method == "POST":

        name = request.form["name"]
        attendance = float(request.form["attendance"])
        study = float(request.form["study"])
        internal_total = float(request.form["internal_total"])
        internal_obtained = float(request.form["internal_obtained"])

        assignment_total = float(request.form["assignment_total"])
        assignment_obtained = float(request.form["assignment_obtained"])

        total_marks = float(request.form["total_marks"])
        obtained_marks = float(request.form["obtained_marks"])

        # ================= INPUT VALIDATION =================

        errors = []
        if not name:
            errors.append("Please enter the student's name.")

        if not 0 <= attendance <= 100:
            errors.append("Attendance must be between 0 and 100%.")

        if not 0 <= study <= 24:
            errors.append("Study hours must be between 0 and 24 hours per day.")

        if internal_total <= 0:
            errors.append("Internal total marks must be greater than 0.")
        elif not 0 <= internal_obtained <= internal_total:
            errors.append("Internal obtained marks cannot exceed total marks.")

        if assignment_total <= 0:
            errors.append("Assignment total marks must be greater than 0.")
        elif not 0 <= assignment_obtained <= assignment_total:
            errors.append("Assignment obtained marks cannot exceed total marks.")

        if total_marks <= 0:
            errors.append("Previous semester total marks must be greater than 0.")
        elif not 0 <= obtained_marks <= total_marks:
            errors.append("Previous semester obtained marks cannot exceed total marks.")

        if errors:
            return render_template(
                "predict.html",
                result=None,
                errors=errors
            )

        internal = (internal_obtained / internal_total) * 100
        assignment = (assignment_obtained / assignment_total) * 100
        previous = (obtained_marks / total_marks) * 100

        # ================= MACHINE LEARNING PREDICTION =================
     
        data = [[
            attendance,
            study,
            internal,
            assignment,
            previous
        ]]

        score = model.predict(data)[0]

        if score > 100:
            score = 100

        if score < 0:
            score = 0

        score = round(score, 2)

        # ================= GRADE =================

        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B+"
        elif score >= 60:
            grade = "B"
        elif score >= 50:
            grade = "C"
        elif score >= 40:
            grade = "D"
        else:
            grade = "F"

        # ================= RISK =================

        if score >= 75:
            risk = "Low"
        elif score >= 50:
            risk = "Medium"
        else:
            risk = "High"

        # ================= SAVE TO DATABASE =================

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (
            name,
            attendance,
            study_hours,
            internal_marks,
            assignment_marks,
            previous_marks,
            predicted_score,
            grade,
            risk
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            name,
            attendance,
            study,
            internal,
            assignment,
            previous,
            score,
            grade,
            risk

        ))

        conn.commit()
        conn.close()

        # ================= RESULT =================

        result = {

            "name": name,
            "score": score,
            "grade": grade,
            "risk": risk

        }

    return render_template("predict.html", result=result)


# ---------------- HISTORY ----------------

@app.route("/history")
def history():

    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    ORDER BY id DESC
    """)

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        students=students
    )


# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- SETTINGS ----------------

@app.route("/settings")
def settings():
    return render_template("settings.html")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)